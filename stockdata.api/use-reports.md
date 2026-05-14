# StockData API 설정 사용 통합 분석 보고서

- 작성일: 2026-05-13
- 기준 보고서: `stockdata.api/stockdata.api.settings-analysis.html`
- 연결 보고서:
  - `설정분석.html`
  - `FinUp.StockData.ChartCapture.App/FinUp.StockData.ChartCapture.App.analysis.html`
- 산출물: `stockdata.api/use-reports.md`, `stockdata.api/use-reports.html`
- 민감정보 처리: 원본 설정 보고서에는 DB 암호문, API key, 계정/비밀번호가 포함되어 있으므로 이 통합본에는 URL, 설정키, 실행 모드, 의존 관계만 남기고 민감값은 제외했다.

## 1. 한 장 결론

세 보고서를 연결해서 보면 `stockdata.api.settings-analysis.html`의 핵심은 “StockData API URL 설정키가 어디서 어떤 목적에 쓰이는가”이고, `설정분석.html`은 그 설정값이 실제 배포 후보 config 전체에서 어떤 대표값·파일·실행모드로 퍼져 있는지를 보여준다. `FinUp.StockData.ChartCapture.App.analysis.html`은 그중 `FinUp.StockData.ChartCapture.App`의 `StockDataUrl`이 실제 런타임에서 어떤 외부 연동 표면을 만드는지 상세히 설명한다.

핵심 연결은 다음과 같다.

| 구분 | 중심 설정 | 값 형태 | 연결 의미 |
| --- | --- | --- | --- |
| 공통 StockData API base | `ApiStockPriceAddress`, `StockDataApi`, `WebAPIAddress` | `https://stockdata.finup.co.kr/api` | 값 자체에 `/api`가 포함된다. 코드가 `/price/...`, `/market/...` 등을 뒤에 붙인다. |
| StockData host base | `ThemeConfig:StockDataApiUrl`, `StockDataUrl` | `https://stockdata.finup.co.kr` | 값에는 `/api`가 없다. 코드가 `/api/...` 또는 `/chart/...`를 목적별로 붙인다. |
| Chart capture endpoint | `ChartAPIAddress` | `http://stockdata.finup.co.kr/api/chart/capture` 또는 pre 환경 endpoint | base가 아니라 완성 endpoint다. RoboAnalysis가 외부에서 차트 캡처를 트리거하는 경계다. |
| ChartCapture 실행 모드 | `StartUp=Chart` 또는 `StartUp=Scheduler` | 실행 Form 분기 | 같은 `StockDataUrl`이 TCP 테마 차트 서버와 배치성 차트 캡처 작업에서 서로 다르게 쓰인다. |

가장 중요한 운영 판단은 `StockDataUrl`과 `WebAPIAddress`를 같은 “StockData 주소”로 묶어 바꾸면 안 된다는 점이다. 하나는 `/api` 포함 base이고, 하나는 `/api` 미포함 host다. 이 규칙을 어기면 `/api/api/...` 중복 또는 `/chart/...` 경로 깨짐이 발생할 수 있다.

## 2. 세 파일의 역할 연결

| 파일 | 보고서가 제공하는 정보 | 이 통합본에서의 사용 방식 |
| --- | --- | --- |
| `stockdata.api/stockdata.api.settings-analysis.html` | 7개 프로젝트/실행 변형의 StockData 관련 설정키 사용처, 현재 사용 여부, 코드 근거 | 기준 축. 프로젝트별 “설정키 → 코드 사용 → 실제 URL → 리스크”를 정리하는 뼈대로 사용 |
| `설정분석.html` | 전체 config의 대표 설정값, 파일별 설정키, 배포 후보 파일명/IP/서비스명 | 기준 보고서의 소스 분석을 실제 배포 후보 config 값과 연결. 특히 `https://stockdata.finup.co.kr/api`, `https://stockdata.finup.co.kr`, `StartUp`, `ChartAPIAddress` 대표값 확인에 사용 |
| `FinUp.StockData.ChartCapture.App.analysis.html` | ChartCapture의 `Scheduler`, `Chart`, `Robo` 옵션별 실행 흐름과 외부 연동 상세 | `StockDataUrl`이 실제로 시장 일정 API, 차트 HTML, TCP listener, 파일 저장, Chat API/DB 연동과 어떻게 연결되는지 보강 |

## 3. 설정값 계보도

```text
https://stockdata.finup.co.kr/api
├─ FinUp.Radar.App.AlphaBot: ApiStockPriceAddress
│  ├─ /price/diff
│  └─ /market/{from}/{to}
├─ FinUp.Stock.App.AlphaBot: StockDataApi
│  └─ /price/highlowlist
├─ FinUp.StockData.Price.App: WebAPIAddress
│  └─ /market/{from}/{to}
├─ KiwoomReal_FinUp.StockData.Price.App: WebAPIAddress
│  └─ /market/{from}/{to}
└─ FinUp.StockData.RoboAnalysis.App: WebAPIAddress
   └─ /market/{from}/{to}

https://stockdata.finup.co.kr
├─ FinUp.Analysis.Theme.App: ThemeConfig:StockDataApiUrl
│  └─ /api/index/last?codes=001,101
└─ FinUp.StockData.ChartCapture.App: StockDataUrl
   ├─ /api/market/{from}/{to}
   └─ /chart/*.html

http://stockdata.finup.co.kr/api/chart/capture
└─ FinUp.StockData.RoboAnalysis.App: ChartAPIAddress
   └─ ?date=yyyy-MM-dd
```

## 4. 대표 설정값과 실제 사용처

`설정분석.html`의 대표값 표와 파일별 설정 표를 기준 보고서에 연결하면 다음과 같다.

| 대표값 / 설정값 | 설정키 | 파일·서비스 | 현재 의미 |
| --- | --- | --- | --- |
| `https://stockdata.finup.co.kr/api` | `appSettings:ApiStockPriceAddress` | `FinUp.Radar.App.AlphaBot.exe.config` / 레이더 알파봇 | 가격 diff와 장 시작 delay 계산용 StockData API base |
| `https://stockdata.finup.co.kr/api` | `appSettings:StockDataApi` | `FinUp.Stock.App.AlphaBot.exe.config` / 스탁 알파봇 | 고가·저가 판정용 `/price/highlowlist` 호출 base |
| `https://stockdata.finup.co.kr/api` | `appSettings:WebAPIAddress` | `FinUp.StockData.Price.App.exe.config` / 일봉 수집 | 시장 일정 조회용. 배포 후보는 `StartUp=S` |
| `https://stockdata.finup.co.kr/api` | `appSettings:WebAPIAddress` | `KiwoomReal_FinUp.StockData.Price.App.exe.config` / 키움 실시간 종목 수집 | 같은 코드베이스의 Kiwoom Real 실행 변형. `StartUp=KR` |
| `https://stockdata.finup.co.kr/api` | `appSettings:WebAPIAddress` | `FinUp.StockData.RoboAnalysis.App.exe.config` / 로보어드바이저 | 로보 분석 스케줄의 시장 일정 조회 |
| `https://stockdata.finup.co.kr` | `ThemeConfig:StockDataApiUrl` | `FinUp.Analysis.Theme.App.appsettings.json` / 테마 키워드 랭킹 | 코드가 `/api/index/last`를 붙인다. `/api` 미포함이어야 한다. |
| `https://stockdata.finup.co.kr` | `appSettings:StockDataUrl` | `scheduler_FinUp.StockData.ChartCapture.App.exe.config` / 머니서퍼 차트 캡쳐 | Scheduler 모드에서 시장 일정 API와 chart HTML base로 사용 |
| `http://stockdata.finup.co.kr/api/chart/capture` | `appSettings:ChartAPIAddress` | `FinUp.StockData.RoboAnalysis.App.exe.config` / 로보어드바이저 | 차트 캡처 API 완성 endpoint. base URL이 아니다. |

## 5. 기준 보고서 중심 프로젝트별 연결 분석

### 5.1 FinUp.Radar.App.AlphaBot — `ApiStockPriceAddress`

- 설정값: `https://stockdata.finup.co.kr/api`
- 실제 URL:
  - `/price/diff`
  - `/market/{from}/{to}`
- 목적:
  - 종목 가격 diff 조회
  - 테마로그 알림의 장 시작 지연 시간 계산
- 연결해서 볼 설정:
  - `설정분석.html`에서는 이 값이 다른 StockData 클라이언트들과 같은 대표값으로 묶인다.
  - 가격 API와 시장 일정 API를 같은 base 아래에서 쓰므로, 장애 시 `/price/diff`만 보지 말고 `/market/...`도 같이 확인해야 한다.
- 주의점:
  - 기준 보고서는 `/price/diff` URL 조립 문자열 뒤 공백 가능성을 지적한다. API client가 trim하지 않으면 endpoint mismatch가 날 수 있다.

### 5.2 FinUp.Stock.App.AlphaBot — `StockDataApi`

- 설정값: `https://stockdata.finup.co.kr/api`
- 실제 URL:
  - `/price/highlowlist`
- 목적:
  - 채팅/시그널 대상의 고가·저가 판정
- 연결해서 볼 설정:
  - 같은 config에는 Chat API, StockPoint API, API key류가 함께 있어 StockData API 결과가 채팅/시그널 처리로 이어진다.
  - `설정분석.html`에서는 `StockDataApi`가 공통 StockData API base 대표값에 포함된다.
- 주의점:
  - 요청 압축 옵션을 사용하는 호출로 분석되어 API 쪽 압축 요청 지원 여부를 같이 확인해야 한다.

### 5.3 FinUp.StockData.Price.App / KiwoomReal 변형 — `WebAPIAddress`

- 설정값: `https://stockdata.finup.co.kr/api`
- 실제 URL:
  - `/market/{from}/{to}`
- 목적:
  - 가격 수집 스케줄러의 장 일정·다음 장 시작 시각 계산
- 연결해서 볼 설정:
  - `FinUp.StockData.Price.App.exe.config`: `StartUp=S`
  - `KiwoomReal_FinUp.StockData.Price.App.exe.config`: `StartUp=KR`, `MarketType=ALL`, `FIDType=PRICE`
- 판단:
  - KiwoomReal은 별도 소스 프로젝트라기보다 `FinUp.StockData.Price.App` 코드베이스를 Kiwoom Real 전용 config로 실행하는 배포 변형으로 보는 것이 타당하다.
- 주의점:
  - 소스 config와 배포 후보 config의 `StartUp`이 다르면 “현재 사용 경로”가 달라진다. 운영 확인 시 실행 파일명뿐 아니라 실제 로드 config를 확인해야 한다.

### 5.4 FinUp.StockData.RoboAnalysis.App — `WebAPIAddress`, `ChartAPIAddress`

- `WebAPIAddress`
  - 값: `https://stockdata.finup.co.kr/api`
  - 역할: 로보 분석 JOB 스케줄의 시장 일정 조회
- `ChartAPIAddress`
  - 배포 후보 값: `http://stockdata.finup.co.kr/api/chart/capture`
  - 소스 분석 기준에는 pre 환경 endpoint가 존재한다.
  - 역할: `?date=yyyy-MM-dd`만 붙여 차트 캡처 API 호출
- 연결해서 볼 설정:
  - `UIType=JOB`, `IsManual=N` 또는 소스 기준 `IsManual=Y`
  - `ChartAPIAddress`는 ChartCapture 계층을 외부에서 호출하는 경계로 보인다.
- 판단:
  - `WebAPIAddress`는 StockData API 시장 일정 의존성이고, `ChartAPIAddress`는 ChartCapture 실행 결과를 필요로 하는 후처리 의존성이다. 두 설정은 같은 StockData 이름을 갖지만 성격이 다르다.
- 주의점:
  - 운영/pre 혼재가 가장 큰 리스크다. 소스는 pre/http, 배포 후보는 운영/http로 분석되어 실제 적용 config 확인이 필요하다.
  - `ChartAPIAddress`는 base가 아니라 endpoint이므로 `/api` 포함 규칙으로 일반화하면 안 된다.

### 5.5 FinUp.Analysis.Theme.App — `ThemeConfig:StockDataApiUrl`

- 설정값: `https://stockdata.finup.co.kr`
- 실제 URL:
  - `/api/index/last?codes=001,101`
- 목적:
  - 테마 메시지의 코스피·코스닥 마감 지수 조회
- 연결해서 볼 설정:
  - `설정분석.html`에서는 이 값이 `scheduler_FinUp.StockData.ChartCapture.App`의 `StockDataUrl`과 같은 대표값으로 묶인다.
- 주의점:
  - 이 값은 `/api` 미포함 host다. `https://stockdata.finup.co.kr/api`로 바꾸면 `/api/api/index/last`가 될 수 있다.

### 5.6 FinUp.StockData.ChartCapture.App — `StockDataUrl`

- 설정값: `https://stockdata.finup.co.kr`
- 실행 모드:
  - 소스 기준: `StartUp=Chart`
  - scheduler 배포 후보: `StartUp=Scheduler`
- 실제 URL:
  - Chart 모드: `/chart/lwthemechart_1250_400.html?keywordIdx=...` 또는 legacy `/chart/themechart.html?...`
  - Scheduler 모드: `/api/market/{from}/{to}`, `/chart/trchart.html`, `/chart/custchart.html`, `/chart/themelogchart.html`
- 연결해서 볼 설정:
  - `설정분석.html`에서 일반 `FinUp.StockData.ChartCapture.App.exe.config`에는 `StockDataUrl`이 보이지 않고, `scheduler_FinUp.StockData.ChartCapture.App.exe.config`에는 `StockDataUrl`이 존재한다.
  - `FinUp.StockData.ChartCapture.App.analysis.html`에 따르면 ChartCapture는 옵션별로 외부 연동 표면이 크게 달라진다.
- 판단:
  - `StockDataUrl`은 단순 API base가 아니라 차트 HTML 렌더링과 시장 일정 API를 동시에 만드는 host base다. `/api`를 포함시키면 차트 URL이 깨진다.

## 6. ChartCapture 상세 연결

`FinUp.StockData.ChartCapture.App.analysis.html`의 옵션별 분석은 기준 보고서의 `3.7 FinUp.StockData.ChartCapture.App — appSettings:StockDataUrl`을 다음처럼 보강한다.

| 옵션 | 실행 Form | `StockDataUrl` 사용 | 주요 외부 연동 | 운영상 의미 |
| --- | --- | --- | --- | --- |
| Scheduler | `Scheduler` | `{StockDataUrl}/api/market/{from}/{to}`, `{StockDataUrl}/chart/trchart.html`, `/custchart.html`, `/themelogchart.html` | 시장 일정 API, chart HTML, 파일 저장, Windows impersonation | 장 종료 후 예탁금/신용잔고/테마록 차트를 배치 생성 |
| Chart | `TcpListenerChart` | `{StockDataUrl}/chart/lwthemechart_1250_400.html?...` 또는 legacy theme chart | TCP 8280, chart HTML, 파일 저장 | 기본 설정값 기준 테마 차트 즉시 캡처 서버 |
| Robo | `TcpListenerRobo` | 주로 `ChartUrl`/BizStock chart HTML과 DB/Chat API 사용. `StockDataUrl`보다는 로보 후처리 연동이 핵심 | TCP 8279, DBStockPoint SQL, BizStock chart HTML, Chat API multipart POST, 파일 저장 | 외부 연동이 가장 넓고 장애 영향이 가장 큼 |

ChartCapture 상세 보고서의 리스크를 기준 보고서와 연결하면 다음이 중요하다.

1. Scheduler는 시장 일정 API 실패 시 전체 배치가 시작되지 않을 수 있다.
2. Chart 모드는 listener 포트가 설정값이 아니라 코드 상수처럼 분석되어 운영자가 config만 바꿔도 적용되지 않을 수 있다.
3. Robo 모드는 SQL, 차트 렌더링, 파일 저장, Chat API가 한 요청에 직렬로 묶여 장애 전파 범위가 가장 넓다.
4. `RoboAnalysis.App`의 `ChartAPIAddress`와 ChartCapture의 실제 실행 모드·config가 맞지 않으면 로보 분석 후 차트 생성이 성공해도 후속 반영이 실패할 수 있다.

## 7. `/api` 포함 규칙

| 설정군 | 올바른 값 형태 | 코드 조립 방식 | 잘못 바꿨을 때 위험 |
| --- | --- | --- | --- |
| `ApiStockPriceAddress`, `StockDataApi`, `WebAPIAddress` | `https://stockdata.finup.co.kr/api` | 뒤에 `/price/...`, `/market/...`를 붙임 | `/api`를 제거하면 호출 endpoint가 한 단계 빠짐 |
| `ThemeConfig:StockDataApiUrl`, `StockDataUrl` | `https://stockdata.finup.co.kr` | 코드가 `/api/...` 또는 `/chart/...`를 붙임 | `/api`를 넣으면 `/api/api/...` 또는 `/api/chart/...` 오류 |
| `ChartAPIAddress` | `http://stockdata.finup.co.kr/api/chart/capture` | `?date=yyyy-MM-dd`만 붙임 | base URL처럼 취급하면 chart capture endpoint가 깨짐 |

## 8. 운영/배포 config에서 같이 봐야 할 부분

| 점검 영역 | 확인할 내용 | 관련 파일·서비스 |
| --- | --- | --- |
| 실제 로드 config | 소스 `App.config`와 `/mnt/c/App/Config/*.exe.config` 중 운영 서비스가 읽는 파일 | Price, KiwoomReal, RoboAnalysis, ChartCapture |
| 실행 모드 | `StartUp`, `UIType`, `IsManual` 값 | Price: `S/KR`, ChartCapture: `Chart/Scheduler/Robo`, RoboAnalysis: `JOB`, manual 여부 |
| URL base 규칙 | `/api` 포함/미포함/완성 endpoint 구분 | 전체 StockData 관련 설정 |
| ChartCapture 배포 후보 | 일반 ChartCapture config에는 `StockDataUrl` 누락 가능, scheduler config에는 존재 | `FinUp.StockData.ChartCapture.App.exe.config`, `scheduler_FinUp.StockData.ChartCapture.App.exe.config` |
| 운영/pre 혼재 | RoboAnalysis `ChartAPIAddress`가 소스와 배포 후보에서 다름 | `FinUp.StockData.RoboAnalysis.App` |
| 장애 관측 | 시장 일정 API, chart HTML render, 파일 저장, Chat API, DB를 분리 관측 | ChartCapture Scheduler/Chart/Robo, RoboAnalysis |

## 9. 장애 영향 흐름

```text
StockData 시장 일정 API 장애
├─ FinUp.StockData.Price.App: 가격 수집 스케줄 산정 영향
├─ KiwoomReal 변형: 실시간 수집 시작 시각 산정 영향
├─ FinUp.StockData.RoboAnalysis.App: 로보 분석 JOB 예약/지연 발송 영향
└─ FinUp.StockData.ChartCapture.App Scheduler: 배치 차트 캡처 일정 산정 영향

StockData chart HTML 장애
├─ ChartCapture Scheduler: 예탁금/신용잔고/테마록 이미지 미생성
└─ ChartCapture Chart: 테마 차트 즉시 캡처 실패

ChartCapture API 또는 Robo chart 연동 장애
└─ RoboAnalysis.App: 로보 분석 후 차트 이미지 생성/반영 지연 또는 실패
```

## 10. 우선 조치 체크리스트

- [ ] StockData 관련 URL 설정을 세 타입으로 분류한다: `/api` 포함 base, `/api` 미포함 host, 완성 endpoint.
- [ ] config 변경 검증에 다음 규칙을 추가한다.
  - `WebAPIAddress`, `StockDataApi`, `ApiStockPriceAddress`는 `/api`로 끝나야 한다.
  - `StockDataUrl`, `StockDataApiUrl`은 `/api`로 끝나면 안 된다.
  - `ChartAPIAddress`는 `/api/chart/capture` endpoint여야 한다.
- [ ] 운영 서비스별 실제 로드 config를 확인한다.
  - Price 일반 서비스: `StartUp=S`인지 확인
  - KiwoomReal 서비스: `StartUp=KR`인지 확인
  - ChartCapture 일반 서비스: `StockDataUrl` 누락 여부 확인
  - ChartCapture scheduler 서비스: `StartUp=Scheduler`, `StockDataUrl` 확인
  - RoboAnalysis: `UIType=JOB`, `IsManual`, `ChartAPIAddress` 환경 확인
- [ ] 시장 일정 API 장애와 chart HTML 렌더링 장애를 같은 “StockData 장애”로 뭉뚱그리지 말고 별도 관측한다.
- [ ] ChartCapture Chart/Robo TCP listener는 포트와 payload 검증 리스크를 별도로 점검한다.
- [ ] 민감값이 포함된 원본 config 보고서는 공유 범위를 제한하고, 운영 문서에는 마스킹된 설정키/URL만 남긴다.

## 11. 근거 색인

### 기준 보고서: `stockdata.api/stockdata.api.settings-analysis.html`

- `1. 전체 결론`
- `2.1 /api 포함 여부가 프로젝트마다 다름`
- `2.3 같은 StockData 시장 일정 API 의존성`
- `2.4 운영/프리 환경 혼재`
- `3.1` ~ `3.7` 프로젝트별 상세 분석
- `4. 설정키별 현재 사용 여부 요약`
- `5. 리스크/점검 포인트`

### 전체 설정 보고서: `설정분석.html`

- 대표값 `https://stockdata.finup.co.kr/api`
- 대표값 `https://stockdata.finup.co.kr`
- `FinUp.StockData.ChartCapture.App.exe.config` 파일별 설정
- `scheduler_FinUp.StockData.ChartCapture.App.exe.config` 파일별 설정
- `FinUp.StockData.RoboAnalysis.App.exe.config` 파일별 설정
- `FinUp.StockData.Price.App.exe.config`, `KiwoomReal_FinUp.StockData.Price.App.exe.config` 파일별 설정

### ChartCapture 상세 보고서: `FinUp.StockData.ChartCapture.App/FinUp.StockData.ChartCapture.App.analysis.html`

- `1. 핵심 결론`
- `3. 공통 구성 및 외부 연동 표면`
- `4. 옵션 1 — Scheduler 정밀 분석`
- `5. 옵션 2 — Chart / TcpListenerChart 정밀 분석`
- `6. 옵션 3 — 기타/ Robo / TcpListenerRobo 정밀 분석`
- `8. 외부 연동 중요도 순위`
- `9. 옵션별 운영 점검 체크리스트`
