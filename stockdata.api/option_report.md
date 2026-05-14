# StockData 운영 URL 엔드포인트 사용 상세 분석 리포트

- 작성일: 2026-05-14
- 작성 위치: `C:\reports\stockdata.api\option_report.md`, `C:\reports\stockdata.api\option_report.html`
- 분석 대상 URL: `stockdata.finup.co.kr`
- 주요 입력 리포트:
  - `C:\reports\FinUp.StockData.Price.Api\FinUp.StockData.Price.Api_report.html`
  - `C:\reports\설정분석.html`
  - `C:\reports\stockdata.api\stockdata.api.settings-analysis.html`
  - `C:\reports\FinUp.StockData.ChartCapture.App\FinUp.StockData.ChartCapture.App.analysis.html`
- 실제 소스 근거: `C:\Dev` 및 배포 후보 설정 `C:\App\Config`
- 민감정보 처리: DB 문자열, 계정, API key 등은 인용하지 않고 URL, 설정키, 클래스, 메소드, 라인 번호만 남겼다.

## 1. 결론 요약

`stockdata.finup.co.kr`은 한 가지 URL 형태로만 쓰이지 않는다. 실제 코드에서는 다음 세 종류로 구분된다.

| 구분 | 설정값 형태 | 대표 설정키 | 코드 조립 방식 | 핵심 위험 |
|---|---|---|---|---|
| API base | `https://stockdata.finup.co.kr/api` | `ApiStockPriceAddress`, `StockDataApi`, `WebAPIAddress` | 코드가 `/price/...`, `/market/...` 등을 뒤에 붙임 | `/api`를 제거하면 호출 endpoint가 한 단계 빠진다. |
| Host base | `https://stockdata.finup.co.kr` | `StockDataUrl`, `ThemeConfig:StockDataApiUrl` | 코드가 `/api/...` 또는 `/chart/...`를 목적별로 붙임 | 여기에 `/api`를 넣으면 `/api/api/...` 또는 `/api/chart/...` 오류가 난다. |
| 완성 endpoint | `http://stockdata.finup.co.kr/api/chart/capture` | `ChartAPIAddress` | 코드가 `?date=yyyy-MM-dd`만 붙임 | base URL로 취급하면 chart capture endpoint가 깨진다. |

확인된 핵심 endpoint는 다음과 같다.

```text
https://stockdata.finup.co.kr/api/price/diff
https://stockdata.finup.co.kr/api/price/highlowlist
https://stockdata.finup.co.kr/api/market/{from}/{to}
https://stockdata.finup.co.kr/api/index/last?codes=001,101
http://stockdata.finup.co.kr/api/chart/capture?date={yyyy-MM-dd}
https://stockdata.finup.co.kr/api/chart/capture/theme?keyword={keyword}&keywordIdx={keywordIdx}
https://stockdata.finup.co.kr/chart/lwthemechart_1250_400.html?keywordIdx={keywordIdx}
https://stockdata.finup.co.kr/chart/themechart.html?Keyword={keyword}&KeywordIdx={keywordIdx}
https://stockdata.finup.co.kr/chart/trchart.html
https://stockdata.finup.co.kr/chart/custchart.html
https://stockdata.finup.co.kr/chart/themelogchart.html
```

차트 HTML은 단순 정적 페이지가 아니라 내부 JavaScript에서 다시 Price.Api endpoint를 호출한다. 예를 들어 `lwthemechart_1250_400.html`은 `/api/v2/chart/lw/theme?keywordIdx=...`, `trchart.html`과 `custchart.html`은 `/api/chart/stockdeposit`, `themelogchart.html`은 `/api/ThemeCaptureChart`, `/api/ThemeRelationStock`, `/api/ThemeLog/play/info`, `/api/ThemeLog/play`을 호출한다.

## 2. 설정 파일 기준 사용처

`설정분석.html`과 `stockdata.api.settings-analysis.html`에서 `stockdata.finup.co.kr`로 묶이는 운영 후보 설정은 아래와 같다.

| 파일/서비스 | 설정키 | 값 | 실행/사용 의미 | 실제 프로젝트 |
|---|---|---|---|---|
| `FinUp.Radar.App.AlphaBot.exe.config` | `appSettings:ApiStockPriceAddress` | `https://stockdata.finup.co.kr/api` | 가격 diff, 장 시작 delay 계산 | `C:\Dev\FinUp.Radar.App.AlphaBot` |
| `FinUp.Stock.App.AlphaBot.exe.config` | `appSettings:StockDataApi` | `https://stockdata.finup.co.kr/api` | 채팅/시그널 고가·저가 판정 | `C:\Dev\FinUp.Stock.App.AlphaBot` |
| `FinUp.StockData.Price.App.exe.config` | `appSettings:WebAPIAddress` | `https://stockdata.finup.co.kr/api` | 일봉/가격 수집 스케줄 산정 | `C:\Dev\FinUp.StockData.Price.App` |
| `KiwoomReal_FinUp.StockData.Price.App.exe.config` | `appSettings:WebAPIAddress` | `https://stockdata.finup.co.kr/api` | 같은 Price.App 코드의 Kiwoom Real 변형 | `C:\Dev\FinUp.StockData.Price.App` |
| `FinUp.StockData.RoboAnalysis.App.exe.config` | `appSettings:WebAPIAddress` | `https://stockdata.finup.co.kr/api` | 로보 분석/발송 스케줄 산정 | `C:\Dev\FinUp.StockData.RoboAnalysis.App` |
| `FinUp.StockData.RoboAnalysis.App.exe.config` | `appSettings:ChartAPIAddress` | `http://stockdata.finup.co.kr/api/chart/capture` | 로보 분석 후 차트 캡처 트리거 | `C:\Dev\FinUp.StockData.RoboAnalysis.App` |
| `FinUp.Analysis.Theme.App.appsettings.json` | `ThemeConfig:StockDataApiUrl` | `https://stockdata.finup.co.kr` | 코스피/코스닥 지수 메시지 | `C:\Dev\FinUp.Analysis.Theme.App` |
| `scheduler_FinUp.StockData.ChartCapture.App.exe.config` | `appSettings:StockDataUrl` | `https://stockdata.finup.co.kr` | ChartCapture Scheduler의 시장 일정/차트 HTML base | `C:\Dev\FinUp.StockData.ChartCapture.App` |

## 3. 엔드포인트별 호출 상세

### 3.1 `POST /api/price/diff`

| 항목 | 내용 |
|---|---|
| 완성 URL | `https://stockdata.finup.co.kr/api/price/diff` |
| 서버 route | `PriceController.GetPriceDiffList(PriceListParam param)` — `C:\Dev\FinUp.StockData.Price.Api\Controllers\PriceController.cs:81-86` |
| 서버 역할 | 복수 종목 현재가/등락률 조회. `param.Params[].StockCode`별 현재가를 가져와 결과 목록을 반환한다. |

#### 호출자 A — Radar AlphaBot 공통 가격 조회

| 항목 | 내용 |
|---|---|
| 프로젝트 | `FinUp.Radar.App.AlphaBot` |
| 설정 | `App.config:53` / 배포 후보 `C:\App\Config\FinUp.Radar.App.AlphaBot.exe.config:51`, `ApiStockPriceAddress=https://stockdata.finup.co.kr/api` |
| 설정 로딩 | `Config.AppSetting.ApiStockPriceAddress` — `C:\Dev\FinUp.Radar.App.AlphaBot\Config\AppSetting.cs:16` |
| 클래스/메소드/라인 | `Operation.ProcessUnit.BaseProcessUnit.GetStockPrice(List<string>)` — `BaseProcessUnit.cs:383-400` |
| URL 조립 | `string apiUrl = $"{AppSetting.ApiStockPriceAddress}/price/diff "` — `BaseProcessUnit.cs:395` |
| HTTP 방식 | POST. `SendPostApiStock(apiUrl, data)` — `BaseProcessUnit.cs:400` |
| 요청값 | `ApiPriceListParam.Params`에 `ApiStockParam { StockCode = listStockCode[i] }` 추가 후 JSON 직렬화 — `BaseProcessUnit.cs:387-393` |
| 목적 | 알파봇 처리 중 종목 코드 목록의 현재가, 거래시각, 거래량, 등락률을 확보해 메시지/조건 판단에 사용한다. 응답 매핑은 `BaseProcessUnit.cs:402-412`이다. |
| 주의 | URL 문자열 끝에 공백이 있다. HTTP client가 trim하지 않으면 endpoint mismatch 가능성이 있다. |

#### 호출자 B — Radar AlphaBot StockPrice 내부 하드코딩 경로

| 항목 | 내용 |
|---|---|
| 프로젝트 | `FinUp.Radar.App.AlphaBot` |
| 클래스/메소드/라인 | `Operation.ProcessUnit.StockPrice.GetStockPriceApi(List<string>)` — `StockPrice.cs:407-424` |
| URL 조립 | `string apiUrl = "https://stockdata.finup.co.kr/api/price/diff"` — `StockPrice.cs:419` |
| HTTP 방식 | POST. `SendPostApiStock(apiUrl, data)` — `StockPrice.cs:424` |
| 요청값 | `ApiPriceListParam.Params[].StockCode` — `StockPrice.cs:411-417` |
| 목적 | `StockPrice` 클래스 내부의 테마/종목 가격 캐시 계산용 후보 경로. 현재 파일 안에서 `GetStockPriceApi` 직접 호출은 확인되지 않아 “정의됨/잠재 사용”으로 보는 것이 안전하다. |

#### 추가 후보 — Radar.Api

| 항목 | 내용 |
|---|---|
| 프로젝트 | `FinUp.Radar.Api` |
| 클래스/메소드/라인 | `Cache.StockPrice.GetStockPrice(List<string>)` — `C:\Dev\FinUp.Radar.Api\Cache\StockPrice.cs:205-222` |
| URL | `http://stockdata.finup.co.kr/api/price/diff` — `StockPrice.cs:217` |
| 목적 | Radar API 캐시 계층에서 종목 가격 diff 목록을 조회한다. |

### 3.2 `POST /api/price/highlowlist`

| 항목 | 내용 |
|---|---|
| 완성 URL | `https://stockdata.finup.co.kr/api/price/highlowlist` |
| 서버 route | `PriceController.GetHighLowList(HighLowListParam param)` — `C:\Dev\FinUp.StockData.Price.Api\Controllers\PriceController.cs:254-260` |
| 서버 역할 | 요청된 종목별 장중 고가/저가/거래량/거래대금 정보를 Redis에서 조회한다. `Ref`, `ItemType`은 client 매핑값으로 되돌린다 — `PriceController.cs:286-314`. |
| 호출 프로젝트 | `FinUp.Stock.App.AlphaBot` |
| 설정 | `App.config:52`, `StockDataApi=https://stockdata.finup.co.kr/api` |
| 설정 로딩 | `Operation.ProcessBase.StockDataApi` — `C:\Dev\FinUp.Stock.App.AlphaBot\Operation\ProcessBase.cs:83-85` |
| 클래스/메소드/라인 | `Operation.ProcessUnit.CheckSignalQueue(string OIdx, string OTIdx)` — `ProcessUnit.cs:3200-3238` |
| URL 조립 | `string apiUrl = $"{StockDataApi}/price/highlowlist"` — `ProcessUnit.cs:3233` |
| HTTP 방식 | POST JSON + request gzip/compress 옵션. `NetUtil.WebRequestPostJsonAsync(apiUrl, data, requiredRequestCompress: true)` — `ProcessUnit.cs:3237` |
| 요청값 | `HighLowListParam.Params[]`: `StockCode=item.ItemCode`, `From=item.RegDT` 또는 `DateTime.Now.AddMinutes(-5)`, `Ref=item.SignalQueueIdx` — `ProcessUnit.cs:3220-3229` |
| 목적 | 채팅/시그널 큐 대상 종목의 신호 발생 이후 고가·저가를 확인해 체결/조건 충족 여부를 판정한다 — `ProcessUnit.cs:3240-3251`. |

### 3.3 `GET /api/market/{from}/{to}`

| 항목 | 내용 |
|---|---|
| 완성 URL 패턴 | `https://stockdata.finup.co.kr/api/market/{from}/{to}` |
| 서버 route | `PriceController.GetMarket(string from, string to, int? offday = null)` — `C:\Dev\FinUp.StockData.Price.Api\Controllers\PriceController.cs:328-332` |
| 서버 역할 | StockCalendar에서 개장 여부, 시작/종료시각, `YYYY_MM_DD` 목록을 반환한다 — `PriceController.cs:340-352`. |
| 공통 조립 함수 | `FinUp.StockData.Fundamentals.Util.GetMarketInfo(string url, string from="", string to="")` — `C:\Dev\FinUp.StockData.Fundamentals\Util.cs:29-61` |
| 공통 URL 조립 | `string apiUrl = $"{url}/market/{from}/{to}"` — `Util.cs:49` |
| 기본값 | `from` 미지정 시 오늘, `to` 미지정 시 오늘+10일 — `Util.cs:39-45` |
| 과거 포함 스케줄 | `GetScheduleMarket()`은 `from=DateTime.Today.AddDays(-10)`로 호출 — `Util.cs:125-132` |
| 다음 장 스케줄 | `GetScheduleNextMarket()`은 기본 `GetMarketInfo(url)` 사용 — `Util.cs:91-103` |

#### 호출자 A — Radar AlphaBot 테마로그 알림 delay

| 항목 | 내용 |
|---|---|
| 프로젝트 | `FinUp.Radar.App.AlphaBot` |
| 클래스/메소드/라인 | `ThemeLogAlarm.Run(string OTIdx)` — `C:\Dev\FinUp.Radar.App.AlphaBot\Operation\ProcessUnit\ThemeLogAlarm.cs:20-43` |
| 호출 | `Util.DelayMarketStartTime(AppSetting.ApiStockPriceAddress, delayMin)` — `ThemeLogAlarm.cs:43` |
| 내부 값 | `DelayMarketStartTime()` → `GetMarketToday()` → `GetMarketInfo(url)`로 오늘~오늘+10일 시장 일정 조회 — `Util.cs:371-385`, `Util.cs:319-329`, `Util.cs:39-49` |
| 목적 | 장 시작 기준 `ThemeLogPushRankingDelay`분 후 테마로그 랭킹 알림을 실행하기 위한 delay 계산 — `ThemeLogAlarm.cs:25-48`. |

#### 호출자 B — StockData Price.App 일반 스케줄러

| 항목 | 내용 |
|---|---|
| 프로젝트 | `FinUp.StockData.Price.App` |
| 배포 후보 설정 | `C:\App\Config\FinUp.StockData.Price.App.exe.config:25`, `WebAPIAddress=https://stockdata.finup.co.kr/api` |
| 진입 분기 | `Program.Main()`에서 `StartUp=S`이면 `SchedulerXingTR` 실행, `StartUp=KR`이면 `SchedulerKiwoomReal` 실행 — `Program.cs:20-30` |
| 클래스/메소드/라인 | `SchedulerXingTR.Scheduler_Load(object, EventArgs)` — `SchedulerXingTR.cs:67-72` |
| 호출 | `Util.GetScheduleMarket(0, ConfigurationManager.AppSettings["WebAPIAddress"])` — `SchedulerXingTR.cs:71` |
| 실제 날짜 범위 | 공통 함수 기준 `from=today-10`, `to=today+10` — `Util.cs:125-132`, `Util.cs:43-49` |
| 목적 | 일봉/가격 수집 스케줄러의 현재/이전 시장 일정을 얻어 실행 기준을 만든다. |

#### 호출자 C — KiwoomReal_FinUp.StockData.Price.App 배포 변형

| 항목 | 내용 |
|---|---|
| 프로젝트 | 소스는 `C:\Dev\FinUp.StockData.Price.App`, 배포 설정명은 `KiwoomReal_FinUp.StockData.Price.App.exe.config` |
| 배포 후보 설정 | `C:\App\Config\KiwoomReal_FinUp.StockData.Price.App.exe.config:30-32`, `WebAPIAddress=https://stockdata.finup.co.kr/api`, `StartUp=KR` |
| 클래스/메소드/라인 | `SchedulerKiwoomReal.InitSchedule()` — `SchedulerKiwoomReal.cs:116-128` |
| 호출 | `Util.GetScheduleNextMarket(_startDelay, ConfigurationManager.AppSettings["WebAPIAddress"])` — `SchedulerKiwoomReal.cs:128` |
| 실제 날짜 범위 | 기본 `from=today`, `to=today+10` — `Util.cs:39-49`, `Util.cs:91-103` |
| 목적 | Kiwoom 실시간 수집 시작 delay와 장 종료시각을 계산해 `StartSchedule()`에 전달한다 — `SchedulerKiwoomReal.cs:135-139`. |

#### 호출자 D — RoboAnalysis.App 스케줄/실시간 계열

| 항목 | 내용 |
|---|---|
| 프로젝트 | `FinUp.StockData.RoboAnalysis.App` |
| 설정 | 소스 `App.config:53`, 배포 후보 `C:\App\Config\FinUp.StockData.RoboAnalysis.App.exe.config:44`, `WebAPIAddress=https://stockdata.finup.co.kr/api` |
| 설정 로딩 | `Common.Constants.WebAPIAddress` — `C:\Dev\FinUp.StockData.RoboAnalysis.App\Common\Constants.cs:23` |
| 클래스/메소드/라인 | `Scheduler.InitSchedule()` — `Scheduler.cs:80-85`; `SchedulerExpression.InitSchedule()` — `SchedulerExpression.cs:77-84`; `RealtimeScheduler.InitSchedule()` — `Analysis\Realtime\RealtimeScheduler.cs:78-83`; `RealtimeSchedulerMars.InitSchedule()` — `Analysis\Realtime\RealtimeSchedulerMars.cs:103-108` |
| 추가 호출 | 예약 발송 delay: `Scheduler.cs:211`, `Scheduler.cs:438` |
| 목적 | 로보 분석 JOB/검색식/실시간 분석이 장 일정 및 다음 장 시작 기준으로 작업/발송 시점을 계산한다. |

#### 호출자 E — ChartCapture Scheduler

| 항목 | 내용 |
|---|---|
| 프로젝트 | `FinUp.StockData.ChartCapture.App` |
| 배포 후보 설정 | `C:\App\Config\scheduler_FinUp.StockData.ChartCapture.App.exe.config:10-11`, `StockDataUrl=https://stockdata.finup.co.kr`, `StartUp=Scheduler` |
| 진입 분기 | `Program.Main()`에서 `StartUp=Scheduler`이면 `new Scheduler()` — `Program.cs:21-24` |
| 클래스/메소드/라인 | `Scheduler.InitSchedule()` — `C:\Dev\FinUp.StockData.ChartCapture.App\Scheduler.cs:62-67` |
| URL 조립 | `GetScheduleMarket(0, $"{ConfigurationManager.AppSettings["StockDataUrl"]}/api")` — `Scheduler.cs:66`; 공통 함수에서 `/market/{from}/{to}` 추가 |
| 실제 날짜 범위 | `from=today-10`, `to=today+10` |
| 목적 | 장 종료 후 예탁금/신용잔고/테마로그 차트 캡처 배치 시작 시각을 계산한다. 실패 시 스케줄 초기화를 중단한다 — `Scheduler.cs:67-70`. |

### 3.4 `GET /api/index/last?codes=001,101`

| 항목 | 내용 |
|---|---|
| 완성 URL | `https://stockdata.finup.co.kr/api/index/last?codes=001,101` |
| 서버 route | `IndexController.GetIndexLast(string[] codes)` — `C:\Dev\FinUp.StockData.Price.Api\Controllers\IndexController.cs:16-20` |
| 호출 프로젝트 | `FinUp.Analysis.Theme.App` |
| 설정 | `appsettings.json:47`, `ThemeConfig.StockDataApiUrl=https://stockdata.finup.co.kr` |
| 설정 모델 | `Model.ThemeConfig.StockDataApiUrl` — `ThemeConfig.cs:32-35` |
| 클래스/메소드/라인 | `Repository.ThemeChatMessageRepository`의 Index 메시지 처리 분기 — `ThemeChatMessageRepository.cs:144-152` |
| URL 조립 | `var url = $"{_config.StockDataApiUrl}/api/index/last?codes=001,101"` — `ThemeChatMessageRepository.cs:149` |
| HTTP 방식 | GET. `FinUp.Core.NET.Web.Util.WebRequestAsync(url: url)` — `ThemeChatMessageRepository.cs:151` |
| 목적/값 | 코스피(`001`)·코스닥(`101`) 마감 지수를 조회해 테마 메시지에 넣는다 — `ThemeChatMessageRepository.cs:146-155`. |

### 3.5 `GET /api/chart/capture?date={yyyy-MM-dd}`

| 항목 | 내용 |
|---|---|
| 완성 URL | `http://stockdata.finup.co.kr/api/chart/capture?date={DateTime.Today:yyyy-MM-dd}` |
| 서버 route | `ChartController.Capture(string date)` — `C:\Dev\FinUp.StockData.Price.Api\Controllers\ChartController.cs:69-72` |
| 서버 동작 | self host의 TCP 8279로 `{date}|<EOF>`를 보내 차트 캡처를 위임 — `ChartController.cs:78-92` |
| 호출 프로젝트 | `FinUp.StockData.RoboAnalysis.App` |
| 설정 | 배포 후보 `C:\App\Config\FinUp.StockData.RoboAnalysis.App.exe.config:46`, `ChartAPIAddress=http://stockdata.finup.co.kr/api/chart/capture`; 소스 `App.config:55`는 pre endpoint |
| 클래스/메소드/라인 | `Scheduler.JobChart(TimeSpan delay, CancellationToken token)` — `Scheduler.cs:452-472` |
| URL 조립 | `string chartCaptureUrl = $"{_chartAPIAddress}?date={DateTime.Today:yyyy-MM-dd}"` — `Scheduler.cs:466` |
| HTTP 방식 | GET. `WebRequestAsync(chartCaptureUrl)` — `Scheduler.cs:471` |
| 목적 | 로보 분석 후 지정 날짜의 차트 캡처 API를 호출해 ChartCapture 계층을 트리거한다. |
| 주의 | 이 설정은 API base가 아니라 완성 endpoint다. 소스는 `pre-stockdata`, 배포 후보는 운영 `stockdata`라 실제 로드 config 확인이 중요하다. |

### 3.6 `GET /api/chart/capture/theme?keyword=...&keywordIdx=...`

| 항목 | 내용 |
|---|---|
| 완성 URL | `https://stockdata.finup.co.kr/api/chart/capture/theme?keyword={Keyword}&keywordIdx={KeywordIdx}` |
| 서버 route | `ChartController.CaptureTheme(string keyword, int keywordIdx)` — `ChartController.cs:106-108` |
| 서버 동작 | self host의 TCP 8280으로 `ThemeChart|{keyword}|{keywordIdx}|<EOF>` 전송 — `ChartController.cs:115-129` |
| 확인된 추가 호출자 | `FinUp.Finance.Admin` |
| 클래스/메소드/라인 | `Utils.DataUtil.ThemeChartCapture(string KeywordIdx, string Keyword)` — `C:\Dev\FinUp.Finance.Admin\Utils\DataUtil.cs:802-807` |
| 목적/값 | Finance/Admin 쪽에서 테마 차트 이미지를 생성하기 위해 keyword, keywordIdx를 query string으로 전달한다. |

## 4. ChartCapture `StockDataUrl` 기반 차트 HTML 로드

`FinUp.StockData.ChartCapture.App`의 `StockDataUrl`은 API base가 아니라 chart page host다. CEF browser가 HTML을 로드하고, 그 HTML 내부 JS가 Price.Api endpoint를 다시 호출한다.

### 4.1 Chart 모드 — 테마 차트 즉시 캡처

| 항목 | 내용 |
|---|---|
| 설정 | 소스 `App.config:28-33`, `StockDataUrl=https://stockdata.finup.co.kr`, `StartUp=Chart`, `ChartUrlVersion=v2` |
| 진입 분기 | `Program.Main()`에서 `StartUp=Chart`이면 `new TcpListenerChart()` — `Program.cs:21-25` |
| 클래스/메소드/라인 | `TcpListenerChart.CaptureThemeChart(string keyword, string keywordIdx)` — `TcpListenerChart.cs:147-158` |
| v2 실제 URL | `https://stockdata.finup.co.kr/chart/lwthemechart_1250_400.html?keywordIdx={keywordIdx}` — `TcpListenerChart.cs:151-152` |
| legacy URL | `https://stockdata.finup.co.kr/chart/themechart.html?Keyword={keyword}&KeywordIdx={keywordIdx}` — `TcpListenerChart.cs:149` |
| 목적/값 | TCP 요청으로 받은 `keyword`, `keywordIdx`를 사용해 테마 chart HTML을 렌더링하고 PNG를 저장한다. 현재 config가 `ChartUrlVersion=v2`라 `keyword`는 URL에 반영되지 않고 `keywordIdx`만 사용된다. |
| 내부 API | `lwthemechart_1250_400.html`은 `/api/v2/chart/lw/theme?keywordIdx={keywordIdx}`를 GET — `Chart\lwthemechart_1250_400.html:146-149`; 서버는 `ChartController.GetThemeChartAsync_v2(int keywordIdx)` — `ChartController.cs:236-238`. |

### 4.2 Scheduler 모드 — 예탁금/신용잔고/테마로그 차트 배치 캡처

| 항목 | 내용 |
|---|---|
| 설정 | 배포 후보 `scheduler_FinUp.StockData.ChartCapture.App.exe.config:10-11`, `StockDataUrl=https://stockdata.finup.co.kr`, `StartUp=Scheduler` |
| `Deposit.Start()` URL | `https://stockdata.finup.co.kr/chart/trchart.html` — `Job\Deposit.cs:34-41`; `https://stockdata.finup.co.kr/chart/custchart.html` — `Job\Deposit.cs:54-58` |
| `Themelog.Start()` URL | `https://stockdata.finup.co.kr/chart/themelogchart.html` — `Job\Themelog.cs:34-39` |
| 목적 | 장 종료 후 차트 HTML을 offscreen browser로 렌더링해 파일로 저장한다. |
| 내부 API 1 | `trchart.html`, `custchart.html`은 `/api/chart/stockdeposit` GET — `Chart\trchart.html:15-18`, `Chart\custchart.html:15-18`; 서버는 `ChartController.StockDepositTrend()` — `ChartController.cs:143-145`. |
| 내부 API 2 | `themelogchart.html`은 `stockDataApiUrl='https://stockdata.finup.co.kr/api'` — `Chart\ThemeLogChart.html:1043-1044`; 별도 JS가 아래 endpoint들을 호출한다. |

### 4.3 `themelogchart.html` 내부 endpoint

| 내부 endpoint | JS 함수/라인 | 서버 메소드/라인 | 목적/값 |
|---|---|---|---|
| `POST /api/ThemeCaptureChart` | `getThemeChartData()` — `Scripts\themelog\themelog.api.js:3-27`; `refreshChartData()` — `themelog.api.js:102-116` | `ThemeLogController.GetThemeCaptureChart(ThemeScoreDisplayParam)` — `ThemeLogController.cs:26-30` | 테마록 차트 최초/갱신 데이터. 요청 JSON에 `CaptureIdx` 포함. |
| `POST /api/ThemeRelationStock` | `getThemeRelationStock()` 흐름 — `themelog.api.js:232-247` | `ThemeLogController.GetThemeRelationStock(ThemeScoreDisplayParam)` — `ThemeLogController.cs:38-42` | 선택 테마의 관련 종목 조회. 요청 JSON에 `CaptureIdx`, `KeywordIdx` 포함. |
| `POST /api/ThemeLog/play/info` | `getThemePlayInfo()` — `themelog.api.js:412-426` | `ThemeLogController.GetThemePlayInfo(ThemePlayInfoParam)` — `ThemeLogController.cs:77-80` | 플레이 구간/page 정보 조회. `StartDT`, `EndDT`, `PageSize` 포함. |
| `POST /api/ThemeLog/play` | `getThemePlayChartData()` — `themelog.api.js:488-493` | `ThemeLogController.GetThemePlay(ThemePlayParam)` — `ThemeLogController.cs:88-91` | 페이지 구간별 테마 재생 차트 데이터. `CaptureItemIdxStart`, `CaptureItemIdxEnd` 포함. |

## 5. 목적별 의존성 정리

| 목적 | 사용 endpoint | 사용하는 앱/클래스 | 장애 영향 |
|---|---|---|---|
| 종목 현재가/등락률 | `/api/price/diff` | Radar AlphaBot `BaseProcessUnit.GetStockPrice` | 알파봇 메시지/조건 판단 값 누락 또는 지연 |
| 채팅/시그널 고가·저가 판정 | `/api/price/highlowlist` | Stock AlphaBot `ProcessUnit.CheckSignalQueue` | 시그널 체결/조건 판정 실패 |
| 장 일정/다음 장 시작 계산 | `/api/market/{from}/{to}` | Price.App, KiwoomReal 변형, RoboAnalysis, ChartCapture Scheduler, Radar AlphaBot | 수집/분석/차트 캡처 스케줄이 시작되지 않거나 delay가 잘못 계산됨 |
| 마감 지수 메시지 | `/api/index/last?codes=001,101` | Analysis.Theme.App `ThemeChatMessageRepository` | 코스피/코스닥 지수 메시지 누락 |
| 로보 분석 후 차트 캡처 트리거 | `/api/chart/capture?date=...` | RoboAnalysis `Scheduler.JobChart` | 로보 분석 결과 차트 생성/반영 지연 |
| 테마 차트 즉시 캡처 | `/chart/lwthemechart_1250_400.html` → `/api/v2/chart/lw/theme` | ChartCapture `TcpListenerChart` | 테마 차트 이미지 미생성/오래된 이미지 |
| 예탁금/신용잔고 차트 배치 | `/chart/trchart.html`, `/chart/custchart.html` → `/api/chart/stockdeposit` | ChartCapture `Job.Deposit` | 장 종료 후 예탁금/신용잔고 이미지 미생성 |
| 테마로그 차트 배치 | `/chart/themelogchart.html` → ThemeLog API들 | ChartCapture `Job.Themelog` | 테마로그 차트 이미지 미생성 또는 빈 데이터 |

## 6. 전역 검색에서 확인된 추가 직접 사용 후보

아래 항목은 세 named 설정 보고서의 중심 설정키 목록에는 없거나 부록 성격이지만, `C:\Dev` 전역에서 `stockdata.finup.co.kr` 직접 사용이 확인된 대표 사례다.

| 프로젝트/파일 | endpoint | 클래스/함수/라인 | 목적/비고 |
|---|---|---|---|
| `FinUp.Radar.Api\Cache\StockPrice.cs` | `http://stockdata.finup.co.kr/api/price/diff` | `Cache.StockPrice.GetStockPrice(List<string>)` — `StockPrice.cs:205-222` | Radar API 캐시 계층의 가격 diff 조회 |
| `FinUp.Mars.LLM\src\service\StockService.py` | `/api/price/minutes/{stockCode}/{nowStr}/{nowStr}` | `StockService.__get_stock_min_data_from_api` — `StockService.py:50-58` | 특정 종목/일자의 분봉 조회 |
| `C:\Dev\src\service\StockService.py` | `/api/price/minutes/{stockCode}/{nowStr}/{nowStr}` | `StockService.__get_stock_min_data_from_api` — `StockService.py:49-59` | Mars LLM과 유사/복사본 후보 |
| `FinUp.Finance.Admin\Utils\DataUtil.cs` | `/api/chart/capture/theme` | `DataUtil.ThemeChartCapture` — `DataUtil.cs:802-807` | 테마 차트 캡처 트리거 |
| `Finup.Stock.Admin\Scripts\ngPrice.js` | `/api/profit` | Angular `$scope.Get` — `ngPrice.js:24-29` | Stockpoint Admin 진행 종목/수익 관련 조회 |
| `Finup.Stock.Admin\Scripts\ngChart.js` | `/api/chart/nvd3/{code}` | Angular `$scope.Chart` — `ngChart.js:64-69` | NVD3 차트 데이터 조회 |
| `Finup.Stock.Admin\Common\Chart\CaptureView.aspx` | `/api/tv/history` | page script ajax — `CaptureView.aspx:81-87` | TradingView history 조회 |
| `FinUp.Stock.MobileWeb\Robo\GoldenSignalStockView.aspx` | `/api/tv` | TradingView datafeed 설정 — `GoldenSignalStockView.aspx:84-90` | 모바일 골든시그널 차트 datafeed |
| `FinUp.Chat.Admin\Scripts\hoga\api.js` 및 유사 복제본 | `/api/data/{hoga|price|trader}/...`, `/api/prevday/...`, `/api/tv/history` | `getDataLink`, `getPrevDay`, `getChartData` — `api.js:19-25`, `49-54`, `67-79` | 호가/체결/거래원/전일/TV history 조회. Guide/General/Mars/Tssa/Finance/Stock 계열에 유사 파일 존재 |

## 7. 운영 점검 포인트

1. **URL 타입을 먼저 구분한다.** `WebAPIAddress`/`StockDataApi`/`ApiStockPriceAddress`는 `/api` 포함 base, `StockDataUrl`/`StockDataApiUrl`은 host base, `ChartAPIAddress`는 완성 endpoint다.
2. **소스 `App.config`와 배포 후보 `C:\App\Config`가 다르다.** 예: RoboAnalysis의 `ChartAPIAddress`는 소스 기준 pre, 배포 후보 기준 운영 URL이다.
3. **ChartCapture는 실행 모드별 사용 endpoint가 완전히 다르다.** `StartUp=Scheduler`는 시장 일정과 chart HTML 배치 캡처, `StartUp=Chart`는 TCP 테마 차트 서버, 기타는 Robo TCP 흐름이다.
4. **시장 일정 API 장애는 여러 배치/실시간 앱에 동시에 전파된다.** Price.App, KiwoomReal, RoboAnalysis, ChartCapture Scheduler, Radar AlphaBot이 모두 `/api/market/{from}/{to}` 계열에 의존한다.
5. **차트 HTML 장애와 API 장애를 분리 관측해야 한다.** ChartCapture는 HTML 로드 성공 후 내부 Ajax 실패가 별도 장애로 나타날 수 있다.
6. **하드코딩 URL도 있다.** Radar AlphaBot `StockPrice.cs`, Radar.Api, Finance.Admin, Stock.Admin JS 등은 설정 변경만으로는 endpoint가 바뀌지 않는다.
7. **HTTP/HTTPS 혼재가 있다.** `/api/chart/capture` 운영 후보와 Radar.Api 일부는 `http://stockdata...`를 사용한다. SSL/리다이렉트/방화벽 정책 점검 대상이다.

## 8. 근거 색인

| 근거 | 확인 내용 |
|---|---|
| `FinUp.StockData.Price.Api_report.html/.md` | Price.Api route 목록과 서버 controller/method 라인 |
| `설정분석.html` | 운영 후보 config 파일명, 설정키, 대표값(`https://stockdata.finup.co.kr/api`, `https://stockdata.finup.co.kr`, `http://stockdata.finup.co.kr/api/chart/capture`) |
| `stockdata.api.settings-analysis.html` | 설정키별 사용 분석과 `/api` 포함/미포함 규칙 |
| `FinUp.StockData.ChartCapture.App.analysis.html` | ChartCapture Scheduler/Chart/Robo 옵션별 외부 연동과 장애 영향 |
| `rg` 전역 검색 | `C:\Dev`, `C:\App\Config`에서 `stockdata.finup.co.kr` 직접 참조와 line 재확인 |

## 9. 분석 한계

- 실제 운영 프로세스가 어느 config 파일을 최종 로드하는지는 저장소와 `C:\App\Config` 후보만으로 100% 확정할 수 없다. 본 보고서는 파일명/설정값/소스 분기 기준의 정적 분석이다.
- 일부 JS/ASPX 화면은 사용 여부가 배포/라우팅/메뉴 노출에 따라 달라질 수 있다. 라인에 endpoint가 존재한다는 사실과 실제 트래픽 발생량은 별도 로그로 검증해야 한다.
- `FinUp.StockData.Price.Api_report.html`의 전체 route 중 본 보고서는 `stockdata.finup.co.kr` 운영 URL을 통해 실제 호출 경로가 확인된 endpoint에 집중했다.
