# FinUp.DB.* - T_SmsLog Type 등록 경로 확인 리포트

- 작성일: 2026-05-14
- 대상 경로: `/mnt/c/Dev/FinUp.DB.*`
- 확인 대상: Stored Procedure SQL 파일 전체 기준 `T_SmsLog` 직접 INSERT 및 `USP_SmsLog_Insert` 호출
- 산출물: `/mnt/c/reports/FinUp.DB.SmsLog.Type.report.md`

## 요약

- `FinUp.DB.*` 하위 Stored Procedure SQL 파일 2,620개를 확인했다.
- `T_SmsLog`에 직접 INSERT하는 SP는 총 7개다.
- `USP_SmsLog_Insert`를 호출하는 SP는 총 1개다.
- 단, 확인된 호출부(`USP_UserCertify`)는 `@SmsType = 4`로 호출하며, `USP_SmsLog_Insert` 내부 로직상 이 경우 `T_SmsLog`가 아니라 `T_SmsLogLimit`에 INSERT한다.
- 따라서 현재 소스 기준으로 `USP_SmsLog_Insert` 호출을 통해 실제 `T_SmsLog`에 등록되는 호출부는 발견되지 않았다.

## Type 코드 참고

`T_SmsLog.Type`은 `INT NOT NULL` 컬럼이며 설명은 `푸쉬타입 #Ref - T_Code.Code(SmsType)`이다.

| Type 값 | 코드상 확인된 의미 | 근거 |
|---:|---|---|
| 1 | 전문가 발송 | `USP_UserNotify_Insert.sql`, `USP_UserNotify_Insert_Game.sql` CASE 주석 |
| 2 | 관리자 발송 | `USP_UserNotify_Insert.sql`, `USP_UserNotify_Insert_Game.sql` CASE 주석 |
| 3 | 시스템 발송 | 여러 직접 INSERT 및 CASE ELSE 주석 |
| 4 | `USP_SmsLog_Insert`에서 사용자 발송기록 분기값. 이 값은 `T_SmsLog`가 아니라 `T_SmsLogLimit`에 기록됨 | `USP_SmsLog_Insert.sql:42-57`, `USP_UserCertify.sql:50-56` |

## T_SmsLog 직접 INSERT SP

| 구분 | DB 프로젝트 / SP 파일 | INSERT 방식 | T_SmsLog.Type 입력값 | 비고 |
|---|---|---|---|---|
| 직접 INSERT | `FinUp.DB.SQLServer.DbStockPoint/dbo/Stored Procedures/USP_SmsLog_Insert.sql` | `INSERT INTO T_SmsLog` | `@SmsType` | `@SmsType <> 4`인 경우만 `T_SmsLog`에 등록. `@SmsType = 4`면 `T_SmsLogLimit`로 분기. 근거: lines 42-57 |
| 직접 INSERT | `FinUp.DB.SQLServer.DbStockPoint/dbo/Stored Procedures/USP_User_Notify.sql` | `INSERT INTO DbStockPoint.dbo.T_SmsLog` | `3` | 주석: `시스템 발송`. 근거: lines 687-697 |
| 직접 INSERT | `FinUp.DB.SQLServer.DbStockPoint/dbo/Stored Procedures/USP_UserNotify_Insert.sql` | `INSERT INTO DbStockPoint.dbo.T_SmsLog` | `CASE WHEN @ActorType = 30 THEN 1 WHEN @ActorType = 20 THEN 2 ELSE 3 END` | 1=전문가, 2=관리자, 3=시스템. 근거: lines 1706-1722 |
| 직접 INSERT | `FinUp.DB.SQLServer.DbStockPoint/dbo/Stored Procedures/USP_UserNotify_Insert_Game.sql` | `INSERT INTO DbStockPoint.dbo.T_SmsLog` | `CASE WHEN @ActorType = 30 THEN 1 WHEN @ActorType = 20 THEN 2 ELSE 3 END` | 1=전문가, 2=관리자, 3=시스템. 근거: lines 251-267 |
| 직접 INSERT | `FinUp.DB.SQLServer.DbStockPoint/dbo/Stored Procedures/USP_UserNotify_Insert_FeatureBoard.sql` | `INSERT INTO DbStockPoint.dbo.T_SmsLog` | `3` | 시스템 발송으로 고정. 근거: lines 167-177 |
| 직접 INSERT | `FinUp.DB.SQLServer.DbStockPoint/dbo/Stored Procedures/USP_UserNotify_Insert_FeatureBoard_Game.sql` | `INSERT INTO DbStockPoint.dbo.T_SmsLog` | `3` | 시스템 발송으로 고정. 근거: lines 185-195 |
| 직접 INSERT | `FinUp.DB.SQLServer.DbStockPoint/dbo/Stored Procedures/USP_Bat_SmsQueue_Insert_NonMember_FreeLive.sql` | `INSERT INTO DbStockPoint.dbo.T_SmsLog` | `3` | 시스템 발송으로 고정. 근거: lines 60-70 |

## USP_SmsLog_Insert 호출 SP

| 구분 | DB 프로젝트 / SP 파일 | 호출 방식 | 전달 Type 값 | 실제 T_SmsLog 등록 여부 | 비고 |
|---|---|---|---|---|---|
| SP 호출 | `FinUp.DB.SQLServer.FinUp/dbo/StoredProcedures/USP_UserCertify.sql` | `EXEC DbStockPoint.dbo.USP_SmsLog_Insert` | `@SmsType = 4` | 아니오 | `USP_SmsLog_Insert`는 `@SmsType = 4`일 때 `T_SmsLogLimit`에 INSERT하고 `T_SmsLog` INSERT 분기를 타지 않는다. 근거: `USP_UserCertify.sql:50-56`, `USP_SmsLog_Insert.sql:42-57` |

## 제외/주의 사항

- `T_SmsLog`를 조회만 하는 SP도 발견되었으나 INSERT 경로가 아니므로 위 표에서 제외했다. 예: `USP_Bat_StatService.sql`, `USP_Bat_MentorCalculate.sql`, `USP_Bat_MentorCalculate_202408.sql`.
- `T_SmsLogLimit`는 별도 테이블이며, `T_SmsLog` 직접 INSERT 대상이 아니므로 별도로 구분했다.
- `T_SmsLog.Type`의 전체 코드 마스터 데이터(`T_Code.Code(SmsType)`) seed는 이번 검색 범위에서 확인되지 않았고, 위 의미는 SP 주석/분기에서 직접 확인 가능한 값만 정리했다.

## 검증에 사용한 검색 기준

- 대상 루트: `/mnt/c/Dev/FinUp.DB.*`
- Stored Procedure SQL 파일 수: 2,620개
- 직접 INSERT 검색: `insert\s+(into\s+)?...T_SmsLog` 대소문자 무시
- 호출 검색: `USP_SmsLog_Insert` 대소문자 무시
- 테이블/함수의 단순 정의/조회는 SP INSERT/호출 분류에서 제외
