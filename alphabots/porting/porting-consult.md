# AlphaBot Java 포팅 컨설팅 리포트

> 작성일: 2026-05-15  
> 대상 위치: `/mnt/c/reports/alphabots/porting`  
> 디자인: Starbucks-inspired XLarge report (`/home/kmyoon/.codex/skills/codex-design/starbucks/DESIGN.md`)  
> 주의: 소스코드는 수정하지 않았고, 민감정보 값은 출력하지 않았다.

## 1. Executive Summary

현재 AlphaBot 계열은 **WPF/WinExe shell + DB 기반 Operation/OperationTerm 스케줄 + Thread 실행 + DB history/log 기록** 구조다. Java/Linux로 포팅할 때는 WPF를 그대로 옮기는 것이 아니라, **headless CLI/worker + 중앙 스케줄러 + 구조화 로그 + operation_run 상태 저장소**로 재설계하는 것이 맞다.

권장 결론:

1. **Java 25 LTS + Spring Boot/Spring Batch/picocli 기반 CLI worker**를 표준으로 둔다.
2. 기존 `OIdx/OTIdx/OperationTerm` DB 스케줄은 1차 포팅에서 유지하되, Java enum registry와 `operation_run` 테이블로 실행 상태를 표준화한다.
3. Linux 운영은 초기에는 **Docker + systemd/ECS scheduled task**, 운영 표준화 단계에서는 **Kubernetes Job/CronJob** 또는 **ECS/Fargate Scheduled Task**가 적합하다.
4. 로그는 S3 직접 appender보다 **stdout JSON → 수집기 → CloudWatch/OpenSearch/Loki + S3 장기보관**이 안전하다.
5. 가장 먼저 포팅할 후보는 **Finance Biz(작업 3개, 의존성 작음)**, 다음은 **CollectData Biz**, 이후 **Radar/Stock 대형 모듈 분해** 순서가 합리적이다.

## 2. 대상 프로젝트 인벤토리

| Target | Role | Framework | Output | WPF/Windows | CS files | Timer refs | Thread refs | Empty catch |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| FinUp.CollectData.App.AlphaBot | WPF shell: AlphaBot scheduler/control surface for collect-data jobs | net6.0-windows7.0 | WinExe | Y | 7 | 4 | 2 | 3 |
| FinUp.CollectData.App.AlphaBot.Biz | Business/job library: crawlers, market index, news/site crawling, Mongo cleanup | net6.0 | - | - | 54 | 0 | 6 | 13 |
| FinUp.Finance.App.Alphabot | WPF shell: Finance AlphaBot scheduler/control surface | net6.0-windows | WinExe | Y | 5 | 4 | 2 | 3 |
| FinUp.Finance.App.Alphabot.Biz | Business/job library: ranking, investment RSS, stock schedule/file upload jobs | net6.0 | - | - | 28 | 0 | 6 | 8 |
| FinUp.Radar.App.AlphaBot | WPF-style .NET Framework monolith: radar/theme/news/push/payment/receipt/cache jobs | v4.7 | WinExe | Y | 85 | 8 | 8 | 23 |
| FinUp.Stock.App.AlphaBot | WPF-style .NET Framework monolith: stockpoint/finance notifications, AWS monitoring, app push, SMS/payment, data sync jobs | v4.7 | WinExe | Y | 30 | 6 | 15 | 15 |

### 경로/이름 주의

- 요청명 `FinUp.CollectData.App.AlphaBot.Biz`는 repo root 독립 폴더가 아니라 `FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot.Biz`에 있다.
- 요청명 `FinUp.Finance.App.Alphabot.Biz`도 `FinUp.Finance.App.AlphaBot/FinUp.Finance.App.Alphabot.Biz`에 있다. `AlphaBot/Alphabot` 대소문자 혼재가 있어 Linux 포팅 시 namespace/path 정책을 통일해야 한다.

## 3. 현재 공통 실행 아키텍처

```text
WPF App / MainWindow or MainViewModel
  ├─ App.config / transform config 로 DB, API, token, interval 로드
  ├─ Operation/OperationTerm DB 조회
  ├─ OIdx → method delegate 매핑
  ├─ DispatcherTimer observe/confirm tick
  ├─ Thread(ProcessStart) 실행
  ├─ RunTask / actionOperation 수행
  └─ OperationTermHistory / UI log / file log / telegram 등으로 결과 기록
```

공통적으로 `LastExecDT`, `LoopInterval`, `OnceTime`, `LoopStartTime`, `LoopEndTime`, `StockOpen`, `OffDay`, `ManualExec` 같은 DB 스케줄 값에 의존한다. 따라서 Java 포팅 시 cron 식만으로는 부족하고, **DB schedule evaluator**를 별도 컴포넌트로 만들어야 한다.

## 4. 프로젝트별 분석


### FinUp.CollectData.App.AlphaBot

- **역할**: WPF shell: AlphaBot scheduler/control surface for collect-data jobs
- **현재 기술**: framework=`net6.0-windows7.0`, output=`WinExe`, WPF/Windows surface=`yes`
- **핵심 실행 흐름**: WPF App → MainViewModel.InitializeMember → AlphaBotBiz.GetOperationModel → DispatcherTimer(tMainTimer/tObserveTimer) → AlphaBotBiz.StartConfirmProcess → Thread(ProcessStart). Evidence: ViewModel/MainViewModel.cs:27-63, 76-99, 135-170.
- **프로젝트 참조**: ..\..\FinUp.Core.DS.App\FinUp.Core.DS.App\FinUp.Core.DS.App.csproj; ..\FinUp.CollectData.App.AlphaBot.Biz\FinUp.CollectData.App.AlphaBot.Biz.csproj
- **패키지/외부 라이브러리**: -
- **DB/설정**: config keys `AlphaBot.ObServeTime, ChatIdCoin, ChatIdGameFocus, ChatIdHts, ChatIdHtsIncludeFilter, ChatIdHtsNoFilter, ChatIdHtsTestFilter, ChatIdKoreaBreifing, ChatIdMinjoo, ChatIdPartners, ChatIdSpecialStock, CoinAlarmEndTime, CoinAlarmStartTime, CoinCrawlEndTime, CoinCrawlStartTime, CrawlIntervalSecCoinOne, CrawlIntervalSecUpbit, CrawlerSiteCheckChannel, GameFocusAlarmEndTime, GameFocusAlarmStartTime`; connection names `ConnectionKafka, DBThemeRadar, DBThemeRadarReal, MongoConnection, MongoConnectionLog, MongoConnectionNews`. 실제 연결 문자열/비밀번호 값은 출력하지 않음.
- **외부 접근**: http://schemas.microsoft.com/expression/blend/2008, http://schemas.microsoft.com/winfx/2006/xaml, http://schemas.microsoft.com/winfx/2006/xaml/presentation, http://schemas.openxmlformats.org/markup-compatibility/2006, http://www.nlog-project.org/schemas/NLog.xsd, http://www.w3.org/2001/XMLSchema-instance, https://api.upbit.com/v1/ticker, https://finance.naver.com/marketindex/, https://finance.naver.com/marketindex/exchangeDetail.nhn, https://finance.naver.com/marketindex/worldExchangeDetail.naver
- **민감정보 위치(값 미출력)**: FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot/App.Debug.config, FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot/App.Release.config, FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot/App.Staging.config, FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot/Config/AppSetting.cs
- **포팅 판단**: UI는 제거하고 `FinUp.CollectData.App.AlphaBot` 단위가 아니라 **operation 단위 CLI/worker**로 쪼개는 것이 안전. 기존 OIdx 매핑은 Java enum/registry로 이전하고, OperationTerm DB 테이블은 1차 전환에서 유지 가능.
- **주요 리스크 지표**: cs files=7, SQL pattern=19, HTTP pattern=0, Thread=2, DispatcherTimer=4, empty catch=3, log pattern=17.

### FinUp.CollectData.App.AlphaBot.Biz

- **역할**: Business/job library: crawlers, market index, news/site crawling, Mongo cleanup
- **현재 기술**: framework=`net6.0`, output=`-`, WPF/Windows surface=`no`
- **핵심 실행 흐름**: DB OperationTerm(Data) 로드 → OIdx 30010~30070을 ProcCrawlerSite/Index/NaverStockRank/InfoStock/MongoClean 등으로 매핑 → RunTask가 START/ERROR/STOP history 기록. Evidence: AlphaBotBiz.cs:45-117, 219-337; AlphaBotBiz.Connect.cs:12-49.
- **프로젝트 참조**: ..\..\FinUp.Core.DS.Dac\FinUp.Core.DS.Dac\FinUp.Core.DS.Dac.csproj
- **패키지/외부 라이브러리**: CefSharp.OffScreen.NETCore 135.0.170, Microsoft.Bcl.AsyncInterfaces 8.0.0, NLog 4.7.11, WebDriverManager 2.17.5
- **DB/설정**: config keys `-`; connection names `-`. 실제 연결 문자열/비밀번호 값은 출력하지 않음.
- **외부 접근**: http://m.infostock.co.kr/sector/sector.asp, http://m.infostock.co.kr/sector/sector_detail.asp, http://medipana.com, http://search.yahoo.com/mrss/, http://www.epnc.co.kr, http://www.korea.kr, http://www.press9.kr, http://www.press9.kr/news/, http://www.sentv.co.kr, http://www.thebell.co.kr/free/content/
- **민감정보 위치(값 미출력)**: FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot.Biz/Config/AppSetting.cs, FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot.Biz/Operation/Unit/CrawlerInfoStock.cs, FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot.Biz/Operation/Unit/CrawlerSite.cs, FinUp.CollectData.App.AlphaBot/FinUp.CollectData.App.AlphaBot.Biz/Operation/Unit/MongoClean.cs
- **포팅 판단**: UI는 제거하고 `FinUp.CollectData.App.AlphaBot.Biz` 단위가 아니라 **operation 단위 CLI/worker**로 쪼개는 것이 안전. 기존 OIdx 매핑은 Java enum/registry로 이전하고, OperationTerm DB 테이블은 1차 전환에서 유지 가능.
- **주요 리스크 지표**: cs files=54, SQL pattern=77, HTTP pattern=17, Thread=6, DispatcherTimer=0, empty catch=13, log pattern=54.

### FinUp.Finance.App.Alphabot

- **역할**: WPF shell: Finance AlphaBot scheduler/control surface
- **현재 기술**: framework=`net6.0-windows`, output=`WinExe`, WPF/Windows surface=`yes`
- **핵심 실행 흐름**: WPF App shell → MainViewModel timers → Finance Biz AlphaBotBiz. App.config의 파일 경로/업로드 계정/DBStockData 설정 사용. Evidence: ViewModel/MainViewModel.cs, App.config.
- **프로젝트 참조**: ..\FinUp.Finance.App.Alphabot.Biz\FinUp.Finance.App.Alphabot.Biz.csproj
- **패키지/외부 라이브러리**: -
- **DB/설정**: config keys `AlphaBot.ObServeTime, FilePath, FilePathNormal, FilePathSub, FileUrl, FileUserID, FileUserPwd`; connection names `DBStockData`. 실제 연결 문자열/비밀번호 값은 출력하지 않음.
- **외부 접근**: http://schemas.microsoft.com/expression/blend/2008, http://schemas.microsoft.com/winfx/2006/xaml, http://schemas.microsoft.com/winfx/2006/xaml/presentation, http://schemas.openxmlformats.org/markup-compatibility/2006, https://pre-img.finup.co.kr/Finance/Contents/Editor
- **민감정보 위치(값 미출력)**: FinUp.Finance.App.AlphaBot/FinUp.Finance.App.Alphabot/App.config
- **포팅 판단**: UI는 제거하고 `FinUp.Finance.App.Alphabot` 단위가 아니라 **operation 단위 CLI/worker**로 쪼개는 것이 안전. 기존 OIdx 매핑은 Java enum/registry로 이전하고, OperationTerm DB 테이블은 1차 전환에서 유지 가능.
- **주요 리스크 지표**: cs files=5, SQL pattern=19, HTTP pattern=0, Thread=2, DispatcherTimer=4, empty catch=3, log pattern=2.

### FinUp.Finance.App.Alphabot.Biz

- **역할**: Business/job library: ranking, investment RSS, stock schedule/file upload jobs
- **현재 기술**: framework=`net6.0`, output=`-`, WPF/Windows surface=`no`
- **핵심 실행 흐름**: OperationTerm(Finance) 로드 → OIdx 40001 Ranking, 40002 InvestRss, 40003 StockSchedule → RunTask history 기록. Evidence: Alphabot.Biz/AlphaBotBiz.cs:293-353; AlaphaBotBiz.Connect.cs:17-35.
- **프로젝트 참조**: ..\..\FinUp.Core.NET.Data\FinUp.Core.NET.Data.csproj; ..\..\FinUp.Core.NET\FinUp.Core.NET.csproj
- **패키지/외부 라이브러리**: HtmlAgilityPack 1.11.43, SimpleImpersonation 4.2.0, System.Configuration.ConfigurationManager 5.0.0, System.ServiceModel.Syndication 6.0.0
- **DB/설정**: config keys `-`; connection names `-`. 실제 연결 문자열/비밀번호 값은 출력하지 않음.
- **외부 접근**: https://www.investnews.co.kr/rss/S1N1.xml, https://www.investnews.co.kr/rss/S1N4.xml
- **민감정보 위치(값 미출력)**: FinUp.Finance.App.AlphaBot/FinUp.Finance.App.Alphabot.Biz/Operation/Unit/InvestRss.cs, FinUp.Finance.App.AlphaBot/FinUp.Finance.App.Alphabot.Biz/Sql/Query/Extension.cs, FinUp.Finance.App.AlphaBot/FinUp.Finance.App.Alphabot.Biz/Sql/Query/Query.cs, FinUp.Finance.App.AlphaBot/FinUp.Finance.App.Alphabot.Biz/Sql/Query/Sql.cs, FinUp.Finance.App.AlphaBot/FinUp.Finance.App.Alphabot.Biz/Sql/Query/SqlBase.cs
- **포팅 판단**: UI는 제거하고 `FinUp.Finance.App.Alphabot.Biz` 단위가 아니라 **operation 단위 CLI/worker**로 쪼개는 것이 안전. 기존 OIdx 매핑은 Java enum/registry로 이전하고, OperationTerm DB 테이블은 1차 전환에서 유지 가능.
- **주요 리스크 지표**: cs files=28, SQL pattern=166, HTTP pattern=2, Thread=6, DispatcherTimer=0, empty catch=8, log pattern=5.

### FinUp.Radar.App.AlphaBot

- **역할**: WPF-style .NET Framework monolith: radar/theme/news/push/payment/receipt/cache jobs
- **현재 기술**: framework=`v4.7`, output=`WinExe`, WPF/Windows surface=`yes`
- **핵심 실행 흐름**: MainWindow.InitializeMember → Load()가 OperationTerm 로드 → DispatcherTimer 1초 observe + 주기 confirm → OIdx 10010~10530 다수 ProcessUnit 실행 → RunTask history 기록. Evidence: MainWindow.xaml.cs:60-190, 551-692, 699-725, 1001-1080.
- **프로젝트 참조**: ..\FinUp.Core.Data.MongoDB\FinUp.Core.Data.MongoDB.csproj; ..\FinUp.Core.Data\FinUp.Core.Data.csproj; ..\FinUp.Core.Log\FinUp.Core.Log.csproj; ..\FinUp.Core.Redis\FinUp.Core.Redis.csproj; ..\FinUp.Core\FinUp.Core.csproj; ..\FinUp.Radar\FinUp.Radar.csproj; ..\FinUp.StockData.Biz.Redis\FinUp.StockData.Biz.Redis.csproj; ..\FinUp.StockData.Fundamentals\FinUp.StockData.Fundamentals.csproj; ..\FinUp.StockData.Model\FinUp.StockData.Model.csproj
- **패키지/외부 라이브러리**: Crc32C.NET 1.0.5.0, DnsClient 1.3.2, Google.Apis 1.42.0, Google.Apis.AndroidPublisher.v3 1.42.0.1796, Google.Apis.Auth 1.42.0, Google.Apis.Core 1.42.0, Microsoft.Bcl.AsyncInterfaces 5.0.0, MongoDB.Bson 2.10.4, MongoDB.Driver 2.10.4, MongoDB.Driver.Core 2.10.4, MongoDB.Libmongocrypt 1.0.0, Newtonsoft.Json 12.0.1, Pipelines.Sockets.Unofficial 2.0.22, Selenium.WebDriver 4.10.0, SharpCompress 0.23.0, Snappy.NET 1.1.1.8, StackExchange.Redis 2.0.601, System.Buffers 4.5.1, System.Diagnostics.PerformanceCounter 4.5.0, System.IO.Pipelines 4.5.1
- **DB/설정**: config keys `ApiLogSender, ApiLogUrl, ApiRadarHealthCheck, ApiStockPriceAddress, AttentionNews, CacheWordFilter1, CacheWordFilter2, CountPrivate, CountPublic, DBThemeRadar, DBThemeRadarReal, IndustryCacheUrl, IndustryCacheUrl1, IndustryCacheUrl2, KafkaUrl, KeywordAnalysisDiff, LogCaseType, LogCommunication, LogThreshold, MongoConnection`; connection names `-`. 실제 연결 문자열/비밀번호 값은 출력하지 않음.
- **외부 접근**: http://apiradar01.finup.co.kr/Cache/WordFilter, http://apiradar01.finup.co.kr/cache/setcache, http://apiradar02.finup.co.kr/Cache/WordFilter, http://apiradar02.finup.co.kr/cache/setcache, http://apiradar02.finup.co.kr/cache/setcacheindustry, http://dart.fss.or.kr/api/todayRSS.xml, http://dart.fss.or.kr/dsaf001/main.do, http://localhost, http://pre-apiradar.finup.co.kr/cache/setcacheindustry, http://pre-apiradar01.finup.co.kr/cache/setcacheindustry
- **민감정보 위치(값 미출력)**: FinUp.Radar.App.AlphaBot/App.config, FinUp.Radar.App.AlphaBot/client_secrets.json, FinUp.Radar.App.AlphaBot/Operation/Payment/BillPhone.cs, FinUp.Radar.App.AlphaBot/Operation/Payment/FunctionPhone.cs, FinUp.Radar.App.AlphaBot/Operation/ProcessUnit/DisclosureApi.cs, FinUp.Radar.App.AlphaBot/Operation/ProcessUnit/ReceiptCheck.cs, FinUp.Radar.App.AlphaBot/Operation/ProcessUnit/ThemeLogAlarm.cs, FinUp.Radar.App.AlphaBot/Utils/ReceiptiOSVerification.cs
- **포팅 판단**: UI는 제거하고 `FinUp.Radar.App.AlphaBot` 단위가 아니라 **operation 단위 CLI/worker**로 쪼개는 것이 안전. 기존 OIdx 매핑은 Java enum/registry로 이전하고, OperationTerm DB 테이블은 1차 전환에서 유지 가능.
- **주요 리스크 지표**: cs files=85, SQL pattern=463, HTTP pattern=45, Thread=8, DispatcherTimer=8, empty catch=23, log pattern=64.

### FinUp.Stock.App.AlphaBot

- **역할**: WPF-style .NET Framework monolith: stockpoint/finance notifications, AWS monitoring, app push, SMS/payment, data sync jobs
- **현재 기술**: framework=`v4.7`, output=`WinExe`, WPF/Windows surface=`yes`
- **핵심 실행 흐름**: MainWindow.Load → timer confirm/observe/alive → OIdx 1~175/1000을 SMS/AppPush/AWSMonitoring/Email/Payment/Telegram 등으로 매핑 → ProcessStart에서 START/ERROR/END를 finally 기록. Evidence: MainWindow.xaml.cs:419-731.
- **프로젝트 참조**: ..\FinUp.Core.Fundamentals\FinUp.Core.Fundamentals.csproj; ..\FinUp.Stock.App\FinUp.Stock.App.csproj
- **패키지/외부 라이브러리**: AWSSDK.CloudWatch 3.3.104.3, AWSSDK.Core 3.3.104, AWSSDK.EC2 3.3.142, AWSSDK.RDS 3.3.114, FirebaseAdmin 3.0.0, Google.Api.Gax 4.8.0, Google.Api.Gax.Rest 4.8.0, Google.Apis 1.67.0, Google.Apis.Auth 1.67.0, Google.Apis.Core 1.67.0, Google.Apis.YouTube.v3 1.43.0.1834, HtmlAgilityPack 1.11.17, Microsoft.Bcl.AsyncInterfaces 6.0.0, Microsoft.Extensions.DependencyInjection.Abstractions 6.0.0, MoonAPNS 0.0.4.188, NLog 4.4.12, Newtonsoft.Json 13.0.3, System.Buffers 4.5.1, System.CodeDom 7.0.0, System.Collections.Immutable 8.0.0
- **DB/설정**: config keys `AWSAccessKey, AWSSecretKey, ApiDBStockPoint, ApiLogSender, ApiLogUrl, ChatApiEnable, ChatApiKey, ChatApiUrl, ChatCacheLoadUrl, DBMessageServiceDanal, DBMessageServiceLgu, DBStockPoint, FinUpImgUrl, FinUpStockUrl, MentorStockUrl, NaverApiClientId, NaverApiClientSecretId, NaverApiRedirectUrl, NaverCafeAttendBoardMenuId, NaverCafeId`; connection names `-`. 실제 연결 문자열/비밀번호 값은 출력하지 않음.
- **외부 접근**: http://admin.digging-stock.dunamu.com/v1/products, http://admin.digging-stock.dunamu.com/v1/products/purchased, http://api.stockpoint.co.kr/Api/App/LoadChatCacheCheck, http://biz.finup.co.kr/, http://chatapi01.finup.co.kr/api/check, http://chatapi02.finup.co.kr/api/check, http://devapi.stockpoint.co.kr/api/app/post/, http://finance.naver.com/item/main.nhn, http://fx.kebhana.com/fxportal/jsp/RS/DEPLOY_EXRATE/23678_0.html, http://leaguestock.finup.co.kr/
- **민감정보 위치(값 미출력)**: FinUp.Stock.App.AlphaBot/App.config, FinUp.Stock.App.AlphaBot/packages.config, FinUp.Stock.App.AlphaBot/Operation/Process.cs, FinUp.Stock.App.AlphaBot/Operation/ProcessBase.cs, FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs, FinUp.Stock.App.AlphaBot/Operation/Push.cs, FinUp.Stock.App.AlphaBot/Operation/ItemStockUpload/ItemStockUploadUtil.cs, FinUp.Stock.App.AlphaBot/Operation/Payment/BillPhone.cs
- **포팅 판단**: UI는 제거하고 `FinUp.Stock.App.AlphaBot` 단위가 아니라 **operation 단위 CLI/worker**로 쪼개는 것이 안전. 기존 OIdx 매핑은 Java enum/registry로 이전하고, OperationTerm DB 테이블은 1차 전환에서 유지 가능.
- **주요 리스크 지표**: cs files=30, SQL pattern=771, HTTP pattern=78, Thread=15, DispatcherTimer=6, empty catch=15, log pattern=586.


## 5. Windows 프로젝트일 필요성 판단

- **필요 없음**: 스케줄링, DB 조회/업데이트, REST 호출, Telegram/FCM, S3/CloudWatch, RSS/HTML 파싱, Mongo/Redis 작업은 Linux Java worker로 충분하다.
- **대체 필요**: WPF UI, `DispatcherTimer`, `MainWindow`, XAML, Windows path, `.exe` 실행/감시, `Interop.DANALCOMLib`, CefSharp OffScreen, 일부 인증서/로컬 파일 기반 push credential.
- **전환 방향**: UI 상태 표시는 CLI/관리 API/Grafana 대시보드로 대체한다. 결제/다날 COM은 vendor HTTP API 또는 Linux 지원 SDK 여부를 먼저 확인해야 한다.

## 6. CLI 포팅 설계


### 권장 CLI 명령 모델

```bash
alphabot list --domain collect|finance|radar|stock
alphabot run --domain radar --op 10390 --wait --timeout 30m
alphabot status --exec-id 20260515-radar-10390-000001
alphabot tail --exec-id 20260515-radar-10390-000001 --follow
alphabot cancel --exec-id 20260515-radar-10390-000001
alphabot doctor --check db,redis,mongo,s3,external-api
```

### 실행/종료 확인 방식

1. **operation_run 저장소**: `exec_id`, `domain`, `op_id`, `ot_id`, `status`, `started_at`, `ended_at`, `duration_ms`, `host`, `pid`, `exit_code`, `error_class`, `error_message`, `trace_id`.
2. **heartbeat**: 장시간 작업은 10~30초마다 `last_heartbeat_at`, `progress`, `current_step` 갱신.
3. **exit code**: `0=success`, `1=business failure`, `2=invalid args`, `3=config/secrets missing`, `4=external dependency unavailable`, `130=cancelled`.
4. **락/중복 방지**: `op_id + schedule_slot` unique key 또는 DB advisory lock/Redis lock. 재시작 시 `RUNNING` stale row를 `UNKNOWN/RECOVERING`으로 전환.
5. **관측 API**: CLI 외에 `/actuator/health`, `/actuator/metrics`, `/operations/{execId}` 또는 read-only admin endpoint 제공.
6. **로그 상관관계**: 모든 로그에 `execId`, `domain`, `opId`, `otId`, `traceId`, `attempt`, `step` 포함.


### Operation registry 예시

```java
enum AlphaBotDomain { COLLECT, FINANCE, RADAR, STOCK }
record OperationKey(AlphaBotDomain domain, int oidx) {}
interface AlphaBotOperation { OperationResult run(OperationContext ctx) throws Exception; }

Map<OperationKey, AlphaBotOperation> registry = Map.of(
  new OperationKey(COLLECT, 30030), collectProcess::procNaverStockRank,
  new OperationKey(FINANCE, 40002), financeProcess::procInvestRss,
  new OperationKey(RADAR, 10390), radarProcess::procNewsTelegramMessage,
  new OperationKey(STOCK, 45), stockProcess::awsMonitoring
);
```

## 7. Logging / S3 / Observability 설계


### S3 Logging 가능 여부

가능하다. 다만 **S3는 검색/실시간 모니터링 저장소가 아니라 저비용 원본/장기 보관 저장소**로 쓰는 것이 맞다.

권장 파이프라인:

- 애플리케이션: stdout JSON 로그 + optional local rolling file
- 수집: Fluent Bit / Vector / CloudWatch Agent / OpenTelemetry Collector
- 단기 조회: CloudWatch Logs, OpenSearch, Loki, Grafana 등
- 장기 보관: S3 partitioned path `s3://bucket/alphabot/domain=radar/date=2026-05-15/hour=13/*.json.gz`
- 보안: SSE-KMS, bucket policy, object lock/retention, lifecycle transition, 민감 필드 마스킹

애플리케이션이 직접 S3에 매 로그 이벤트를 쓰는 방식은 네트워크 지연·실패·비용·backpressure 문제가 있어 비권장이다. 작업 종료 시 결과 artifact, raw crawl snapshot, 실패 HTML/screenshot, 대용량 감사 로그를 S3에 업로드하는 것은 적합하다.


### 필수 로그 필드

```json
{
  "timestamp":"2026-05-15T13:00:00+09:00",
  "level":"INFO",
  "service":"alphabot-worker",
  "domain":"radar",
  "opId":10390,
  "otId":1,
  "execId":"20260515-radar-10390-000001",
  "traceId":"...",
  "step":"send_telegram_message",
  "status":"RUNNING",
  "durationMs":1234,
  "message":"operation step completed"
}
```

### 기존 대비 개선 포인트

- UI list 50건 제한 로그는 제거하고, 모든 실행 로그를 구조화한다.
- `catch { }`는 금지한다. 예외는 `operation_run` + structured log + metric counter에 남긴다.
- START/ERROR/END는 Stock App처럼 `finally`에서 보장하되, 모든 도메인에 동일한 contract를 적용한다.
- 외부 API 호출은 timeout/retry/circuit-breaker 정책과 결과 code를 로그 필드로 남긴다.

## 8. Linux 인프라 선택지

| Use case | Option | Why | Caution |
| --- | --- | --- | --- |
| 가벼운 초기 이전 | Linux VM + systemd timer/service | 현재 WPF 타이머 구조를 CLI로 가장 빨리 치환. journalctl로 stdout 로그 확인 가능. | HA/스케일아웃/동시성 제어는 별도 구현 필요 |
| 운영 표준화 | Docker + Kubernetes CronJob/Job | 작업 단위 격리, restartPolicy, history, logs, resource limit, secrets/configmap 관리가 쉬움. | 클러스터 운영 역량 필요 |
| AWS 운영형 | ECS/Fargate Scheduled Task 또는 AWS Batch | 서버 관리 최소화, IAM Role, CloudWatch Logs/S3/Secrets Manager 연계가 자연스러움. | 장시간 상주/초단기 고빈도 작업의 비용 모델 검토 필요 |
| 짧은 이벤트 작업 | Lambda + EventBridge Scheduler | 짧고 독립적인 API 호출/정리 작업에 적합. | 15분 제한/브라우저 크롤링/무거운 JVM에는 부적합 |
| 상시 워커 | Spring Boot Worker + Quartz/Spring Scheduler | DB 스케줄을 앱 안에서 관리하면서 REST/Actuator로 상태 조회 가능. | 다중 인스턴스 락/중복 실행 방지 필수 |

## 9. Java 언어/라이브러리 추천

| Area | Recommendation | Reason |
| --- | --- | --- |
| Runtime | Java 25 LTS 권장, Java 21 LTS 보수안 | 2026-05 기준 Oracle roadmap에서 25가 최신 LTS. Spring Boot 4는 Java 17+ 요구. |
| CLI | picocli | subcommand/exit code/help가 성숙. `run`, `status`, `tail`, `cancel`, `list` 구현에 적합. |
| App framework | Spring Boot 4.x 또는 3.x LTS 라인 검토 | Actuator, configuration, DI, scheduling, observability 통합. Boot 4는 Java 17+ 및 Spring Framework 7 기반. |
| Batch | Spring Batch | 대용량 처리, restart/skip/statistics/job repository가 필요한 작업에 적합. |
| Scheduler | Quartz 또는 Kubernetes CronJob | DB 기반 반복/1회 실행 조건이면 Quartz, 인프라 스케줄이면 CronJob. |
| DB | HikariCP + JdbcTemplate/MyBatis/jOOQ | 기존 SQL 보존은 MyBatis/JdbcTemplate, 타입 안정 SQL 재설계는 jOOQ. |
| HTTP/API | Java 21+ HttpClient 또는 OkHttp + Resilience4j | timeout/retry/circuit breaker/rate limit 표준화. |
| Crawler | Jsoup, Selenium Java, Playwright Java | 정적 HTML은 Jsoup, 브라우저 필요 시 Playwright/Selenium. CefSharp는 Java/Linux 직접 대체 필요. |
| Logging | SLF4J + Logback JSON encoder | stdout JSON을 기본으로 하고 파일/S3는 수집기로 처리. |
| Observability | OpenTelemetry Java Agent + Micrometer/Prometheus | trace/log/metric correlation, zero-code agent부터 시작 가능. |
| AWS | AWS SDK for Java 2.x | S3 업로드/CloudWatch/Secrets Manager/STS/IAM Role 통합. |
| Secrets | AWS Secrets Manager 또는 Parameter Store | App.config 민감정보 제거. Kubernetes 사용 시 External Secrets 연계. |
| Test | JUnit 5, AssertJ, Testcontainers, WireMock | DB/API/외부 서비스 계약 테스트와 재시도 정책 검증. |

## 10. DB 접근/데이터 포팅 전략

1. **1단계 - SQL 보존 포팅**: 기존 stored procedure/raw SQL을 Java Repository로 래핑한다. DB schema 변경 없이 read/write contract를 캡처한다.
2. **2단계 - 실행 상태 표준화**: `OperationTermHistory`를 유지하면서 `operation_run` 또는 view를 추가해 상태 조회/재시작/중복 방지를 구현한다.
3. **3단계 - 쿼리 정리**: 반복 SQL 문자열, `ExecQuery`, `GetDataTable` 패턴을 typed mapper로 이동한다.
4. **4단계 - 테스트 DB**: Testcontainers 또는 staging DB snapshot으로 job별 integration test를 만든다. 운영 DB 직접 접속은 금지한다.

## 11. 외부 API/파일/네트워크 접근 요약

- **CollectData**: Naver Finance/Stock, Upbit, TradingEconomics, Infostock, 언론사/뉴스 사이트, Mongo/Kafka/Telegram 설정.
- **Finance**: investnews RSS, 이미지/파일 업로드 경로, DBStockData, 파일 계정 설정.
- **Radar**: FinUp Radar/Theme API, stockdata API, Redis/Mongo, Google Android Publisher receipt check, Firebase/FCM, Telegram, Danal payment functions, Selenium.
- **Stock**: StockPoint/FinUp API, AWS CloudWatch/EC2/RDS, Firebase, YouTube API, SMS/LGU+/Danal, Telegram, external upload, Naver Cafe/Email.

## 12. 위험 보고서

| Priority | Risk | Evidence | Recommendation |
| --- | --- | --- | --- |
| P0 | 민감정보/운영 설정 노출 | App.config, client_secrets.json, Firebase service-account JSON, AWS/Telegram/Bitly/API 토큰 패턴이 다수 감지됨. 값은 리포트에 출력하지 않음. | Secrets Manager/Parameter Store/Vault로 이동, 로컬 repo 이력 정리, 런타임 IAM Role 사용 |
| P0 | Windows UI/프로세스 결합 | 대부분 WinExe/WPF/DispatcherTimer이며 App shell이 스케줄러·상태·실행 제어를 직접 보유. | CLI + headless worker + external scheduler로 분리 |
| P0 | 작업 완료/실패 관측 불완전 | Collect/Finance/Radar는 내부 Thread에서 RunTask 후 상태를 Stop으로 바꾸고 catch가 비어있는 구간이 많음. Stock만 START/ERROR/END finally 패턴이 상대적으로 좋음. | operation_run 테이블, execId, heartbeat, cancel token, exit code 표준화 |
| P1 | DB 스케줄 의존과 raw SQL 확산 | Operation/OperationTerm을 DB에서 읽어 실행. SqlSender/DBUtil/GetDataTable/ExecQuery 패턴이 넓게 분산. | Repository 계층, idempotent job contract, transaction boundary 명시 |
| P1 | 외부 API/크롤링 취약성 | Naver/Upbit/Infostock/Google/Firebase/Danal/FinUp API, Selenium/CefSharp, HTTP URL 혼재. | HTTP client timeout/retry/rate-limit/circuit-breaker/contract test |
| P1 | 로그는 있으나 검색/상관관계 부족 | NLog/LogWriter/UI list/DB history/Console 혼합. traceId/execId/opId 일관성이 약함. | JSON structured logging + OpenTelemetry + 중앙 수집 |
| P2 | 포팅 시 의존성 재선택 필요 | CefSharp OffScreen, WPF, DANALCOMLib, Windows path/exe 실행은 Linux Java 직접 포팅 난이도 높음. | 기능별 어댑터/대체 라이브러리 선정 후 단계 포팅 |

## 13. 포팅 우선순위 / 로드맵

### Phase 0 — Discovery hardening

- OIdx/OTIdx 전체 운영 목록을 DB에서 export하여 operation catalog 확정.
- 민감정보 inventory 작성 및 secret rotation 계획 수립.
- 각 operation별 입력/출력/side effect/API/DB table/write scope 작성.

### Phase 1 — 공통 Java runtime 골격

- `alphabot-cli` repo/package 생성: picocli, Spring Boot, structured logging, config/secrets, DB connection, operation_run.
- `list/run/status/tail/cancel/doctor` 명령 구현.
- 기존 DB OperationTerm evaluator를 Java로 복제하고 unit test 작성.

### Phase 2 — Finance Biz 우선 포팅

- `40001 ProcRanking`, `40002 ProcInvestRss`, `40003 ProcStockSchedule` 순서.
- 파일 업로드/계정/경로 설정은 Linux path와 secret으로 분리.
- RSS/HTML parsing은 Jsoup/Syndication 대체.

### Phase 3 — CollectData Biz 포팅

- 크롤러별 adapter 분리: Naver/Upbit/Infostock/news sites/MongoClean.
- 브라우저 필요한 작업은 Playwright/Selenium 컨테이너로 격리.
- 크롤링 raw response, screenshot, failure page를 S3 artifact로 저장.

### Phase 4 — Radar monolith 분해

- Push/Telegram/News/Theme/Receipt/Payment/Cache 작업군으로 패키지 분리.
- Google/Firebase/Danal credential을 Secrets Manager로 이동.
- Redis/Mongo/HTTP timeout/retry 표준화.

### Phase 5 — Stock monolith 분해

- AWS monitoring, SMS/payment, push/email, item-stock upload, event/point/league jobs로 bounded context 분리.
- 현재 Stock의 START/ERROR/END finally 패턴을 공통 runtime의 기준 구현으로 승격.
- 직접 AWS key 사용 제거, IAM Role 기반으로 전환.

## 14. 참고한 공식 문서

- Oracle Java SE Support Roadmap — Java 8/11/17/21/25 LTS 및 Java 25 support timeline 확인: https://www.oracle.com/java/technologies/java-se-support-roadmap.html
- Spring Boot System Requirements — Boot 4.0.6 Java 17+ 및 build tool requirements 확인: https://docs.spring.io/spring-boot/system-requirements.html
- picocli API — subcommand/exit code CLI 설계 근거: https://picocli.info/apidocs-all/info.picocli/picocli/CommandLine.html
- AWS SDK for Java 2.x S3 examples — S3 upload/transfer client 선택 근거: https://docs.aws.amazon.com/en_us/sdk-for-java/latest/developer-guide/examples-s3.html
- OpenTelemetry Java instrumentation — Java agent, logs/traces/metrics correlation 근거: https://opentelemetry.io/docs/languages/java/instrumentation/
- Spring Batch reference — batch logging/tracing, transaction, job restart/skip/statistics 기능 근거: https://docs.spring.io/spring-batch/docs/5.0.5/reference/html/index-single.html
- Kubernetes CronJob docs — Linux/container scheduling 선택지 근거: https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/

## 15. 산출물 검증 체크리스트

| 요구사항 | 리포트 반영 위치 | 증거 |
|---|---|---|
| 6개 포팅 대상 분석 | 2, 4장 | 대상 경로별 csproj/config/source scan |
| 포팅 언어 Java | 6, 9, 13장 | Java runtime/library/roadmap 명시 |
| Windows 프로젝트 필요성 판단 | 5장 | WPF/WinExe/DispatcherTimer/Interop 근거 |
| CLI 형식 고려 | 6장 | 명령/exit code/status/tail/cancel 설계 |
| 어떤 operation이 동작/종료되는지 확인 | 6, 7장 | operation_run/heartbeat/execId/log fields |
| Logging 강화 | 7장 | structured logging, exception, metrics 설계 |
| S3 logging 활용 가능성 | 7장 | 수집기→S3 장기보관 권고 |
| Linux 인프라 종류 | 8장 | systemd, Kubernetes, ECS/Fargate, Batch, Lambda/EventBridge |
| Java 라이브러리 추천 | 9장 | runtime/framework/scheduler/db/http/crawler/logging/test |
| Starbucks XLarge 디자인 | `index.html` | Starbucks palette, cream/green cards, large layout CSS 적용 |
| 위치 `/mnt/c/reports/alphabots/porting` | 파일 저장 위치 | `porting-consult.md`, `index.html` |
