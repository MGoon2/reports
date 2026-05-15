# 코드 구조 분석

## 모듈/계층 구조

| 계층/모듈 | 주요 파일 | 역할 |
| --- | --- | --- |
| App/UI | App.xaml(.cs), MainWindow.xaml(.cs) | WPF 시작, 타이머/버튼 이벤트, 작업 실행 스케줄링 |
| Operation | Operation/ProcessBase.cs, Process.cs, ProcessUnit.cs | 공통 설정/DB 헬퍼, 업무 배치 메소드 |
| Payment | Operation/Payment/*.cs | Danal 카드/휴대폰 결제 요청/응답 파싱 |
| Push | Operation/Push.cs | Android/iOS/FCM/MQTT 푸시 |
| ItemStockUpload | Operation/ItemStockUpload/ItemStockUploadUtil.cs | 네이버 카페 업로드용 HTML/이미지/로그인 보조 |
| Utils | Utils/*.cs | HTTP/메일/네이버 로그인/iOS 영수증 |
| Type | Type/*.cs | 상태 Enum, DTO, 파라미터 모델 |

## 네임스페이스 목록

| Namespace | 타입 수 | 대표 타입 |
| --- | --- | --- |
| FinUp.Stock.App.AlphaBot | 2 | App, MainWindow |
| FinUp.Stock.App.AlphaBot.Operation | 5 | Process, ProcessBase, Push, PushHandsUp, Process |
| FinUp.Stock.App.AlphaBot.Operation.ItemStockUpload | 6 | ItemStockUploadUtil, HtmlToImageConvert, PublishedItemStockUploadHtml, DailyUploadHtml, JsonResult, NaverOAuthById |
| FinUp.Stock.App.AlphaBot.Operation.Payment | 8 | BillCardWiseInvest, BillPhoneWiseInvest, BillPhone, FunctionCardWiseInvest, FunctionCard, BillCard, FunctionPhoneWiseInvest, FunctionPhone |
| FinUp.Stock.App.AlphaBot.Properties | 2 | Resources, Settings |
| FinUp.Stock.App.AlphaBot.Type | 30 | AppAuthTokenMember, AppAuthParamMember, AppAuthRefreshParamMember, AppAuthDefaultMember, AWSServiceType, AWSServiceStatus, AWSSummaryType, AWSMetricMember, AWSMonitoringMember, AWSMonitoringValueMember, AWSThresholdMember, AWSThresholdValueMember |
| FinUp.Stock.App.AlphaBot.Utils | 14 | Stock, CommonUtil, EmailHelper, Account, LoginResult, NaverOAuth, PostReponse, CafeBoardResult, OAuthMeObject, OAuthMeInfoObject, NaverLoginHelper, LZString |

## 핵심 업무 흐름

| 단계 | 파일/위치 | 확인된 동작 |
| --- | --- | --- |
| 시작 | App.xaml:5 | MainWindow.xaml을 StartupUri로 지정 |
| 초기화 | MainWindow.xaml.cs:73-107 | ObservableCollection, Process, DispatcherTimer, SqlSender 초기화 후 Load 호출 |
| 스케줄 로딩 | MainWindow.xaml.cs:123-191 | DB에서 Operation/OperationTerm 데이터를 조회해 작업 목록 구성 |
| 주기 확인 | MainWindow.xaml.cs:293-335 | 5초 Tick마다 활성 작업과 Loop/Once 조건 확인 |
| 실행 | MainWindow.xaml.cs:678-730 | 새 Thread에서 히스토리 START/END/ERROR 기록 후 actionOperation 호출 |
| 업무 처리 | Operation/ProcessUnit.cs | 결제/푸시/SMS/API/AWS/메일/네이버/포인트 등 작업 수행 |
| 로그 | MainWindow.xaml.cs:840-870 | 화면 로그, Telegram 오류 알림, LogWriter 파일 기록 |

## 주요 패턴

| 분류 | 패턴 | 주요 위치 | 비고 |
| --- | --- | --- | --- |
| DB 접근 | DBUtil/GetDataTable/GetDataRow/ExecQuery 사용 | MainWindow.xaml.cs, Operation/ProcessUnit.cs 전반 | DBUtil 구현은 외부 프로젝트라 Dispose 확인 필요 |
| 외부 API | NetUtil/HttpClient/WebRequest/AWS/YouTube/Firebase/Naver/Bitly | Operation/Process*.cs, Utils/* | 타임아웃/재시도 정책 일부 확인 필요 |
| 로그 | SetLogProcess -> MainWindow.SetLog -> LogWriter.Writer/Telegram | MainWindow.xaml.cs:840-870, Operation/Process.cs:170-174 | 일부 catch는 로그 없음 |
| 예외 처리 | try/catch 다수, throw ex/catch{} 혼재 | MainWindow.xaml.cs, ProcessUnit.cs, Push.cs | 스택 손실/예외 삼킴 위험 |
| 반복/배치 | DispatcherTimer + Thread + DB 스케줄 | MainWindow.xaml.cs:80-90, 293-335 | DB 설정에 따라 Loop/Once 실행 |

## 반복 루프 / 배치 처리 구조 분석

| 반복 방식 | 시작 위치 | 반복 주기 | 종료 조건/비고 |
| --- | --- | --- | --- |
| DispatcherTimer | MainWindow.xaml.cs:80-90, 912-931 | tMainTimer 5초, tObserveTimer 1초, tAlphaBotTimer 1분 | Start/Stop 버튼으로 main/AlphaBot 타이머 제어, ObserveTimer는 Load 후 즉시 시작 |
| Thread | MainWindow.xaml.cs:335, 400, 949 | 조건 만족/수동 실행 시 ProcessStart를 새 Thread로 실행 | member.actionState로 Running이면 skip |
| Thread.Sleep | Operation/ProcessUnit.cs:671-672 | ObserveStockRadar*3*1000ms 대기 | 중간 취소/타임아웃 확인 없음 |
| async void | Operation/ProcessUnit.cs:3200, 5073, 6168, 7468 | 비동기 작업을 void로 실행 | 호출 측에서 await/실패 관찰 어려움 |

## DB 접근 메소드 후보

| 파일 | 메소드 | 근거 |
| --- | --- | --- |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetResultUploadHtml | line 262, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetProfitImage | line 345, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetContentsHtml | line 400, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetProfitRowHtml | line 427, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetReviewHtml | line 446, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetWrapperHtml | line 476, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetDailyHtml | line 549, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetWrapperHtml | line 476, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetDailyHtml | line 549, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/Payment/BillCardWiseInvest.cs | RequestPaymentDanalCardWiseInvest | line 27, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/Payment/BillPhoneWiseInvest.cs | RequestPaymentDanalPhoneWiseInvest | line 30, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/Payment/BillPhone.cs | RequestPaymentDanalPhone | line 32, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/Payment/BillCard.cs | RequestPaymentDanalCard | line 29, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/Process.cs | GetMetric | line 94, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/Process.cs | SetOperationTermHistory | line 149, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessBase.cs | ProcessBase | line 97, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessBase.cs | GetDBUtil | line 140, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessBase.cs | GetDBUtilMySQL | line 152, DBUtil/ExecQuery/GetDataTable 등 |
| MainWindow.xaml.cs | GetDBUtil | line 115, DBUtil/ExecQuery/GetDataTable 등 |
| MainWindow.xaml.cs | Load | line 123, DBUtil/ExecQuery/GetDataTable 등 |
| MainWindow.xaml.cs | UpdateData | line 352, DBUtil/ExecQuery/GetDataTable 등 |
| MainWindow.xaml.cs | ProcessStart | line 678, DBUtil/ExecQuery/GetDataTable 등 |
| MainWindow.xaml.cs | SetOperationTermHistory | line 884, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | OrderAuto | line 51, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | AppPush | line 167, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | SMS | line 348, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | StockCollector | line 399, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | SmsMonitor | line 431, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | SalesStockPoint | line 457, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ItemStockSearchingManual | line 504, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | NaverStockPriceCompare | line 574, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | Alarm | line 745, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiService | line 823, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServiceKakao | line 913, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServiceKakaoContentsReg | line 931, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServiceKakaoContentsApproveCheck | line 1085, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServiceKakaoSalesGet | line 1182, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServiceFuturewizChatInsert | line 1275, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServiceFuturewizChatGet | line 1301, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | KrxData | line 1411, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiVirtualCurrency | line 1739, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyBithumb | line 1954, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyCoinone | line 2048, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyKorbit | line 2140, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyCpdax | line 2228, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyCoinnest | line 2316, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyPoloniex | line 2404, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyBittrex | line 2498, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyUpbit | line 2626, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyBitfinex | line 2726, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | SetApiVirtualCurrencyData | line 2830, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | PriceMornitoring | line 2912, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | HandsUpPush | line 2987, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | HandsUpCoupon | line 3019, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | BatContentsSatisfactionNotify | line 3121, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | BatReviewNotify | line 3150, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | BatCouponUnUsedNotify | line 3174, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | CheckSignalQueue | line 3199, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ClearSignalQueue | line 3292, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetMonitoringMemberList | line 3567, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | InsertMonitoringValue | line 3857, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | GetThresholdList | line 4006, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | InsertThresholdLog | line 4056, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | AWSMonitoringSummaryInsert | line 4139, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServicePublishedItemStockQueueInsert | line 4177, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServicePublishedItemStockToExternalSiteUpload | line 4210, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServiceItemStockToExternalSiteUploadDaily | line 4331, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | MyMentorActivityExpired | line 4404, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | PackageISMentorItemStockUnderCnt | line 4428, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | MyMentorUserSelectCheck | line 4446, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | CheckOrderAutoReceipt | line 4514, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServicePublishedMentorMarketQueueInsert | line 4820, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | ApiServicePublishedMentorMarketToExternalSiteUpload | line 4853, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | InactiveUserEmailSend | line 4957, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | BatInactiveUserQueue | line 5044, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | EmailSend | line 5073, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | EmailSendCompleted | line 5138, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | LGUItemStockSearch | line 5172, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | LGUDailySendMessage | line 5215, DBUtil/ExecQuery/GetDataTable 등 |
| Operation/ProcessUnit.cs | SMSExternalLGUPlus | line 5251, DBUtil/ExecQuery/GetDataTable 등 |

## 외부 API/IO 호출 메소드 후보

| 파일 | 메소드 | 근거 |
| --- | --- | --- |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | GetNaverLogin | line 22, HTTP/SDK/Process/File/Push 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | ImagePostSend | line 93, HTTP/SDK/Process/File/Push 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | NaverOAuthById | line 627, HTTP/SDK/Process/File/Push 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | NaverOAuthById | line 627, HTTP/SDK/Process/File/Push 등 |
| Operation/ItemStockUpload/ItemStockUploadUtil.cs | NaverOAuthById | line 627, HTTP/SDK/Process/File/Push 등 |
| Operation/Payment/BillCardWiseInvest.cs | RequestPaymentDanalCardWiseInvest | line 27, HTTP/SDK/Process/File/Push 등 |
| Operation/Payment/BillPhoneWiseInvest.cs | RequestPaymentDanalPhoneWiseInvest | line 30, HTTP/SDK/Process/File/Push 등 |
| Operation/Payment/BillPhone.cs | RequestPaymentDanalPhone | line 32, HTTP/SDK/Process/File/Push 등 |
| Operation/Payment/FunctionCardWiseInvest.cs | CallCreditWiseInvest | line 195, HTTP/SDK/Process/File/Push 등 |
| Operation/Payment/FunctionCard.cs | CallCredit | line 65, HTTP/SDK/Process/File/Push 등 |
| Operation/Payment/BillCard.cs | RequestPaymentDanalCard | line 29, HTTP/SDK/Process/File/Push 등 |
| Operation/Payment/FunctionPhoneWiseInvest.cs | CallTeledit | line 45, HTTP/SDK/Process/File/Push 등 |
| Operation/Payment/FunctionPhone.cs | CallTeledit | line 43, HTTP/SDK/Process/File/Push 등 |
| Operation/Process.cs | Process | line 78, HTTP/SDK/Process/File/Push 등 |
| Operation/Process.cs | GetMetric | line 94, HTTP/SDK/Process/File/Push 등 |
| Operation/Process.cs | ShortenUrl | line 233, HTTP/SDK/Process/File/Push 등 |
| Operation/Process.cs | GetYoutubeLiveStatus | line 265, HTTP/SDK/Process/File/Push 등 |
| Operation/Push.cs | Push | line 47, HTTP/SDK/Process/File/Push 등 |
| Operation/Push.cs | SendAndroid | line 59, HTTP/SDK/Process/File/Push 등 |
| Operation/Push.cs | SendAndroidV1 | line 99, HTTP/SDK/Process/File/Push 등 |
| Operation/Push.cs | SendIOSFcm | line 144, HTTP/SDK/Process/File/Push 등 |
| Operation/Push.cs | SendIOSFcmV1 | line 175, HTTP/SDK/Process/File/Push 등 |
| Operation/Push.cs | SendMqtt | line 289, HTTP/SDK/Process/File/Push 등 |
| Operation/Push.cs | SendFCM | line 306, HTTP/SDK/Process/File/Push 등 |
| Operation/Push.cs | SendPush | line 416, HTTP/SDK/Process/File/Push 등 |
| Operation/Stock.cs | GetStockPrice | line 16, HTTP/SDK/Process/File/Push 등 |
| Utils/CommonUtil.cs | getHttpStatus | line 39, HTTP/SDK/Process/File/Push 등 |
| Utils/CommonUtil.cs | getHttpSiteCheck | line 54, HTTP/SDK/Process/File/Push 등 |
| Utils/CommonUtil.cs | getHttpPostResponse | line 74, HTTP/SDK/Process/File/Push 등 |
| Utils/CommonUtil.cs | IsLiveAsync | line 168, HTTP/SDK/Process/File/Push 등 |
| Utils/EmailHelper.cs | SendMail | line 22, HTTP/SDK/Process/File/Push 등 |
| Utils/EmailHelper.cs | SendMail | line 40, HTTP/SDK/Process/File/Push 등 |
| Utils/EmailHelper.cs | SendMail | line 61, HTTP/SDK/Process/File/Push 등 |
| Utils/EmailHelper.cs | SendMail | line 82, HTTP/SDK/Process/File/Push 등 |
| Utils/EmailHelper.cs | SendMail | line 103, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | LoginResult | line 26, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | Login | line 156, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | GetAccessToken | line 337, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | GetRefreshToken | line 354, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | AsyncPostRequest | line 375, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | AsyncPostRequest | line 424, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | WriteCafeBoard | line 476, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | AccessTokenCheck | line 561, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | GetNaverDynamicKey | line 622, HTTP/SDK/Process/File/Push 등 |
| Utils/NaverLogin.cs | GetNaverSessionInfo | line 665, HTTP/SDK/Process/File/Push 등 |
| Utils/ReceiptiOSVerification.cs | PurchaseItem | line 21, HTTP/SDK/Process/File/Push 등 |
| Utils/ReceiptiOSVerification.cs | VerifyIOSReceipt | line 77, HTTP/SDK/Process/File/Push 등 |
| App.xaml.cs | App | line 20, HTTP/SDK/Process/File/Push 등 |
| App.xaml.cs | CurrentDomain_UnhandledException | line 30, HTTP/SDK/Process/File/Push 등 |
| App.xaml.cs | Dispatcher_UnhandledException | line 42, HTTP/SDK/Process/File/Push 등 |
| App.xaml.cs | OnExit | line 49, HTTP/SDK/Process/File/Push 등 |
| MainWindow.xaml.cs | GetActionOperation | line 419, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | NaverStockPriceCompare | line 574, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | Alarm | line 745, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | OpenStockRadar | line 784, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | ApiService | line 823, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | ApiServiceKakaoContentsReg | line 931, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | ApiServiceKakaoContentsApproveCheck | line 1085, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | ApiServiceKakaoSalesGet | line 1182, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | ApiServiceFuturewizChatGet | line 1301, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | KrxData | line 1411, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | OpenXingDataRealTime | line 1712, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiExchangeRateUSD | line 1899, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyBithumb | line 1954, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyCoinone | line 2048, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyKorbit | line 2140, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyCpdax | line 2228, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyCoinnest | line 2316, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyPoloniex | line 2404, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyBittrex | line 2498, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyUpbit | line 2626, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetApiVirtualCurrencyBitfinex | line 2726, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | ServerChatLoadCacheCheck | line 3043, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | ServerMainWebLoadCache | line 3091, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | CheckSignalQueue | line 3199, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | SetCheckChatSignal | line 3332, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | ApiSiteHealthCheck | line 3348, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | AWSMonitoring | line 3488, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | GetMonitoringMemberList | line 3567, HTTP/SDK/Process/File/Push 등 |
| Operation/ProcessUnit.cs | IsMonitoringEnable | line 3631, HTTP/SDK/Process/File/Push 등 |

## 추정

- `SqlSender`, `SqlApi`, `SqlProcess` 등은 SQL 문자열 생성기이며 실제 DB 실행은 `DBUtil` 계열이 담당하는 구조로 추정된다.
- `AlphaBotMember.actionOperation`은 `ProcessUnit`의 각 업무 메소드 delegate를 저장해 스케줄러가 실행하는 구조로 추정된다.

## 분석 한계

- 현재 폴더의 소스와 프로젝트 파일을 기준으로 정적 분석했다. 런타임 DB 데이터, 실제 스케줄 설정값, 외부 API 응답, 배포 서버 상태는 실행 검증하지 않았다.
- `FinUp.Stock.App` 및 `FinUp.Core.Fundamentals`는 프로젝트 참조로 확인되지만 본 리포트의 세부 클래스/메소드 분석 범위는 현재 폴더의 `FinUp.Stock.App.AlphaBot` 소스에 한정했다.
- `DBUtil`, `SqlSender`, `LogWriter`, `NetUtil` 등 핵심 구현 일부는 참조 프로젝트에 있어 커넥션 해제/SQL 생성/로그 경로의 최종 동작은 `확인 필요`로 표시했다.
- 민감값은 원문 대신 `[REDACTED]`로 마스킹했다.
