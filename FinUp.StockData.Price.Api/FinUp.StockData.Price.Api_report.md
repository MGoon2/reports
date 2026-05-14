# FinUp.StockData.Price.Api 분석 보고서

- 생성일: 2026-05-13
- 분석 대상: `/mnt/c/Dev/FinUp.StockData.Price.Api`
- 산출물: Markdown 및 HTML 두 형식
- 범위: Web API 라우팅/엔드포인트 역할, `Web.config` 설정값 역할 분석

## 1. 요약

- 이 프로젝트는 ASP.NET Web API 2 기반의 .NET Framework 4.7 API 프로젝트다. `Global.asax.cs`는 `WebApiConfig.Register`만 등록하므로 실제 API 라우팅은 Web API 설정이 중심이다.
- `WebApiConfig`는 gzip 요청 해제 handler, CORS, 전역 예외 필터, attribute routing, 기본 `api/{controller}/{id}` 라우트, API 로그 handler, 상세 오류 반환 정책을 등록한다.
- 실제 명시 라우트는 컨트롤러의 `[Route]` 기준 93개 항목이다. 중복 경로/다중 버전 경로가 포함된다: 예) `api/chart/capture` 오버로드, `api/tv/marks` v1/v2/v3.
- 데이터 소스는 Redis(실시간/캐시), MongoDB(체결·호가·분봉·테마 집계), SQL Biz 계층(종목/캘린더/재무/뉴스 등), 외부 실시간 StockData API가 혼합되어 있다.

## 2. 라우팅/공통 파이프라인 근거

| 항목 | 역할 | 근거 |
|---|---|---|
| Application_Start | `GlobalConfiguration.Configure(WebApiConfig.Register)` 호출로 Web API만 초기화 | `Global.asax.cs:12-15` |
| CompressedRequestHandler | 요청 `Content-Encoding: gzip`이면 request body를 해제 | `App_Start/WebApiConfig.cs:16; Handler/CompressedRequestHandler.cs:14-21` |
| CORS | `config.EnableCors()`와 여러 컨트롤러의 `[EnableCors(origins:"*", headers:"*", methods:"*")]`로 교차 출처 허용 | `App_Start/WebApiConfig.cs:18; Controllers/PriceController.cs:24` |
| ExceptionFilter | 예외 발생 시 Trace 기록 후 HTTP 500과 예외 Message 반환 | `App_Start/WebApiConfig.cs:21; Filter/ExceptionFilter.cs:10-24` |
| Attribute routing | `config.MapHttpAttributeRoutes()`로 컨트롤러 `[Route]`를 활성화 | `App_Start/WebApiConfig.cs:24-25` |
| DefaultApi | `api/{controller}/{id}` 기본 라우트도 존재. 단, 보고서의 엔드포인트 표는 명시 `[Route]` 기준 | `App_Start/WebApiConfig.cs:27-31` |
| WebAPILogHandler | 요청/응답/상태/지연시간/IP/Origin 등을 `FinUp.Core.Log.Logger.Instance.Insert`로 기록 | `App_Start/WebApiConfig.cs:33; Handler/WebAPILogHandler.cs:21-150` |
| IncludeErrorDetailPolicy | 상세 오류를 항상 반환하도록 설정하고 handler에서 로그 후 응답을 필터링하려는 구조 | `App_Start/WebApiConfig.cs:35-36; Handler/WebAPILogHandler.cs:88-101` |

## 3. URL 엔드포인트별 역할

| # | 영역 | HTTP | URL | 액션 | 역할 | 근거 |
|---:|---|---|---|---|---|---|
| 1 | Chart | GET | `api/chart/capture` | `Capture(cidx, stockCode, height, width=600)` | 종목 차트 캡처 요청을 로컬 소켓 8278로 전달하고 캡처 결과 문자열을 반환 | `Controllers/ChartController.cs:32-67` |
| 2 | Chart | GET | `api/chart/capture` | `Capture(date)` | 일자 기준 차트 캡처 요청을 로컬 소켓 8279로 전달 | `Controllers/ChartController.cs:69-104` |
| 3 | Chart | GET | `api/chart/capture/theme` | `CaptureTheme(keyword, keywordIdx)` | 테마 차트 캡처 요청을 로컬 소켓 8280으로 전달 | `Controllers/ChartController.cs:106-141` |
| 4 | Chart | GET | `api/chart/stockDeposit` | `StockDepositTrend()` | 주식 예탁금 추이 차트 데이터 조회 | `Controllers/ChartController.cs:143-151` |
| 5 | Chart | GET | `api/chart/themeday` | `ThemeDay(keywordIdx)` | 테마 일자별 집계 차트 데이터 조회 | `Controllers/ChartController.cs:153-160` |
| 6 | Chart | GET | `api/chart/lw/theme` | `GetThemeChartAsync(keywordIdx)` | Lightweight Charts용 테마 캔들/이동평균 데이터 조회 | `Controllers/ChartController.cs:163-234` |
| 7 | Chart | GET | `api/v2/chart/lw/theme` | `GetThemeChartAsync_v2(keywordIdx)` | v2 테마 차트: 당일 포함 집계와 관련 종목 거래대금 볼륨 정보 추가 | `Controllers/ChartController.cs:236-284` |
| 8 | Check | GET | `api/check/health` | `HealthCheck()` | StockData DB 연결 문자열을 복호화해 간단한 SQL 조회로 상태 확인; 성공 시 1000, 실패 시 9999 | `Controllers/CheckController.cs:16-31` |
| 9 | Data | GET | `api/data/hoga/last/{code}/{day}/{time}/{count}` | `GetLastHoga` | 지정 시각 이전/기준 최근 호가 N건 조회 | `Controllers/DataController.cs:29-39` |
| 10 | Data | GET | `api/data/trader/last/{code}/{day}/{time}/{count}` | `GetLastTrader` | 지정 시각 이전/기준 최근 거래원 N건 조회 | `Controllers/DataController.cs:49-60` |
| 11 | Data | GET | `api/data/price/last/{code}/{day}/{time}/{count}` | `GetLastPrice` | 지정 시각 이전/기준 최근 체결가 N건 조회 | `Controllers/DataController.cs:71-80` |
| 12 | Data | GET | `api/data/hoga/{code}/{day}/{start}/{end}` | `GetHoga` | 특정 일자·구간 호가 목록 조회 | `Controllers/DataController.cs:84-95` |
| 13 | Data | GET | `api/data/currenthoga/{code}` | `GetCurrentHoga` | 종목 현재 호가 조회 | `Controllers/DataController.cs:98-109` |
| 14 | Data | GET | `api/data/price/{code}/{day}/{start}/{end}` | `GetPrice` | 특정 일자·구간 체결가 목록 조회 | `Controllers/DataController.cs:112-123` |
| 15 | Data | GET | `api/data/trader/{code}/{day}/{start}/{end}` | `GetTrader` | 특정 일자·구간 거래원 목록 조회 | `Controllers/DataController.cs:126-137` |
| 16 | Data | GET | `api/data/traderlast/{code}/{day}/{end}` | `GetTraderLast` | 특정 종료 시각 기준 최근 거래원 데이터 조회 | `Controllers/DataController.cs:140-151` |
| 17 | Data | GET | `api/data/currenttrader/{code}` | `GetCurrentTrader` | 종목 현재 거래원 데이터 조회 | `Controllers/DataController.cs:154-165` |
| 18 | Data | GET | `api/data/traderday/{code}/{startday}/{endday}` | `GetTraderDay` | 종목별 일자 범위 거래원 집계 조회 | `Controllers/DataController.cs:168-179` |
| 19 | Data | GET | `api/data/stock/{code}` | `GetStockDetailAsync` | 종목 기본/상세 정보 조회 | `Controllers/DataController.cs:182-193` |
| 20 | Data | GET | `api/data/financial/{code}/{pageNo?}/{pageSize?}/{isQuarter?}` | `GetFinancialDetail` | 종목 재무 데이터 페이징 조회; 분기 여부 옵션 지원 | `Controllers/DataController.cs:196-211` |
| 21 | Data | GET | `api/data/vi/{code}/{date}` | `GetStockVIs` | 지정일 종목 VI(변동성 완화장치) 이력 조회 | `Controllers/DataController.cs:214-238` |
| 22 | Data | GET | `api/data/marketopen/{isRealTime}` | `IsTodayMarketOpen` | 금일 장 개장 여부 조회 | `Controllers/DataController.cs:241-249` |
| 23 | Index | GET | `api/index/last` | `GetIndexLast(codes)` | 지수 코드 배열의 최신 지수 데이터 조회 | `Controllers/IndexController.cs:16-22` |
| 24 | Keyword | GET | `api/keyword/news` | `GetKeywordNewsAsync` | 키워드/타입 조건별 뉴스 목록 조회 | `Controllers/KeywordController.cs:33-55` |
| 25 | Keyword | GET | `api/stock/calendar` | `GetStockOpenDateAsync` | 거래일/휴장일 캘린더 조회 | `Controllers/KeywordController.cs:58-80` |
| 26 | Keyword | GET | `api/keyword/stock/industry/{industryidx}/{stockcode}` | `GetIndustryRelationStockAsync` | 업종과 종목의 관련 종목 목록 조회 | `Controllers/KeywordController.cs:83-106` |
| 27 | Keyword | GET | `api/keyword/{keywordidx}` | `GetKeywordDetailPrice` | 키워드/테마 상세 가격 정보 조회 | `Controllers/KeywordController.cs:109-132` |
| 28 | Keyword | GET | `api/keyword/theme/similarity/{keywordidx}` | `GetKeywordSimilarityTheme` | 유사 테마/키워드 목록 조회 | `Controllers/KeywordController.cs:135-158` |
| 29 | Keyword | GET | `api/keyword/stock/golden-signal-form/{stockCode}` | `GetGoldenSignalStockData` | 종목의 골든시그널 화면 구성 데이터(테마/업종/뉴스)를 조회 | `Controllers/KeywordController.cs:161-183` |
| 30 | Keyword | GET | `api/keyword/stock/holder/{stockCode}` | `GetStockHolder` | 종목 주주/보유자 관련 정보 조회 | `Controllers/KeywordController.cs:187-209` |
| 31 | Keyword | GET | `api/keyword/stock/ranking/{type}` | `GetStockRanking` | 타입별 종목 랭킹 조회 | `Controllers/KeywordController.cs:212-233` |
| 32 | Keyword | GET | `api/keyword/stock/theme/{stockCode}` | `GetStockRelationTheme` | 종목 관련 테마 목록 조회 | `Controllers/KeywordController.cs:236-257` |
| 33 | Keyword | GET | `api/keyword/stock/industry/stock/{stockCode}` | `GetStockRelationIndustry` | 종목 관련 업종 목록 조회 | `Controllers/KeywordController.cs:260-281` |
| 34 | Keyword | GET | `api/keyword/theme/diff/{keywordidx}` | `GetThemeDiff` | 테마의 기간별 차이/변동 데이터 조회; 기본은 전일~금일 | `Controllers/KeywordController.cs:285-337` |
| 35 | Keyword | GET | `api/keyword/theme/stock/{keywordidx}` | `GetThemeRelationStock` | 테마에 속한 관련 종목 조회 | `Controllers/KeywordController.cs:340-361` |
| 36 | Keyword | POST | `api/keyword/news/summary-search` | `GetThemeNewsSummarySearch` | 테마 뉴스 요약/검색 결과 조회 | `Controllers/KeywordController.cs:364-390` |
| 37 | NewsContents | GET | `api/news-contents/board` | `UploadNewsContentsBoard(date)` | 뉴스 콘텐츠 HTML 본문을 조회해 text/html로 반환 | `Controllers/NewsContentsController.cs:34-53` |
| 38 | News | POST | `api/news/NewsListPage` | `NewsListPage` | 키워드/종목 조건 뉴스 페이지 조회 | `Controllers/NewsController.cs:23-30` |
| 39 | News | POST | `api/news/theme` | `NewsListPageTheme` | 테마 기준 뉴스 페이지 조회 | `Controllers/NewsController.cs:33-39` |
| 40 | News | POST | `api/news/stock` | `NewsListPageStock` | 종목 기준 뉴스 페이지 조회 | `Controllers/NewsController.cs:42-48` |
| 41 | Price | GET | `api/price/{code}` | `GetPrice` | 단일 종목 현재가 조회(Redis) | `Controllers/PriceController.cs:36-52` |
| 42 | Price | POST | `api/pricelist` | `GetPriceList` | 복수 종목 현재가 일괄 조회 | `Controllers/PriceController.cs:55-73` |
| 43 | Price | POST | `api/price/diff` | `GetPriceDiffList` | 복수 종목 현재가와 등락률 데이터 조회 | `Controllers/PriceController.cs:76-119` |
| 44 | Price | GET | `api/profit` | `GetItemStockProfit` | Stockpoint Admin 진행 종목/수익 관련 데이터 조회 | `Controllers/PriceController.cs:122-136` |
| 45 | Price | GET | `api/chart/nvd3/{code}` | `GetNvd3Chart` | NVD3용 1분봉 차트 데이터 조회 | `Controllers/PriceController.cs:139-152` |
| 46 | Price | GET | `api/chart/nvd3/minutes/{code}/{minutes}` | `GetCandleAllChart` | NVD3용 N분봉 차트 데이터 조회 | `Controllers/PriceController.cs:155-168` |
| 47 | Price | GET | `api/price/highlow/{code}/{from}` | `GetHighLow` | 시작 시각 이후 단일 종목 고가/저가 조회 | `Controllers/PriceController.cs:171-206` |
| 48 | Price | GET | `api/price/highlowvalue/{code}/{from}` | `GetHighLowValue` | 시작 시각 이후 단일 종목 고가/저가/거래량/거래대금 조회 | `Controllers/PriceController.cs:209-245` |
| 49 | Price | POST | `api/price/highlowlist` | `GetHighLowList` | 복수 종목 고가/저가/거래량/거래대금 일괄 조회; 응답 gzip 필터 적용 | `Controllers/PriceController.cs:248-325` |
| 50 | Price | GET | `api/market/{from}/{to}/{offday?}` | `GetMarket` | 기간별 장 운영 캘린더 조회 | `Controllers/PriceController.cs:328-352` |
| 51 | Price | GET | `api/prevday/{date}/{code}` | `GetPrevDay` | 요청일 이전 마지막 영업일의 일봉 조회 | `Controllers/PriceController.cs:355-377` |
| 52 | Price | GET | `api/priceliststock/{code}` | `GetPriceListStock` | 체결 목록 조회; 장중은 Redis, 장외는 Mongo 백업 사용 | `Controllers/PriceController.cs:380-413` |
| 53 | Price | GET | `api/dayprice/{code}/{from}/{to}` | `GetDayPrice(range)` | 기간 일봉 조회 | `Controllers/PriceController.cs:416-433` |
| 54 | Price | GET | `api/dayprice/paging/{code}/{pageNo?}/{pageSize?}` | `GetDayPrice(paging)` | 일봉 페이징 조회와 수정주가 반영 | `Controllers/PriceController.cs:436-474` |
| 55 | Price | GET | `api/price/tradesummary/{code}/{from}/{to}` | `GetPriceSummary` | 기간별 체결 요약 조회 | `Controllers/PriceController.cs:497-504` |
| 56 | Price | GET | `api/price/minutes/{code}/{from}/{to}` | `GetMinutes` | 기간별 분봉 조회; 과거는 Mongo, 금일은 Redis 조합, 31일 이상은 빈 결과 | `Controllers/PriceController.cs:507-542` |
| 57 | Price | GET | `api/price/limitprice/{code}` | `GetLimitPrice` | 종목 상한가/하한가 조회 | `Controllers/PriceController.cs:545-556` |
| 58 | Price | GET | `api/price/quote/{code}` | `GetQuoteAsync` | 종목 시세 quote(현재가, 등락, 고저시가, 거래량/대금, 전일종가) 조회 | `Controllers/PriceController.cs:559-585` |
| 59 | Price | POST | `api/price/search-history` | `GetSearchHistoryPrice` | 검색 이력에 포함된 종목/테마 가격을 묶어 조회 | `Controllers/PriceController.cs:588-604` |
| 60 | PriceMonitor | GET | `api/pricemonitor/stock/set` | `SetStock` | 체결감시 기준 종목 캐시 구성/갱신 | `Controllers/PriceMonitorController.cs:16-27` |
| 61 | PriceMonitor | GET | `api/pricemonitor/stock` | `GetStock` | 체결감시 기준 종목 목록 조회 | `Controllers/PriceMonitorController.cs:30-45` |
| 62 | PriceMonitor | POST | `api/pricemonitor/rank` | `GetPriceMonitorRank` | 체결감시 상위 랭킹 조회; 장전 DB/장중 Redis 분기 | `Controllers/PriceMonitorController.cs:48-77` |
| 63 | PriceMonitor | POST | `api/pricemonitor/stock` | `GetPriceMonitorStockPaging` | 특정 종목의 체결감시 페이징 조회 | `Controllers/PriceMonitorController.cs:104-127` |
| 64 | PriceMonitor | POST | `api/pricemonitor/paging` | `GetPriceMonitorPaging` | 체결감시 전체 페이징 조회 | `Controllers/PriceMonitorController.cs:130-155` |
| 65 | PriceMonitor | POST | `api/pricemonitor/list/paging` | `GetPriceMonitorListPaging` | 체결감시 목록 페이징 결과 조회 | `Controllers/PriceMonitorController.cs:158-180` |
| 66 | PriceMonitor | POST | `api/pricemonitor/chart/price` | `GetStockPriceChart` | 체결감시 주가 차트 데이터 조회; 장전 Mongo, 장중 Redis 분기 | `Controllers/PriceMonitorController.cs:184-243` |
| 67 | PriceMonitor | POST | `api/pricemonitor/chart/count` | `GetStockCountChart` | 체결감시 누적 빈도 차트 데이터 조회 | `Controllers/PriceMonitorController.cs:246-271` |
| 68 | PriceMonitor | GET | `api/pricemonitor/preopen` | `IsPreMarketOpen` | 현재가 장전/장중 데이터 소스 선택 기준 확인 | `Controllers/PriceMonitorController.cs:275-315` |
| 69 | RadarAlarm | GET | `api/alarm/alarm-list` | `GetServiceList()` | 뉴스 알람 서비스 목록 조회 | `Controllers/RadarAlarmController.cs:27-49` |
| 70 | RadarAlarm | GET | `api/news/news_market_issue/{type}` | `GetServiceList(type)` | 시장 이슈 뉴스 알람 이력 조회 | `Controllers/RadarAlarmController.cs:53-69` |
| 71 | RadarAlarm | GET | `api/alarm/alarm-history-issue-theme` | `GetIssueThemeList` | 이슈 테마 알람 이력 조회 | `Controllers/RadarAlarmController.cs:75-91` |
| 72 | RadarAlarm | GET | `api/alarm/alarm-history-stock-signal/{type}` | `GetStockSignalList` | 종목 신호 알람 이력 조회 | `Controllers/RadarAlarmController.cs:97-113` |
| 73 | ThemeLog | POST | `api/ThemeCaptureChart` | `GetThemeCaptureChart` | 테마 캡처 차트 전체/기본 목록 조회 | `Controllers/ThemeLogController.cs:26-33` |
| 74 | ThemeLog | POST | `api/ThemeRelationStock` | `GetThemeRelationStock` | 테마 관련 종목 조회 | `Controllers/ThemeLogController.cs:38-45` |
| 75 | ThemeLog | GET | `api/ThemeLog/ThemeRankingByDiff` | `GetThemeRankingByDiff` | 변동폭 기준 테마 랭킹 조회 | `Controllers/ThemeLogController.cs:50-57` |
| 76 | ThemeLog | POST | `api/ThemeLog/Diff` | `GetThemeDiffList` | 테마 변동 목록 조회 | `Controllers/ThemeLogController.cs:67-73` |
| 77 | ThemeLog | POST | `api/ThemeLog/play/info` | `GetThemePlayInfo` | 테마 재생/타임라인 정보 조회 | `Controllers/ThemeLogController.cs:78-84` |
| 78 | ThemeLog | POST | `api/ThemeLog/play` | `GetThemePlay` | 테마 재생 구간별 차트 데이터 조회 | `Controllers/ThemeLogController.cs:89-95` |
| 79 | ThemeLog | POST | `api/themelog` | `GetThemeLog` | captureIdx 기준 테마 로그 조회 | `Controllers/ThemeLogController.cs:107-112` |
| 80 | ThemeLog | GET | `api/themelog/keyword/rank` | `GetThemelogKeywordRank` | 테마로그 키워드 랭킹 조회 | `Controllers/ThemeLogController.cs:123-128` |
| 81 | ThemeLog | POST | `api/themelog/keyword/relation-stocks` | `GetThemeLogRelationStocks` | 테마로그 키워드 관련 종목 조회 | `Controllers/ThemeLogController.cs:139-144` |
| 82 | ThemeLog | POST | `api/themelog/keyword/Diff` | `GetThemelogKeywordDiffList` | 테마로그 키워드 변동 목록 조회 | `Controllers/ThemeLogController.cs:155-160` |
| 83 | TradingView | GET | `api/tv/config` | `GetConfig` | TradingView UDF config 반환(거래소/지원 resolution/symbol type) | `Controllers/TradingViewController.cs:18-38` |
| 84 | TradingView | GET | `api/tv/symbol_info` | `GetSymbolInfo` | 기본 심볼 메타데이터 반환 | `Controllers/TradingViewController.cs:42-50` |
| 85 | TradingView | GET | `api/tv/symbols` | `GetSymbols` | 종목코드로 TradingView 심볼 상세 조회 | `Controllers/TradingViewController.cs:54-93` |
| 86 | TradingView | GET | `api/tv/time` | `GetTime` | 현재 UTC Unix time 반환 | `Controllers/TradingViewController.cs:102-106` |
| 87 | TradingView | GET | `api/tv/marks` | `GetMarks` | TradingView 차트 이벤트/수정주가 mark 데이터 조회 | `Controllers/TradingViewController.cs:110-148` |
| 88 | TradingView | GET | `api/v2/tv/marks` | `GetMarks` | v2 TradingView mark 호환 경로 | `Controllers/TradingViewController.cs:110-148` |
| 89 | TradingView | GET | `api/v3/tv/marks` | `GetMarks` | v3 TradingView mark 호환 경로 | `Controllers/TradingViewController.cs:110-148` |
| 90 | TradingView | GET | `api/tv/history` | `GetHistory` | TradingView v1 OHLCV history 조회; Redis/Mongo 또는 SQL 경로 사용 | `Controllers/TradingViewController.cs:152-183` |
| 91 | TradingView | GET | `api/v2/tv/history` | `GetHistoryV2` | TradingView v2 history 조회; countback 옵션 지원 | `Controllers/TradingViewController.cs:194-224` |
| 92 | TradingView | GET | `api/v3/tv/history` | `GetHistoryV3` | TradingView v3 history 조회; 비동기 Redis/Mongo 조회 경로 | `Controllers/TradingViewController.cs:236-266` |
| 93 | TradingViewTicker | GET | `api/v2/tv/ticker/history` | `GetHistoryV2` | 업종/티커용 TradingView v2 history 조회 | `Controllers/TradingViewTickerController.cs:29-53` |

## 4. Web.config 설정값 역할 분석

보안상 내부 IP/호스트, 암호화된 연결 문자열 원문은 표에 반복 기재하지 않았다. 값의 존재와 역할은 `Web.config` 라인 기준으로 확인했다.

| 설정 | 역할 | 분석 | 근거 |
|---|---|---|---|
| `configSections/finup` | FinUp.Core.Redis 전용 사용자 정의 설정 섹션 등록 | FinUp.Core.Redis.Configuration.FinUp 타입으로 <finup> 섹션을 해석 | `Web.config:3-5` |
| `finup.redis.clusters.cluster name="chat"` | Redis 클러스터 정의 | 채팅이라는 이름이지만 Redis 기반 가격/감시 Biz가 참조할 수 있는 공통 Redis 클러스터 설정 | `Web.config:6-21` |
| `redis options allowAdmin` | Redis 관리자 명령 허용 여부 | true라서 관리 명령이 필요한 라이브러리 동작을 허용 | `Web.config:9-10` |
| `redis options abortConnect` | 초기 연결 실패 시 중단 여부 | false라서 시작 시 Redis 연결 실패가 있어도 재시도를 허용 | `Web.config:10` |
| `redis options connectTimeout/connectRetry/syncTimeout/keepAlive` | Redis 연결/재시도/동기 타임아웃/keepalive 제어 | 연결 안정성 및 대기 시간을 조정 | `Web.config:10` |
| `redis options databases` | Redis DB 인덱스 범위 | 0-10 범위를 사용 대상으로 선언 | `Web.config:10` |
| `redis host default` | Redis 기본 호스트 | 읽기전용이 아닌 기본 Redis endpoint. 보고서에는 보안상 endpoint 전체를 재기재하지 않음 | `Web.config:15` |
| `MongoDB` | 주요 MongoDB 연결 문자열 | Data/Index/Price/Constants에서 체결·호가·분봉·일봉 등 운영 데이터 조회에 사용 | `Web.config:24; Controllers/DataController.cs:19; Controllers/PriceController.cs:27` |
| `MongoDBLab` | Lab/분석 MongoDB 연결 문자열 | Chart/ThemeLog/Keyword 서비스가 테마·뉴스·집계성 데이터 조회에 사용 | `Web.config:25; Controllers/ChartController.cs:23; Controllers/ThemeLogController.cs:21` |
| `MongoDBLabAggregate` | 집계 전용 MongoDB 연결 문자열 | Chart와 KeywordNewsService의 집계 조회에 사용. ChartController는 없으면 MongoDBLab으로 대체 | `Web.config:26; Controllers/ChartController.cs:24-29; Services/KeywordNewsService.cs:15-16` |
| `StockData` | 암호화된 SQL/StockData 연결 문자열 | HealthCheck에서 DecAES()로 복호화 후 DBUtil 조회 수행 | `Web.config:35; Controllers/CheckController.cs:19-31` |
| `KafkaUrl` | 로그/이벤트 Kafka bootstrap 주소 | 로컬 코드 직접 참조는 없지만 FinUp.Core.Log 프로젝트 참조 및 WebAPILogHandler의 Logger.Insert 호출과 함께 로그 통신 설정으로 추정 | `Web.config:42; Handler/WebAPILogHandler.cs:143-150` |
| `UseLog` | 로그 활성화 플래그 | 로컬 직접 참조는 없고 외부 FinUp.Core.Log가 읽는 설정으로 추정 | `Web.config:43; FinUp.StockData.Price.Api.csproj:663-665` |
| `System` | 로그 시스템명 | 로그에 기록될 시스템 식별자. 값은 StockData.Api | `Web.config:44` |
| `SystemType` | 로그 시스템 유형 | API 유형 서비스임을 나타내는 로그 메타데이터 | `Web.config:45` |
| `LogThreshold` | 로그 임계값 | 외부 로깅 라이브러리의 수집/필터링 기준으로 추정 | `Web.config:46` |
| `LogCaseType` | 로그 수집 케이스 유형 | Collected로 설정되어 수집형 로그 정책을 나타냄 | `Web.config:47` |
| `LogCommunication` | 로그 전송 방식 | kafka로 설정되어 Kafka 기반 로그 전송을 지시 | `Web.config:48` |
| `Compression` | 압축 사용 플래그 | 로컬 직접 참조는 없음. 외부 라이브러리 또는 운영 로그/통신 압축 설정으로 추정 | `Web.config:49` |
| `CompressionType` | 압축 방식 플래그 | 로컬 직접 참조는 없음. 1이 특정 압축 타입을 의미하는 내부 규약으로 추정 | `Web.config:50` |
| `StockDataRealtimeUrl` | 실시간 StockData API base URL | StockDataRealtimeApiService가 금일 분봉 데이터를 외부 API에서 가져올 때 base URL로 사용 | `Web.config:51; Services/StockDataRealtimeApiService.cs:19-35` |
| `StockDataRealtimeMinuteUrlPath` | 실시간 분봉 API path | {base}{path}/{code} 형식의 금일 분봉 요청 경로 | `Web.config:52; Services/StockDataRealtimeApiService.cs:19-35` |
| `system.diagnostics trace listener` | Trace 출력 파일 대상 | FinUp.Core.Diagnostics.TextFileTraceListener가 C:\trace\api\stockdata.log에 Trace를 기록 | `Web.config:54-60` |
| `system.web compilation/debug` | ASP.NET 컴파일 설정 | targetFramework 4.7, debug=true. 운영이라면 상세 디버그 정보 노출/성능 영향 검토 필요 | `Web.config:69-72` |
| `httpRuntime targetFramework` | ASP.NET 런타임 호환성 대상 | 4.7 런타임 동작을 지정 | `Web.config:71` |
| `runtime assemblyBinding` | 어셈블리 바인딩 리다이렉트 | System.Web.Http, Newtonsoft.Json, Mongo/Redis 의존 System.* 계열 버전 충돌을 지정 버전으로 통일 | `Web.config:73-128` |
| `system.codedom compilers` | 런타임 C#/VB 컴파일러 | Razor/동적 컴파일 시 Microsoft.CodeDom provider와 언어 버전 지정 | `Web.config:129-134` |
| `system.webServer handlers` | IIS handler 설정 | ExtensionlessUrlHandler 재등록, OPTIONS/TRACE 기본 handler 제거로 ASP.NET Web API extensionless URL 처리를 보장 | `Web.config:135-142` |

## 5. 데이터 흐름 관찰

- **Redis 실시간/캐시 경로**: 현재가, 고저가, 체결감시, 장중 분봉 등은 `Biz.Redis.*` 또는 mapper가 Redis에서 조회한다. 예: `api/price/{code}`, `api/price/highlowlist`, `api/pricemonitor/*`.
- **MongoDB 이력/집계 경로**: 호가/거래원/체결 이력, 분봉 과거 데이터, 테마 차트/테마로그는 `Biz.MongoDB.*`를 사용한다.
- **SQL/Biz 경로**: 종목 상세, 재무, 캘린더, 뉴스 목록, 예탁금 추이 등은 `FinUp.StockData.Biz` 계층을 통해 조회한다.
- **TradingView 호환 경로**: `/api/tv/*`, `/api/v2/tv/*`, `/api/v3/tv/*`는 TradingView UDF 스타일의 config/symbol/history/marks 응답을 제공한다.
- **외부 실시간 API 경로**: `StockDataRealtimeApiService`는 `StockDataRealtimeUrl` + `StockDataRealtimeMinuteUrlPath` 조합으로 금일 분봉 데이터를 가져오는 보조 경로를 가진다.

## 6. 주의/한계

- 이 보고서는 코드 정적 분석 기준이다. 실제 배포 URL, IIS 사이트 바인딩, 인증/방화벽, 외부 DLL 내부 동작은 실행 환경 없이는 확정할 수 없다.
- `KafkaUrl`, `UseLog`, `Compression` 등 일부 appSettings는 이 프로젝트 C# 파일에서 직접 참조되지 않는다. 다만 `FinUp.Core.Log`/`FinUp.Core.Redis` 프로젝트 참조와 logger 호출이 있어 외부 공통 라이브러리 설정으로 보는 것이 가장 강하게 지지된다.
- `Web.config`의 `debug="true"`, `IncludeErrorDetailPolicy.Always`, 내부 endpoint/연결 문자열은 운영 보안 관점에서 별도 검토 대상이다.

## 7. 검증 내역

- 컨트롤러 `[Route]` 어트리뷰트 파싱 결과: 93개 라우트 항목 확인.
- 주요 파일 확인: `App_Start/WebApiConfig.cs`, `Global.asax.cs`, `Controllers/*.cs`, `Handler/*.cs`, `Filter/*.cs`, `Services/StockDataRealtimeApiService.cs`, `Web.config`, `FinUp.StockData.Price.Api.csproj`.
- 산출물 생성 위치: `/mnt/c/reports/FinUp.StockData.Price.Api`.
