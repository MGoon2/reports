# AlphaBot 레거시 윈도우앱 반복 처리 구조 분석 보고서 — DB 스냅샷 반영본

- 원본 보고서: `/mnt/c/reports/stockdata.api/AlphaBot 레거시 윈도우앱 반복 처리 구조 분석 보고서.md`
- 신규 저장 파일: `/mnt/c/reports/stockdata.api/AlphaBot 레거시 윈도우앱 반복 처리 구조 분석 보고서_DB스냅샷반영_2026-05-14.md`
- 반영 데이터: 사용자가 제공한 `T_Operation`, `T_OperationTerm` 스냅샷.
- 분석 범위: `FinUp.CollectData.App.AlphaBot`, `FinUp.Finance.App.AlphaBot`, `FinUp.Radar.App.AlphaBot`, `FinUp.Stock.App.AlphaBot`.
- 코드 변경 여부: 없음. 보고서 파일만 신규 생성.

> 표기 원칙: 코드에서 확인한 내용은 **근거**로 표시했고, 제공 DB 스냅샷에서 도출한 내용은 **DB 스냅샷 근거**로 표시했다. 운영 DB의 SP 내부 구현은 현재 코드 저장소만으로 확인되지 않아 **추가 확인 필요**로 분리했다.

---

## 1. 시스템 요약

| 프로젝트 | 앱 유형 | 실제 조회 `SvcType` | 실행 후보 조건 | 제공 DB 스냅샷상 주요 활성 작업 |
|---|---|---|---|---|
| `FinUp.CollectData.App.AlphaBot` | WPF / `WinExe` / .NET 6 Windows | `Data` | `DelDT IS NULL`, `T_OperationTerm.DelDT IS NULL`, `DisplayAlphabot = 1`, `SvcType = 'Data'`, `Active = 1` | 정책/파트너스 아침 발송, 시장지수 크롤링, 네이버 키워드 랭킹, MongoDB 정리, 뉴스 크롤링 체크 |
| `FinUp.Finance.App.AlphaBot` | WPF / `WinExe` / .NET 6 Windows | `Finance` | 동일, `SvcType = 'Finance'` | 랭킹 집계, 인베스트RSS |
| `FinUp.Radar.App.AlphaBot` | WPF / `WinExe` / .NET Framework 4.7 | `ThemeRadar` | 동일, `SvcType = 'ThemeRadar'` | 공시 수집, 종목 가격 업데이트, 키워드 분석, 랭킹, Clean, MongoDB/API/뉴스 체크, 검색/유사도/브리핑/사용자 알림 |
| `FinUp.Stock.App.AlphaBot` | WPF / `WinExe` / .NET Framework 4.7 | `StockPoint` | 동일, `SvcType = 'StockPoint'` | SMS/APP/Alarm Push, 자동결제, API Service, 사이트 체크, AWS 모니터링, Email/SMS 외부 발송, 휴면/알림/통계/포인트/유튜브/럭키박스 관련 작업 |

### 핵심 변경 판단

1. 기존 보고서의 “중복 실행 위험”은 DB 스냅샷으로 더 강하게 확인된다.
   - `T_Operation.LastExecDT`가 실행 선점/완료 시각 역할을 겸하고 있다.
   - 별도 `Running`, `ClaimedBy`, `ClaimedAt`, `RetryCount` 컬럼은 제공 스냅샷에 없다.
2. `T_OperationTerm.MaxDuration` 컬럼은 운영상 중요한 제한값처럼 보이지만, 현재 4개 앱의 스케줄 조회 코드에서는 선택/사용되지 않는다.
3. `T_Operation.AliveCheck`, `EnableAlarm`, `LastSeek`, `OperationType`도 현재 4개 앱의 공통 스케줄 조회 SQL에는 포함되지 않는다.
4. `DisplayAlphabot = 0`인데 `Active = 1`이고 `LastExecDT`가 최신인 행이 존재한다. 이 작업들은 현재 분석 대상 AlphaBot 코드의 공통 조회 조건으로는 제외되므로, 다른 서비스/구버전/별도 배치에서 갱신 중인지 추가 확인이 필요하다.

---

## 2. 실행 진입점

| 프로젝트 | 진입점 | 메인 화면/초기화 | 자동 시작 |
|---|---|---|---|
| CollectData | `App.xaml` → `MainWindow.xaml` | `MainWindow.xaml`에서 `MainViewModel` 생성 | 수동 시작 버튼 |
| Finance | `App.xaml` → `MainWindow.xaml` | `MainWindow.xaml`에서 `MainViewModel` 생성 | 수동 시작 버튼 |
| Radar | `App.xaml` → `MainWindow.xaml` | `MainWindow.Loaded`에서 `InitializeMember()` | `AppSetting.ConfigServerType == "REAL"`이면 자동 시작 |
| Stock | `App.xaml` → `MainWindow.xaml` | `MainWindow.Loaded`에서 `InitializeMember()` | 수동 시작 버튼 |

**근거**

- `Program.cs`는 4개 대상 프로젝트에서 발견되지 않음.
- WPF 시작점:
  - `FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot/App.xaml:5` — `StartupUri="MainWindow.xaml"`
  - `FinUp.Finance.App.AlphaBot/FinUp.Finance.App.Alphabot/App.xaml:5` — `StartupUri="MainWindow.xaml"`
  - `FinUp.Radar.App.AlphaBot/App.xaml:5` — `StartupUri="MainWindow.xaml"`
  - `FinUp.Stock.App.AlphaBot/App.xaml:5` — `StartupUri="MainWindow.xaml"`
- WPF/WinExe:
  - `FinUp.CollectData.App.AlphaBot/...csproj:5-7` — `OutputType=WinExe`, `UseWPF=true`
  - `FinUp.Finance.App.AlphaBot/...csproj:4-6` — `OutputType=WinExe`, `UseWPF=true`
  - `FinUp.Radar.App.AlphaBot/FinUp.Radar.App.AlphaBot.csproj:8-13` — `OutputType=WinExe`, WPF ProjectTypeGuid
  - `FinUp.Stock.App.AlphaBot/FinUp.Stock.App.AlphaBot.csproj:8-14` — `OutputType=WinExe`, WPF ProjectTypeGuid

---

## 3. 루프 구조

| 프로젝트 | 루프 시작 위치 | 루프 방식 | 기본 Tick | DB 실행 주기 반영 방식 | 중첩 위험 |
|---|---|---|---:|---|---|
| CollectData | `MainViewModel.CommandStart_Click` | `DispatcherTimer` + `new Thread` | 설정 `AlphaBot.ObServeTime`, 제공 Release config는 5초 | 매 Tick마다 `T_OperationTerm.LoopInterval`/`OnceTime` 비교 | High |
| Finance | `MainViewModel.CommandStart_Click` | `DispatcherTimer` + `new Thread` | 5초 고정 | 동일 | High |
| Radar | `MainWindow.btnStart_Click` | `DispatcherTimer` + `new Thread` | 5초 | 동일 | High |
| Stock | `MainWindow.btnStart_Click` | `DispatcherTimer` + `new Thread` + Alive 1분 Timer | 5초 | 동일 | Medium~High |

**근거**

- CollectData:
  - `FinUp.CollectData.../ViewModel/MainViewModel.cs:43-44` — `tMainTimer`, `tObserveTimer`
  - `FinUp.CollectData.../ViewModel/MainViewModel.cs:137-149` — Start/Stop은 Timer만 제어
  - `FinUp.CollectData.../Biz/AlphaBotBiz.cs:290`, `325-331` — 작업 Thread 생성 후 내부에서 다시 Thread 생성
- Finance:
  - `FinUp.Finance.../ViewModel/MainViewModel.cs:42-43`, `136-148`
  - `FinUp.Finance.../Biz/AlphaBotBiz.cs:271`, `306-312`
- Radar:
  - `FinUp.Radar.App.AlphaBot/MainWindow.xaml.cs:123-139`, `918-934`
  - `FinUp.Radar.App.AlphaBot/MainWindow.xaml.cs:454`, `712-718`
- Stock:
  - `FinUp.Stock.App.AlphaBot/MainWindow.xaml.cs:80-90`, `912-918`, `928-933`
  - `FinUp.Stock.App.AlphaBot/MainWindow.xaml.cs:335`, `678-730`

### DB 스냅샷으로 확인된 고빈도 작업

| 앱 | OIdx / 작업 | Type | LoopInterval / OnceTime | 위험 포인트 |
|---|---|---|---|---|
| Stock | `1 SMS Push` | Loop | 5초 | Timer tick도 5초라 매 Tick 실행 후보. 처리 지연 시 중복/지연 위험 |
| Stock | `2 APP Push` | Loop | 10초 | 고빈도 Push 처리 |
| Stock | `11 API Service` | Loop | 10초 | 외부 API/DB 동시 부하 가능 |
| Stock | `151 외부 SMS - 다날` | Loop | 5초 | 외부 SMS 연동 중복 발송 Critical 가능성 |
| Stock | `130 Email Push` | Loop | 10초 | 대량 이메일 발송 큐 중복 위험 |
| ThemeRadar | `10020 공시 수집` | Loop | 30초 | 외부 공시/뉴스 수집 중복 가능 |
| ThemeRadar | `10030 종목 가격 업데이트` | Loop | 60초 | 종목 가격/캐시 갱신 부하 |
| ThemeRadar | `10200 MongoDB 상태 체크` | Loop | 60초 | DB/외부 연결 상태 체크 |
| Data | `30070 뉴스 크롤링 체크` | Loop | 3600초 | 뉴스 수집 상태 감시 |
| Finance | `40001 랭킹 집계` | Loop | 3600초 | 집계성 작업, 장시간 실행 시 중복 위험 |

**DB 스냅샷 근거**

- `T_OperationTerm.OTIdx=1`, `OIdx=1`, `Type=2`, `LoopInterval=5`, `MaxDuration=60`
- `T_OperationTerm.OTIdx=151`, `OIdx=151`, `Type=2`, `LoopInterval=5`, `MaxDuration=20`
- `T_OperationTerm.OTIdx=10002`, `OIdx=10020`, `Type=2`, `LoopInterval=30`, `LoopStartTime=07:35:00`, `LoopEndTime=23:25:00`
- `T_OperationTerm.OTIdx=40001`, `OIdx=40001`, `Type=2`, `LoopInterval=3600`

---

## 4. DB 처리 흐름

### 4.1 공통 스케줄 조회 SQL 구조

```sql
SELECT      TOT.OIdx,
            Name,
            ManualExec,
            LastExecDT,
            OTIdx,
            'TermType' = Type,
            CASE WHEN TOT.Active = 0 THEN 0 ELSE TOT.Active END Active,
            TOT.Active AS OperActive,
            CASE WHEN TOT.Active = 0 THEN '비활성화' ELSE '활성화' END ActiveName,
            StockOpen,
            (SELECT OffDay
             FROM StockData.dbo.T_StockCalendar WITH(NOLOCK)
             WHERE YYYY_MM_DD = CONVERT(VARCHAR, GETDATE(), 23)) OffDay,
            OnceTime,
            LoopInterval,
            LoopStartTime,
            LoopEndTime,
            GETDATE() DateTimeNow
FROM        SystemData.dbo.T_Operation TOT WITH(NOLOCK)
INNER JOIN  SystemData.dbo.T_OperationTerm TOTM WITH(NOLOCK)
        ON  TOT.OIdx = TOTM.OIdx
WHERE       TOT.DelDT IS NULL
AND         TOTM.DelDT IS NULL
AND         TOT.DisplayAlphabot = 1
AND         TOT.SvcType = ...
```

**근거**

- CollectData: `FinUp.Core.DS.Dac/FinUp.Core.DS.Dac/Sql/SqlOperationDac.cs:15-49`, `SvcType=@SvcType`
- Finance: `FinUp.Finance.App.AlphaBot/.../SqlOperationDao.cs:19-54`, `SvcType=@SvcType`
- Radar: `FinUp.Radar/Sql/SqlOperation.cs:11-47`, `SvcType='ThemeRadar'`
- Stock: `FinUp.Stock.App/Sql/SqlSender.cs:12-47`, `SvcType='StockPoint'`

### 4.2 제공 DB 컬럼 중 현재 스케줄러가 사용하지 않는 컬럼

| 테이블 | 컬럼 | 제공 DB상 의미로 보이는 것 | 현재 4개 AlphaBot 스케줄러 사용 여부 | 위험 |
|---|---|---|---|---|
| `T_Operation` | `OperationType` | 작업 분류 | 조회 SQL에 없음 | 운영자가 Type을 바꿔도 앱 동작에 반영되지 않을 수 있음 |
| `T_Operation` | `AliveCheck` | Alive 감시 여부 | 조회 SQL에 없음 | 코드의 Alive는 별도 하드코딩 경로 사용 |
| `T_Operation` | `EnableAlarm` | 알람 여부 | 조회 SQL에 없음 | 장애 알림 정책과 실제 앱 동작 불일치 가능 |
| `T_Operation` | `LastSeek` | 진행 커서/마지막 처리 위치 추정 | 조회 SQL에 없음 | 예: `OIdx=170`의 `LastSeek=14591706`은 별도 작업 내부에서만 의미 있을 가능성 |
| `T_OperationTerm` | `MaxDuration` | 최대 실행 허용 시간 | 조회 SQL에 없음 | 장시간 실행 감지/강제 중단에 사용되지 않음 |

**근거**

- 위 공통 조회 SQL은 `OperationType`, `AliveCheck`, `EnableAlarm`, `LastSeek`, `MaxDuration`을 SELECT하지 않는다.
- `rg` 검색 결과 `MaxDuration`은 4개 앱/관련 SQL에서 사용 흔적이 확인되지 않았다.
- `FinUp.Stock.App.AlphaBot/Type/OperationType.cs:89`에 `EnableAlarm` 속성은 있으나 생성자/업데이트 및 조회 SQL에서 값이 주입되지 않는다.

---

## 5. 반복 업무 상태 흐름

### 5.1 코드 기준 흐름

```text
T_Operation / T_OperationTerm 조회
→ DisplayAlphabot, SvcType, DelDT 조건으로 후보 제한
→ member.Active == 1 확인
→ operation.Active == 1 확인
→ StockOpen / OffDay / LoopInterval / OnceTime 조건 확인
→ LastExecDT 업데이트
→ Thread 시작
→ actionState = Running
→ 작업 실행
→ OperationTermHistory START / ERROR / STOP(또는 END) 기록
→ actionState = Stop
```

### 5.2 DB 스냅샷을 반영한 상태 의미

| 상태 요소 | 실제 저장 위치 | 코드 사용 방식 | 문제점 |
|---|---|---|---|
| 대기/활성 | `T_Operation.Active`, `T_OperationTerm.Active` | 둘 다 1이어야 실행 후보 | 둘 중 하나만 0이면 실행 안 됨. 운영자는 두 테이블 동시 확인 필요 |
| 실행 시각 | `T_Operation.LastExecDT` | 실행 전에 업데이트하거나, Stock은 실행 시작부에서 업데이트 | 완료 시각이 아니라 “시도/선점 시각”에 가까움 |
| 실행 이력 | `USP_OperationTermHistory_Insert` | START/ERROR/STOP 또는 START/ERROR/END | SP 내부 스키마 확인 필요 |
| 실행 중 | 메모리 `member.actionState` | 같은 프로세스 내 중복 방지 | 다중 프로세스/서버 간 중복 방지 불가 |
| 최대 시간 | `T_OperationTerm.MaxDuration` | 현재 스케줄러 미사용 | 장시간 Running 감시가 코드에 연결되지 않음 |

---

## 6. DB 스냅샷 기반 활성 작업 분석

### 6.1 CollectData / `SvcType='Data'`

| OIdx | Name | Operation Active | DisplayAlphabot | 실행 여부 판단 | Term 요약 |
|---:|---|---:|---:|---|---|
| 30010 | 뉴스 크롤링 | 1 | 0 | 현재 공통 조회 SQL 기준 제외 | `Loop 30초`, `OTIdx=30010` |
| 30011 | 정책 크롤링 아침 발송 | 1 | 1 | 실행 후보 | `Once 08:00`, `StockOpen=1` |
| 30012 | 파트너스 크롤링 아침 발송 | 1 | 1 | 실행 후보 | `Once 08:00` |
| 30020 | 시장지수 크롤링 | 1 | 1 | 실행 후보 | `06:20`, `08:00`, `15:40`, `16:10` 다중 Once |
| 30030 | 네이버 키워드 랭킹 | 1 | 1 | 실행 후보 | `Once 15:40` |
| 30040 | 증시일정 크롤링 | 0 | 0 | 제외 | Term도 Active 0 |
| 30050 | MongoDB 정리 | 1 | 1 | 실행 후보 | `Once 05:00` |
| 30060 | 테마 사이트 크롤링 | 0 | 0 | 제외 | Term Active 0 |
| 30070 | 뉴스 크롤링 체크 | 1 | 1 | 실행 후보 | `Loop 3600초` |

**운영상 특이점**

- `OIdx=30010`은 `Active=1`이고 `LastExecDT=2026-05-14 12:55:52`로 최신이지만 `DisplayAlphabot=0`이다.
- 현재 확인한 `SqlOperationDac.ListOperationTerm("Data")`는 `TOT.DisplayAlphabot = 1`을 요구하므로, 이 앱 코드만으로는 `30010`이 실행 후보에 포함되지 않는다.
- **추측**: `30010`은 다른 프로세스, 구버전, hotfix 빌드, 또는 다른 조회 로직에서 실행 중일 가능성이 있다. DB 실행 주체 확인 필요.

### 6.2 Finance / `SvcType='Finance'`

| OIdx | Name | Operation Active | DisplayAlphabot | 실행 여부 판단 | Term 요약 |
|---:|---|---:|---:|---|---|
| 40001 | 랭킹 집계 | 1 | 1 | 실행 후보 | `Loop 3600초`, 전일/금일 LastExec 최신 |
| 40002 | 인베스트RSS | 1 | 1 | 실행 후보 | `Loop 10800초`, `09:00~18:00` |
| 40003 | 증시일정이관 | 0 | 0 | 제외 | `Loop 3600초`, Term Active 0 |

**운영상 특이점**

- `40003`은 `Active=0`, `DisplayAlphabot=0`인데 `LastExecDT=2026-05-14 12:15:24`로 최신이다.
- 현재 Finance AlphaBot의 `ListOperationTerm("Finance")` 조건과 불일치하므로 실행 주체 추가 확인 필요.

### 6.3 Radar / `SvcType='ThemeRadar'`

| OIdx | Name | Operation Active | DisplayAlphabot | 실행 여부 판단 | Term 요약 |
|---:|---|---:|---:|---|---|
| 10020 | 공시 수집 | 1 | 1 | 실행 후보 | `Loop 30초`, `07:35~23:25` |
| 10030 | 종목 가격 업데이트 | 1 | 1 | 실행 후보 | `Loop 60초`, `04:55~15:40` |
| 10040 | 키워드 단어 분석 | 1 | 1 | 실행 후보 | `Once 04:00`, `MaxDuration=2500` 미사용 |
| 10060 | 랭킹 | 1 | 1 | 실행 후보 | `Loop 1800초` |
| 10070 | Clean | 1 | 1 | 실행 후보 | `Once 04:30`, `MaxDuration=9000` 미사용 |
| 10140 | 1시간 푸시 | 1 | 1 | 실행 후보 | `Loop 3600초`, `08:00~23:59:59` |
| 10200 | MongoDB 상태 체크 | 1 | 1 | 실행 후보 | `Loop 60초` |
| 10240 | API Health체크 | 1 | 1 | 실행 후보 | `Loop 300초` |
| 10260 | 뉴스 수집 체크 | 1 | 1 | 실행 후보 | `Loop 7200초` |
| 10360 | 뉴스중복포함 건수집계 | 1 | 1 | 실행 후보 | `Once 02:00` |
| 10370 | 뉴스최근건수 건수집계 | 1 | 1 | 실행 후보 | `Loop 600초` |
| 10390 | 뉴스텔레그램 마케팅 전송 | 1 | 1 | 실행 후보 | `Once 20:00` |
| 10400 | 검색 인덱스 테이블 갱신 | 1 | 1 | 실행 후보 | `Loop 600초` |
| 10410 | 테마 유사도 계산 | 1 | 1 | 실행 후보 | `Once 22:00` |
| 10440 | 브리핑 푸시 | 1 | 1 | 실행 후보 | `Once 07:30`, `08:15`, `15:50` |
| 10500 | 다트공시 장전브리핑 | 1 | 1 | 실행 후보 | `Once 23:30` |
| 10520 | 테마록 랭킹정보 사용자 알림 | 1 | 1 | 실행 후보 | `Once 07:00`, `07:10`, `07:20`, `StockOpen=1` |

**운영상 특이점**

- `10150`, `10160`은 `T_OperationTerm.Active=1`이지만 `T_Operation.Active=0`이므로 코드상 실행되지 않는다.
- `10000`은 `AliveCheck=1`이지만 `DisplayAlphabot=0`이라 일반 조회에는 제외된다. Radar 코드는 별도 `tAlive`에서 `OIdx=10000`, `OTIdx=10023`으로 이력을 기록한다.
  - 근거: `FinUp.Radar.App.AlphaBot/MainWindow.xaml.cs:153-159`

### 6.4 Stock / `SvcType='StockPoint'`

| OIdx | Name | Operation Active | DisplayAlphabot | 실행 여부 판단 | Term 요약 |
|---:|---|---:|---:|---|---|
| 1 | SMS Push | 1 | 1 | 실행 후보 | `Loop 5초` |
| 2 | APP Push | 1 | 1 | 실행 후보 | `Loop 10초` |
| 3 | Alarm Push | 1 | 1 | 실행 후보 | `Loop 30초` |
| 4 | 매출현황 | 1 | 1 | 실행 후보 | `Loop 3600초`, 코드에서 정시 실행 제한 |
| 5 | 자동결제 | 1 | 1 | 실행 후보 | `Once 10:00`, `16:00`, `20:00` |
| 8 | SMS 모니터 | 1 | 1 | 실행 후보 | `Once 08:30` |
| 11 | API Service | 1 | 1 | 실행 후보 | `Loop 10초` |
| 30 | StockPoint 사이트 체크 | 1 | 1 | 실행 후보 | `Loop 600초` |
| 38 | 메인웹 캐시 업데이트 | 1 | 1 | 실행 후보 | `Loop 300초` |
| 39 | 만족도 평가 대상자 PUSH | 1 | 1 | 실행 후보 | `Once 12:00` |
| 40 | 리뷰 대상자 PUSH | 1 | 1 | 실행 후보 | `Once 18:00` |
| 41 | 쿠폰 만료 대상자 PUSH | 1 | 1 | 실행 후보 | `Once 08:30` |
| 44 | API 사이트 Health 체크 | 1 | 1 | 실행 후보 | `Loop 300초` |
| 45 | AWS 모니터링 Process | 1 | 1 | 실행 후보 | `Loop 60초` |
| 46 | AWS 모니터링 Summary(1시간) | 1 | 1 | 실행 후보 | `Loop 3600초` |
| 47 | AWS 모니터링 Summary(하루) | 1 | 1 | 실행 후보 | `Once 04:00` |
| 122~126 | 멘토/사이트/영수증 관련 | 1 | 1 | 실행 후보 | Once/Loop 혼재 |
| 130 | Email Push | 1 | 1 | 실행 후보 | `Loop 10초` |
| 138 | 사이트 동작 체크 | 1 | 1 | 실행 후보 | `Loop 60초` |
| 140 | 마케팅 수신 동의 안내 | 1 | 1 | 실행 후보 | `Once 13:00` |
| 144~151 | 멘토/TSSA/SMS 등 | 1 | 1 | 실행 후보 | Once/Loop 혼재, `151`은 `Loop 5초` |
| 154, 156, 163, 166~175 | 이벤트/포인트/통계/유튜브/럭키박스 | 1 | 1 | 실행 후보 | 대부분 Once 또는 300초 Loop |

**운영상 특이점**

- `OIdx=1`, `151`은 `LoopInterval=5초`다. 앱의 `tMainTimer`도 5초이므로 작업 시간이 5초를 넘거나 DB 갱신이 실패하면 다음 Tick과 경합하기 쉽다.
- `OIdx=5 자동결제`는 `OTIdx=5`, `6`, `139`로 하루 3회 실행된다. 결제성 작업이므로 중복 실행 시 Critical 위험이다.
- `OIdx=170 컨텐츠 조회수 업데이트 처리`는 `LastSeek=14591706` 값을 가진다. 하지만 스케줄러 조회 SQL에는 `LastSeek`가 포함되지 않으므로, 이 값은 개별 작업 내부에서 별도로 조회/사용하는지 확인해야 한다.

---

## 7. 중복 처리 위험

| 위험도 | 위치 | DB 스냅샷 반영 시나리오 | 원인 | 권장 확인/개선 |
|---|---|---|---|---|
| Critical | Stock `OIdx=5 자동결제`, `151 외부 SMS`, `1 SMS Push`, `2 APP Push`, `130 Email Push` | 5~10초 단위 작업 또는 결제/발송 작업이 다중 인스턴스에서 동시에 실행 | `LastExecDT`만 갱신하고 원자적 claim 컬럼/조건 없음 | `USP_Operation_Update` 내부에 조건부 갱신/락이 있는지 확인. 없다면 `Claim` SP 추가 |
| Critical | Collect/Radar 뉴스·공시·푸시 계열 | 외부 발송 성공 후 이력/상태 저장 실패 시 재발송 또는 누락 | 외부 연동과 DB 상태 저장이 하나의 트랜잭션으로 묶일 수 없음 | 발송 idempotency key 또는 대상별 처리 상태 필요 |
| High | 모든 앱 | `MaxDuration` 초과 작업이 다음 주기까지 Running으로 남거나, 반대로 메모리 상태만 Stop으로 돌아가 중복 실행 | `MaxDuration` 미사용, 실행 상태는 메모리 값 | `OperationTermHistory` 기반 장기 실행 감시 또는 DB Running 상태 필요 |
| High | Data `30010`, Finance `40003` | 현재 코드 조건으로 제외되어야 할 행의 `LastExecDT`가 최신 | 다른 실행 주체 존재 가능 | 실제 배포 서버/프로세스 목록 대조 필요 |
| Medium | `DisplayAlphabot=0` + `Active=1` 행 | 운영자가 Active만 보고 실행 중이라고 판단하나 AlphaBot UI/조회에서는 제외 | 실행 후보 조건이 복합적 | 운영 대시보드에서 Active/Display/Term Active를 함께 표시 |

---

## 8. 예외/복구 구조

| 프로젝트 | 현재 구조 | DB 스냅샷 반영 평가 |
|---|---|---|
| CollectData | 다수 `catch { }`, `RunTask`에서 ERROR/STOP 이력 기록 | `MaxDuration`이 있어도 코드가 사용하지 않아 장시간 실행 감지 약함 |
| Finance | 다수 `catch { }`, `RunTask`에서 ERROR/STOP 이력 기록 | 실행 후보가 적지만 집계/RSS 작업 실패 원인 추적이 약함 |
| Radar | App 전역 예외 처리 + `Trace`, 작업 이력 기록 | 다수 고빈도/외부 연동 작업이 있어 `Task.Run` fire-and-forget 실패 추적 필요 |
| Stock | 전역 Telegram, `ProcessStart`의 `try/catch/finally`로 ERROR/END 기록 | 결제/발송 작업은 구조가 상대적으로 명확하지만 중복 선점 방지는 여전히 DB 확인 필요 |

**근거**

- CollectData `RunTask`: `FinUp.CollectData.../Biz/AlphaBotBiz.cs:337-373`
- Finance `RunTask`: `FinUp.Finance.../Biz/AlphaBotBiz.cs:318-353`
- Radar `RunTask`: `FinUp.Radar.App.AlphaBot/MainWindow.xaml.cs:1001-1036`
- Stock `ProcessStart`: `FinUp.Stock.App.AlphaBot/MainWindow.xaml.cs:678-730`

---

## 9. DB 부하 위험

| 위험도 | 항목 | DB 스냅샷 반영 근거 | 설명 |
|---|---|---|---|
| High | 5초 Polling + 고빈도 Loop | Stock `OIdx=1`, `151`은 5초, `2`, `11`, `130`은 10초 | 매 Tick마다 메타 조회 후 실행 조건 판단. 활성 작업이 많아질수록 DB 부하 증가 |
| High | `WITH(NOLOCK)` | 공통 조회 SQL에 `T_Operation`, `T_OperationTerm`, `T_StockCalendar WITH(NOLOCK)` 사용 | Dirty read로 Active/LastExecDT/OffDay를 잘못 읽을 수 있음 |
| Medium | `MaxDuration` 미사용 | 제공 `T_OperationTerm.MaxDuration`에 값 존재하나 코드 미사용 | 장시간 실행 작업이 DB 차원에서 감시되지 않을 수 있음 |
| Medium | `LastExecDT` 단일 컬럼 의존 | 대부분 작업의 `LastExecDT`가 최근 값으로 계속 갱신 | 실행 시작/완료/실패/재시도 의미가 혼재 |

---

## 10. 리팩터링 우선순위

| 우선순위 | 개선 대상 | 이유 | 권장 방식 |
|---:|---|---|---|
| 1 | DB 원자 선점 | 결제/SMS/Push/Email 중복은 Critical | `USP_Operation_Claim` 또는 `UPDATE ... WHERE LastExecDT = @previous AND Active=1` + 영향 행 수 확인 |
| 2 | Running 상태 컬럼/이력 강화 | 현재는 메모리 `actionState`라 다중 인스턴스 방지 불가 | `Status`, `ClaimedAt`, `ClaimedBy`, `ExecID`, `RetryCount` 추가 검토 |
| 3 | `MaxDuration` 적용 | DB에 이미 존재하는 운영 기준이 코드에 반영되지 않음 | `OperationType` 모델에 `MaxDuration` 추가 후 장시간 실행 감시 |
| 4 | `catch { }` 제거 | 장애 원인 추적성 부족 | 공통 `SetLog`/NLog/OperationTermHistory ERROR 기록으로 통일 |
| 5 | Stop/종료 제어 | Stop 버튼은 Timer만 멈춤 | `CancellationToken`, 실행 Thread registry, 안전 종료 대기 |
| 6 | 설정/운영 UI 정합성 | `Active`, `DisplayAlphabot`, `Term.Active` 불일치 다수 | 운영 화면/보고서에서 “실제 실행 후보” 계산 컬럼 제공 |

---

## 11. 다음 분석 단계

1. **SP 내부 확인**
   - `SystemData.dbo.USP_Operation_Update`
   - `SystemData.dbo.USP_OperationTermHistory_Insert`
   - 원자적 업데이트, 락, 중복 방지 조건이 있는지 확인해야 한다.

2. **실제 실행 주체 확인**
   - `Data OIdx=30010`, `Finance OIdx=40003`처럼 현재 코드 조회 조건과 맞지 않지만 `LastExecDT`가 최신인 작업의 실행 주체 확인.
   - 운영 서버의 실행 exe, Windows 작업 스케줄러, 서비스, 구버전 배포본, hotfix exe 확인 필요.

3. **`MaxDuration` 운영 의미 확인**
   - DB에는 존재하지만 코드에서 미사용이다.
   - 운영자가 이 값을 장애 판단 기준으로 믿고 있다면 실제 감시 누락 위험이 크다.

4. **고위험 작업 단위 상세 추적**
   - Stock `OIdx=5 자동결제`, `151 외부 SMS - 다날`, `1 SMS Push`, `2 APP Push`, `130 Email Push`
   - Radar `10020 공시 수집`, `10030 종목 가격 업데이트`, `10440 브리핑 푸시`, `10520 사용자 알림`
   - 각 작업 내부의 대상 조회 조건, 처리 전 상태 변경, 완료/실패 업데이트, 재시도 정책을 별도 분석해야 한다.

5. **운영 로그 대조**
   - `OperationTermHistory`에서 동일 `OIdx/OTIdx`의 `START`가 겹치는지 확인.
   - `ERROR` 후 `STOP/END`가 항상 남는지 확인.
   - `MaxDuration` 초과 실행 기록이 있는지 확인.

---

## 12. 결론

제공된 `T_Operation`, `T_OperationTerm` 스냅샷을 반영하면, 이 AlphaBot 계열은 단순 Timer 앱이 아니라 DB 테이블을 스케줄 정의 저장소로 사용하는 운영 배치 플랫폼에 가깝다. 다만 현재 코드 기준으로는 DB 스케줄 정의 중 일부 중요한 컬럼(`MaxDuration`, `AliveCheck`, `EnableAlarm`, `LastSeek`)이 공통 스케줄러에 연결되어 있지 않다.

가장 큰 운영 리스크는 다음 3가지다.

1. **중복 선점 부재**: `LastExecDT` 갱신만으로 다중 인스턴스 중복 실행을 막기 어렵다.
2. **고빈도 결제/발송 작업**: 5~10초 Loop 작업이 SMS, API, Email, 외부 SMS에 존재한다.
3. **DB 정의와 코드 사용 범위 불일치**: `DisplayAlphabot=0`인데 최근 실행된 작업, `MaxDuration` 미사용, Alive/Alarm 컬럼 미사용이 확인된다.

따라서 다음 단계는 코드 수정이 아니라, 우선 `USP_Operation_Update`와 `USP_OperationTermHistory_Insert`의 실제 구현 및 운영 실행 주체를 확인하는 것이 안전하다.
