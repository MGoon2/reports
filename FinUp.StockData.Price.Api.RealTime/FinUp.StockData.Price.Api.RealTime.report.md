# FinUp.StockData.Price.Api.RealTime 분석 보고서

- 작성일: 2026-05-13
- 분석 대상: `/mnt/c/Dev/FinUp.StockData.Price.Api.RealTime`
- 산출물: Markdown + HTML
- 검증 범위: 컨트롤러 라우팅, SSE 파라미터 바인딩, 서비스/캐시 흐름, `web.config`, `appsettings.json`
- 검증 한계: 현재 셸에 `dotnet` 명령이 없어 빌드/실행 검증은 수행하지 못함 (`dotnet: command not found`). 아래 내용은 소스 정적 분석 기준임.

## 1. 요약

이 프로젝트는 ASP.NET Core 6 기반 실시간 주가 API이며, 주요 기능은 다음과 같다.

1. Redis Pub/Sub에서 주가/테마 메시지를 수신한다.
2. 최신 주가와 테마 점수를 메모리 캐시에 유지한다.
3. HTTP GET 캐시 조회 API와 SSE(Server-Sent Events) 스트리밍 API를 제공한다.
4. SQL Server 저장 프로시저에서 장 운영일정과 앱 정책(`/Price/Interval`)을 조회한다.
5. MongoDB에서 최신 테마 점수(`ThemeScoreDisplay`) 초기 데이터를 로딩한다.
6. IIS 배포 시 `web.config`의 ASP.NET Core Module V2가 애플리케이션 프로세스를 호스팅한다.

> 중요 참고: `Controllers/v1_0/SseController.cs`는 `MinuteCacheHostedService`, `_cacheTheme.First()`, `_cacheTheme.GetStocks()`, `_cacheTheme.ExistsKeyword()`를 사용하지만, 현재 `Program.cs`에서는 `MinuteCacheHostedService` 등록이 주석 처리되어 있고 `ThemeCacheHostedService.cs`에는 해당 공개 메서드가 보이지 않는다. 빌드 검증은 도구 부재로 확인하지 못했으므로, 이 보고서는 “현재 소스에 선언된 엔드포인트와 의도된 역할” 기준으로 정리한다.

## 2. URL 엔드포인트별 역할

### 2.1 Legacy 엔드포인트

| HTTP | 엔드포인트 | 구현 위치 | 역할 | 입력/동작 | 응답/이벤트 |
|---|---|---|---|---|---|
| GET | `/api/cache/price` | `Controllers/Legacy/CacheController.cs:29-31` | 메모리 주가 캐시 전체 조회 | `PriceCacheHostedService.GetAll()` 호출 | `IEnumerable<StockPrice>` |
| GET | `/api/cache/price/{code}` | `Controllers/Legacy/CacheController.cs:33-35` | 특정 종목의 최신 주가 캐시 조회 | `{code}`를 단일 코드 배열로 조회 | `StockPrice` 또는 null |
| GET | `/api/cache/price/schedule` | `Controllers/Legacy/CacheController.cs:42-44` | 주가 캐시 초기화/스케줄 잔여시간 조회 | `PriceCacheHostedService.State()` 호출 | `dd.hh:mm:ss` 형태 문자열 |
| GET | `/api/policy/{path?}` | `Controllers/Legacy/PolicyController.cs:21-23` | 정책 캐시 조회 | `path`가 없으면 전체 정책, 있으면 해당 경로 검색 | `Policy` |
| GET | `/api/policy/reset` | `Controllers/Legacy/PolicyController.cs:25-27` | 정책 캐시 수동 리로드 | SQL에서 `StockDataR` 정책 재조회 | `OK!!` 또는 `Fail!!` |
| GET | `/api/scope` | `Controllers/Legacy/ScopeController.cs:32-34` | 현재 SSE 연결 Scope 전체 조회 | `ScopeService.GetAll()` 호출 | Scope 목록 |
| GET | `/api/scope/id/{id}` | `Controllers/Legacy/ScopeController.cs:36-38` | Scope ID 기준 단일 연결 조회 | `{id}`로 내부 딕셔너리 검색 | `Scope` 또는 null |
| GET | `/api/scope/ip/{ip}` | `Controllers/Legacy/ScopeController.cs:40-42` | IP 기준 SSE 연결 조회 | `{ip}`와 Scope의 `IpAddress` 비교 | Scope 목록 |
| GET | `/api/scope/count` | `Controllers/Legacy/ScopeController.cs:44-46` | 전체 SSE 연결 수 조회 | 상태 필터 없음 | 정수 |
| GET | `/api/scope/count/interval` | `Controllers/Legacy/ScopeController.cs:48-50` | interval/polling 방식 연결 수 조회 | `IsRealtime == false` 카운트 | 정수 |
| GET | `/api/scope/count/realtime` | `Controllers/Legacy/ScopeController.cs:52-54` | realtime 방식 연결 수 조회 | `IsRealtime == true` 카운트 | 정수 |
| GET | `/api/sse` | `Controllers/Legacy/SseController.cs:38-40` | Legacy SSE 주가 스트림 | `SseParam` 바인딩 후 `PriceInterval > 0`이면 캐시 polling, 아니면 Scope 이벤트 구독 | `event: price` |
| GET | `/api/sse/test/eventstream` | `Controllers/Legacy/SseController.cs:157-169` | SSE 연결 테스트 | 100ms 주기로 테스트 이벤트 쓰기 | `event: price`, `data: sse test` |

### 2.2 Version 1.0 엔드포인트

`Program.cs:49-61`에서 기본 API 버전은 1.0이고 URL 내 버전 치환을 사용한다. 컨트롤러 라우트는 `api/v{version:apiVersion}/[controller]` 형식이다. ASP.NET Core 라우팅은 일반적으로 대소문자 구분 없이 매칭되므로 아래 표는 소문자 형태로 표기한다.

| HTTP | 엔드포인트 | 구현 위치 | 역할 | 입력/동작 | 응답/이벤트 |
|---|---|---|---|---|---|
| GET | `/api/v1/cache/price` | `Controllers/v1_0/CacheController.cs:29-31` | v1 주가 캐시 전체 조회 | `PriceCacheHostedService.GetAll()` 호출 | HTTP 200 + 주가 목록 |
| GET | `/api/v1/cache/price/{code}` | `Controllers/v1_0/CacheController.cs:33-41` | v1 특정 종목 주가 캐시 조회 | `{code}`로 캐시 조회 | 있으면 200, 없으면 404 |
| GET | `/api/v1/cache/price/schedule` | `Controllers/v1_0/CacheController.cs:63-65` | v1 주가 캐시 초기화/스케줄 잔여시간 조회 | `PriceCacheHostedService.State()` 호출 | HTTP 200 + 문자열 |
| GET | `/api/v1/sse` | `Controllers/v1_0/SseController.cs:62-63` | v1 통합 SSE 스트림 | `types`, `codes`, `keywordidx`, `app`/`intervaltype`, `interval`을 바인딩. 테마 요청이면 초기 테마 전송 및 OnTheme 구독. 주가 요청이고 정책 interval이 0보다 크면 캐시 polling | `event: theme`, `event: price`, `event: alive` |
| GET | `/api/v1/sse/price/{code}` | `Controllers/v1_0/SseController.cs:219-221` | v1 단일 종목 실시간 주가 SSE | 장중 여부 확인 후 특정 종목 Scope 등록, Redis 수신 주가를 Scope 이벤트로 전달. 체결이 없으면 30초마다 alive 전송, 장 종료 후 연결 종료 | `event: price`, `event: alive` |

### 2.3 비활성/주석 처리 엔드포인트

| 엔드포인트 | 근거 | 상태 |
|---|---|---|
| `/api/cache/minute/{code}` | `Controllers/Legacy/CacheController.cs:37-39`, `Controllers/v1_0/CacheController.cs:44-60` | 주석 처리됨 |
| `/api/cache/minute/schedule` | `Controllers/Legacy/CacheController.cs:46-48`, `Controllers/v1_0/CacheController.cs:67-69` | 주석 처리됨 |
| `/api/v1/sse/stock/simulate/{code}` | `Controllers/v1_0/SseController.cs:315-444` | 전체 메서드 주석 처리됨 |

## 3. SSE 요청 파라미터와 동작

`SseParamModelBinder`가 `SseParam`을 커스텀 바인딩한다 (`Program.cs:143-147`, `Models/SseParamModelBinder.cs:128-140`).

| 파라미터 | 필수 여부 | 역할 | 근거 |
|---|---:|---|---|
| `types` | 필수 | 요청 데이터 타입. `1=Price`, `2=Theme`, `3=ThemeAutoPrice`. `3`이면 내부적으로 Price와 Theme 모두 요구 상태가 된다. | `Models/SseParam.cs:12-33`, `Models/SseParamModelBinder.cs:28-57` |
| `codes` | `types`에 1이 포함되면 필수 | 조회/구독할 종목 코드 목록. 콤마로 분리하며 각 코드는 6자리여야 한다. | `Models/SseParamModelBinder.cs:59-77` |
| `keywordidx` | 선택 | 특정 테마 키워드 기준 종목 매핑/테마 조회에 사용된다. 없으면 0. | `Models/SseParamModelBinder.cs:80-95`, `Controllers/v1_0/SseController.cs:87-105` |
| `app` | 정책 interval 선택에 필요 | `/Price/Interval` 정책 하위에서 앱명과 매칭되는 interval 값을 찾는다. | `Models/SseParamModelBinder.cs:36-38`, `Models/SseParamModelBinder.cs:102-117` |
| `intervaltype` | `app`의 구 파라미터/대체값 | `app`이 없을 때 fallback으로 사용된다. | `Models/SseParamModelBinder.cs:32-38` |
| `interval` | 임시 파라미터 | 값 자체를 파싱하지 않고 정책의 첫 번째 interval을 선택하도록 우회한다. | `Models/SseParamModelBinder.cs:105-109` |

`PriceInterval <= 0`이면 `SseParam.IsRealtime`이 true가 된다 (`Models/SseParam.cs:45`). Legacy `/api/sse`는 이 경우 Scope의 `OnPrice` 이벤트를 구독한다. v1 `/api/v1/sse`의 주가 송신은 `RequiredPrice && PriceInterval > 0` polling 경로에만 구현되어 있고, 단일 종목 실시간 주가는 `/api/v1/sse/price/{code}`에서 처리한다.

## 4. 내부 데이터 흐름

### 4.1 주가 흐름

1. `Program.cs:93-104`에서 Redis, SQL, Mongo 설정을 DI에 등록한다.
2. `Program.cs:108-121`에서 주가/테마/정책/캘린더 hosted service를 등록한다.
3. `RedisSubscriberHostedService.StartAsync()`가 `stockdatapubsub` Redis subscriber를 만들고 `REDIS_CHANNEL_PRICE`, `REDIS_CHANNEL_THEME`를 구독한다 (`Service/RedisSubscriberHostedService.cs:250-255`).
4. 주가 메시지는 `RedisWebAPIMessage`로 역직렬화되고, 필요 시 gzip 해제 후 `List<StockPrice>`로 변환된다 (`Service/RedisSubscriberHostedService.cs:53-80`).
5. `PriceCacheHostedService.SetCache()`가 종목코드별 최신 주가를 메모리 캐시에 저장한다 (`Service/PriceCacheHostedService.cs:46-63`).
6. `ScopeService.PublishPrice()`가 실시간 Scope 중 요청 종목과 겹치는 연결에 `PushPrice()`를 호출한다 (`Service/ScopeService.cs:64-100`).
7. SSE 컨트롤러는 Scope 이벤트 또는 주기적 캐시 polling으로 `event: price`를 전송한다.

### 4.2 테마 흐름

1. 앱 시작 시 `ThemeCacheHostedService.StartAsync()`가 MongoDB에서 `CaptureIdx == 10`인 최신 `CaptureItemIdx` 묶음을 로딩한다 (`Service/ThemeCacheHostedService.cs:52-79`).
2. Redis 테마 메시지는 deflate 또는 일반 JSON으로 해석되어 `ThemeScoreDisplay` 목록으로 변환된다 (`Service/RedisSubscriberHostedService.cs:98-119`).
3. `ThemeCacheHostedService.SetCache()`가 키워드별 테마 캐시를 교체한다 (`Service/ThemeCacheHostedService.cs:26-35`).
4. `ScopeService.PublishTheme()`가 테마 요청 Scope에 `PushTheme()`을 호출한다 (`Service/ScopeService.cs:103-116`).
5. v1 `/api/v1/sse`는 테마 요청 시 초기 `event: theme`을 즉시 보내고 이후 변경 이벤트를 보낸다 (`Controllers/v1_0/SseController.cs:87-105`, `160-195`).

### 4.3 정책/장운영일 흐름

| 데이터 | 소스 | 사용처 |
|---|---|---|
| 앱 정책 `StockDataR`, `/Price/Interval` | SQL 저장 프로시저 `SystemData.dbo.USP_AppPolicy_List` | SSE interval 결정, 정책 API 응답 |
| 장 운영일정 | SQL 저장 프로시저 `StockData.dbo.USP_StockCalendar_List` | 캐시 초기화 스케줄, 장 시작 전 alive, 단일 종목 SSE 장중 여부 판단 |

정책은 `PolicyHostedService`가 시작 시 로드하고 30초마다 다시 로드한다 (`Service/PolicyHostedService.cs:42-56`). 장 운영일정은 `CalendarHostedService`와 `PriceCacheHostedService`가 각각 스케줄 계산에 사용한다 (`Service/CalendarHostedService.cs:21-33`, `Service/PriceCacheHostedService.cs:22-38`).

## 5. `appsettings.json` 설정 값 역할 분석

### 5.1 최상위 설정

| 경로 | 현재 값 요약 | 역할 | 사용 위치/근거 |
|---|---|---|---|
| `Logging:LogLevel:Default` | `Information` | 기본 Microsoft.Extensions.Logging 로그 레벨 | `appsettings.json:2-7` |
| `Logging:LogLevel:Microsoft` | `Warning` | Microsoft 네임스페이스 로그 노이즈 축소 | `appsettings.json:2-7` |
| `Logging:LogLevel:Microsoft.Hosting.Lifetime` | `Information` | 호스트 시작/종료 로그 레벨 | `appsettings.json:2-7` |
| `ConnectionStrings:StockData` | AES 암호문 형태의 연결 문자열 | `DecAES()`로 복호화되어 `ConnectionStrings.Default`에 들어가며 SQL query 서비스가 사용한다. 장 운영일정/정책 조회의 기반 DB 연결이다. | `appsettings.json:9-10`, `Program.cs:93-104`, `Repository/StockBiz.cs:33-80` |
| `Serilog:MinimumLevel` | `Debug` | Serilog 최소 로그 레벨 | `appsettings.json:12-24`, `Program.cs:35-38` |
| `Serilog:WriteTo[0]:Name` | `File` | Serilog File sink 사용 | `appsettings.json:14-22` |
| `Serilog:WriteTo[0]:Args:path` | `./logs/stockinfo_.log` | 파일 로그 기본 경로/파일명 prefix | `appsettings.json:16-19` |
| `Serilog:WriteTo[0]:Args:rollingInterval` | `Hour` | 시간 단위 rolling 로그 생성 | `appsettings.json:17-20` |
| `Serilog:WriteTo[0]:Args:retainedFileCountLimit` | `168` | 보관 로그 파일 수 제한. Hour 기준 약 7일치 | `appsettings.json:17-21` |

### 5.2 Redis 설정

| 경로 | 현재 값 요약 | 역할 | 사용 위치/근거 |
|---|---|---|---|
| `Redis:Clusters[0]:Name` | `stockdatapubsub` | 코드에서 subscriber를 가져올 때 사용하는 Redis 클러스터 식별자 | `appsettings.json:25-29`, `Service/RedisSubscriberHostedService.cs:250-255` |
| `Redis:Clusters[0]:Hosts[0]:ReadOnly` | `false` | 해당 Redis endpoint를 read/write 대상으로 사용 가능함을 표시 | `appsettings.json:29-33` |
| `Redis:Clusters[0]:Hosts[0]:EndPoint` | AWS ElastiCache 형태의 `:6379` endpoint | Redis Pub/Sub 연결 대상 | `appsettings.json:29-33`, `Program.cs:93-98` |
| `Redis:Clusters[0]:Options:AllowAdmin` | `true` | Redis admin 명령 허용 옵션 | `appsettings.json:35-43` |
| `Redis:Clusters[0]:Options:AbortConnect` | `false` | 초기 연결 실패 시 즉시 abort하지 않도록 하는 옵션 | `appsettings.json:35-43` |
| `Redis:Clusters[0]:Options:ConnectTimeout` | `60000` | Redis 연결 timeout(ms) | `appsettings.json:35-43` |
| `Redis:Clusters[0]:Options:KeepAlive` | `0` | Redis keep-alive 설정값 | `appsettings.json:35-43` |
| `Redis:Clusters[0]:Options:ConnectRetry` | `10` | Redis 연결 재시도 횟수 | `appsettings.json:35-43` |
| `Redis:Clusters[0]:Options:SyncTimeout` | `60000` | 동기 작업 timeout(ms) | `appsettings.json:35-43` |
| `Redis:Clusters[0]:Options:Databases` | `0-8` | Redis DB index 범위 설정 | `appsettings.json:35-43` |

Redis 채널 역할은 코드 상수로 정의된다: `REDIS_CHANNEL_PRICE`는 주가, `REDIS_CHANNEL_THEME`는 테마 채널이다 (`Models/Contracts.cs:7-20`).

### 5.3 MongoDB 설정

| 경로 | 현재 값 요약 | 역할 | 사용 위치/근거 |
|---|---|---|---|
| `MongoConfig:DefautlConnectionString` | 내부 MongoDB URI | MongoDB 기본 연결 문자열. 키 이름에 오타(`Defautl`)가 있지만 외부 라이브러리 모델이 이 이름을 기대할 수 있으므로 현재 소스만으로 오타 여부를 단정하지 않는다. | `appsettings.json:47-48`, `Program.cs:104-105` |
| `MongoConfig:Collections[0]:ClassTypeName` | `ThemeScoreDisplay` | 모델 타입과 컬렉션 매핑 | `appsettings.json:49-53`, `Service/ThemeCacheHostedService.cs:52-79` |
| `MongoConfig:Collections[0]:DBName` | `Lab` | 테마 점수 조회 DB명 | `appsettings.json:49-53` |
| `MongoConfig:Collections[0]:CollectoinName` | `T_ThemeScoreDisplay` | 테마 점수 조회 컬렉션명. 키 이름에 오타(`Collectoin`)가 있음 | `appsettings.json:49-53` |

### 5.4 `appsettings.Development.json`

Development 파일은 `Logging` 레벨만 기본값과 유사하게 정의한다 (`appsettings.Development.json:1-8`). Redis, Mongo, ConnectionStrings, Serilog 설정은 Development 파일에서 별도 override 하지 않는다.

## 6. `web.config` 설정 값 역할 분석

`web.config`는 IIS 배포 시 ASP.NET Core Module 설정을 담당한다.

| 설정 | 현재 값 | 역할 | 근거 |
|---|---|---|---|
| `<system.webServer>` | 존재 | IIS 웹 서버용 설정 섹션 | `web.config:5-21` |
| `<handlers><remove name="aspNetCore" />` | 기존 handler 제거 | 중복/기존 ASP.NET Core handler를 제거하고 아래 V2 handler로 대체 | `web.config:6-9` |
| `<add name="aspNetCore" path="*" verb="*" modules="AspNetCoreModuleV2" resourceType="Unspecified" />` | 모든 path/verb | IIS의 모든 요청을 ASP.NET Core Module V2로 전달 | `web.config:8-10` |
| `<aspNetCore processPath="%LAUNCHER_PATH%" />` | publish 치환 변수 | 실행할 .NET host 또는 exe 경로. 배포/게시 과정에서 실제 값으로 치환되는 placeholder | `web.config:11-12` |
| `<aspNetCore arguments="%LAUNCHER_ARGS%" />` | publish 치환 변수 | 실행 인자. framework-dependent 배포라면 DLL 경로 등이 들어갈 수 있음 | `web.config:11-12` |
| `stdoutLogEnabled` | `false` | ASP.NET Core Module stdout 로그 비활성화. 장애 진단 시 true로 바꿔 사용할 수 있음 | `web.config:13-14` |
| `stdoutLogFile` | `.\logs\stdout` | stdout 로그 활성화 시 파일 prefix/경로 | `web.config:13-14` |
| `hostingModel` | `InProcess` | IIS worker process 안에서 ASP.NET Core 앱을 in-process 호스팅 | `web.config:15` |
| `requestTimeout` | `00:00:10` | ASP.NET Core Module 요청 timeout 설정값. SSE처럼 오래 지속되는 요청이 있는 서비스에서 운영 영향 여부는 IIS/ANCM 런타임 동작과 함께 별도 확인 필요 | `web.config:16` |
| `<handlerSettings>` | 주석 처리 | ANCM debug 로그 설정 예시이나 현재 비활성 | `web.config:17-20` |

## 7. 주요 리스크 및 확인 필요 사항

| 항목 | 관찰 | 영향 | 근거 |
|---|---|---|---|
| v1 SSE DI/컴파일 가능성 | `MinuteCacheHostedService`는 v1 SSE 생성자에 필요하지만 DI 등록은 주석 처리됨 | 런타임 생성 실패 또는 빌드/구성 문제 가능성 | `Controllers/v1_0/SseController.cs:33-47`, `Program.cs:111-112` |
| 테마 캐시 메서드 불일치 | `_cacheTheme.First()`, `GetStocks()`, `ExistsKeyword()` 사용처가 있으나 현재 `ThemeCacheHostedService.cs`에 선언이 보이지 않음 | 빌드 실패 가능성 | `Controllers/v1_0/SseController.cs:92-99`, `177-185`, `Service/ThemeCacheHostedService.cs:15-88` |
| v1 `/api/v1/sse` 주가 realtime 경로 | `RequiredPrice && PriceInterval > 0` polling 경로만 있고 `PriceInterval <= 0` 단독 주가 realtime은 별도 `/price/{code}`가 담당 | 클라이언트가 통합 SSE에서 realtime price를 기대하면 연결이 바로 끝날 수 있음 | `Controllers/v1_0/SseController.cs:137-158`, `197` |
| 빌드 검증 미수행 | 현재 환경에 `dotnet` 없음 | 정적 분석과 실제 실행 가능 상태가 다를 수 있음 | 검증 명령 결과: `dotnet: command not found` |

## 8. 근거 파일 목록

| 파일 | 분석에 사용한 내용 |
|---|---|
| `Program.cs` | DI 구성, API versioning, Swagger, CORS, compression, middleware, config binding |
| `Controllers/Legacy/*.cs` | Legacy cache/policy/scope/sse 라우트와 역할 |
| `Controllers/v1_0/*.cs` | v1 cache/sse 라우트와 역할 |
| `Models/SseParam.cs` | SSE 타입/interval/realtime 판정 모델 |
| `Models/SseParamModelBinder.cs` | SSE query parameter 검증 및 정책 interval 바인딩 |
| `Service/*HostedService.cs` | 주가/테마/정책/캘린더/Redis 구독 데이터 흐름 |
| `Repository/StockBiz.cs` | SQL 저장 프로시저 호출 |
| `appsettings.json` | 로그, SQL, Redis, Mongo 설정 |
| `appsettings.Development.json` | 개발환경 override 범위 |
| `web.config` | IIS/ANCM 호스팅 설정 |
