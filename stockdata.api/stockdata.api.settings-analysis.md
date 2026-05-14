# StockData API 설정키 사용 분석 보고서

- 작성일: 2026-05-13
- 분석 루트: `/mnt/c/Dev`
- 산출 경로: `/mnt/c/reports/stockdata.api`
- 산출물: `stockdata.api.settings-analysis.md`, `stockdata.api.settings-analysis.html`
- 분석 대상: 요청된 7개 프로젝트/실행 변형과 지정 설정키
- 민감정보 처리: 원본 config 주변에는 DB 암호문, API key, 계정/비밀번호가 존재하지만 본 보고서는 지정 설정키의 URL 값과 코드 사용처 중심으로만 기록한다.

## 1. 전체 결론

> Full HD 1920px 기준으로 외부 좌우 여백을 각 `48px`로 두어 HTML body 총폭을 `1824px`로 잡고, 내부 padding을 각 `48px`로 두어 실제 content 폭을 `1728px`로 계산했다. 1번 결론 테이블은 `No 56px + 프로젝트/키 390px + 상세 요청 URL 620px + 사용/목적 650px = 1716px`로 맞춰 content 폭 1728px 안에서 줄바꿈되도록 조정했다.

| No | 프로젝트 / 설정키 | 상세 요청 URL(`/api` 뒤 포함) | 현재 사용 / 목적 |
|---:|---|---|---|
| 1 | `FinUp.Radar.App.AlphaBot`<br>`appSettings:ApiStockPriceAddress` | `https://stockdata.finup.co.kr/api/price/diff`<br>`https://stockdata.finup.co.kr/api/market/{from}/{to}` | 사용 중. 종목 가격 diff 조회와 장 시작 지연 계산용 |
| 2 | `FinUp.Stock.App.AlphaBot`<br>`appSettings:StockDataApi` | `https://stockdata.finup.co.kr/api/price/highlowlist` | 사용 중. 채팅/시그널 고가·저가 판정용 |
| 3 | `FinUp.StockData.Price.App`<br>`appSettings:WebAPIAddress` | `https://stockdata.finup.co.kr/api/market/{from}/{to}` | 사용 중. 장 일정 조회용. 소스는 `StartUp=KR`, 일반 배포 후보는 `StartUp=S` |
| 4 | `FinUp.StockData.RoboAnalysis.App`<br>`appSettings:WebAPIAddress` | `https://stockdata.finup.co.kr/api/market/{from}/{to}` | 사용 중. 로보 분석/발송 스케줄 산정용 |
| 5 | `FinUp.StockData.RoboAnalysis.App`<br>`appSettings:ChartAPIAddress` | 소스: `http://pre-stockdata.finup.co.kr/api/chart/capture?date={yyyy-MM-dd}`<br>배포 후보: `http://stockdata.finup.co.kr/api/chart/capture?date={yyyy-MM-dd}` | 사용 중. 로보 분석 이후 차트 캡처 API 트리거 |
| 6 | `KiwoomReal_FinUp.StockData.Price.App`<br>`appSettings:WebAPIAddress` | `https://stockdata.finup.co.kr/api/market/{from}/{to}` | 사용 중. `KiwoomReal_...exe.config`의 `StartUp=KR` 변형에서 Kiwoom Real 일정 조회 |
| 7 | `FinUp.Analysis.Theme.App`<br>`ThemeConfig:StockDataApiUrl` | `https://stockdata.finup.co.kr/api/index/last?codes=001,101` | 사용 중. 마감 지수 메시지용 코스피/코스닥 최종 지수 조회 |
| 8 | `FinUp.StockData.ChartCapture.App`<br>`appSettings:StockDataUrl` | Scheduler: `https://stockdata.finup.co.kr/api/market/{from}/{to}`<br>Chart/Scheduler chart HTML: `/chart/lwthemechart_1250_400.html?keywordIdx={keywordIdx}`, `/chart/trchart.html`, `/chart/custchart.html`, `/chart/themelogchart.html` | 사용 중. 소스 `StartUp=Chart`, scheduler 배포 config는 `StartUp=Scheduler`; 일반 배포 config에는 `StockDataUrl` 없음 |

요청에 `FinUp.Analysis.Theme.App`의 `ThemeConfig:StockDataApiUrl`이 두 번 기재되어 있어 동일 키로 한 번 분석했다.

### 1.1 `/mnt/c/App/Config` 배포 후보 config 대조

소스 config 외에 `/mnt/c/App/Config`에 동일 서비스명의 실행 config 후보가 존재해 함께 확인했다. 중요한 차이는 다음과 같다.

| 항목 | 소스 config | `/mnt/c/App/Config` 배포 후보 | 의미 |
|---|---|---|---|
| `FinUp.StockData.Price.App` | `StartUp=KR` | `FinUp.StockData.Price.App.exe.config`는 `StartUp=S` | 일반 배포명은 Xing TR 스케줄러일 수 있음 |
| `KiwoomReal_FinUp.StockData.Price.App` | 별도 소스 폴더 없음 | `KiwoomReal_FinUp.StockData.Price.App.exe.config` 존재, `StartUp=KR` | Kiwoom Real은 별도 배포 config 변형으로 확인됨 |
| `FinUp.StockData.RoboAnalysis.App:ChartAPIAddress` | `http://pre-stockdata.finup.co.kr/api/chart/capture` | `http://stockdata.finup.co.kr/api/chart/capture` | 소스와 배포 후보의 호출 환경이 다름 |
| `FinUp.StockData.RoboAnalysis.App:IsManual` | `Y` | `N` | 수동/자동 스케줄 지연 동작이 다름 |
| `FinUp.StockData.ChartCapture.App` | 소스 `App.config`에 `StockDataUrl`, `StartUp=Chart` | 일반 config에는 `StockDataUrl` 없음. scheduler config에는 `StockDataUrl`, `StartUp=Scheduler` | ChartCapture는 실행 config 파일 종류를 반드시 구분해야 함 |


## 2. 공통 패턴 및 같이 봐야 할 부분

### 2.1 `/api` 포함 여부가 프로젝트마다 다름

| 키 | 값 형태 | 호출 조립 방식 | 주의점 |
|---|---|---|---|
| `ApiStockPriceAddress`, `StockDataApi`, `WebAPIAddress` | `https://stockdata.finup.co.kr/api`처럼 `/api` 포함 | 코드가 `/price/...`, `/market/...` 등을 바로 붙임 | 값에서 `/api`를 제거하면 호출이 깨질 수 있음 |
| `ThemeConfig:StockDataApiUrl`, `StockDataUrl` | `https://stockdata.finup.co.kr`처럼 `/api` 미포함 | 코드가 `/api/...` 또는 `/chart/...`를 목적별로 붙임 | 값에 `/api`를 넣으면 `/api/api/...` 또는 차트 URL 오류 가능 |
| `ChartAPIAddress` | 완성 endpoint `http://pre-stockdata.finup.co.kr/api/chart/capture` | 코드가 `?date=yyyy-MM-dd`만 붙임 | base URL이 아니라 API endpoint 자체임 |

### 2.2 상세 요청 URL 목록

| 프로젝트/키 | 코드에서 확인한 상세 요청 URL | HTTP/호출 방식 | 근거 |
|---|---|---|---|
| `FinUp.Radar.App.AlphaBot:ApiStockPriceAddress` | `/price/diff` | POST성 호출: `SendPostApiStock(apiUrl, data)` | `BaseProcessUnit.cs:395-400` |
| `FinUp.Radar.App.AlphaBot:ApiStockPriceAddress` | `/market/{from}/{to}` | GET: `DelayMarketStartTime()` → `GetMarketToday()` → `GetMarketInfo()` | `ThemeLogAlarm.cs:43`, `FinUp.StockData.Fundamentals/Util.cs:327-379`, `Util.cs:49-59` |
| `FinUp.Radar.App.AlphaBot` 관련 하드코딩 | `https://stockdata.finup.co.kr/api/price/diff` | POST성 호출. 지정 키를 쓰지 않는 중복 경로 | `StockPrice.cs:407-424` |
| `FinUp.Stock.App.AlphaBot:StockDataApi` | `/price/highlowlist` | POST JSON, `requiredRequestCompress: true` | `ProcessUnit.cs:3232-3238` |
| `FinUp.StockData.Price.App:WebAPIAddress` | `/market/{from}/{to}` | GET. `GetScheduleNextMarket()`는 기본 `{today}`~`{today+10}`, `GetScheduleMarket()` 일부는 `{today-10}`부터 조회 | `SchedulerKiwoomReal.cs:128`, `SchedulerXingTR.cs:71`, `FinUp.StockData.Fundamentals/Util.cs:49-59`, `Util.cs:91-141` |
| `KiwoomReal_FinUp.StockData.Price.App:WebAPIAddress` | `/market/{from}/{to}` | GET. Kiwoom Real 배포 config `StartUp=KR` → `SchedulerKiwoomReal` | `/mnt/c/App/Config/KiwoomReal_FinUp.StockData.Price.App.exe.config:30-32`, `SchedulerKiwoomReal.cs:128` |
| `FinUp.StockData.RoboAnalysis.App:WebAPIAddress` | `/market/{from}/{to}` | GET. `Scheduler`, `SchedulerExpression`, realtime scheduler 계열의 장 일정 조회 | `Scheduler.cs:85`, `SchedulerExpression.cs:84`, `RealtimeScheduler.cs:83`, `FinUp.StockData.Fundamentals/Util.cs:49-59` |
| `FinUp.StockData.RoboAnalysis.App:ChartAPIAddress` | `/chart/capture?date={yyyy-MM-dd}` | GET: `WebRequestAsync(chartCaptureUrl)` | `Scheduler.cs:466-472`; 소스 config `App.config:55`, 배포 config `/mnt/c/App/Config/FinUp.StockData.RoboAnalysis.App.exe.config:46` |
| `FinUp.Analysis.Theme.App:ThemeConfig:StockDataApiUrl` | `/api/index/last?codes=001,101` (`/api` 뒤 상세 path는 `/index/last?codes=001,101`) | GET: `FinUp.Core.NET.Web.Util.WebRequestAsync(url)` | `ThemeChatMessageRepository.cs:149-152` |
| `FinUp.StockData.ChartCapture.App:StockDataUrl` | `/api/market/{from}/{to}` | GET. Scheduler 모드의 장 일정 조회 | `Scheduler.cs:66`, `FinUp.StockData.Fundamentals/Util.cs:49-59` |
| `FinUp.StockData.ChartCapture.App:StockDataUrl` | `/chart/lwthemechart_1250_400.html?keywordIdx={keywordIdx}` 또는 `/chart/themechart.html?Keyword={keyword}&KeywordIdx={keywordIdx}` | CefSharp browser navigation. 현재 소스 `ChartUrlVersion=v2`이면 lwthemechart 사용 | `TcpListenerChart.cs:147-158` |
| `FinUp.StockData.ChartCapture.App:StockDataUrl` | `/chart/trchart.html`, `/chart/custchart.html`, `/chart/themelogchart.html` | CefSharp browser navigation. Scheduler 모드 배치 캡처 | `Job/Deposit.cs:37-55`, `Job/Themelog.cs:36` |

### 2.3 같은 StockData 시장 일정 API 의존성

`FinUp.StockData.Price.App`, `FinUp.StockData.RoboAnalysis.App`, `FinUp.StockData.ChartCapture.App`는 모두 장 시작/종료 일정 계산에 StockData API를 사용한다. 내부 공통 경로는 `FinUp.StockData.Fundamentals.Util.GetMarketInfo()`이며 URL은 `{base}/market/{from}/{to}`로 조립된다.

- Price/RoboAnalysis의 `WebAPIAddress=https://stockdata.finup.co.kr/api`는 결과적으로 `https://stockdata.finup.co.kr/api/market/{from}/{to}`가 된다.
- ChartCapture의 `StockDataUrl=https://stockdata.finup.co.kr`는 코드에서 `/api`를 붙여 같은 API host로 만든다.

### 2.4 운영/프리 환경 혼재

- 대부분의 StockData API 키는 운영 도메인 `https://stockdata.finup.co.kr`을 가리킨다.
- 소스 기준 `FinUp.StockData.RoboAnalysis.App`의 `ChartAPIAddress`는 `http://pre-stockdata.finup.co.kr/api/chart/capture`로 pre 환경이며 HTTP다.
- 배포 후보 `/mnt/c/App/Config/FinUp.StockData.RoboAnalysis.App.exe.config`에서는 `ChartAPIAddress=http://stockdata.finup.co.kr/api/chart/capture`, `IsManual=N`으로 소스와 다르다.
- ChartCapture도 소스 `App.config`는 `StartUp=Chart`이나, 배포 후보는 일반 config와 scheduler config가 분리되어 있다. `/mnt/c/App/Config/FinUp.StockData.ChartCapture.App.exe.config`에는 `StockDataUrl`이 없고, `/mnt/c/App/Config/scheduler_FinUp.StockData.ChartCapture.App.exe.config`에만 `StockDataUrl`과 `StartUp=Scheduler`가 있다.

### 2.5 `KiwoomReal_FinUp.StockData.Price.App` 해석

소스 루트 `/mnt/c/Dev`에서는 `KiwoomReal_FinUp.StockData.Price.App`라는 독립 프로젝트 폴더가 확인되지 않았다. 그러나 `/mnt/c/App/Config/KiwoomReal_FinUp.StockData.Price.App.exe.config` 배포 후보 파일이 존재하며, 그 안의 `StartUp=KR`이 소스 `Program.cs`에서 `SchedulerKiwoomReal`을 실행한다. 따라서 요청된 항목은 `FinUp.StockData.Price.App` 코드베이스를 Kiwoom Real 전용 config로 실행하는 배포 변형으로 보는 것이 가장 타당하다.

## 3. 프로젝트별 상세 분석

## 3.1 `FinUp.Radar.App.AlphaBot` — `appSettings:ApiStockPriceAddress`

### 정의

- `App.config:53` — `ApiStockPriceAddress=https://stockdata.finup.co.kr/api`
- `Config/AppSetting.cs:16` — `ConfigurationManager.AppSettings["ApiStockPriceAddress"]`를 정적 필드 `AppSetting.ApiStockPriceAddress`로 로드한다.

### 사용 목적

1. 종목 가격 diff 조회
   - `Operation/ProcessUnit/BaseProcessUnit.cs:383-400`에서 `GetStockPrice()`가 종목코드 목록을 JSON으로 만들고, URL을 `$"{AppSetting.ApiStockPriceAddress}/price/diff "`로 조립한 뒤 `SendPostApiStock(apiUrl, data)`를 호출한다.
   - 목적은 응답 JSON을 `ApiStockPrice` 목록으로 역직렬화해 현재가/거래시간/거래량 등 가격 정보를 얻는 것이다 (`BaseProcessUnit.cs:402-410`).

2. 테마로그 알림 지연 시간 계산
   - `Operation/ProcessUnit/ThemeLogAlarm.cs:43`에서 `DelayMarketStartTime(AppSetting.ApiStockPriceAddress, delayMin)`를 호출한다.
   - 목적은 장 시작 기준 N분 뒤 알림을 보내기 위한 delay 계산이다.

3. 과거/비활성 사용 흔적
   - `Operation/ProcessUnit/ThemeLogSendMessage.cs:29-31`에 `IsOverMarketStartTime(AppSetting.ApiStockPriceAddress, 5)` 호출이 주석 처리되어 있다. 현재 실행 코드로 보지는 않는다.

### 현재 사용하는가?

사용 중이다. 설정값은 정적 AppSetting에 로드되고, 활성 코드 경로인 `GetStockPrice()`와 `ThemeLogAlarm.Run()`에서 참조된다. 단, `ThemeLogSendMessage`의 장시작 체크는 주석 처리되어 현재 사용이 아니다.

### 연관해서 봐야 할 부분

- `BaseProcessUnit.GetStockPrice()`의 URL 문자열에 `/price/diff ` 뒤 공백이 포함되어 있다 (`BaseProcessUnit.cs:395`). HTTP client가 trim하지 않으면 endpoint mismatch 가능성이 있다.
- 같은 config에는 Redis, Mongo, Radar healthcheck, Telegram 등 외부 연동 키가 많다. StockData API 장애가 레이더 알림/가격 정보 처리와 함께 장애로 보일 수 있으므로 API 로그와 레이더 healthcheck를 함께 봐야 한다.
- `DelayMarketStartTime`은 StockData 시장 일정 API에 의존하므로, 가격 API(`/price/diff`)와 시장 일정 API(`/market/...`)가 같은 host/base URL 아래 동시에 정상인지 확인해야 한다.

## 3.2 `FinUp.Stock.App.AlphaBot` — `appSettings:StockDataApi`

### 정의

- `App.config:52` — `StockDataApi=https://stockdata.finup.co.kr/api`
- `Operation/ProcessBase.cs:84` — `ConfigurationManager.AppSettings["StockDataApi"]`를 인스턴스 필드 `StockDataApi`로 로드한다.

### 사용 목적

- `Operation/ProcessUnit.cs:3220-3238`에서 채팅/시그널 대상 목록을 `HighLowListParam`으로 만들고, URL을 `$"{StockDataApi}/price/highlowlist"`로 조립한다.
- `NetUtil.WebRequestPostJsonAsync(apiUrl, data, requiredRequestCompress: true)`로 POST하고, 응답을 `IList<HighLowPrice>`로 역직렬화한다.
- 이후 응답 high/low 값으로 `checkSignalPrice()`를 수행해 신호 체결/조건 만족 여부를 판단한다 (`ProcessUnit.cs:3240-3255`).

### 현재 사용하는가?

사용 중이다. `ProcessBase`의 protected field로 로드되고, `ProcessUnit`의 활성 코드에서 `/price/highlowlist` 호출에 사용된다.

### 연관해서 봐야 할 부분

- 요청 압축 옵션 `requiredRequestCompress: true`가 켜져 있다 (`ProcessUnit.cs:3237`). StockData API 쪽에서 압축 요청을 계속 지원하는지 확인해야 한다.
- 같은 class는 `ChatApiUrl`, `ChatCacheLoadUrl`, `StockPointApi` 등 채팅/StockPoint API와 함께 동작한다 (`ProcessBase.cs:84-89`). 가격 API 결과가 채팅 메시지/신호 처리로 이어지는 구조이므로, StockData API만 단독으로 보지 말고 채팅 갱신 흐름과 같이 봐야 한다.
- 현재 config에는 다수의 외부 credential/API key가 같은 파일에 있다. 키 교체 또는 환경 분리 시 `StockDataApi`만 바꾸는 배포가 아닌 전체 config 검증이 필요하다.

## 3.3 `FinUp.StockData.Price.App` — `appSettings:WebAPIAddress`

### 정의

- `App.config:30` — `WebAPIAddress=https://stockdata.finup.co.kr/api`
- `App.config:32` — 소스 기준 `StartUp=KR`
- `/mnt/c/App/Config/FinUp.StockData.Price.App.exe.config:25`, `38` — 배포 후보 일반 config는 `WebAPIAddress` 동일, `StartUp=S`
- `/mnt/c/App/Config/KiwoomReal_FinUp.StockData.Price.App.exe.config:30`, `32` — KiwoomReal 배포 config는 `WebAPIAddress` 동일, `StartUp=KR`
- `Program.cs:20-34` — `StartUp` 값에 따라 실행 Form이 결정되며, `KR`은 `SchedulerKiwoomReal`, `S`는 `SchedulerXingTR`을 실행한다.

### 사용 목적

`WebAPIAddress`는 대부분 가격 수집/스케줄러에서 시장 일정 API base URL로 사용된다.

주요 사용처:

- `SchedulerKiwoomReal.cs:128` — 현재 설정(`StartUp=KR`)에서 직접 실행되는 `SchedulerKiwoomReal`이 `GetScheduleNextMarket(_startDelay, WebAPIAddress)`를 호출한다.
- `SchedulerKiwoomTR.cs:100` — Kiwoom TR 스케줄에서 `GetScheduleMarket(0, WebAPIAddress)` 호출.
- `SchedulerXingReal.cs:98`, `SchedulerXingTR.cs:71`, `SchedulerXingTR.cs:137` — Xing 실시간/TR 스케줄에서 사용.
- `Wisefn/CompanyCrawling.cs:188`, `Wisefn/FinancialCrawling.cs:429`, `Wisefn/FinancialCrawling_v2.cs:592` — 기업/재무 크롤링 스케줄에서도 사용.
- `Mig/eBestRemove.cs:89`, `SchedulerHogaTraderMove.cs:54` 등 마이그레이션/이관성 작업에서도 사용.

### 현재 사용하는가?

사용 중이다. 소스 `App.config` 기준으로는 `StartUp=KR`이 `SchedulerKiwoomReal`을 선택하고, 이 클래스의 `InitSchedule()`이 `WebAPIAddress`를 읽어 장 일정 API를 호출한다. 다만 `/mnt/c/App/Config/FinUp.StockData.Price.App.exe.config` 배포 후보는 `StartUp=S`이므로 일반 서비스명으로 실행되는 배포본은 `SchedulerXingTR` 경로일 수 있다. Kiwoom Real 전용 배포 config는 별도 `/mnt/c/App/Config/KiwoomReal_FinUp.StockData.Price.App.exe.config`에서 확인된다.

### 연관해서 봐야 할 부분

- 이 프로젝트는 하나의 `WebAPIAddress`를 여러 실행 모드가 공유한다. 현재 실행은 `KR`이지만 config 또는 배포 파일이 바뀌면 `S`, `KT`, `X`, `CC` 등 다른 Form에서도 같은 키를 사용한다.
- `StockDataHandle.exe_real.config`와 `/mnt/c/App/Config/FinUp.StockData.Price.App.exe.config`에도 `WebAPIAddress=https://stockdata.finup.co.kr/api`와 `StartUp=S`가 있다. 운영 배포가 이 파일을 사용한다면 현재 소스 `App.config`와 실제 실행 모드가 다를 수 있다.
- `App.config:41-42`의 `MarketType=ALL`, `FIDType=PRICE`가 `SchedulerKiwoomReal` 생성자에서 실행 범위를 결정한다 (`SchedulerKiwoomReal.cs:43-76`). WebAPIAddress는 단순 URL이지만 실제 구독 범위/로그 OIdx는 이 설정과 같이 봐야 한다.

## 3.4 `KiwoomReal_FinUp.StockData.Price.App` — `appSettings:WebAPIAddress`

### 프로젝트 위치 해석

독립 소스 폴더 `KiwoomReal_FinUp.StockData.Price.App`는 확인되지 않았다. 대신 `/mnt/c/App/Config/KiwoomReal_FinUp.StockData.Price.App.exe.config` 배포 후보 파일이 존재한다. 코드 기준으로는 `FinUp.StockData.Price.App`의 `StartUp=KR` 실행 변형이 Kiwoom Real이다.

근거:

- `FinUp.StockData.Price.App/App.config:32` — 소스 기준 `StartUp=KR`
- `/mnt/c/App/Config/KiwoomReal_FinUp.StockData.Price.App.exe.config:30`, `32`, `41-42` — 배포 후보의 `WebAPIAddress`, `StartUp=KR`, `MarketType=ALL`, `FIDType=PRICE`
- `FinUp.StockData.Price.App/Program.cs:29-30` — `KR`이면 `SchedulerKiwoomReal` 실행
- `FinUp.StockData.Price.App/SchedulerKiwoomReal.cs:16` — Kiwoom Real Form class
- `FinUp.StockData.Price.App/SchedulerKiwoomReal.cs:128` — `WebAPIAddress`를 `GetScheduleNextMarket()`에 전달

### 현재 사용하는가?

사용 중이다. `FinUp.StockData.Price.App`의 현재 설정이 이미 Kiwoom Real 변형(`KR`)이며, `WebAPIAddress`가 장 시작 스케줄 산정에 직접 사용된다.

### 연관해서 봐야 할 부분

- 이 항목은 3.3과 물리 프로젝트/설정키가 동일하므로 중복 관리가 필요하다.
- 배포/문서에서 `KiwoomReal_FinUp.StockData.Price.App`라는 이름을 별도 서비스명으로 쓰고 있다면, 실제 파일은 `FinUp.StockData.Price.App.exe.config` 또는 `StockDataHandle.exe_real.config` 중 무엇인지 확인해야 한다.

## 3.5 `FinUp.StockData.RoboAnalysis.App` — `appSettings:WebAPIAddress`, `appSettings:ChartAPIAddress`

### 정의

- `App.config:52` — 현재 `UIType=JOB`
- `App.config:53` — `WebAPIAddress=https://stockdata.finup.co.kr/api`
- `App.config:55` — 소스 기준 `ChartAPIAddress=http://pre-stockdata.finup.co.kr/api/chart/capture`
- `App.config:59` — 소스 기준 `IsManual=Y`
- `/mnt/c/App/Config/FinUp.StockData.RoboAnalysis.App.exe.config:44`, `46`, `50` — 배포 후보는 `WebAPIAddress` 동일, `ChartAPIAddress=http://stockdata.finup.co.kr/api/chart/capture`, `IsManual=N`

### 실행 모드 근거

- `Program.cs:20-21` — `UIType=JOB`이면 `Scheduler` Form 실행.
- `Program.cs:29-38` — `EXP`, `MR`, `MS` 등 다른 UIType도 존재하며 일부는 `WebAPIAddress`를 사용한다.

### `WebAPIAddress` 사용 목적

`WebAPIAddress`는 로보 분석 작업의 장 일정/다음 개장 시각 계산에 사용된다.

- `Common/Constants.cs:23` — `Constants.WebAPIAddress`로 정적 로드.
- `Scheduler.cs:80-85` — 현재 `JOB` 모드의 `Scheduler.InitSchedule()`에서 `_scheduleTime` 기준 시장 일정을 조회한다.
- `Scheduler.cs:208-213`, `Scheduler.cs:433-439` — 지연 발송 로직에서 다음 장 시작 기준 delay를 계산한다.
- `SchedulerExpression.cs:77-85` — `EXP` 모드에서도 시장 일정 조회에 사용.
- `Analysis/Realtime/RealtimeScheduler.cs:78-84`, `Analysis/Realtime/RealtimeSchedulerMars.cs:103-109` — 실시간 계열 모드에서도 직접 appSettings 값을 사용한다.

### `ChartAPIAddress` 사용 목적

`ChartAPIAddress`는 로보 분석 후 차트 캡처를 외부 API로 트리거하는 완성 endpoint다.

- `Scheduler.cs:27-28` — `_chartAPIAddress`에 `ChartAPIAddress`를 로드한다.
- `Scheduler.cs:108-113` — 시장 종료 기준 chart job delay를 예약한다. 현재 `IsManual=Y`이면 10분 뒤로 설정된다.
- `Scheduler.cs:452-472` — `$"{_chartAPIAddress}?date={DateTime.Today:yyyy-MM-dd}"`로 URL을 만들고 `WebRequestAsync()`로 호출한다.

### 현재 사용하는가?

둘 다 사용 중이다.

- 소스와 배포 후보 모두 `UIType=JOB`이므로 `Scheduler`가 실행된다.
- `Scheduler.InitSchedule()`은 `Constants.WebAPIAddress`를 사용한다.
- 같은 `Scheduler`의 `JobChart()`는 `_chartAPIAddress`를 사용해 chart capture API를 호출한다.
- 단, 소스는 `ChartAPIAddress`가 pre/http이고 `IsManual=Y`, 배포 후보는 운영 host/http이고 `IsManual=N`이라 실제 호출 대상과 지연 시간이 다르다.

### 연관해서 봐야 할 부분

- 소스 기준 `WebAPIAddress`는 운영 `https://stockdata.finup.co.kr/api`인데 `ChartAPIAddress`는 pre 환경 `http://pre-stockdata.finup.co.kr/api/chart/capture`다. 반면 배포 후보는 `ChartAPIAddress=http://stockdata.finup.co.kr/api/chart/capture`다. 어떤 config가 실제 서비스에 적용되는지 반드시 확인해야 한다.
- `ChartAPIAddress`는 base URL이 아니라 완성 API endpoint이므로, trailing path 변경 영향이 크다.
- `IsManual=Y`일 때도 `JobChart()`는 예약된다. 다만 차트 job delay가 장 종료 +40분이 아니라 현재 시각 +10분으로 변경된다 (`Scheduler.cs:108-113`). 수동 실행 시 의도치 않은 pre chart API 호출이 발생할 수 있다.
- 이 프로젝트는 DB, Redis, Kafka, Chat API, 차트 이미지 저장 설정까지 함께 존재한다. 차트 API 장애는 로보 결과 생성/발송 지연과 함께 분석해야 한다.

## 3.6 `FinUp.Analysis.Theme.App` — `ThemeConfig:StockDataApiUrl`

### 정의

- `FinUp.Analysis.Theme.App/appsettings.json:37-48` — `ThemeConfig` 섹션에 `StockDataApiUrl=https://stockdata.finup.co.kr` 정의.
- `Model/ThemeConfig.cs:34` — `ThemeConfig.StockDataApiUrl` property.
- `App.xaml.cs:71` — `services.Configure<ThemeConfig>(_config.GetSection("ThemeConfig"))`로 config binding.
- `App.xaml.cs:105` — `ThemeChatMessageRepository`가 DI singleton으로 등록된다.

### 사용 목적

- `Repository/ThemeChatMessageRepository.cs:149` — 마감 지수 메시지 생성 시 URL을 `$"{_config.StockDataApiUrl}/api/index/last?codes=001,101"`로 조립한다.
- `ThemeChatMessageRepository.cs:151-155` — API 응답을 `List<StockDataIndex>`로 역직렬화하고 코스피(`001`), 코스닥(`101`) 값을 추출한다.
- `ThemeChatMessageRepository.cs:163` — 지수 값/등락 정보를 메시지 문구에 반영한다.

### 현재 사용하는가?

사용 중이다. `ThemeConfig`가 DI로 binding되고, `ThemeChatMessageRepository`의 활성 코드에서 `_config.StockDataApiUrl`을 사용해 StockData 지수 API를 호출한다.

### 연관해서 봐야 할 부분

- 이 키는 `/api`를 포함하지 않는 host 값이다. 코드가 `/api/index/last`를 붙이므로 config 값을 `https://stockdata.finup.co.kr/api`로 바꾸면 URL이 `.../api/api/index/last`가 될 수 있다.
- 같은 `ThemeConfig`에는 `ChatApiMessageUrl`, `ChatApiKeyFinance`, `FinanceUrl`이 함께 있다. 지수 API 호출 결과가 채팅 메시지 발송 흐름에 들어가므로 Chat API 설정과 같이 확인해야 한다.
- 요청에 동일 키가 두 번 기재되어 있었으나 저장소에는 하나의 property/설정값만 확인된다.

## 3.7 `FinUp.StockData.ChartCapture.App` — `appSettings:StockDataUrl`

### 정의

- `App.config:28` — 소스 기준 `StockDataUrl=https://stockdata.finup.co.kr`
- `App.config:29` — 소스 기준 `StartUp=Chart`
- `/mnt/c/App/Config/FinUp.StockData.ChartCapture.App.exe.config:6-17` — 배포 후보 일반 config에는 `StockDataUrl`이 없다.
- `/mnt/c/App/Config/scheduler_FinUp.StockData.ChartCapture.App.exe.config:10-11` — scheduler 배포 config에는 `StockDataUrl=https://stockdata.finup.co.kr`, `StartUp=Scheduler`가 있다.
- `Program.cs:21-27` — `StartUp` 값에 따라 `Scheduler`, `TcpListenerChart`, `TcpListenerRobo` 중 하나를 실행한다.

### 사용 목적

1. 현재 기본 실행 모드인 `Chart`
   - `TcpListenerChart.cs:30` — `_chartUrl`에 `StockDataUrl` 로드.
   - `TcpListenerChart.cs:147-158` — 테마 차트 URL을 만든다. 현재 `ChartUrlVersion=v2`이면 `https://stockdata.finup.co.kr/chart/lwthemechart_1250_400.html?keywordIdx=...` 형태가 된다.

2. `Scheduler` 모드
   - `Scheduler.cs:66` — `$"{StockDataUrl}/api"`를 `GetScheduleMarket()`에 넘겨 시장 일정 API를 조회한다.
   - `Job/Deposit.cs:17`, `Job/Deposit.cs:37` — `StockDataUrl/chart/trchart.html` 로드.
   - `Job/Deposit.cs:55` — `StockDataUrl/chart/custchart.html` 로드.
   - `Job/Themelog.cs:17`, `Job/Themelog.cs:36` — `StockDataUrl/chart/themelogchart.html` 로드.

### 현재 사용하는가?

소스 기준으로는 사용 중이다. `StartUp=Chart`이면 `TcpListenerChart`가 실행되고, 해당 클래스가 `StockDataUrl`을 사용해 테마 차트 HTML을 로드한다. `Scheduler` 모드도 같은 키를 사용한다. 배포 후보 기준으로는 주의가 필요하다. `/mnt/c/App/Config/FinUp.StockData.ChartCapture.App.exe.config`에는 `StockDataUrl`이 없으므로 이 파일로 현재 소스 바이너리를 실행하면 `Chart`/`Scheduler`의 StockDataUrl 의존 경로가 깨질 수 있다. 반면 `/mnt/c/App/Config/scheduler_FinUp.StockData.ChartCapture.App.exe.config`에는 해당 키가 존재하고 `StartUp=Scheduler`다.

### 연관해서 봐야 할 부분

- 이 키는 `/api` 없는 host다. Chart HTML 경로(`/chart/...`)와 API 경로(`/api`)를 모두 만들기 때문에 `/api` 포함 값으로 바꾸면 차트 URL이 깨진다.
- `FinUp.StockData.RoboAnalysis.App`의 `ChartAPIAddress`는 ChartCapture 계층을 외부에서 호출하는 역할로 보인다. RoboAnalysis의 chart capture API와 ChartCapture의 실제 `StockDataUrl`/`StartUp` 설정을 같이 봐야 한다.
- 현재 ChartCapture는 `StartUp=Chart`라 TCP listener 기반 테마 차트 캡처 서버로 동작한다. `Scheduler` 모드로 바꾸면 같은 `StockDataUrl`이 시장 일정 API와 배치 차트 캡처에 쓰인다.

## 4. 설정키별 현재 사용 여부 요약

| 설정키 | 정의됨 | 코드 참조됨 | 현재 설정 기준 실행 경로에서 사용 | 비고 |
|---|---|---|---|---|
| `FinUp.Radar.App.AlphaBot:ApiStockPriceAddress` | 예 | 예 | 예 | 가격 diff 및 장 시작 delay 계산 |
| `FinUp.Stock.App.AlphaBot:StockDataApi` | 예 | 예 | 예 | `/price/highlowlist` POST |
| `FinUp.StockData.Price.App:WebAPIAddress` | 예 | 예 | 예 | 소스 `StartUp=KR`, 일반 배포 후보 `StartUp=S`; 두 경로 모두 일정 API에 사용 |
| `KiwoomReal_FinUp.StockData.Price.App:WebAPIAddress` | 배포 config 존재 | 예 | 예 | `/mnt/c/App/Config/...`의 `StartUp=KR` 변형 |
| `FinUp.StockData.RoboAnalysis.App:WebAPIAddress` | 예 | 예 | 예 | 소스/배포 후보 모두 `UIType=JOB`; `Scheduler`에서 사용 |
| `FinUp.StockData.RoboAnalysis.App:ChartAPIAddress` | 예 | 예 | 예 | 소스와 배포 후보의 endpoint가 다르며 `JobChart()`에서 호출 |
| `FinUp.Analysis.Theme.App:ThemeConfig:StockDataApiUrl` | 예 | 예 | 예 | DI binding 후 지수 API 호출 |
| `FinUp.StockData.ChartCapture.App:StockDataUrl` | 예 | 예 | 예 | 현재 `StartUp=Chart`; 차트 HTML host |

## 5. 리스크/점검 포인트

| 영역 | 점검 포인트 | 관련 프로젝트 |
|---|---|---|
| URL base 규칙 | `/api` 포함/미포함 규칙을 문서화하고 config 변경 시 자동 검증 필요 | 전체 |
| 운영/pre 혼재 | RoboAnalysis 소스와 배포 후보의 `ChartAPIAddress`가 다름. 실제 적용 config 확인 | `FinUp.StockData.RoboAnalysis.App`, `FinUp.StockData.ChartCapture.App` |
| 실제 배포 config | 소스 `App.config`, `/mnt/c/App/Config/*.exe.config`, `*_real.config` 중 실제 서비스가 읽는 파일 확인 | `FinUp.StockData.Price.App`, `KiwoomReal_FinUp.StockData.Price.App`, `FinUp.StockData.ChartCapture.App` |
| 시장 일정 API 장애 | Price/Robo/ChartCapture scheduler가 모두 장 일정 API에 의존 | `FinUp.StockData.Price.App`, `FinUp.StockData.RoboAnalysis.App`, `FinUp.StockData.ChartCapture.App` |
| API 응답 검증 | 가격/지수 API 응답 deserialization 실패 시 예외/빈 결과 처리 확인 | `FinUp.Radar.App.AlphaBot`, `FinUp.Stock.App.AlphaBot`, `FinUp.Analysis.Theme.App` |
| 수동 실행 모드 | `IsManual=Y`가 chart API 호출 시간을 변경하므로 수동 실행 시 외부 호출 발생 확인 | `FinUp.StockData.RoboAnalysis.App` |
| 중복 서비스명 | `KiwoomReal_FinUp.StockData.Price.App`가 독립 프로젝트인지 실행 변형 명칭인지 배포 문서와 대조 | `FinUp.StockData.Price.App` |

## 6. 근거 파일 색인

### `FinUp.Radar.App.AlphaBot`

- `App.config:53` — `ApiStockPriceAddress` 정의
- `Config/AppSetting.cs:16` — 설정 로드
- `Operation/ProcessUnit/BaseProcessUnit.cs:383-400` — `/price/diff` 호출
- `Operation/ProcessUnit/ThemeLogAlarm.cs:43` — 장 시작 delay 계산
- `Operation/ProcessUnit/ThemeLogSendMessage.cs:29-31` — 주석 처리된 과거 사용 흔적

### `FinUp.Stock.App.AlphaBot`

- `App.config:52` — `StockDataApi` 정의
- `Operation/ProcessBase.cs:84` — 설정 로드
- `Operation/ProcessUnit.cs:3220-3238` — `/price/highlowlist` POST 호출

### `FinUp.StockData.Price.App` / Kiwoom Real 변형

- `App.config:30` — `WebAPIAddress` 정의
- `App.config:32` — 현재 `StartUp=KR`
- `Program.cs:20-34` — `KR` → `SchedulerKiwoomReal`
- `SchedulerKiwoomReal.cs:43-76` — MarketType/FIDType 기반 실행 범위
- `SchedulerKiwoomReal.cs:116-139` — `WebAPIAddress`를 사용한 다음 장 일정 조회
- `StockDataHandle.exe_real.config:10`, `22` — real config 후보의 `WebAPIAddress`, `StartUp=S`
- `/mnt/c/App/Config/FinUp.StockData.Price.App.exe.config:25`, `38` — 배포 후보 일반 config의 `WebAPIAddress`, `StartUp=S`
- `/mnt/c/App/Config/KiwoomReal_FinUp.StockData.Price.App.exe.config:30`, `32`, `41-42` — Kiwoom Real 배포 config의 `WebAPIAddress`, `StartUp=KR`, `MarketType/FIDType`

### `FinUp.StockData.RoboAnalysis.App`

- `App.config:52-55` — 소스의 `UIType`, `WebAPIAddress`, `ChartAPIAddress` 정의
- `App.config:59` — 소스의 `IsManual=Y`
- `/mnt/c/App/Config/FinUp.StockData.RoboAnalysis.App.exe.config:43-50` — 배포 후보의 `UIType=JOB`, `WebAPIAddress`, 운영 `ChartAPIAddress`, `IsManual=N`
- `Program.cs:20-38` — UIType별 실행 Form
- `Common/Constants.cs:23` — `WebAPIAddress` 정적 로드
- `Scheduler.cs:80-85` — `WebAPIAddress`로 시장 일정 조회
- `Scheduler.cs:208-213`, `433-439` — 지연 발송용 다음 장 일정 조회
- `Scheduler.cs:27-28`, `452-472` — `ChartAPIAddress` 로드 및 chart capture API 호출
- `SchedulerExpression.cs:77-85`, `Analysis/Realtime/RealtimeScheduler.cs:78-84`, `Analysis/Realtime/RealtimeSchedulerMars.cs:103-109` — 다른 UIType의 `WebAPIAddress` 사용

### `FinUp.Analysis.Theme.App`

- `appsettings.json:37-48` — `ThemeConfig.StockDataApiUrl` 정의
- `App.xaml.cs:71`, `105` — config binding 및 repository 등록
- `Model/ThemeConfig.cs:34` — property 정의
- `Repository/ThemeChatMessageRepository.cs:29-37` — `IOptions<ThemeConfig>` 주입
- `Repository/ThemeChatMessageRepository.cs:149-155` — `/api/index/last?codes=001,101` 호출

### `FinUp.StockData.ChartCapture.App`

- `App.config:28-29` — 소스의 `StockDataUrl`, `StartUp=Chart`
- `/mnt/c/App/Config/FinUp.StockData.ChartCapture.App.exe.config:6-17` — 일반 배포 후보에는 `StockDataUrl` 없음
- `/mnt/c/App/Config/scheduler_FinUp.StockData.ChartCapture.App.exe.config:10-11` — scheduler 배포 후보의 `StockDataUrl`, `StartUp=Scheduler`
- `Program.cs:21-27` — 실행 모드 분기
- `TcpListenerChart.cs:30`, `147-158` — 현재 Chart 모드의 테마 차트 URL 생성
- `Scheduler.cs:66` — Scheduler 모드의 `/api` 시장 일정 조회
- `Job/Deposit.cs:17`, `37`, `55` — 신용잔고/예탁금 chart HTML 호출
- `Job/Themelog.cs:17`, `36` — 테마록 chart HTML 호출

## 7. 완료 감사 체크리스트

| 요구사항 | 증거/산출 |
|---|---|
| 각 프로젝트 조사 | 3장 프로젝트별 분석, 6장 근거 파일 색인 |
| 지정 설정키 목적 분석 | 각 프로젝트 섹션의 “사용 목적” |
| 현재 사용하는지 조사 | 4장 “현재 사용 여부 요약” 및 각 프로젝트 섹션 |
| 연관해서 봐야 할 부분 리포팅 | 2장 공통 패턴, 각 프로젝트의 “연관해서 봐야 할 부분”, 5장 리스크/점검 포인트 |
| `FinUp.Radar.App.AlphaBot:ApiStockPriceAddress` | 3.1 섹션 |
| `FinUp.Stock.App.AlphaBot:StockDataApi` | 3.2 섹션 |
| `FinUp.StockData.Price.App:WebAPIAddress` | 3.3 섹션 |
| `FinUp.StockData.RoboAnalysis.App:WebAPIAddress, ChartAPIAddress` | 3.5 섹션 |
| `KiwoomReal_FinUp.StockData.Price.App:WebAPIAddress` | 3.4 섹션 |
| `FinUp.Analysis.Theme.App:ThemeConfig:StockDataApiUrl` | 3.6 섹션 |
| `FinUp.StockData.ChartCapture.App:StockDataUrl` | 3.7 섹션 |
| `/api` 뒤 상세 요청 URL 추가 | 1장 결론 테이블의 상세 요청 URL 열, 2.2 상세 요청 URL 목록 |
| Full HD 기준 1장 테이블 개선 | 1장에 1920px → body 1824px → content 1728px → summary table 1716px 계산 명시, HTML summary table CSS/colgroup 적용 |
| `/mnt/c/reports/stockdata.api` 저장 | 본 파일 및 HTML 파일 저장 경로 |
| HTML/MD 두 벌 생성 | `stockdata.api.settings-analysis.md`, `stockdata.api.settings-analysis.html` |
