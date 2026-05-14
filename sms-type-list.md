# FinUp.Stock.* - USP_User_Notify / USP_UserNotify_Insert 사용 로직 리포트

- 작성일: 2026-05-14
- 대상 경로: `/mnt/c/Dev/FinUp.Stock*`, `/mnt/c/Dev/Finup.Stock.Admin`
- 리포팅 파일: `/mnt/c/reports/sms-type-list.md`
- 확인 대상 SP: `DbStockPoint.dbo.USP_User_Notify`, `DbStockPoint.dbo.USP_UserNotify_Insert`
- 제외: `USP_User_Notify_Mentor`는 이름이 유사하지만 요청 대상 SP와 다른 프로시저라 별도 집계에서 제외했다. 주석 처리된 호출부도 제외했다.

## 1. 결론 요약

- 요청 대상 SP를 직접 감싸는 활성 메소드는 6개다.
- 그중 실제 호출 로직이 확인된 메소드는 3개다.
  - `SqlAdmin.AdminProcUserNotify(...)` → `USP_User_Notify`
  - `SqlAdmin.USPUserNotifyInsertInline(...)` → `USP_UserNotify_Insert`
  - `SqlGeneral.USPUserNotifyInsert(...)` → `USP_UserNotify_Insert`
- 정의는 있으나 현재 검색 범위에서 호출부가 없는 메소드도 있다.
  - `SqlAdmin.AdminProcUserNotifyInline(...)`
  - `SqlLeague.USPUserNotify(...)`
  - `FinUp.Stock.App/Sql/SqlSender.USPUserNotifyInsert(...)`
- 실제 UI/업무 로직 호출부는 총 19개 지점이다.

## 2. SMS Type 산정 기준

DB SP 분석 기준으로 `T_SmsLog.Type`은 다음처럼 들어간다.

| SP | 코드 래퍼 | T_SmsLog.Type 산정 | 비고 |
|---|---|---|---|
| `USP_User_Notify` | `SqlAdmin.AdminProcUserNotify`, `SqlLeague.USPUserNotify`, `SqlAdmin.AdminProcUserNotifyInline` | `3` 고정 | `USP_User_Notify`의 직접 INSERT는 `Type = 3 -- 시스템 발송`. 단, `PushMode = "PUSH"`이면 SMS 발송 조건을 타지 않아 `T_SmsLog`가 남지 않을 수 있다. |
| `USP_UserNotify_Insert` | `SqlGeneral.USPUserNotifyInsert`, `SqlAdmin.USPUserNotifyInsertInline`, `SqlSender.USPUserNotifyInsert` | `ActorType = 30`이면 `1`, `ActorType = 20`이면 `2`, 그 외는 `3` | 코드 상수는 `FinUp.Stock/Constants.cs:166-170` 기준 `System=10`, `Admin=20`, `Mentor=30`. |

> 주의: 아래 “예상 Type”은 해당 호출이 SMS 경로를 실제로 탈 때의 값이다. `NotifyType = 1` 또는 `PushMode = "PUSH"`처럼 PUSH 전용으로 강제되는 경우에는 `T_SmsLog` INSERT가 발생하지 않을 수 있다.

## 3. SP 래퍼 메소드 정의

| 상태 | 파일:라인 | 메소드 | 호출 SP | 반환/동작 |
|---|---|---|---|---|
| 사용됨 | `FinUp.Stock/Sql/SqlAdmin.cs:146` | `AdminProcUserNotify(...)` | `DbStockPoint.dbo.USP_User_Notify` | `QueryFactory`로 실행 후 `ExecuteNonQuery()` |
| 호출부 없음 | `FinUp.Stock/Sql/SqlAdmin.cs:181` | `AdminProcUserNotifyInline(...)` | `DbStockPoint.dbo.USP_User_Notify` | 배치 실행용 SQL 문자열 생성 |
| 사용됨 | `FinUp.Stock/Sql/SqlAdmin.cs:225` | `USPUserNotifyInsertInline(...)` | `DbStockPoint.dbo.USP_UserNotify_Insert` | 배치 실행용 SQL 문자열 생성 |
| 호출부 없음 | `FinUp.Stock/Sql/SqlLeague.cs:2993` | `USPUserNotify(...)` | `DbStockPoint.dbo.USP_User_Notify` | `ExecuteNonQuery()` |
| 사용됨 | `FinUp.Stock/Sql/SqlGeneral.cs:2045` | `USPUserNotifyInsert(...)` | `DbStockPoint.dbo.USP_UserNotify_Insert` | `ExecuteScalar()` |
| 호출부 없음 | `FinUp.Stock.App/Sql/SqlSender.cs:866` | `USPUserNotifyInsert(...)` | `DbStockPoint.dbo.USP_UserNotify_Insert` | SQL 문자열 생성 |

## 4. 전체 호출 로직 목록

| # | 파일:라인 | 로직/핸들러 | 래퍼 | NotifyIdx | ActorType | 발송 제어 | 예상 T_SmsLog.Type |
|---:|---|---|---|---|---|---|---|
| 1 | `FinUp.Stock.Mentor/UserControl/Package5.ascx.cs:121` | 멘토 패키지 구독자 수동 알림 `btnAlarm_Click` | `SqlGeneral.USPUserNotifyInsert` | `NotifyIdx` 변수: `126` 또는 `164` | `Mentor(30)` | `NotifyType` 미지정, CodeNotify 정책 의존 | `1` 가능 |
| 2 | `FinUp.Stock.Mentor/UserControl/Package4.ascx.cs:224` | 멘토 리딩 구독자 수동 알림 `btnAlarm_Click` | `SqlAdmin.AdminProcUserNotify` | `97` | `Mentor(30)` | `NoticeChk` 전달, `PushMode` 미지정 | `3` 가능 |
| 3 | `FinUp.Stock.Mentor/UserControl/Leading.ascx.cs:238` | 멘토 리딩 구독자 수동 알림 `btnAlarm_Click` | `SqlAdmin.AdminProcUserNotify` | `22` | `Mentor(30)` | `NoticeChk` 전달, `PushMode` 미지정 | `3` 가능 |
| 4 | `Finup.Stock.Admin/Member/UserList.aspx.cs:137` | 관리자 회원 목록 개별 PUSH 발송 `btnPSave_Click` | `SqlAdmin.AdminProcUserNotify` | `14` | `Admin(20)` | UI 주석은 PUSH 발송, `PushMode` 미지정 | `3` 가능 |
| 5 | `Finup.Stock.Admin/Member/PUSHDetail.aspx.cs:59` | 관리자 전체 PUSH 발송 `btnSubmit_Click` | `SqlGeneral.USPUserNotifyInsert` | `ddlNotifyIdx.SelectedValue` | `Admin(20)` | `NotifyType` 미지정, CodeNotify 정책 의존 | `2` 가능 |
| 6 | `Finup.Stock.Admin/Tech/TechTradingView.aspx.cs:329` | 매매기법 구독자 알림 `btnNTSave_Click` | `SqlAdmin.AdminProcUserNotify` | `17` | `Admin(20)` | `PushMode` 미지정 | `3` 가능 |
| 7 | `Finup.Stock.Admin/Manage/QnaView.aspx.cs:169` | Q&A 답변 등록 알림 `btnUpdate` | `SqlAdmin.AdminProcUserNotify` | `54` | `Admin(20)` | `PushMode = "PUSH"` | SMS 없음 가능성이 큼 |
| 8 | `FinUp.Stock.Web/Intro/CustomerInquiry.aspx.cs:129` | 고객문의 자동답변 알림 `btnSubmit_Click` | `SqlAdmin.AdminProcUserNotify` | `140` | `System(10)` | `PushMode = "PUSH"` | SMS 없음 가능성이 큼 |
| 9 | `Finup.Stock.Admin/Lecture/LectureVodView.aspx.cs:541` | VOD 구독자 알림 `btnNTSave_Click` | `SqlAdmin.AdminProcUserNotify` | `18` | `Admin(20)` | `PushMode` 미지정 | `3` 가능 |
| 10 | `Finup.Stock.Admin/Lecture/LectureLiveView.aspx.cs:622` | LIVE 구독자 알림 `btnNTSave_Click` | `SqlAdmin.AdminProcUserNotify` | `16` | `Admin(20)` | `PushMode` 미지정 | `3` 가능 |
| 11 | `Finup.Stock.Admin/Manage/Data/ExcelEncrypt.aspx.cs:391` | 엑셀 업로드 사용자별 PUSH/알림 배치 `ExcelPushSand` | `SqlAdmin.USPUserNotifyInsertInline` | `14` | `Admin(20)` | 행별 SQL 문자열 누적 후 `ExecQuery(sSql)` | `2` 가능 |
| 12 | `Finup.Stock.Admin/Package/PackageVipUserList.aspx.cs:403` | VIP 종목알리미 구독자 알림 | `SqlGeneral.USPUserNotifyInsert` | `1130` | `Admin(20)` | `NotifyType = rblPushMode.SelectedValue` | 런타임 값이 SMS면 `2` |
| 13 | `Finup.Stock.Admin/Package/PackageVipUserList.aspx.cs:416` | VIP 종목알리미 쿠폰구독자 알림 | `SqlGeneral.USPUserNotifyInsert` | `1130` | `Admin(20)` | `NotifyType = "1"` PUSH 전용 | SMS 없음 가능성이 큼 |
| 14 | `Finup.Stock.Admin/Offline/OfflineView.aspx.cs:447` | 오프라인 강의 전체 구독자 알림 `btnNTSave_Click` | `SqlAdmin.AdminProcUserNotify` | `78` | `Admin(20)` | `NoticeChk` 전달, `PushMode` 미지정 | `3` 가능 |
| 15 | `Finup.Stock.Admin/Package/PackageUserAlarmList.aspx.cs:196` | 패키지 구독자 알림 `btnNTSave_Click` | `SqlGeneral.USPUserNotifyInsert` | `NotifyIdx` 변수: `39`, `126`, `164` | `Admin(20)` | `NotifyType` 미지정 | `2` 가능 |
| 16 | `Finup.Stock.Admin/Package/PackageMentorList.aspx.cs:190` | My 멘토 알리미 멘토 선택 유저 알림 `btnPopNotifySave_Click` | `SqlGeneral.USPUserNotifyInsert` | `1713` | `Admin(20)` | `NotifyType` 미지정 | `2` 가능 |
| 17 | `Finup.Stock.Admin/Mentor/MentorActivePolicyWrite.aspx.cs:170` | 멘토 전체 SMS 발송 | `SqlGeneral.USPUserNotifyInsert` | `100` | `Admin(20)` | 코드 주석상 SMS 발송 | `2` 가능성이 큼 |
| 18 | `Finup.Stock.Admin/Chat/ChatView.aspx.cs:692` | 리딩 현재구독자 알림 `btnNTSave_Click` | `SqlAdmin.AdminProcUserNotify` | `22`/`56`/`63` 조건식 | `Admin(20)` | `NoticeChk` 전달, `PushMode` 미지정 | `3` 가능 |
| 19 | `Finup.Stock.Admin/Chat/ChatView.aspx.cs:715` | 리딩 전체구독자 알림 `btnNTSave_Click` | `SqlAdmin.AdminProcUserNotify` | `21`/`55`/`62` 조건식 | `Admin(20)` | `NoticeChk` 전달, `PushMode` 미지정 | `3` 가능 |

## 5. 미사용/비활성 항목

| 파일:라인 | 항목 | 판단 |
|---|---|---|
| `FinUp.Stock/Sql/SqlAdmin.cs:181` | `AdminProcUserNotifyInline(...)` | 정의만 있고 현재 검색 범위에서 호출부 없음 |
| `FinUp.Stock/Sql/SqlLeague.cs:2993` | `USPUserNotify(...)` | 정의만 있고 현재 검색 범위에서 호출부 없음 |
| `FinUp.Stock.App/Sql/SqlSender.cs:866` | `USPUserNotifyInsert(...)` | 정의만 있고 현재 검색 범위에서 호출부 없음 |
| `FinUp.Stock/Sql/SqlFeature.Notify.cs:225` | `USPUserNotifyInsert(...)` | 전체가 주석 처리된 레거시 코드 |
| `Finup.Stock.Admin/Contents/ContentsDetail.aspx.cs:1397` | `sqlAdmin.USPUserNotifyInsert(...)` | 주석 처리된 호출부 |

## 6. 검증 근거

- SP 문자열 직접 검색 결과 활성 정의 위치:
  - `FinUp.Stock/Sql/SqlAdmin.cs:160`, `:197`, `:248`
  - `FinUp.Stock/Sql/SqlLeague.cs:3007`
  - `FinUp.Stock/Sql/SqlGeneral.cs:2066`
  - `FinUp.Stock.App/Sql/SqlSender.cs:878`
- 래퍼 심볼 호출 검색 결과 활성 호출부 19개를 위 표에 반영했다.
- `ActorType` 상수는 `FinUp.Stock/Constants.cs:166-170`에서 `System=10`, `Admin=20`, `Mentor=30`으로 확인했다.
- `USP_UserNotify_Insert`의 `ActorType`별 Type CASE와 `USP_User_Notify`의 Type=3 고정 INSERT는 이전 DB SP 분석 결과와 동일한 근거를 사용했다.
