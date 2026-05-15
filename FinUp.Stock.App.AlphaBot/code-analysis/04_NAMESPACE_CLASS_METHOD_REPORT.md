# 네임스페이스 / 클래스 / 메소드 분석 리포트


## Namespace: FinUp.Stock.App.AlphaBot


### Class: App

- 파일 경로: `App.xaml.cs`
- 선언 위치: line 17
- 역할: App.xaml에 대한 상호 작용 논리
- 주요 책임:
  - App.xaml에 대한 상호 작용 논리


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) FinUp.Stock.App.Util.TelegramSender telegramSender (line 19) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `App()` | (기본값/확인 필요) | public | App.xaml에 대한 상호 작용 논리 (`App.xaml.cs:20`) | N | Y | N |
| `CurrentDomain_UnhandledException()` | private | void | App.xaml에 대한 상호 작용 논리 (`App.xaml.cs:30`) | N | Y | N |
| `Dispatcher_UnhandledExceptionFilter()` | private | void | 확인 필요 (`App.xaml.cs:37`) | N | N | N |
| `Dispatcher_UnhandledException()` | private | void | 확인 필요 (`App.xaml.cs:42`) | N | Y | N |
| `OnExit()` | protected | void | 확인 필요 (`App.xaml.cs:49`) | N | Y | Y |
| `SendTelegram()` | public | void | 메시지/메일/푸시를 발송한다 (`App.xaml.cs:58`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: MainWindow

- 파일 경로: `MainWindow.xaml.cs`
- 선언 위치: line 25
- 역할: MainWindow.xaml에 대한 상호 작용 논리
- 주요 책임:
  - MainWindow.xaml에 대한 상호 작용 논리


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) int iObserveTime (line 31) |
| 필드/속성 | private SqlSender sqlMain (line 38) |
| 필드/속성 | private System.Windows.Threading.DispatcherTimer tMainTimer (line 47) |
| 필드/속성 | private System.Windows.Threading.DispatcherTimer tObserveTimer (line 48) |
| 필드/속성 | private System.Windows.Threading.DispatcherTimer tAlphaBotTimer (line 49) |
| 필드/속성 | private ObservableCollection<AlphaBotMember> _lstMember (line 50) |
| 필드/속성 | public ObservableCollection<AlphaBotMember> lstMember (line 52) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `MainWindow()` | (기본값/확인 필요) | public | 확인 필요 (`MainWindow.xaml.cs:59`) | N | N | N |
| `InitializeMember()` | private | void | 멤버 초기화 (`MainWindow.xaml.cs:73`) | N | N | Y |
| `GetDBUtil()` | private | DBUtil | Get DBUtil (`MainWindow.xaml.cs:115`) | Y | N | N |
| `Load()` | private | void | 최초 수행 프로세스 값설정 (`MainWindow.xaml.cs:123`) | Y | N | Y |
| `ProcessObserve()` | private | void | 프로세스 쓰레드 관찰 (`MainWindow.xaml.cs:200`) | N | N | Y |
| `ProcessAliveAlphaBot()` | private | void | 프로세스 실행 또는 타이머 처리를 수행한다 (`MainWindow.xaml.cs:268`) | N | N | N |
| `ProcessConfirm()` | private | void | 멤버 초기화 후 시작 프로세스 (`MainWindow.xaml.cs:293`) | N | N | Y |
| `UpdateData()` | private | void | 데이터 업데이트 프로그램 실행시 추가된 리스트의 상태 변경 (`MainWindow.xaml.cs:352`) | Y | N | Y |
| `GetActionOperation()` | private | ActionOperation | Index To Action (해당 인덱스키 별로 수행할 프로세스 맵핑) (`MainWindow.xaml.cs:419`) | N | Y | N |
| `ProcessStart()` | private | void | Action 수행 (`MainWindow.xaml.cs:678`) | Y | N | N |
| `GetLoopTimeToRun()` | private | bool | Loop일때 실행여부 확인 (`MainWindow.xaml.cs:742`) | N | N | N |
| `GetBetweenTime()` | private | bool | Loop일때 현재 시간이 설정된 시간 사이에 있는 확인 (`MainWindow.xaml.cs:765`) | N | N | N |
| `GetOnceTimeToRun()` | private | bool | 하루 한번 실행여부 (`MainWindow.xaml.cs:787`) | N | N | N |
| `SetLog()` | private | void | 로그 설정 (`MainWindow.xaml.cs:840`) | N | N | N |
| `SetOperationTermHistory()` | private | void | 상태 또는 로그/DB 값을 저장한다 (`MainWindow.xaml.cs:884`) | Y | N | N |
| `btnStart_Click()` | private | void | 프로세스 시작 (`MainWindow.xaml.cs:912`) | N | N | Y |
| `btnStop_Click()` | private | void | 프로세스 스톱 (`MainWindow.xaml.cs:928`) | N | N | Y |
| `btnManual_Click()` | private | void | 수동 실행 (`MainWindow.xaml.cs:941`) | N | N | Y |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


## Namespace: FinUp.Stock.App.AlphaBot.Operation


### Class: Process

- 파일 경로: `Operation/Process.cs`
- 선언 위치: line 37
- 역할: 배치/연동 업무 로직을 묶은 partial 클래스이다
- 주요 책임:
  - 배치/연동 업무 로직을 묶은 partial 클래스이다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | private System.Diagnostics.Process ProcessStockRadar (line 46) |
| 필드/속성 | (기본값/확인 필요) AWSCredentials AWSCredential (line 57) |
| 필드/속성 | (기본값/확인 필요) AmazonCloudWatchClient CloudWatchClient (line 62) |
| 필드/속성 | (기본값/확인 필요) List<AWSMetricMember> MetricList (line 67) |
| 필드/속성 | (기본값/확인 필요) string serviceAccountFile (line 68) |
| 필드/속성 | (기본값/확인 필요) FirebaseApp FirebaseApp (line 70) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `Process()` | (기본값/확인 필요) | public | 생성자 (`Operation/Process.cs:78`) | N | Y | N |
| `GetMetric()` | private | void | 지표 조회 (`Operation/Process.cs:94`) | Y | Y | Y |
| `GetStandardUnit()` | private | StandardUnit | Get 측정 단위 (`Operation/Process.cs:121`) | N | N | N |
| `SetOperationTermHistory()` | private | void | 히스토리 DB Insert (`Operation/Process.cs:149`) | Y | N | N |
| `SetLogProcess()` | private | void | 로그 기록 (`Operation/Process.cs:170`) | N | N | N |
| `LogVirtualCurrency()` | private | void | 가상화폐 로그 저장 공통 (`Operation/Process.cs:186`) | N | N | N |
| `WriteLogVirtualCurrency()` | private | void | 가상화폐 거래소 전용 로그기록 (`Operation/Process.cs:218`) | N | N | N |
| `ShortenUrl()` | public | Task<string> | Short URL Process (`Operation/Process.cs:233`) | N | Y | Y |
| `GetYoutubeLiveStatus()` | public | string | 데이터를 조회하거나 계산한다 (`Operation/Process.cs:265`) | N | Y | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: ProcessBase

- 파일 경로: `Operation/ProcessBase.cs`
- 선언 위치: line 13
- 역할: 공통 설정 로딩, DBUtil 생성, SQL 헬퍼 초기화를 담당한다
- 주요 책임:
  - 공통 설정 로딩, DBUtil 생성, SQL 헬퍼 초기화를 담당한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | protected WriteLog SetLog (line 18) |
| 필드/속성 | protected bool bIsReal (line 23) |
| 필드/속성 | protected string API_KAKAO_ACCESS_TOKEN (line 33) |
| 필드/속성 | protected string API_KAKAO_URL_PRODUCT (line 34) |
| 필드/속성 | protected string API_KAKAO_URL_PRODUCT_PURCHASED (line 35) |
| 필드/속성 | protected string API_FUTUREWIZ_URL_CHAT (line 42) |
| 필드/속성 | protected string API_NAVER_FINANCE (line 43) |
| 필드/속성 | protected SqlSender sqlOrderAuto (line 49) |
| 필드/속성 | protected SqlSender sqlSms (line 51) |
| 필드/속성 | protected SqlMonitor sqlMonitor (line 52) |
| 필드/속성 | protected SqlSender sqlMain (line 53) |
| 필드/속성 | protected SqlSender sqlAlarm (line 54) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `ProcessBase()` | (기본값/확인 필요) | public | 프로세스 실행 또는 타이머 처리를 수행한다 (`Operation/ProcessBase.cs:97`) | Y | N | N |
| `GetDBUtil()` | protected | DBUtil | Get DBUtil (`Operation/ProcessBase.cs:140`) | Y | N | N |
| `GetDBUtilMySQL()` | protected | DBUtilMySQL | Get DBUtilMySQL (`Operation/ProcessBase.cs:152`) | Y | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: Process

- 파일 경로: `Operation/ProcessUnit.cs`
- 선언 위치: line 42
- 역할: 배치/연동 업무 로직을 묶은 partial 클래스이다
- 주요 책임:
  - 배치/연동 업무 로직을 묶은 partial 클래스이다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `OrderAuto()` | public | void | 자동 결제 (`Operation/ProcessUnit.cs:51`) | Y | N | Y |
| `AppPush()` | public | void | 앱 푸시 발송 (`Operation/ProcessUnit.cs:167`) | Y | N | Y |
| `SMS()` | public | void | SMS발송 (`Operation/ProcessUnit.cs:348`) | Y | N | Y |
| `StockCollector()` | public | void | 종목 수집 알림 (`Operation/ProcessUnit.cs:399`) | Y | N | N |
| `SmsMonitor()` | public | void | 개발팀 SMS발송 (`Operation/ProcessUnit.cs:431`) | Y | N | N |
| `SalesStockPoint()` | public | void | 매출현황 (`Operation/ProcessUnit.cs:457`) | Y | N | N |
| `ItemStockSearchingManual()` | public | void | 종목 네이버 현재가와 비교 (이전 버전) (`Operation/ProcessUnit.cs:504`) | Y | N | Y |
| `NaverStockPriceCompare()` | public | void | 종목 네이버 현재가와 비교 (`Operation/ProcessUnit.cs:574`) | Y | Y | Y |
| `Alarm()` | public | void | 메신져 알림 발송 (`Operation/ProcessUnit.cs:745`) | Y | Y | Y |
| `OpenStockRadar()` | public | void | StockRadar 실행 (`Operation/ProcessUnit.cs:784`) | N | Y | Y |
| `ApiService()` | public | void | API Service 연동 (`Operation/ProcessUnit.cs:823`) | Y | Y | Y |
| `ApiServiceKakao()` | public | void | API Service 연동 (Kakao) (`Operation/ProcessUnit.cs:913`) | Y | N | N |
| `ApiServiceKakaoContentsReg()` | private | void | ApiService 카카오스탁 컨텐츠 등록 ComIdx: 100 (`Operation/ProcessUnit.cs:931`) | Y | Y | Y |
| `ApiServiceKakaoContentsApproveCheck()` | private | void | ApiService 카카오스탁 컨텐츠 승인 확인 ComIdx: 120 (`Operation/ProcessUnit.cs:1085`) | Y | Y | N |
| `ApiServiceKakaoSalesGet()` | private | void | ApiService 카카오스탁 판매건수 조회 ComIdx: 110 (`Operation/ProcessUnit.cs:1182`) | Y | Y | Y |
| `ApiServiceFuturewizChatInsert()` | public | void | VideoChat 정보를 주기적으로 T_ApiServiceQueue에 저장 (`Operation/ProcessUnit.cs:1275`) | Y | N | N |
| `ApiServiceFuturewizChatGet()` | private | void | ApiService 퓨처위즈 채팅내역 저장 ComIdx: 200 (`Operation/ProcessUnit.cs:1301`) | Y | Y | Y |
| `KrxData()` | public | void | KRX Data 증권거래소의 특이종목을 업데이트 (`Operation/ProcessUnit.cs:1411`) | Y | Y | Y |
| `OpenXingDataRealTime()` | public | void | 실시간 종목 수집 프로그램을 실행한다. (`Operation/ProcessUnit.cs:1712`) | N | Y | N |
| `ApiVirtualCurrency()` | public | void | 가상화폐 정보 수집 (`Operation/ProcessUnit.cs:1739`) | Y | N | Y |
| `GetApiExchangeRateUSD()` | private | double | 환율 정보를 가져 온다. (`Operation/ProcessUnit.cs:1899`) | N | Y | Y |
| `GetApiVirtualCurrencyBithumb()` | private | void | 빗썸 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:1954`) | Y | Y | Y |
| `GetApiVirtualCurrencyCoinone()` | private | void | 코인원 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:2048`) | Y | Y | Y |
| `GetApiVirtualCurrencyKorbit()` | private | void | 코빗 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:2140`) | Y | Y | Y |
| `GetApiVirtualCurrencyCpdax()` | private | void | 코인플러그 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:2228`) | Y | Y | Y |
| `GetApiVirtualCurrencyCoinnest()` | private | void | 코인네스트 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:2316`) | Y | Y | Y |
| `GetApiVirtualCurrencyPoloniex()` | private | void | 폴로닉스 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:2404`) | Y | Y | Y |
| `GetApiVirtualCurrencyBittrex()` | private | void | 비트렉스 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:2498`) | Y | Y | Y |
| `GetApiVirtualCurrencyUpbit()` | private | void | 업비트 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:2626`) | Y | Y | Y |
| `GetApiVirtualCurrencyBitfinex()` | private | void | 파인넥스 Api 호출 하여 데이터를 저장 (`Operation/ProcessUnit.cs:2726`) | Y | Y | Y |
| `SetApiVirtualCurrencyData()` | private | void | 가상화폐 정보 저장 (`Operation/ProcessUnit.cs:2830`) | Y | N | Y |
| `SiteCheckStockPoint()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:2878`) | N | N | Y |
| `PriceMornitoring()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:2912`) | Y | N | N |
| `HandsUpPush()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:2987`) | Y | N | Y |
| `HandsUpCoupon()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:3019`) | Y | N | N |
| `ServerChatLoadCacheCheck()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:3043`) | N | Y | N |
| `ServerMainWebLoadCache()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:3091`) | N | Y | N |
| `BatContentsSatisfactionNotify()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:3121`) | Y | N | N |
| `BatReviewNotify()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:3150`) | Y | N | N |
| `BatCouponUnUsedNotify()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:3174`) | Y | N | N |
| `CheckSignalQueue()` | public | void | 상태를 검사한다 (`Operation/ProcessUnit.cs:3199`) | Y | Y | Y |
| `checkSignalPrice()` | private | bool | 확인 필요 (`Operation/ProcessUnit.cs:3262`) | N | N | N |
| `ClearSignalQueue()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:3292`) | Y | N | Y |
| `SetCheckChatSignal()` | private | void | 상태 또는 로그/DB 값을 저장한다 (`Operation/ProcessUnit.cs:3332`) | N | Y | N |
| `ApiSiteHealthCheck()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:3348`) | N | Y | Y |
| `AuthAppHealthCheck()` | public | AppAuthTokenMember | 로그인 체크 (`Operation/ProcessUnit.cs:3398`) | N | N | N |
| `AuthRefreshHealthCheck()` | public | void | 토큰 체크 (`Operation/ProcessUnit.cs:3441`) | N | N | Y |
| `AWSMonitoring()` | public | void | AWS 모니터링 Operation (`Operation/ProcessUnit.cs:3488`) | N | Y | N |
| `GetMonitoringList()` | private | List<AWSMonitoringMember> | 모니터링 데이터 수집 및 DB 저장 (`Operation/ProcessUnit.cs:3520`) | N | N | Y |
| `GetMonitoringMemberList()` | private | List<AWSMonitoringMember> | 모니터링 서비스 멤버 조회 (`Operation/ProcessUnit.cs:3567`) | Y | Y | Y |
| `IsMonitoringEnable()` | private | bool | 서비스의 모니터링 가능 여부 return (`Operation/ProcessUnit.cs:3631`) | N | Y | N |
| `GetStatistics()` | private | void | 모니터링 데이터 수집 (`Operation/ProcessUnit.cs:3715`) | N | Y | Y |
| `InsertMonitoringValue()` | private | void | 모니터링 데이터 DB 저장 (`Operation/ProcessUnit.cs:3857`) | Y | Y | N |
| `ThresholdCheck()` | private | void | 임계치 체크 (`Operation/ProcessUnit.cs:3903`) | N | N | Y |
| `GetThresholdList()` | private | List<AWSThresholdMember> | Get 현 시간 임계치 리스트 (`Operation/ProcessUnit.cs:4006`) | Y | Y | Y |
| `InsertThresholdLog()` | private | void | 임계치 로그 DB 저장 (`Operation/ProcessUnit.cs:4056`) | Y | N | Y |
| `AWSMonitoringSummaryOneHour()` | public | void | AWS 서비스 상태/지표를 수집한다 (`Operation/ProcessUnit.cs:4110`) | N | N | N |
| `AWSMonitoringSummaryOneDay()` | public | void | AWS 서비스 상태/지표를 수집한다 (`Operation/ProcessUnit.cs:4122`) | N | N | N |
| `AWSMonitoringSummaryInsert()` | public | void | 모니터링 데이터 집계 (`Operation/ProcessUnit.cs:4139`) | Y | N | N |
| `ApiServicePublishedItemStockQueueInsert()` | public | void | 게시된 추천종목 ApiServiceQueue에 등록 (`Operation/ProcessUnit.cs:4177`) | Y | N | N |
| `ApiServicePublishedItemStockToExternalSiteUpload()` | public | void | 게시된 추천종목 외부 사이트 업로드 (`Operation/ProcessUnit.cs:4210`) | Y | Y | Y |
| `ApiServiceItemStockToExternalSiteUploadDaily()` | public | void | 추천종목 외부 사이트 정기 업로드 (`Operation/ProcessUnit.cs:4331`) | Y | Y | Y |
| `MyMentorActivityExpired()` | public | void | My 멘토 알리미의 멘토 활동 기간 종료예정 알람 (3일전 발송) (`Operation/ProcessUnit.cs:4404`) | Y | N | N |
| `PackageISMentorItemStockUnderCnt()` | public | void | 프리미엄 추천종목 멘토의 추천종목 등록 미달 알람 (매주 수요일 16:00) (`Operation/ProcessUnit.cs:4428`) | Y | N | N |
| `MyMentorUserSelectCheck()` | public | void | CS에 My 멘토 알리미 사용자 중 멘토 미선택된 사용자 1:1등록 (`Operation/ProcessUnit.cs:4446`) | Y | N | N |
| `SiteAttackCheck()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:4474`) | N | Y | N |
| `CheckOrderAutoReceipt()` | public | void | 자동 결제 (`Operation/ProcessUnit.cs:4514`) | Y | N | Y |
| `CheckReceipt()` | public | string[] | 상태를 검사한다 (`Operation/ProcessUnit.cs:4711`) | N | N | N |
| `CheckReceiptiOS()` | public | JObject | 상태를 검사한다 (`Operation/ProcessUnit.cs:4797`) | N | N | N |
| `ApiServicePublishedMentorMarketQueueInsert()` | public | void | 게시된 멘토시황 ApiServiceQueue에 등록 (`Operation/ProcessUnit.cs:4820`) | Y | N | N |
| `ApiServicePublishedMentorMarketToExternalSiteUpload()` | public | void | 게시된 멘토시황 외부 사이트 업로드 (`Operation/ProcessUnit.cs:4853`) | Y | Y | Y |
| `InactiveUserEmailSend()` | public | void | 휴면계정 사용자 Email 전송 (`Operation/ProcessUnit.cs:4957`) | Y | N | Y |
| `BatInactiveUserQueue()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:5044`) | Y | N | N |
| `EmailSend()` | public | void | Email 전송 (`Operation/ProcessUnit.cs:5073`) | Y | N | Y |
| `EmailSendCompleted()` | private | void | 메일 발송 정보 업데이트 (`Operation/ProcessUnit.cs:5138`) | Y | N | N |
| `LGUItemStockSearch()` | public | void | 슬기로운 투자생활 추천종목 조회 (`Operation/ProcessUnit.cs:5172`) | Y | N | N |
| `LGUDailySendMessage()` | public | void | 슬기로운 투자생활 알람 (`Operation/ProcessUnit.cs:5215`) | Y | N | N |
| `SMSExternalLGUPlus()` | public | void | 외부 알림 SMS - LG U+ (`Operation/ProcessUnit.cs:5251`) | Y | N | Y |
| `ExternalExtensionSubscribe()` | public | void | 슬기로운 투자생활 연장 구독 처리 (`Operation/ProcessUnit.cs:5309`) | Y | N | N |
| `ChangeServieceGuideTomorrow()` | public | void | 슬기로운 투자생활 - 슬기로운 투자생활 유료전환 1일전 안내 (`Operation/ProcessUnit.cs:5351`) | Y | N | N |
| `ChangeServieceGuideToDay()` | public | void | 슬기로운 투자생활 - 슬기로운 투자생활 유료전환 안내(전환 당일) (`Operation/ProcessUnit.cs:5387`) | Y | N | N |
| `MonitoringAWSServiceSiteCheck()` | public | void | 사이트 동작 체크 (`Operation/ProcessUnit.cs:5423`) | Y | Y | Y |
| `UserNotifyAgreeMarketing()` | public | void | 마케팅 수신동의 안내 (`Operation/ProcessUnit.cs:5522`) | Y | N | N |
| `ExternalSubscribeCancel()` | public | void | 슬기로운 투자생활 해지 처리 (LG U+) (`Operation/ProcessUnit.cs:5592`) | N | Y | N |
| `LDInsightMentorDailyReportAlarm()` | public | void | 투자 인사이트 멘토 데일리 리포트 미등록 알람 (`Operation/ProcessUnit.cs:5644`) | Y | N | N |
| `ContentsOrderAutoEndUserNotify()` | public | void | 자동결제 만료예정 알람 (`Operation/ProcessUnit.cs:5695`) | Y | N | N |
| `ContentsUserCancelFreeChatMentor()` | public | void | 멘토 무료 채팅방 -  멘토 무료 채팅장 장기간 미입장 유저 구독 해지 (`Operation/ProcessUnit.cs:5728`) | Y | N | N |
| `TssaChallengerLeagueUpdate()` | public | void | TSSA 챌린저 강등 처리 (`Operation/ProcessUnit.cs:5762`) | Y | N | N |
| `TssaLeagueUserLog()` | public | void | TSSA 통계 업데이트 (`Operation/ProcessUnit.cs:5796`) | Y | N | N |
| `TssaMissionUserMVP()` | public | void | 리그 MVP 익일 5일 처리 (`Operation/ProcessUnit.cs:5830`) | Y | N | N |
| `TssaLeagueItemStockStatusUpdate()` | public | void | TSSA 당일 종료 종목 처리 (`Operation/ProcessUnit.cs:5863`) | Y | N | N |
| `SMSExternalDanal()` | public | void | 외부 알림 SMS - 다날 (`Operation/ProcessUnit.cs:5896`) | Y | N | Y |
| `WiseInvestStockEndBriefing()` | public | void | 슬기로운 투자생활 - 장마감 브리핑 (`Operation/ProcessUnit.cs:6106`) | Y | N | N |
| `FinUpEventItemStockStatusUpdate()` | public | void | FinUp 신규가입자 증대 이벤트 종목 종료 처리 (`Operation/ProcessUnit.cs:6136`) | Y | N | N |
| `NaverCafeAttendBoardAutoUpload()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:6168`) | N | Y | Y |
| `OrderAutoWiseInvest()` | public | void | 자동 결제 - 슬기로운 투자생활 (`Operation/ProcessUnit.cs:6246`) | Y | N | Y |
| `TssaItemStockTelegramAlarm()` | public | void | TSSA 추천종목 텔레그램 마케팅 알림 수집 (`Operation/ProcessUnit.cs:6342`) | Y | Y | N |
| `ApiServiceTssaItemStockTelegramAlarm()` | private | void | TSSA 추천종목 텔레그램 마케팅 알림 등록 (`Operation/ProcessUnit.cs:6367`) | Y | Y | Y |
| `ItemStockTelegramAlarm()` | public | void | 추천종목 텔레그램 마케팅 알림 수집 (`Operation/ProcessUnit.cs:6472`) | Y | Y | N |
| `ApiServiceItemStockTelegramAlarm()` | private | void | 추천종목 텔레그램 마케팅 알림 수집 (`Operation/ProcessUnit.cs:6492`) | Y | Y | Y |
| `GetThemeDiff()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ProcessUnit.cs:6618`) | N | Y | N |
| `ChangeServieceGuide7DaysAgo()` | public | void | 슬기로운 투자생활 - 슬기로운 투자생활 유료전환 7일전 안내 (`Operation/ProcessUnit.cs:6656`) | Y | N | N |
| `SuperStockKLeagueItemStockStatusUpdate()` | public | void | 당일 종료 종목 처리 (`Operation/ProcessUnit.cs:6694`) | Y | N | N |
| `SuperStockKLeagueUserLog()` | public | void | 슈퍼스탁K 통계 업데이트 (`Operation/ProcessUnit.cs:6724`) | Y | N | N |
| `PointDisappearanceUserQueue()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:6755`) | Y | N | N |
| `PointDisappearanceUserQueueEmailSend()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:6781`) | Y | N | Y |
| `PointDisappearanceUserProcess()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:6857`) | Y | N | N |
| `ContentsViewLogUpdateProcess()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:6883`) | Y | N | N |
| `ApiServiceChatUserUpsert()` | public | void | Api 통신 - 채팅 유저 생성 (`Operation/ProcessUnit.cs:6912`) | Y | Y | N |
| `ApiServiceChatUserCancel()` | public | void | Api 통신 - 채팅 유저 취소 (`Operation/ProcessUnit.cs:6982`) | Y | Y | N |
| `ApiServiceChatInsert()` | public | void | Api 통신 - 채팅방 생성 (`Operation/ProcessUnit.cs:7023`) | Y | Y | N |
| `ApiServiceChatUpdate()` | public | void | Api 통신 - 채팅방 수정 (`Operation/ProcessUnit.cs:7096`) | Y | Y | N |
| `ApiServiceChatUserDelete()` | public | void | Api 통신 - 채팅방 참여자 방출 (`Operation/ProcessUnit.cs:7185`) | Y | Y | N |
| `ApiServiceChatUserInsert()` | public | void | Api 통신 - Chat.T_User INSERT (`Operation/ProcessUnit.cs:7251`) | Y | Y | N |
| `ApiServiceChatUserUpdate()` | public | void | Api 통신 - Chat.T_User ProfileImage UPDATE (`Operation/ProcessUnit.cs:7300`) | Y | Y | N |
| `ApiServiceUserNicknameUpdate()` | public | void | Api 통신 - Chat.T_User Nickname UPDATE (`Operation/ProcessUnit.cs:7348`) | Y | Y | N |
| `SuperStockKTopRankerItemStockAlram()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:7394`) | Y | N | N |
| `YoutubeChannelLiveStatusUpdate()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:7468`) | Y | N | Y |
| `BatEventBoxUserDecompose()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:7541`) | Y | N | N |
| `BatEventBoxUserDivisionCoinAlarm()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:7567`) | Y | N | N |
| `BatCoinDisappearanceUserProcess()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:7593`) | Y | N | N |
| `USPPointLogInactiveDuplicate()` | public | void | 확인 필요 (`Operation/ProcessUnit.cs:7620`) | Y | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: Push

- 파일 경로: `Operation/Push.cs`
- 선언 위치: line 22
- 역할: Android/iOS/FCM/MQTT 푸시 발송을 담당한다
- 주요 책임:
  - Android/iOS/FCM/MQTT 푸시 발송을 담당한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string ANDROID_API_KEY (line 25) |
| 필드/속성 | (기본값/확인 필요) string ANDROID_JSON_MAPP (line 26) |
| 필드/속성 | (기본값/확인 필요) string SMS (line 28) |
| 필드/속성 | (기본값/확인 필요) string MQTT_MSG_FORMAT (line 29) |
| 필드/속성 | (기본값/확인 필요) string STOCKPOINT_IOS (line 30) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `Push()` | (기본값/확인 필요) | public | 확인 필요 (`Operation/Push.cs:47`) | N | Y | N |
| `SendAndroid()` | public | void | Sends push message for android. (`Operation/Push.cs:59`) | N | Y | N |
| `SendAndroidV1()` | public | void | 신규 안드로이드 푸시 (`Operation/Push.cs:99`) | N | Y | N |
| `SendIOSFcm()` | public | void | Sends push message for android. (`Operation/Push.cs:144`) | N | Y | N |
| `SendIOSFcmV1()` | public | void | 메시지/메일/푸시를 발송한다 (`Operation/Push.cs:175`) | N | Y | N |
| `SendIOS()` | public | string | 메시지/메일/푸시를 발송한다 (`Operation/Push.cs:215`) | N | N | Y |
| `ValidateServerCertificate()` | private | bool | 확인 필요 (`Operation/Push.cs:261`) | N | N | N |
| `HexStringToByteArray()` | private | byte[] | 확인 필요 (`Operation/Push.cs:266`) | N | N | Y |
| `StringToByteArray()` | public | byte[] | 확인 필요 (`Operation/Push.cs:277`) | N | N | N |
| `SendMqtt()` | public | string | 메시지/메일/푸시를 발송한다 (`Operation/Push.cs:289`) | N | Y | N |
| `SendFCM()` | public | string | 메시지/메일/푸시를 발송한다 (`Operation/Push.cs:306`) | N | Y | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: PushHandsUp

- 파일 경로: `Operation/Push.cs`
- 선언 위치: line 351
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string SERVER_PUSH_KEY (line 355) |
| 필드/속성 | (기본값/확인 필요) string PUSH_IOS (line 356) |
| 필드/속성 | (기본값/확인 필요) string PUSH_ANDROID (line 368) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `SendPushMessage()` | public | void | 메시지/메일/푸시를 발송한다 (`Operation/Push.cs:378`) | N | N | Y |
| `SetDevicesReplace()` | private | string | 상태 또는 로그/DB 값을 저장한다 (`Operation/Push.cs:408`) | N | N | N |
| `SendPush()` | private | bool | 메시지/메일/푸시를 발송한다 (`Operation/Push.cs:416`) | N | Y | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


## Namespace: FinUp.Stock.App.AlphaBot.Operation.ItemStockUpload


### Class: ItemStockUploadUtil

- 파일 경로: `Operation/ItemStockUpload/ItemStockUploadUtil.cs`
- 선언 위치: line 17
- 역할: 외부 연동 또는 공통 유틸리티 기능을 제공한다
- 주요 책임:
  - 외부 연동 또는 공통 유틸리티 기능을 제공한다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `GetNaverLogin()` | public | NaverLoginHelper | 네이버 로그인 함수 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:22`) | N | Y | Y |
| `ImagePostSend()` | public | JsonResult | 이미지 업로드 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:93`) | N | Y | N |
| `ReadFileToBoundary()` | public | byte[] | 확인 필요 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:148`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: HtmlToImageConvert

- 파일 경로: `Operation/ItemStockUpload/ItemStockUploadUtil.cs`
- 선언 위치: line 169
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | private System.Threading.ManualResetEvent manualReset (line 172) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `Convert()` | public | JsonResult | 확인 필요 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:173`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: PublishedItemStockUploadHtml

- 파일 경로: `Operation/ItemStockUpload/ItemStockUploadUtil.cs`
- 선언 위치: line 247
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string filePath (line 250) |
| 필드/속성 | (기본값/확인 필요) string ResultHtml (line 251) |
| 필드/속성 | (기본값/확인 필요) string WrapperHtml (line 252) |
| 필드/속성 | (기본값/확인 필요) string ContentsHtml (line 253) |
| 필드/속성 | (기본값/확인 필요) string ProfitRowHtml (line 254) |
| 필드/속성 | (기본값/확인 필요) string SubscribeButtonHtml (line 255) |
| 필드/속성 | (기본값/확인 필요) string ReviewHtml (line 256) |
| 필드/속성 | (기본값/확인 필요) string FinUpImgUrl (line 257) |
| 필드/속성 | (기본값/확인 필요) string FinUpStockUrl (line 259) |
| 필드/속성 | (기본값/확인 필요) string imagePath (line 260) |
| 필드/속성 | (기본값/확인 필요) string filePath (line 460) |
| 필드/속성 | (기본값/확인 필요) string wrapperHtml (line 461) |
| 필드/속성 | public string ResultCode (line 613) |
| 필드/속성 | public string ResultImage (line 614) |
| 필드/속성 | public string NaverId (line 621) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `GetResultUploadHtml()` | public | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:262`) | Y | N | Y |
| `GetContentsImage()` | private | JsonResult | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:332`) | N | N | N |
| `GetProfitImage()` | private | JsonResult | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:345`) | Y | N | N |
| `GetSubscribeButtonImage()` | private | JsonResult | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:358`) | N | N | N |
| `GetReviewImage()` | private | JsonResult | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:371`) | N | N | N |
| `GetResultHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:384`) | N | N | N |
| `GetWrapperHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:392`) | N | N | N |
| `GetContentsHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:400`) | Y | N | N |
| `GetProfitRowHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:427`) | Y | N | N |
| `GetSubscribeButtonHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:438`) | N | N | N |
| `GetReviewHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:446`) | Y | N | N |
| `GetWrapperHtml()` | public | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:476`) | Y | N | Y |
| `GetResultHtml()` | public | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:517`) | N | N | N |
| `GetDailyHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:549`) | Y | N | N |
| `GetButtonHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:584`) | N | N | N |
| `GetButtonImage()` | private | JsonResult | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:594`) | N | N | N |
| `NaverOAuthById()` | (기본값/확인 필요) | public | Response Result Code (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:622`) | N | N | N |
| `NaverOAuthById()` | (기본값/확인 필요) | public | Response Result Code (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:627`) | N | Y | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: DailyUploadHtml

- 파일 경로: `Operation/ItemStockUpload/ItemStockUploadUtil.cs`
- 선언 위치: line 457
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string filePath (line 460) |
| 필드/속성 | (기본값/확인 필요) string wrapperHtml (line 461) |
| 필드/속성 | (기본값/확인 필요) string rankHtml (line 462) |
| 필드/속성 | (기본값/확인 필요) string resultHtml (line 463) |
| 필드/속성 | (기본값/확인 필요) string buttonHtml (line 464) |
| 필드/속성 | (기본값/확인 필요) string FinUpImgUrl (line 465) |
| 필드/속성 | (기본값/확인 필요) string FinUpStockUrl (line 466) |
| 필드/속성 | (기본값/확인 필요) string Rank1Color (line 467) |
| 필드/속성 | (기본값/확인 필요) string Rank2Color (line 469) |
| 필드/속성 | (기본값/확인 필요) string Rank3Color (line 470) |
| 필드/속성 | (기본값/확인 필요) string RankColor (line 471) |
| 필드/속성 | public string firstMentorIdx (line 472) |
| 필드/속성 | public string ResultCode (line 613) |
| 필드/속성 | public string ResultImage (line 614) |
| 필드/속성 | public string NaverId (line 621) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `GetWrapperHtml()` | public | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:476`) | Y | N | Y |
| `GetResultHtml()` | public | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:517`) | N | N | N |
| `GetDailyHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:549`) | Y | N | N |
| `GetButtonHtml()` | private | string | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:584`) | N | N | N |
| `GetButtonImage()` | private | JsonResult | 데이터를 조회하거나 계산한다 (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:594`) | N | N | N |
| `NaverOAuthById()` | (기본값/확인 필요) | public | Response Result Code (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:622`) | N | N | N |
| `NaverOAuthById()` | (기본값/확인 필요) | public | Response Result Code (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:627`) | N | Y | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: JsonResult

- 파일 경로: `Operation/ItemStockUpload/ItemStockUploadUtil.cs`
- 선언 위치: line 607
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string ResultCode (line 613) |
| 필드/속성 | public string ResultImage (line 614) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: NaverOAuthById

- 파일 경로: `Operation/ItemStockUpload/ItemStockUploadUtil.cs`
- 선언 위치: line 618
- 역할: Response Result Code
- 주요 책임:
  - Response Result Code


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string NaverId (line 621) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `NaverOAuthById()` | (기본값/확인 필요) | public | Response Result Code (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:622`) | N | N | N |
| `NaverOAuthById()` | (기본값/확인 필요) | public | Response Result Code (`Operation/ItemStockUpload/ItemStockUploadUtil.cs:627`) | N | Y | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


## Namespace: FinUp.Stock.App.AlphaBot.Operation.Payment


### Class: BillCard

- 파일 경로: `Operation/Payment/BillCard.cs`
- 선언 위치: line 19
- 역할: Danal 결제 요청/암복호화/파라미터 변환을 담당한다
- 주요 책임:
  - Danal 결제 요청/암복호화/파라미터 변환을 담당한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | protected string ChatApiEnable (line 28) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `RequestPaymentDanalCard()` | public | OrderAutoType | 확인 필요 (`Operation/Payment/BillCard.cs:29`) | Y | Y | Y |
| `GetReturmMessage()` | private | string | 자동결제 리턴 메시지 (`Operation/Payment/BillCard.cs:290`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: BillCardWiseInvest

- 파일 경로: `Operation/Payment/BillCardWiseInvest.cs`
- 선언 위치: line 18
- 역할: Danal 결제 요청/암복호화/파라미터 변환을 담당한다
- 주요 책임:
  - Danal 결제 요청/암복호화/파라미터 변환을 담당한다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `RequestPaymentDanalCardWiseInvest()` | public | OrderAutoType | 확인 필요 (`Operation/Payment/BillCardWiseInvest.cs:27`) | Y | Y | N |
| `GetReturmMessage()` | private | string | 자동결제 리턴 메시지 (`Operation/Payment/BillCardWiseInvest.cs:254`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: BillPhone

- 파일 경로: `Operation/Payment/BillPhone.cs`
- 선언 위치: line 17
- 역할: Danal 결제 요청/암복호화/파라미터 변환을 담당한다
- 주요 책임:
  - Danal 결제 요청/암복호화/파라미터 변환을 담당한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | protected string ChatApiEnable (line 31) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `RequestPaymentDanalPhone()` | public | OrderAutoType | 확인 필요 (`Operation/Payment/BillPhone.cs:32`) | Y | Y | Y |
| `GetReturmMessage()` | private | string | 자동결제 리턴 메시지 (`Operation/Payment/BillPhone.cs:315`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: BillPhoneWiseInvest

- 파일 경로: `Operation/Payment/BillPhoneWiseInvest.cs`
- 선언 위치: line 16
- 역할: Danal 결제 요청/암복호화/파라미터 변환을 담당한다
- 주요 책임:
  - Danal 결제 요청/암복호화/파라미터 변환을 담당한다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `RequestPaymentDanalPhoneWiseInvest()` | public | OrderAutoType | 확인 필요 (`Operation/Payment/BillPhoneWiseInvest.cs:30`) | Y | Y | N |
| `GetReturmMessage()` | private | string | 자동결제 리턴 메시지 (`Operation/Payment/BillPhoneWiseInvest.cs:280`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: FunctionCard

- 파일 경로: `Operation/Payment/FunctionCard.cs`
- 선언 위치: line 27
- 역할: Danal 결제 요청/암복호화/파라미터 변환을 담당한다
- 주요 책임:
  - Danal 결제 요청/암복호화/파라미터 변환을 담당한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string ERC_NETWORK_ERROR (line 40) |
| 필드/속성 | public string ERM_NETWORK (line 42) |
| 필드/속성 | public string CPID (line 49) |
| 필드/속성 | public string CRYPTOKEY (line 50) |
| 필드/속성 | public string IVKEY (line 55) |
| 필드/속성 | public string TEST_AMOUNT (line 56) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `CallCredit()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionCard.cs:65`) | N | Y | N |
| `toEncrypt()` | public | string | 확인 필요 (`Operation/Payment/FunctionCard.cs:134`) | N | N | N |
| `toDecrypt()` | public | string | 확인 필요 (`Operation/Payment/FunctionCard.cs:163`) | N | N | N |
| `hexToByteArray()` | public | byte[] | 확인 필요 (`Operation/Payment/FunctionCard.cs:190`) | N | N | N |
| `str2data()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionCard.cs:201`) | N | N | Y |
| `data2str()` | public | string | 확인 필요 (`Operation/Payment/FunctionCard.cs:231`) | N | N | Y |
| `Parsor()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionCard.cs:259`) | N | N | Y |
| `UrlEncoder()` | public | string | 확인 필요 (`Operation/Payment/FunctionCard.cs:279`) | N | N | N |
| `UrlDecoder()` | public | string | 확인 필요 (`Operation/Payment/FunctionCard.cs:284`) | N | N | N |
| `ArrayToString()` | public | string | 확인 필요 (`Operation/Payment/FunctionCard.cs:293`) | N | N | Y |
| `GetLocalhost()` | public | string | 데이터를 조회하거나 계산한다 (`Operation/Payment/FunctionCard.cs:308`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: FunctionCardWiseInvest

- 파일 경로: `Operation/Payment/FunctionCardWiseInvest.cs`
- 선언 위치: line 27
- 역할: Danal 결제 요청/암복호화/파라미터 변환을 담당한다
- 주요 책임:
  - Danal 결제 요청/암복호화/파라미터 변환을 담당한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string ERC_NETWORK_ERROR (line 40) |
| 필드/속성 | public string ERM_NETWORK (line 42) |
| 필드/속성 | public string CPID_WiseInvest (line 53) |
| 필드/속성 | public string CRYPTOKEY_WiseInvest (line 54) |
| 필드/속성 | public string IVKEY (line 57) |
| 필드/속성 | public string TEST_AMOUNT (line 58) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `CallCreditWiseInvest()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:195`) | N | Y | N |
| `toEncryptWiseInvest()` | public | string | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:264`) | N | N | N |
| `toDecryptWiseInvest()` | public | string | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:293`) | N | N | N |
| `hexToByteArray()` | public | byte[] | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:320`) | N | N | N |
| `str2data()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:331`) | N | N | Y |
| `data2str()` | public | string | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:361`) | N | N | Y |
| `Parsor()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:389`) | N | N | Y |
| `UrlEncoder()` | public | string | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:409`) | N | N | N |
| `UrlDecoder()` | public | string | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:414`) | N | N | N |
| `ArrayToString()` | public | string | 확인 필요 (`Operation/Payment/FunctionCardWiseInvest.cs:423`) | N | N | Y |
| `GetLocalhost()` | public | string | 데이터를 조회하거나 계산한다 (`Operation/Payment/FunctionCardWiseInvest.cs:438`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: FunctionPhone

- 파일 경로: `Operation/Payment/FunctionPhone.cs`
- 선언 위치: line 23
- 역할: Danal 결제 요청/암복호화/파라미터 변환을 담당한다
- 주요 책임:
  - Danal 결제 요청/암복호화/파라미터 변환을 담당한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string ID (line 30) |
| 필드/속성 | public string PWD (line 31) |
| 필드/속성 | public string AMOUNT (line 32) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `CallTeledit()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionPhone.cs:43`) | N | Y | N |
| `Parsor()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionPhone.cs:64`) | N | N | Y |
| `MakeItemInfo()` | public | string | 확인 필요 (`Operation/Payment/FunctionPhone.cs:85`) | N | N | N |
| `MakeParam()` | public | string | 확인 필요 (`Operation/Payment/FunctionPhone.cs:100`) | N | N | Y |
| `Map2Str()` | public | string | 확인 필요 (`Operation/Payment/FunctionPhone.cs:119`) | N | N | Y |
| `toEuckr()` | public | string | 확인 필요 (`Operation/Payment/FunctionPhone.cs:138`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: FunctionPhoneWiseInvest

- 파일 경로: `Operation/Payment/FunctionPhoneWiseInvest.cs`
- 선언 위치: line 23
- 역할: Danal 결제 요청/암복호화/파라미터 변환을 담당한다
- 주요 책임:
  - Danal 결제 요청/암복호화/파라미터 변환을 담당한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string ID_WiseInvest (line 31) |
| 필드/속성 | public string PWD_WiseInvest (line 33) |
| 필드/속성 | public string AMOUNT_WiseInvest (line 34) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `CallTeledit()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionPhoneWiseInvest.cs:45`) | N | Y | N |
| `Parsor()` | public | Hashtable | 확인 필요 (`Operation/Payment/FunctionPhoneWiseInvest.cs:66`) | N | N | Y |
| `MakeItemInfo()` | public | string | 확인 필요 (`Operation/Payment/FunctionPhoneWiseInvest.cs:87`) | N | N | N |
| `MakeParam()` | public | string | 확인 필요 (`Operation/Payment/FunctionPhoneWiseInvest.cs:102`) | N | N | Y |
| `Map2Str()` | public | string | 확인 필요 (`Operation/Payment/FunctionPhoneWiseInvest.cs:121`) | N | N | Y |
| `toEuckr()` | public | string | 확인 필요 (`Operation/Payment/FunctionPhoneWiseInvest.cs:140`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


## Namespace: FinUp.Stock.App.AlphaBot.Properties


### Class: Resources

- 파일 경로: `Properties/Resources.Designer.cs`
- 선언 위치: line 25
- 역할: 지역화된 문자열 등을 찾기 위한 강력한 형식의 리소스 클래스입니다.
- 주요 책임:
  - 지역화된 문자열 등을 찾기 위한 강력한 형식의 리소스 클래스입니다.


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `Resources()` | (기본값/확인 필요) | internal | 확인 필요 (`Properties/Resources.Designer.cs:33`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: Settings

- 파일 경로: `Properties/Settings.Designer.cs`
- 선언 위치: line 17
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) Settings defaultInstance (line 19) |
| 필드/속성 | (기본값/확인 필요) Settings Default (line 21) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


## Namespace: FinUp.Stock.App.AlphaBot.Type


### Enum: AWSServiceType

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 10
- 역할: 데이터 전달/상태 표현용 타입이다
- 주요 책임:
  - 데이터 전달/상태 표현용 타입이다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: AWSServiceStatus

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 15
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: AWSSummaryType

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 22
- 역할: 데이터 전달/상태 표현용 타입이다
- 주요 책임:
  - 데이터 전달/상태 표현용 타입이다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AWSMetricMember

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 34
- 역할: 지표 멤버
- 주요 책임:
  - 지표 멤버


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public int MonitoringAWSMetricIdx (line 39) |
| 필드/속성 | public AWSServiceType Type (line 44) |
| 필드/속성 | public string Metric (line 49) |
| 필드/속성 | public StandardUnit Unit (line 54) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AWSMonitoringMember

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 60
- 역할: 모니터링 서비스 멤버
- 주요 책임:
  - 모니터링 서비스 멤버


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public List<AWSMonitoringValueMember> monitoringValueList (line 90) |
| 필드/속성 | public int MonitoringAWSServiceIdx (line 65) |
| 필드/속성 | public AWSServiceStatus ServiceStatus (line 70) |
| 필드/속성 | public AWSServiceType Type (line 75) |
| 필드/속성 | public string ID (line 80) |
| 필드/속성 | public string Name (line 85) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AWSMonitoringValueMember

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 96
- 역할: 지표당 모니터링 측정값 멤버
- 주요 책임:
  - 지표당 모니터링 측정값 멤버


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public int MonitoringAWSMetricIdx (line 101) |
| 필드/속성 | public AWSServiceType MetricType (line 106) |
| 필드/속성 | public string Metric (line 111) |
| 필드/속성 | public double? Value (line 116) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AWSThresholdMember

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 122
- 역할: 모니터링 임계치 멤버
- 주요 책임:
  - 모니터링 임계치 멤버


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public List<AWSThresholdValueMember> thresholdValueList (line 132) |
| 필드/속성 | public int MonitoringAWSServiceIdx (line 127) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AWSThresholdValueMember

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 138
- 역할: 지표당 임계치 값 멤버
- 주요 책임:
  - 지표당 임계치 값 멤버


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public int MonitoringAWSMetricIdx (line 143) |
| 필드/속성 | public AWSServiceType ServiceType (line 148) |
| 필드/속성 | public double ThresholdValue (line 153) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AWSThresholdLogMember

- 파일 경로: `Type/AWSMonitoringMember.cs`
- 선언 위치: line 159
- 역할: 임계치 로그 멤버
- 주요 책임:
  - 임계치 로그 멤버


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public int MonitoringAWSServiceIdx (line 164) |
| 필드/속성 | public int MonitoringAWSMetricIdx (line 169) |
| 필드/속성 | public double MonitoringValue (line 174) |
| 필드/속성 | public double ThresholdValue (line 179) |
| 필드/속성 | public double ExcessValue (line 184) |
| 필드/속성 | public string ID (line 189) |
| 필드/속성 | public string Name (line 194) |
| 필드/속성 | public string Metric (line 199) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: AlphaBotType

- 파일 경로: `Type/AlphaBotMember.cs`
- 선언 위치: line 12
- 역할: 데이터 전달/상태 표현용 타입이다
- 주요 책임:
  - 데이터 전달/상태 표현용 타입이다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: ActionState

- 파일 경로: `Type/AlphaBotMember.cs`
- 선언 위치: line 94
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AlphaBotMember

- 파일 경로: `Type/AlphaBotMember.cs`
- 선언 위치: line 100
- 역할: 데이터 전달/상태 표현용 타입이다
- 주요 책임:
  - 데이터 전달/상태 표현용 타입이다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public List<OperationType> lstOperationType (line 108) |
| 필드/속성 | public DateTime? _lastExcute (line 168) |
| 필드/속성 | public ActionState _actionState (line 185) |
| 필드/속성 | public int ManualExec (line 113) |
| 필드/속성 | public string DisplayName (line 118) |
| 필드/속성 | public int OIdx (line 123) |
| 필드/속성 | public string _nextTime (line 128) |
| 필드/속성 | public string NextTime (line 133) |
| 필드/속성 | public int Active (line 145) |
| 필드/속성 | public string _activeName (line 151) |
| 필드/속성 | public string ActiveName (line 156) |
| 필드/속성 | public DateTime? LastExcute (line 173) |
| 필드/속성 | public ActionState actionState (line 191) |
| 필드/속성 | public ActionOperation actionOperation (line 207) |
| 필드/속성 | public string LastOnceExecDay (line 212) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `AlphaBotMember()` | (기본값/확인 필요) | public | 생성자 (`Type/AlphaBotMember.cs:217`) | N | N | N |
| `RaisePropertyChanged()` | private | void | Notification UI (`Type/AlphaBotMember.cs:227`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AppAuthTokenMember

- 파일 경로: `Type/ApiSiteHealthCheckMember.cs`
- 선언 위치: line 10
- 역할: 데이터 전달/상태 표현용 타입이다
- 주요 책임:
  - 데이터 전달/상태 표현용 타입이다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string Jwt (line 12) |
| 필드/속성 | public string RefreshToken (line 13) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AppAuthParamMember

- 파일 경로: `Type/ApiSiteHealthCheckMember.cs`
- 선언 위치: line 19
- 역할: ID, PWD 로그인
- 주요 책임:
  - ID, PWD 로그인


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string ID (line 21) |
| 필드/속성 | public string Pwd (line 22) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AppAuthRefreshParamMember

- 파일 경로: `Type/ApiSiteHealthCheckMember.cs`
- 선언 위치: line 25
- 역할: ID, PWD 로그인
- 주요 책임:
  - ID, PWD 로그인


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string Jwt (line 28) |
| 필드/속성 | public string RefreshToken (line 29) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: AppAuthDefaultMember

- 파일 경로: `Type/ApiSiteHealthCheckMember.cs`
- 선언 위치: line 32
- 역할: ID, PWD 로그인
- 주요 책임:
  - ID, PWD 로그인


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string AccessType (line 34) |
| 필드/속성 | public string OSVersion (line 35) |
| 필드/속성 | public string OSType (line 41) |
| 필드/속성 | public string UserIP (line 42) |
| 필드/속성 | public string Browser (line 44) |
| 필드/속성 | public string PushKey (line 46) |
| 필드/속성 | public string DeviceID (line 52) |
| 필드/속성 | public string DeviceModel (line 53) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: ChatMember

- 파일 경로: `Type/ChatMember.cs`
- 선언 위치: line 9
- 역할: 데이터 전달/상태 표현용 타입이다
- 주요 책임:
  - 데이터 전달/상태 표현용 타입이다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: ChatSignalQueue

- 파일 경로: `Type/ChatMember.cs`
- 선언 위치: line 12
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public DateTime? RegDT (line 18) |
| 필드/속성 | public int SignalQueueIdx (line 22) |
| 필드/속성 | public int PortfolioSignalIdx (line 26) |
| 필드/속성 | public int Status (line 30) |
| 필드/속성 | public int TypeItem (line 34) |
| 필드/속성 | public string ItemCode (line 38) |
| 필드/속성 | public int Price (line 42) |
| 필드/속성 | public int SellBuyType (line 46) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: HighLowListParam

- 파일 경로: `Type/ChatMember.cs`
- 선언 위치: line 52
- 역할: 분봉 복수 종목 조회용
- 주요 책임:
  - 분봉 복수 종목 조회용


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | private List<HighLowParam> _params (line 54) |
| 필드/속성 | public List<HighLowParam> Params (line 59) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: HighLowParam

- 파일 경로: `Type/ChatMember.cs`
- 선언 위치: line 71
- 역할: 조회 파라메터
- 주요 책임:
  - 조회 파라메터


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string StockCode (line 77) |
| 필드/속성 | public DateTime? From (line 82) |
| 필드/속성 | public int Ref (line 87) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: HighLowPrice

- 파일 경로: `Type/ChatMember.cs`
- 선언 위치: line 93
- 역할: 고가 저가 반환
- 주요 책임:
  - 고가 저가 반환


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string StockCode (line 98) |
| 필드/속성 | public int High (line 103) |
| 필드/속성 | public int Low (line 108) |
| 필드/속성 | public int Price (line 113) |
| 필드/속성 | public int Ref (line 118) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: OperationTerm

- 파일 경로: `Type/OperationType.cs`
- 선언 위치: line 16
- 역할: Operation 수행 Action
- 주요 책임:
  - Operation 수행 Action


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: ThreadStatusDispay

- 파일 경로: `Type/OperationType.cs`
- 선언 위치: line 22
- 역할: Operation 수행 Action
- 주요 책임:
  - Operation 수행 Action


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: OperationType

- 파일 경로: `Type/OperationType.cs`
- 선언 위치: line 30
- 역할: Operation 수행 Action
- 주요 책임:
  - Operation 수행 Action


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public OperationTerm OperationTerm (line 35) |
| 필드/속성 | public int? iLoopInterval (line 49) |
| 필드/속성 | public TimeSpan? tsOnceTime (line 54) |
| 필드/속성 | public TimeSpan? tsLoopStartTime (line 59) |
| 필드/속성 | public TimeSpan? tsLoopEndTime (line 64) |
| 필드/속성 | public int Active (line 69) |
| 필드/속성 | public int StockOpen (line 74) |
| 필드/속성 | public int OffDay (line 79) |
| 필드/속성 | public int OIdx (line 40) |
| 필드/속성 | public int OTIdx (line 44) |
| 필드/속성 | public string LastOnceExecDay (line 84) |
| 필드/속성 | public bool EnableAlarm (line 89) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `OperationType()` | (기본값/확인 필요) | public | 알림 설정 (`Type/OperationType.cs:90`) | N | N | N |
| `UpdateOperationType()` | public | void | 알림 설정 (`Type/OperationType.cs:105`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: OrderAutoResult

- 파일 경로: `Type/OperationType.cs`
- 선언 위치: line 123
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: OrderAutoType

- 파일 경로: `Type/OperationType.cs`
- 선언 위치: line 132
- 역할: 데이터 전달/상태 표현용 타입이다
- 주요 책임:
  - 데이터 전달/상태 표현용 타입이다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public OrderAutoResult Result (line 135) |
| 필드/속성 | public OrderAutoResult OrderResult (line 136) |
| 필드/속성 | public OrderAutoResult SubscribeResult (line 138) |
| 필드/속성 | public string ResultMsg (line 140) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: OperationTermHistoryType

- 파일 경로: `Type/OperationType.cs`
- 선언 위치: line 148
- 역할: 실행중 상태 체크 [1-시작 | 2-종료 | 3-에러 | 4-Alive]
- 주요 책임:
  - 실행중 상태 체크 [1-시작 | 2-종료 | 3-에러 | 4-Alive]


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Enum: OSType

- 파일 경로: `Type/PushTarget.cs`
- 선언 위치: line 9
- 역할: 데이터 전달/상태 표현용 타입이다
- 주요 책임:
  - 데이터 전달/상태 표현용 타입이다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: PushTarget

- 파일 경로: `Type/PushTarget.cs`
- 선언 위치: line 15
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string Target (line 18) |
| 필드/속성 | public string Msg (line 19) |
| 필드/속성 | public string Url (line 20) |
| 필드/속성 | public string sGroupIdx (line 21) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `PushTarget()` | (기본값/확인 필요) | public | 확인 필요 (`Type/PushTarget.cs:22`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: StringFormat

- 파일 경로: `Type/StringFormat.cs`
- 선언 위치: line 9
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string SALES_STOCKPOINT (line 11) |
| 필드/속성 | (기본값/확인 필요) string IS_SUCCESSFAILURE (line 17) |
| 필드/속성 | (기본값/확인 필요) string STOCKDATA_CHECK (line 25) |
| 필드/속성 | (기본값/확인 필요) string IS_ML_SUCCESSFAILURE (line 30) |
| 필드/속성 | (기본값/확인 필요) string AWS_COMMON_ERROR (line 48) |
| 필드/속성 | (기본값/확인 필요) string AWS_SERVICE_ERROR (line 52) |
| 필드/속성 | (기본값/확인 필요) string AWS_THRESHOLD_EXCESS (line 57) |
| 필드/속성 | (기본값/확인 필요) string ITEMSTOCK_ADDITIONAL_SERVICE (line 62) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


## Namespace: FinUp.Stock.App.AlphaBot.Utils


### Class: Stock

- 파일 경로: `Operation/Stock.cs`
- 선언 위치: line 11
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `GetStockPrice()` | public | StockPrice | 네이버에서 현재가 검색. (`Operation/Stock.cs:16`) | N | Y | Y |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: CommonUtil

- 파일 경로: `Utils/CommonUtil.cs`
- 선언 위치: line 15
- 역할: 외부 연동 또는 공통 유틸리티 기능을 제공한다
- 주요 책임:
  - 외부 연동 또는 공통 유틸리티 기능을 제공한다


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `ClientIP()` | public | string | 클라이언트 IP 주소 (`Utils/CommonUtil.cs:20`) | N | N | Y |
| `getHttpStatus()` | public | HttpStatusCode | Call page by get. (`Utils/CommonUtil.cs:39`) | N | Y | N |
| `getHttpSiteCheck()` | public | HttpWebResponse | Call page by get. (`Utils/CommonUtil.cs:54`) | N | Y | N |
| `getHttpPostResponse()` | public | string | Call page by post (`Utils/CommonUtil.cs:74`) | N | Y | Y |
| `ExecID()` | public | string | 실행 고유 아이디 생성 (`Utils/CommonUtil.cs:121`) | N | N | N |
| `StopWatchStart()` | public | Stopwatch | 실행 고유 아이디 생성 (`Utils/CommonUtil.cs:125`) | N | N | N |
| `StopWatchStop()` | public | string | 실행 고유 아이디 생성 (`Utils/CommonUtil.cs:135`) | N | N | N |
| `IsValidEmail()` | public | bool | 실행 고유 아이디 생성 (`Utils/CommonUtil.cs:148`) | N | N | N |
| `ExtractYoutubeChannelID()` | public | string | 확인 필요 (`Utils/CommonUtil.cs:154`) | N | N | N |
| `IsLiveAsync()` | public | Task<bool> | 확인 필요 (`Utils/CommonUtil.cs:168`) | N | Y | Y |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: EmailHelper

- 파일 경로: `Utils/EmailHelper.cs`
- 선언 위치: line 10
- 역할: 외부 연동 또는 공통 유틸리티 기능을 제공한다
- 주요 책임:
  - 외부 연동 또는 공통 유틸리티 기능을 제공한다


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string SMTP_HOST (line 13) |
| 필드/속성 | (기본값/확인 필요) int SMTP_PORT (line 14) |
| 필드/속성 | (기본값/확인 필요) string SMTP_ID (line 15) |
| 필드/속성 | (기본값/확인 필요) string SMTP_PW (line 16) |
| 필드/속성 | (기본값/확인 필요) string DISPLAY_NAME (line 17) |
| 필드/속성 | public string host (line 127) |
| 필드/속성 | public int port (line 128) |
| 필드/속성 | public string id (line 129) |
| 필드/속성 | public string pw (line 130) |
| 필드/속성 | public string name (line 131) |
| 필드/속성 | public string from (line 132) |
| 필드/속성 | public bool enableSsl (line 133) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `SendMail()` | public | void | Gmail (`Utils/EmailHelper.cs:22`) | N | Y | N |
| `SendMail()` | public | System.Threading.Tasks.Task | Gmail (`Utils/EmailHelper.cs:40`) | N | Y | Y |
| `SendMail()` | public | void | 메시지/메일/푸시를 발송한다 (`Utils/EmailHelper.cs:61`) | N | Y | N |
| `SendMail()` | public | void | 메시지/메일/푸시를 발송한다 (`Utils/EmailHelper.cs:82`) | N | Y | N |
| `SendMail()` | public | void | 메시지/메일/푸시를 발송한다 (`Utils/EmailHelper.cs:103`) | N | Y | Y |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: Account

- 파일 경로: `Utils/EmailHelper.cs`
- 선언 위치: line 124
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string host (line 127) |
| 필드/속성 | public int port (line 128) |
| 필드/속성 | public string id (line 129) |
| 필드/속성 | public string pw (line 130) |
| 필드/속성 | public string name (line 131) |
| 필드/속성 | public string from (line 132) |
| 필드/속성 | public bool enableSsl (line 133) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: LoginResult

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 20
- 역할: 로그인 결과값
- 주요 책임:
  - 로그인 결과값


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public bool IsLogin (line 22) |
| 필드/속성 | public CookieContainer LoginCookie (line 23) |
| 필드/속성 | public NaverOAuth NaverOAuthResult (line 24) |
| 필드/속성 | public string FailReason (line 25) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `LoginResult()` | (기본값/확인 필요) | public | 로그인 결과값 (`Utils/NaverLogin.cs:26`) | N | Y | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: NaverOAuth

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 38
- 역할: 네이버 OAuth token값
- 주요 책임:
  - 네이버 OAuth token값


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string AccessToken (line 41) |
| 필드/속성 | public string RefreshToken (line 43) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: PostReponse

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 49
- 역할: Post Request 응답 값
- 주요 책임:
  - Post Request 응답 값


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public Uri ResponseUri (line 51) |
| 필드/속성 | public string Data (line 52) |
| 필드/속성 | public HttpWebResponse Response (line 53) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: CafeBoardResult

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 59
- 역할: 카페 글 등록 응답 값
- 주요 책임:
  - 카페 글 등록 응답 값


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string FailReason (line 61) |
| 필드/속성 | public bool IsSuccess (line 62) |
| 필드/속성 | public string Contents (line 63) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: OAuthMeObject

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 69
- 역할: OAuth 본인 정보 응답 값
- 주요 책임:
  - OAuth 본인 정보 응답 값


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public string ResultCode (line 72) |
| 필드/속성 | public string Message (line 74) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: OAuthMeInfoObject

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 82
- 역할: OAuth 본인 정보 상세 값
- 주요 책임:
  - OAuth 본인 정보 상세 값


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | public long Id (line 85) |
| 필드/속성 | public string EncyptId (line 87) |
| 필드/속성 | public string ProfileImage (line 89) |
| 필드/속성 | public string Age (line 91) |
| 필드/속성 | public string Gender (line 93) |
| 필드/속성 | public string Nickname (line 95) |
| 필드/속성 | public string Email (line 97) |
| 필드/속성 | public string Name (line 99) |
| 필드/속성 | public string Birthday (line 101) |


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: NaverLoginHelper

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 107
- 역할: 네이버 로그인
- 주요 책임:
  - 네이버 로그인


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string UPLOAD_LIMIT_EXCESS (line 110) |
| 필드/속성 | private string OAuthBaseUrl (line 115) |
| 필드/속성 | private string OAuthAuthorizeUrl (line 116) |
| 필드/속성 | private string OAuthTokenUrl (line 117) |
| 필드/속성 | private string ClientId (line 111) |
| 필드/속성 | private string ClientSecretId (line 113) |
| 필드/속성 | private string RedirectUrl (line 114) |
| 필드/속성 | public string OAuthCustomAuthorizeUrl (line 118) |
| 필드/속성 | public NaverOAuth AuthToken (line 131) |
| 필드/속성 | public bool IsLogin (line 132) |
| 필드/속성 | public bool IsBaseInfoExists (line 133) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `NaverLoginHelper()` | (기본값/확인 필요) | public | 확인 필요 (`Utils/NaverLogin.cs:140`) | N | N | N |
| `SetBaseInfo()` | public | void | 상태 또는 로그/DB 값을 저장한다 (`Utils/NaverLogin.cs:145`) | N | N | N |
| `Login()` | public | Task<LoginResult> | 로그인 시도 (`Utils/NaverLogin.cs:156`) | N | Y | Y |
| `NaverAgreeForm()` | private | Task<Uri> | 확인 필요 (`Utils/NaverLogin.cs:293`) | N | N | Y |
| `AuthorizeUrlToLoginUrl()` | private | Task<PostReponse> | 확인 필요 (`Utils/NaverLogin.cs:330`) | N | N | Y |
| `GetAccessToken()` | public | Task<NaverOAuth> | 데이터를 조회하거나 계산한다 (`Utils/NaverLogin.cs:337`) | N | Y | Y |
| `GetRefreshToken()` | public | Task<NaverOAuth> | 데이터를 조회하거나 계산한다 (`Utils/NaverLogin.cs:354`) | N | Y | Y |
| `AsyncPostRequest()` | public | Task<PostReponse> | 확인 필요 (`Utils/NaverLogin.cs:375`) | N | Y | Y |
| `AsyncPostRequest()` | public | Task<PostReponse> | 확인 필요 (`Utils/NaverLogin.cs:424`) | N | Y | Y |
| `WriteCafeBoard()` | public | Task<CafeBoardResult> | 확인 필요 (`Utils/NaverLogin.cs:476`) | N | Y | Y |
| `AccessTokenCheck()` | public | Task<OAuthMeObject> | access token 만료 확인하기 (`Utils/NaverLogin.cs:561`) | N | Y | Y |
| `GetNaverDynamicKey()` | private | string | 데이터를 조회하거나 계산한다 (`Utils/NaverLogin.cs:622`) | N | Y | Y |
| `GetNaverSessionInfo()` | private | string | 데이터를 조회하거나 계산한다 (`Utils/NaverLogin.cs:665`) | N | Y | N |
| `ConvertPassword()` | private | string | 확인 필요 (`Utils/NaverLogin.cs:693`) | N | N | N |
| `EncryptRSA()` | private | string | 확인 필요 (`Utils/NaverLogin.cs:705`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: LZString

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 740
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string keyStrBase64 (line 743) |
| 필드/속성 | (기본값/확인 필요) string keyStrUriSafe (line 744) |
| 필드/속성 | (기본값/확인 필요) GetCharFromInt f (line 747) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `getBaseValue()` | private | int | 확인 필요 (`Utils/NaverLogin.cs:749`) | N | N | Y |
| `compressToBase64()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:762`) | N | N | N |
| `decompressFromBase64()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:776`) | N | N | N |
| `compressToUTF16()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:783`) | N | N | N |
| `decompressFromUTF16()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:789`) | N | N | N |
| `compressToUint8Array()` | public | byte[] | 확인 필요 (`Utils/NaverLogin.cs:796`) | N | N | Y |
| `decompressFromUint8Array()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:810`) | N | N | Y |
| `compressToEncodedURIComponent()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:829`) | N | N | N |
| `decompressFromEncodedURIComponent()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:835`) | N | N | N |
| `compress()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:843`) | N | N | N |
| `_compress()` | private | string | 확인 필요 (`Utils/NaverLogin.cs:848`) | N | N | Y |
| `decompress()` | public | string | 확인 필요 (`Utils/NaverLogin.cs:1120`) | N | N | N |
| `_decompress()` | private | string | 확인 필요 (`Utils/NaverLogin.cs:1133`) | N | N | Y |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Struct: dataStruct

- 파일 경로: `Utils/NaverLogin.cs`
- 선언 위치: line 1127
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


- 확인된 주요 필드/속성 없음 또는 확인 필요


#### Methods


- 메소드 없음 또는 자동 생성/DTO 타입


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


### Class: ReceiptiOSVerification

- 파일 경로: `Utils/ReceiptiOSVerification.cs`
- 선언 위치: line 12
- 역할: 확인 필요
- 주요 책임:
  - 확인 필요


#### 주요 필드/속성


| 구분 | 내용 |
| --- | --- |
| 필드/속성 | (기본값/확인 필요) string IOS_PRODUCT_URL (line 14) |
| 필드/속성 | (기본값/확인 필요) string IOS_SENDBOX_URL (line 15) |
| 필드/속성 | (기본값/확인 필요) string PACKAGE_NAME (line 16) |
| 필드/속성 | (기본값/확인 필요) int IOS_RV_SUCCESS (line 17) |
| 필드/속성 | (기본값/확인 필요) int IOS_RV_FAIL_RETRY (line 19) |
| 필드/속성 | (기본값/확인 필요) int IOS_RV_FAIL (line 20) |


#### Methods


| Method | 접근 제한자 | 반환 타입 | 설명/위치 | DB 접근 | 외부 호출 | 루프 관련 |
| --- | --- | --- | --- | --- | --- | --- |
| `PurchaseItem()` | public | string | 확인 필요 (`Utils/ReceiptiOSVerification.cs:21`) | N | Y | N |
| `VerifyIOSReceipt()` | public | int | 확인 필요 (`Utils/ReceiptiOSVerification.cs:77`) | N | Y | Y |
| `CheckReceipt()` | public | bool | 상태를 검사한다 (`Utils/ReceiptiOSVerification.cs:179`) | N | N | N |
| `Base64Encode()` | public | string | 확인 필요 (`Utils/ReceiptiOSVerification.cs:198`) | N | N | N |


#### 분석 메모

- 파일 경로와 정적 검색 근거 기준으로 작성했다. 역할이 명확하지 않은 DTO/Enum은 `확인 필요` 또는 데이터 표현용으로 표시했다.


## 분석 한계

- 현재 폴더의 소스와 프로젝트 파일을 기준으로 정적 분석했다. 런타임 DB 데이터, 실제 스케줄 설정값, 외부 API 응답, 배포 서버 상태는 실행 검증하지 않았다.
- `FinUp.Stock.App` 및 `FinUp.Core.Fundamentals`는 프로젝트 참조로 확인되지만 본 리포트의 세부 클래스/메소드 분석 범위는 현재 폴더의 `FinUp.Stock.App.AlphaBot` 소스에 한정했다.
- `DBUtil`, `SqlSender`, `LogWriter`, `NetUtil` 등 핵심 구현 일부는 참조 프로젝트에 있어 커넥션 해제/SQL 생성/로그 경로의 최종 동작은 `확인 필요`로 표시했다.
- 민감값은 원문 대신 `[REDACTED]`로 마스킹했다.
