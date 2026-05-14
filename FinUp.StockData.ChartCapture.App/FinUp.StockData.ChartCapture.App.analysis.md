# FinUp.StockData.ChartCapture.App 정밀 분석 보고서

- 작성일: 2026-05-13
- 분석 대상: `/mnt/c/Dev/FinUp.StockData.ChartCapture.App`
- 산출물: `FinUp.StockData.ChartCapture.App.analysis.md`, `FinUp.StockData.ChartCapture.App.analysis.html`
- 분석 범위: `StartUp` 설정으로 선택되는 3가지 실행 옵션(`Scheduler`, `Chart`, 그 외 기본값 `Robo`)과 외부 API/DB/TCP/파일 연동
- 주의: 원본 `App.config`에는 DB 연결 문자열 암호문, API key, 파일 계정/비밀번호가 존재한다. 본 보고서는 노출을 줄이기 위해 민감값을 마스킹해 설명한다.

## 1. 핵심 결론

`FinUp.StockData.ChartCapture.App`는 Windows Forms 기반의 .NET Framework 4.7 WinExe이며, 실제 실행 모드는 `App.config`의 `StartUp` 값에 의해 3가지로 분기된다.

| 옵션 | 실행 Form | 주요 목적 | 주요 외부 연동 | 중요도 요약 |
|---|---|---|---|---|
| `Scheduler` | `Scheduler` | 장 종료 후 정해진 시점에 예탁금/신용잔고/테마록 차트를 캡처 | StockData 시장일정 API, StockData 차트 HTML, 파일 저장/Windows impersonation | 배치성. DB/Chat API 쓰기는 없고 일정 API와 차트 페이지 의존도가 큼 |
| `Chart` | `TcpListenerChart` | TCP 요청을 받아 테마 차트 이미지를 즉시 생성 | TCP 8280, StockData 차트 HTML, 파일 저장/Windows impersonation | 기본 설정값. Finance/editor 쪽에서 파일명을 응답받는 동기식 캡처 서버 역할 |
| 기타/`Robo` | `TcpListenerRobo` | 날짜 기반 로보 추천 차트를 생성하고 DB/채팅 파일 API까지 반영 | TCP 8279, DBStockPoint SQL, BizStock 차트 HTML, Chat API multipart POST, 파일 저장/Windows impersonation | 외부 연동이 가장 많고 장애/보안 영향이 가장 큼 |

현재 `App.config`의 `StartUp`은 `Chart`로 설정되어 있어, 설정 변경이 없으면 `TcpListenerChart`가 실행된다.

## 2. 실행 옵션 판별 근거

### 직접 근거

- `Program.cs:21-27` — `StartUp` appSetting을 읽고 `Scheduler`이면 `Scheduler`, `Chart`이면 `TcpListenerChart`, 그 외 모든 값은 `TcpListenerRobo`를 실행한다.
- `App.config:29` — 현재 설정은 `StartUp=Chart`이다.
- `FinUp.StockData.ChartCapture.App.csproj:8-11` — 프로젝트는 WinExe이고 TargetFrameworkVersion은 `v4.7`이다.
- `FinUp.StockData.ChartCapture.App.csproj:217-221` — 주요 NuGet 의존성은 `CefSharp.OffScreen 105.3.390`, `Newtonsoft.Json 13.0.1`이다.
- `FinUp.StockData.ChartCapture.App.csproj:187-214` — 내부 프로젝트 의존성으로 `FinUp.Core.Data`, `FinUp.Core.Fundamentals`, `FinUp.StockData.Fundamentals`, `FinUp.Chat.Model` 등을 참조한다.

### 추론

- “3가지 옵션”은 코드상 명시된 `StartUp` 분기 3개로 해석하는 것이 가장 근거가 강하다.
- `ManualCapture`, `CaptureTest`도 포함되어 있으나 `Program.Main`에서 선택되지 않으므로 운영 옵션이 아니라 수동/테스트 Form에 가깝다.

## 3. 공통 구성 및 외부 연동 표면

### 공통 설정값

| 설정 키 | 역할 | 근거 |
|---|---|---|
| `ChartUrl` | 로보/수동 캡처용 BizStock 차트 페이지 base URL | `App.config:7`, `TcpListenerRobo.cs:27` |
| `StockDataUrl` | StockData API 및 차트 페이지 base URL | `App.config:28`, `Scheduler.cs:66`, `TcpListenerChart.cs:30`, `Job/Deposit.cs:17`, `Job/Themelog.cs:17` |
| `ImageUrl` | 구버전 로보 메시지의 이미지 URL 조립용 | `App.config:9`, `TcpListenerRobo.cs:28`, `TcpListenerRobo.cs:363` |
| `CacheloadUrl` | 구버전 로보 채팅 캐시 갱신 API | `App.config:23`, `TcpListenerRobo.cs:382-383` |
| `ChatApiUrl` / `ChatApiKey` | V2 로보 업로드 API endpoint 및 header key | `App.config:24-27`, `TcpListenerRobo.cs:137-142` |
| `DBStockPoint` | DB 연결 문자열 암호문. `FinUp.Core.Data`에서 복호화 후 SQL 연결 | `App.config:22`, `FinUp.Core.Data/Extension.cs:77-83`, `FinUp.Core.Data/Sql.cs:35-38` |
| `FilePath*`, `FileUser*` | 캡처 이미지 저장 위치와 파일 저장 시 impersonation 계정 | `App.config:10-16`, `Job/Common.cs:14-18`, `WrapperImpersonationContext.cs:38-66` |

### 외부 연동 전체 목록

| 분류 | 방향 | 사용 옵션 | 상세 | 근거 |
|---|---|---|---|---|
| TCP Listener | inbound | Chart | 로컬 호스트 첫 번째 IP에 8280 바인드, `<EOF>`까지 수신 | `TcpListenerChart.cs:82-95`, `TcpListenerChart.cs:102-129` |
| TCP Listener | inbound | Robo | 로컬 호스트 첫 번째 IP에 8279 바인드, `<EOF>`까지 수신 | `TcpListenerRobo.cs:75-87`, `TcpListenerRobo.cs:95-114` |
| HTTP GET / WebRequest | outbound | Scheduler | `{StockDataUrl}/api/market/{from}/{to}`로 시장 일정 조회 | `Scheduler.cs:66`, `FinUp.StockData.Fundamentals/Util.cs:49-61`, `FinUp.Core.Fundamentals/Web/Util.cs:58-92` |
| Browser navigation | outbound | Scheduler | `StockDataUrl` 하위 차트 HTML 로드 후 PNG 캡처 | `Job/Deposit.cs:37-64`, `Job/Themelog.cs:36-47` |
| Browser navigation | outbound | Chart | 테마 차트 HTML 로드 후 PNG 캡처 | `TcpListenerChart.cs:147-158`, `TcpListenerChart.cs:177-185` |
| Browser navigation | outbound | Robo | BizStock captureview 페이지 로드 후 PNG 캡처 | `TcpListenerRobo.cs:202-218`, `TcpListenerRobo.cs:331-347` |
| SQL Server | outbound | Robo | `DBStockPoint` 조회/프로시저 실행 | `TcpListenerRobo.cs:154-180`, `TcpListenerRobo.cs:221-226`, `FinUp.Core.Data/Sql.cs:35-60` |
| HTTP multipart POST | outbound | Robo V2 | `{ChatApiUrl}/api/v1/chat/0/files:upload-robo`에 이미지와 Ref JSON 업로드 | `TcpListenerRobo.cs:133-142`, `TcpListenerRobo.cs:196-249` |
| HTTP GET | outbound | Robo legacy | `{CacheloadUrl}?chatidx=...` 캐시 갱신. 현재 `UpdateChartImageV2`에서는 미사용 | `TcpListenerRobo.cs:378-386` |
| Windows impersonation + file write | local/network | 전체 캡처 옵션 | 이미지 저장 전 지정 계정으로 impersonation | `Job/Common.cs:14-36`, `TcpListenerChart.cs:188-210`, `TcpListenerRobo.cs:390-411`, `WrapperImpersonationContext.cs:38-66` |

## 4. 옵션 1 — `Scheduler` 정밀 분석

### 4.1 실행 흐름

1. `Program.Main`이 `StartUp=Scheduler`일 때 `Scheduler` Form을 실행한다 (`Program.cs:21-24`).
2. `Scheduler_Load`에서 `Deposit` Job과 `Themelog` Job을 생성하고 이벤트를 연결한다 (`Scheduler.cs:31-46`).
3. `InitSchedule()`이 `StockDataUrl/api`를 넘겨 시장 일정을 조회한다 (`Scheduler.cs:62-67`).
4. 시장 종료시각 기준으로 두 작업을 예약한다.
   - 예수금/신용잔고: `EndTime + 40분` (`Scheduler.cs:77-85`, `Scheduler.cs:109-139`)
   - 테마록: `EndTime + 10분` (`Scheduler.cs:92-99`, `Scheduler.cs:142-167`)
5. `Deposit.Start()`는 신용잔고(`trchart.html`)와 예탁금(`custchart.html`) 차트를 순차 로드/캡처한다 (`Job/Deposit.cs:34-67`).
6. `Themelog.Start()`는 테마록(`themelogchart.html`) 차트를 로드/캡처하고 855x410 영역으로 crop 저장한다 (`Job/Themelog.cs:34-85`).

### 4.2 외부 API/연동 상세

| 연동 | 주소/대상 | 방식 | 데이터 | 실패 영향 |
|---|---|---|---|---|
| 시장 일정 API | `{StockDataUrl}/api/market/{from}/{to}` | `HttpWebRequest.GetResponseAsync()` | `Market` 목록 JSON | 일정 생성 실패. `result.Item1 == null`이면 스케줄 초기화 중단 |
| 차트 페이지 | `{StockDataUrl}/chart/trchart.html`, `/custchart.html`, `/themelogchart.html` | CefSharp OffScreen browser navigation | HTML/JS 렌더링 결과 | 캡처 이미지 미생성 또는 빈/오류 이미지 가능 |
| 파일 저장 | `FilePathStockData\Chart\*.png` | PNG file write | `yyyyMMdd_tr.png`, `yyyyMMdd_cust.png`, `yyyyMMdd_themelog.png` | 경로/권한 장애 시 Job 실패 |
| Windows 인증 | `FileUser` 설정값 | `LogonUser` + `WindowsIdentity.Impersonate()` | 파일 저장 권한 획득 | 계정/비밀번호 불일치 시 저장 실패 |

### 4.3 확인된 설계/운영상 특징

- 시장 일정 조회는 `FinUp.StockData.Fundamentals.Util.GetScheduleMarket()`를 경유하고, 이 함수는 내부적으로 `GetMarketInfo()` → `WebRequestAsync()`를 호출한다 (`FinUp.StockData.Fundamentals/Util.cs:125-141`, `FinUp.StockData.Fundamentals/Util.cs:29-61`).
- 스케줄 시간은 API의 `_marketInfo.EndTime`에 의존한다 (`Scheduler.cs:73-80`, `Scheduler.cs:94`).
- `Deposit.Start()`와 `Themelog.Start()`가 `async void`라 호출자 입장에서는 완료/실패를 await하지 못한다 (`Job/Deposit.cs:34`, `Job/Themelog.cs:34`).
- `_token` 필드가 Deposit 스케줄과 Themelog 스케줄에서 같은 필드로 재할당된다 (`Scheduler.cs:109-145`). `btnStop_Click`은 마지막으로 할당된 token만 취소할 가능성이 있다.
- `StartScheduleDeposit`은 실행 후 다시 `InitSchedule()`을 호출하므로 다음 일정 재등록 의도는 보이지만, 테마록 스케줄과 중복 등록/취소 관계는 코드만으로는 보장되지 않는다 (`Scheduler.cs:128-130`).

### 4.4 리스크 평가

| 리스크 | 심각도 | 근거 | 설명 |
|---|---:|---|---|
| 일정 API 실패 시 전체 배치 미수행 | 높음 | `Scheduler.cs:66-70` | `result.Item1`이 null이면 스케줄 초기화가 중단된다. 재시도/대체 일정은 없다. |
| 취소 토큰 공유로 한쪽 스케줄만 취소될 수 있음 | 중간 | `Scheduler.cs:111`, `Scheduler.cs:144`, `Scheduler.cs:53-56` | `_token`이 두 스케줄에서 덮어써진다. |
| Job 실패 관측/복구 약함 | 중간 | `Job/Deposit.cs:34`, `Job/Themelog.cs:34` | `async void` Job이라 상위 흐름에서 await/재시도/정확한 실패 전파가 어렵다. |
| 파일 계정/비밀번호 설정 의존 | 높음 | `App.config:15-16`, `WrapperImpersonationContext.cs:53-66` | 파일 저장이 Windows 계정 인증에 직접 의존한다. |

## 5. 옵션 2 — `Chart` / `TcpListenerChart` 정밀 분석

### 5.1 실행 흐름

1. `StartUp=Chart`이면 `TcpListenerChart` Form이 실행된다 (`Program.cs:24-25`).
2. 생성자에서 차트 크기(`ChartSize`)를 읽고 CefSharp locale을 `ko-kr`로 초기화한다 (`TcpListenerChart.cs:30-57`).
3. Form Load 시 OffScreen browser를 만들고 별도 Task에서 TCP Listener를 시작한다 (`TcpListenerChart.cs:62-74`).
4. Listener는 첫 번째 로컬 IP의 port 8280에 bind/listen한다 (`TcpListenerChart.cs:82-95`).
5. 요청 문자열을 `<EOF>`까지 UTF-8로 수신하고 `|`로 split한다 (`TcpListenerChart.cs:102-114`).
6. `arr[0] == "ThemeChart"`이면 `arr[1]` keyword, `arr[2]` keywordIdx로 `CaptureThemeChart()`를 호출한다 (`TcpListenerChart.cs:119-126`).
7. ChartUrlVersion이 `v2`이면 `lwthemechart_1250_400.html?keywordIdx=...`를 로드하고, 아니면 `themechart.html?Keyword=...&KeywordIdx=...`를 로드한다 (`TcpListenerChart.cs:147-158`).
8. 1.5초 대기 후 PNG를 캡처해 `FilePathFinance`에 저장하고 파일명을 `OK!!|{fileName}`으로 응답한다 (`TcpListenerChart.cs:159-185`, `TcpListenerChart.cs:128-129`).

### 5.2 외부 API/연동 상세

| 연동 | 주소/대상 | 방식 | 데이터 | 실패 영향 |
|---|---|---|---|---|
| TCP 요청 | `{hostFirstAddress}:8280` | raw socket | `ThemeChart|{keyword}|{keywordIdx}<EOF>` 형태로 추정 | 요청 처리 실패 시 `FAIL` 응답 |
| 차트 페이지 v2 | `{StockDataUrl}/chart/lwthemechart_1250_400.html?keywordIdx={keywordIdx}` | CefSharp navigation | HTML/JS chart rendering | 캡처 실패/잘못된 이미지 생성 |
| 차트 페이지 v1 | `{StockDataUrl}/chart/themechart.html?Keyword={keyword}&KeywordIdx={keywordIdx}` | CefSharp navigation | HTML/JS chart rendering | ChartUrlVersion이 v2가 아닐 때 사용 |
| 파일 저장 | `FilePathFinance\yyyyMMddHHmmssfff_theme.png` | PNG file write | 테마차트 이미지 | 저장 실패 시 `FAIL` 응답 가능 |
| Windows 인증 | 코드 내 `FileUser`/비밀번호 literal 사용 | `WrapperImpersonationContext` | 파일 저장 권한 | 설정값이 아닌 하드코딩 값에 의존 |

### 5.3 확인된 설계/운영상 특징

- `TcpListenerPort` 설정값은 존재하지만 `TcpListenerChart`는 설정을 읽지 않고 port 8280을 하드코딩한다 (`App.config:17`, `TcpListenerChart.cs:85`).
- 현재 `ChartUrlVersion=v2`이므로 실제 사용 URL은 `lwthemechart_1250_400.html?keywordIdx=...` 쪽이다 (`App.config:33`, `TcpListenerChart.cs:151-152`).
- `ThemeChart` 외 명령은 별도 오류 없이 `OK!!|`와 빈 결과를 반환할 수 있다. `result`가 기본값인 상태로 응답 생성이 가능하기 때문이다 (`TcpListenerChart.cs:119-129`).
- 저장 시 `App.config`의 `FileUser`를 쓰지 않고 코드에 사용자/비밀번호 문자열이 직접 들어가 있다 (`TcpListenerChart.cs:204`).

### 5.4 리스크 평가

| 리스크 | 심각도 | 근거 | 설명 |
|---|---:|---|---|
| 입력 검증 부족 | 높음 | `TcpListenerChart.cs:112-125` | `arr[1]`, `arr[2]` 접근 전 길이 검증이 없다. 잘못된 payload는 예외/FAIL로 이어진다. |
| 설정 포트 미사용 | 중간 | `App.config:17`, `TcpListenerChart.cs:85` | 운영자가 config로 포트를 바꿔도 listener는 8280을 사용한다. |
| 응답 성공 기준 약함 | 중간 | `TcpListenerChart.cs:119-129` | 알 수 없는 명령도 `OK!!|` 형태 응답 가능성이 있다. |
| 파일 인증정보 하드코딩 | 높음 | `TcpListenerChart.cs:204` | `App.config`가 아닌 코드 literal에 의존한다. 비밀 관리/교체/감사에 취약하다. |
| 렌더 완료 판정이 고정 delay | 중간 | `TcpListenerChart.cs:156-160` | 차트 JS 렌더 완료 여부를 확인하지 않고 1.5초 후 캡처한다. |

## 6. 옵션 3 — 기타/`Robo` / `TcpListenerRobo` 정밀 분석

### 6.1 실행 흐름

1. `StartUp`이 `Scheduler`도 `Chart`도 아니면 `TcpListenerRobo` Form이 실행된다 (`Program.cs:21-27`).
2. Form Load에서 OffScreen browser를 만들고 TCP Listener를 시작하며, 별도 Task로 `SELECT 1` DB 연결 테스트를 수행한다 (`TcpListenerRobo.cs:48-67`).
3. Listener는 첫 번째 로컬 IP의 port 8279에 bind/listen한다 (`TcpListenerRobo.cs:75-87`).
4. `<EOF>`까지 ASCII로 수신하고 `|` 앞부분만 날짜 문자열로 사용한다 (`TcpListenerRobo.cs:95-107`).
5. 현재 Start 흐름은 `UpdateChartImageV2(receiveData)`를 호출한다 (`TcpListenerRobo.cs:109-112`).
6. V2는 `DBStockPoint`에서 대상 추천/채팅 mapping을 조회한다 (`TcpListenerRobo.cs:154-180`).
7. 각 추천 건별로 BizStock chart captureview URL을 만들고 브라우저로 로드/캡처한다 (`TcpListenerRobo.cs:200-218`).
8. 캡처 파일명을 `USP_FeatureRoboRecommand_Update_Admin`에 반영한다 (`TcpListenerRobo.cs:221-228`).
9. 캡처 이미지들을 multipart form의 `files` 필드에 추가하고, 별도 `Ref` JSON 필드에 날짜/채팅/종목/파일 참조 정보를 담는다 (`TcpListenerRobo.cs:196-247`, `TcpListenerRobo.cs:455-472`).
10. `{ChatApiUrl}/api/v1/chat/0/files:upload-robo`로 POST한다 (`TcpListenerRobo.cs:133-142`, `TcpListenerRobo.cs:249`).
11. 처리 성공 시 `OK!!|{receiveData}`를 TCP로 응답한다 (`TcpListenerRobo.cs:111-114`).

### 6.2 외부 API/연동 상세

| 연동 | 주소/대상 | 방식 | 데이터 | 실패 영향 |
|---|---|---|---|---|
| TCP 요청 | `{hostFirstAddress}:8279` | raw socket | `{yyyy-MM-dd}|...<EOF>` 형태로 추정. `|` 앞만 사용 | 처리 실패 시 `FAIL` 응답 |
| SQL Server | `DBStockPoint` | `FinUp.Core.Data.Query` + `SqlConnection` | 추천/채팅 mapping 조회, 추천 이미지 파일명 update | DB 장애 시 전체 처리 실패 |
| 차트 페이지 | `{ChartUrl}?CODE={StockCode}&INTERVAL=D&COUNT=120&height=300&date={RegDT}` | CefSharp navigation | HTML/JS chart rendering | 캡처 실패/잘못된 이미지 생성 |
| 파일 저장 | `FilePath\Contents\{CIdx}\{timestamp}_{CIdx}_{StockCode}.png` | PNG file write | 로보 추천 차트 이미지 | 저장 실패 시 처리 실패 |
| Chat API upload | `{ChatApiUrl}/api/v1/chat/0/files:upload-robo` | `HttpClient.PostAsync` multipart | `files` + `Ref` JSON, `x-api-key` header | API 실패가 응답 상태 검사 없이 지나갈 수 있음 |
| Legacy cacheload | `{CacheloadUrl}?chatidx={chat}` | HTTP GET | 채팅 캐시 갱신 | 현재 V2 흐름에서는 호출되지 않음 |

### 6.3 V2와 legacy 흐름 차이

| 항목 | V2 `UpdateChartImageV2` | Legacy `UpdateChartImage` |
|---|---|---|
| 현재 TCP Start에서 호출 여부 | 호출됨 (`TcpListenerRobo.cs:111`) | 호출되지 않음 |
| DB 조회 | 추천/콘텐츠/FeatureChat + `ExternalChatChatIdx` 조회 | 추천/콘텐츠/FeatureChat 조회 후 ChatMessage도 조회 |
| 이미지 저장 | 수행 | 수행 |
| 추천 테이블 업데이트 | `USP_FeatureRoboRecommand_Update_Admin` 호출 | 동일 |
| 채팅 메시지 직접 수정 | 하지 않음 | `USP_FeatureChatMessage_Update`로 JSON Message 수정 |
| 캐시 갱신 API | 호출하지 않음 | `CacheloadUrl?chatidx=...` 호출 |
| Chat API | multipart upload API 호출 | 호출하지 않음 |

### 6.4 중요 코드 근거

- DB 연결은 `query.ConnectionString = "DBStockPoint"`로 지정되고, `FinUp.Core.Data.Extension.SetConnectionString()`이 appSettings 값을 `DecAES()`로 복호화한다 (`TcpListenerRobo.cs:154-157`, `FinUp.Core.Data/Extension.cs:77-83`).
- 실제 SQL 연결은 `new SqlConnection(strConnectionString); sqlConnection.Open();`으로 수행된다 (`FinUp.Core.Data/Sql.cs:35-38`).
- V2 조회 SQL은 입력 날짜 문자열을 직접 SQL 문자열에 보간한다 (`TcpListenerRobo.cs:154-180`).
- 차트 캡처 URL은 종목코드/일자 기반으로 생성된다 (`TcpListenerRobo.cs:202-203`).
- 이미지 저장 후 추천 테이블 update 프로시저를 실행한다 (`TcpListenerRobo.cs:221-226`).
- Chat API upload는 `x-api-key` header를 붙이고 `ChatApiUrl` 하위 endpoint로 POST한다 (`TcpListenerRobo.cs:133-142`).
- `HttpResponseMessage response = await UploadFileAsync(form);` 이후 `response.IsSuccessStatusCode` 확인 또는 응답 본문 기록은 없다 (`TcpListenerRobo.cs:249-250`).

### 6.5 리스크 평가

| 리스크 | 심각도 | 근거 | 설명 |
|---|---:|---|---|
| 외부 연동 표면이 가장 넓음 | 높음 | `TcpListenerRobo.cs:154-249` | TCP, DB, 차트 웹, 파일 저장, Chat API가 한 요청에 직렬로 묶인다. 한 곳 장애가 전체 실패로 이어질 수 있다. |
| SQL 문자열 직접 보간 | 높음 | `TcpListenerRobo.cs:157-177`, `TcpListenerRobo.cs:263-282` | TCP 수신 문자열이 날짜로 기대되지만 parameterization이 없다. |
| SQL `WHERE` 조건 우선순위 위험 | 높음 | `TcpListenerRobo.cs:173-177` | `A.RegDT between ... OR A.SecondBuyDate = ... AND A.DelDT IS NULL` 형태라 SQL의 `AND` 우선순위 때문에 `DelDT IS NULL`이 두 조건 전체에 적용되지 않을 수 있다. |
| Chat API 실패를 성공으로 오판 가능 | 높음 | `TcpListenerRobo.cs:249-250`, `TcpListenerRobo.cs:111-114` | POST 응답 상태를 확인하지 않고 TCP 성공 응답을 보낼 수 있다. |
| 운영 endpoint 혼선 | 중간 | `App.config:25-27` | `pre-chatapi`는 주석이고 현재 `ChatApiUrl`은 localhost다. 운영 배포 시 설정 확인이 필수다. |
| 설정 포트 미사용 | 중간 | `App.config:17`, `TcpListenerRobo.cs:78` | config의 `TcpListenerPort=8280`과 무관하게 Robo는 8279를 사용한다. |
| 렌더 완료 판정이 고정 delay | 중간 | `TcpListenerRobo.cs:207-212` | 페이지/네트워크 지연 시 불완전 캡처 가능성이 있다. |
| 민감정보 저장 방식 | 높음 | `App.config:15-24`, `TcpListenerRobo.cs:137` | API key/파일 계정/DB 암호문이 config에 존재한다. DB는 암호문이지만 Chat API key와 파일 계정 정보는 별도 보호 여부가 코드에서 확인되지 않는다. |

## 7. 수동/테스트 Form 보충 분석

`ManualCapture`와 `CaptureTest`는 코드에 포함되어 있으나 `Program.Main`의 3개 실행 옵션에는 연결되어 있지 않다.

- `ManualCapture.Start()`는 port 8278 TCP listener를 구현하지만 `TcpListener_Load`에서 호출 코드가 주석 처리되어 있다 (`ManualCapture.cs:71-83`, `ManualCapture.cs:86-177`).
- `ManualCapture`에는 legacy 로보와 유사한 DB update 및 cacheload 흐름이 버튼 이벤트로 존재한다 (`ManualCapture.cs:309-423`).
- `CaptureTest`는 hard-coded BizStock URL로 WebBrowser/CefSharp 캡처를 시험하는 Form이다 (`CaptureTest.cs:42-70`, `CaptureTest.cs:75-156`).

따라서 운영 분석에서는 보조/테스트 코드로 보되, 보안/정리 관점에서는 같은 민감 설정과 DB/API 호출 패턴을 재검토할 필요가 있다.

## 8. 외부 연동 중요도 순위

| 순위 | 연동 | 해당 옵션 | 중요 이유 | 관측 포인트 |
|---:|---|---|---|---|
| 1 | `DBStockPoint` SQL | Robo | 조회 결과가 캡처 대상과 DB 업데이트를 모두 결정 | connection decrypt 성공, 조회 row 수, 프로시저 실행 결과 |
| 2 | Chat API upload | Robo V2 | 채팅/외부 시스템에 이미지 참조를 넘기는 핵심 후처리 | HTTP status, response body, API key 유효성, endpoint 환경 |
| 3 | StockData/BizStock 차트 HTML | 전체 | 모든 옵션의 이미지 품질과 성공 여부가 브라우저 렌더링에 의존 | load 성공, JS 렌더 완료, screenshot 크기/내용 |
| 4 | 시장 일정 API | Scheduler | 배치 실행 시각 결정 | `/api/market/{from}/{to}` 응답, 휴장일/장종료시각 데이터 |
| 5 | 파일 저장/impersonation | 전체 | 캡처 이미지 산출물 저장의 마지막 단계 | 경로 존재/권한/계정 만료/네트워크 공유 여부 |
| 6 | TCP listener | Chart/Robo | 외부 호출자가 이 앱을 제어하는 인입 경로 | 방화벽, bind IP, payload format, EOF 처리 |

## 9. 옵션별 운영 점검 체크리스트

### `Scheduler`

- [ ] `StockDataUrl`이 실제 환경의 StockData API/차트 host를 가리키는지 확인
- [ ] `/api/market/{from}/{to}` 응답에 오늘/다음 영업일과 `EndTime`이 포함되는지 확인
- [ ] `FilePathStockData\Chart` 저장 권한과 `FileUser` 인증 성공 여부 확인
- [ ] 장 종료 +10/+40분 중복 스케줄, 재등록, Stop 버튼 동작 확인
- [ ] 캡처 파일 크기/이미지 내용이 실제 chart 렌더 완료 후 생성되는지 확인

### `Chart`

- [ ] 호출자가 port 8280으로 `ThemeChart|keyword|keywordIdx<EOF>` 형식 요청을 보내는지 확인
- [ ] `ChartUrlVersion=v2`일 때 `keyword`는 URL에 반영되지 않고 `keywordIdx`만 사용되는 것이 의도인지 확인
- [ ] `FilePathFinance` 저장 경로와 파일 인증정보가 운영 계정과 일치하는지 확인
- [ ] 알 수 없는 명령/파라미터 부족 시 성공 응답이 나가지 않도록 관측
- [ ] `StockDataUrl/chart/lwthemechart_1250_400.html` 렌더링 지연이 1.5초 안에 안정적으로 끝나는지 확인

### `Robo`

- [ ] 호출자가 port 8279로 날짜 문자열과 `<EOF>`를 보내는지 확인
- [ ] 날짜 입력 검증 및 SQL parameterization 여부 검토
- [ ] `DBStockPoint` 복호화/접속/조회 row 수/프로시저 실행 결과 확인
- [ ] 현재 `ChatApiUrl`이 localhost인 점이 배포 환경 의도와 맞는지 확인
- [ ] upload-robo API의 HTTP status와 응답 본문을 기록/검증하도록 운영 로그 확인
- [ ] V2에서 cacheload 또는 ChatMessage 직접 update가 제거된 것이 의도인지 확인

## 10. 전체 판단

### 근거 기반 판단

1. `Chart` 옵션은 현재 기본 실행 모드이며, “테마 차트 이미지 생성 서버”에 집중된 비교적 단순한 외부 연동 구조다. 핵심 의존성은 TCP 8280, StockData chart HTML, 파일 저장 권한이다.
2. `Scheduler` 옵션은 배치성 캡처이며, 시장 일정 API가 시작점이다. DB/Chat API와 직접 결합되어 있지 않아 연동 표면은 중간 수준이지만, 일정 API 실패 시 작업이 시작되지 않는다.
3. `Robo` 옵션은 DB 조회/업데이트와 Chat API upload까지 수행하므로 외부 시스템 결합도가 가장 높다. 장애 영향, 보안 영향, 입력 검증 리스크도 세 옵션 중 가장 크다.

### 확신도

- 실행 옵션 식별: 높음 — `Program.cs`와 `App.config`에 직접 근거가 있다.
- 외부 HTTP/DB/TCP 연동 목록: 높음 — `rg` 검색과 주요 파일 라인 확인으로 직접 근거가 있다.
- 실제 운영 환경 endpoint: 중간 — config에는 localhost/pre/prod 후보가 혼재하고, 배포 시 config transform 또는 수동 변경 여부는 저장소만으로 확인되지 않는다.
- 실제 API 응답 schema/상태 코드 의미: 낮음 — 외부 API 서버 구현과 운영 로그는 이 저장소에 포함되어 있지 않다.

## 11. 근거 파일 색인

- `Program.cs:21-27` — 3가지 실행 옵션 분기
- `App.config:7-33` — 주요 URL, 파일 경로, DB/API/StartUp 설정
- `FinUp.StockData.ChartCapture.App.csproj:8-11`, `187-221` — 프로젝트 유형/프레임워크/참조
- `Scheduler.cs:31-167` — Scheduler 초기화, 시장일정 API 기반 예약
- `Job/Deposit.cs:34-67` — 신용잔고/예탁금 차트 캡처
- `Job/Themelog.cs:34-85` — 테마록 차트 캡처/crop 저장
- `Job/Common.cs:14-36` — 공통 screenshot 저장 및 impersonation
- `TcpListenerChart.cs:77-185` — Chart TCP listener 및 테마 차트 캡처
- `TcpListenerRobo.cs:48-145` — Robo 초기화/TCP listener/Chat API upload wrapper
- `TcpListenerRobo.cs:147-250` — Robo V2 DB 조회, 캡처, DB update, multipart upload
- `TcpListenerRobo.cs:253-388` — Robo legacy DB/ChatMessage/cacheload 흐름
- `WrapperImpersonationContext.cs:38-66` — Windows impersonation 구현
- `/mnt/c/Dev/FinUp.StockData.Fundamentals/Util.cs:29-61`, `125-141` — 시장 일정 API 호출 경로
- `/mnt/c/Dev/FinUp.Core.Fundamentals/Web/Util.cs:58-92` — GET WebRequest 구현
- `/mnt/c/Dev/FinUp.Core.Data/Extension.cs:77-83` — appSettings DB 연결 문자열 복호화
- `/mnt/c/Dev/FinUp.Core.Data/Sql.cs:35-60`, `128-147`, `217-236` — SQL 연결/실행 구현

## 12. 완료 감사 체크리스트

| 요구사항 | 산출/증거 |
|---|---|
| `FinUp.StockData.ChartCapture.App` 분석 | 본 보고서 전체. 대상 경로와 csproj/config/source 파일 확인 |
| 3가지 옵션 각각 정밀 분석 | 4장 Scheduler, 5장 Chart, 6장 Robo |
| 외부 API/외부 연동 중요 분석 | 3장 전체 연동 표, 8장 중요도 순위, 각 옵션의 외부 연동 표 |
| `/mnt/c/reports/FinUp.StockData.ChartCapture.App` 경로 생성 | 보고서 저장 경로로 사용 |
| Markdown 생성 | `FinUp.StockData.ChartCapture.App.analysis.md` |
| HTML 생성 | `FinUp.StockData.ChartCapture.App.analysis.html` |
| 민감정보 보호 | config에 존재하는 키/계정/암호문은 직접 값 대신 위치와 역할만 설명 |
