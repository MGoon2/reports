# AlphaBot 레거시 윈도우앱 반복 처리 구조 분석 보고서

분석은 읽기 전용으로 수행했으며 코드는 수정하지 않았습니다.
완료 감사 기준: 4개 대상 프로젝트의 진입점, 앱 유형, 루프/스레드/DB/예외/로그/설정/중복 위험을 파일 경로·클래스·메서드·SQL/SP·설정 키 근거로 대조했습니다.

———

  ## 1. 시스템 요약

  | 프로젝트                       | 앱 유형                         | 주요 역할                                     | 반복 처리 기준                                                 | 주요 DB/외부 연동                               |
  | ------------------------------ | ------------------------------- | --------------------------------------------- | -------------------------------------------------------------- | ----------------------------------------------- |
  | FinUp.CollectData.App.AlphaBot | WPF, net6.0-windows7.0, WinExe  | 뉴스/지수/테마/크롤러 처리                    | SystemData.dbo.T_Operation, T_OperationTerm의 SvcType = 'Data' | DBThemeRadar, MongoDB, Kafka, Telegram          |
  | FinUp.Finance.App.AlphaBot     | WPF, net6.0-windows, WinExe     | 랭킹, 투자 RSS, 증시 일정                     | SvcType = 'Finance'                                            | DBStockData, 파일 서버                          |
  | FinUp.Radar.App.AlphaBot       | WPF, .NET Framework 4.7, WinExe | 테마레이더, 푸시, 공시, 뉴스, 결제/알림       | SvcType = 'ThemeRadar'                                         | DBThemeRadar, MongoDB, Redis, API, Telegram     |
  | FinUp.Stock.App.AlphaBot       | WPF, .NET Framework 4.7, WinExe | StockPoint 배치, 결제, Push, AWS, 외부 업로드 | SvcType = 'StockPoint'                                         | DBStockPoint, AWS, Firebase, Telegram, 외부 API |

  근거

  - WPF 진입: 각 App.xaml의 StartupUri="MainWindow.xaml"
      - FinUp.CollectData.../App.xaml:5
      - FinUp.Finance.../App.xaml:5
      - FinUp.Radar.../App.xaml:5
      - FinUp.Stock.../App.xaml:5
  - Program.cs는 4개 프로젝트에서 발견되지 않음.
  - WPF/WinExe:
      - CollectData: FinUp.CollectData...csproj:5-7
      - Finance: FinUp.Finance...csproj:4-6
      - Radar: FinUp.Radar...csproj:8-13
      - Stock: FinUp.Stock...csproj:8-14

  ———

  ## 2. 실행 진입점

  | 프로젝트    | 진입점                     | 메인 화면/초기화                                   | 자동 시작 여부                                      |
  | ----------- | -------------------------- | -------------------------------------------------- | --------------------------------------------------- |
  | CollectData | App.xaml → MainWindow.xaml | MainWindow.xaml에서 MainViewModel DataContext 생성 | 수동 시작 버튼 필요                                 |
  | Finance     | App.xaml → MainWindow.xaml | MainWindow.xaml에서 MainViewModel DataContext 생성 | 수동 시작 버튼 필요                                 |
  | Radar       | App.xaml → MainWindow.xaml | MainWindow.Loaded에서 InitializeMember() 호출      | AppSetting.ConfigServerType == "REAL"이면 자동 시작 |
  | Stock       | App.xaml → MainWindow.xaml | MainWindow.Loaded에서 InitializeMember() 호출      | 수동 시작 버튼 필요                                 |

  근거

  - CollectData/Finance DataContext:
      - FinUp.CollectData.../MainWindow.xaml:10-12
      - FinUp.Finance.../MainWindow.xaml:10-12
  - Radar 초기화/자동 시작:
      - FinUp.Radar.App.AlphaBot/MainWindow.xaml.cs:86-99
  - Stock 초기화:
      - FinUp.Stock.App.AlphaBot/MainWindow.xaml.cs:60-67

  ———

  ## 3. 루프 구조

  | 프로젝트    | 루프 시작 위치                   | 방식            |                                       주기 | 작업 실행 방식                                     | 중첩 위험 |
  | ----------- | -------------------------------- | --------------- | -----------------------------------------: | -------------------------------------------------- | --------- |
  | CollectData | MainViewModel.CommandStart_Click | DispatcherTimer | AlphaBot.ObServeTime 설정값, Release는 5초 | new Thread(ProcessStart) 후 내부에서 또 new Thread | High      |
  | Finance     | MainViewModel.CommandStart_Click | DispatcherTimer |                                   5초 고정 | new Thread(ProcessStart) 후 내부에서 또 new Thread | High      |
  | Radar       | MainWindow.btnStart_Click        | DispatcherTimer |                                        5초 | new Thread(ProcessStart) 후 내부에서 또 new Thread | High      |
  | Stock       | MainWindow.btnStart_Click        | DispatcherTimer |                            5초 + Alive 1분 | new Thread(ProcessStart)                           | Medium    |

  근거

  - CollectData:
      - 타이머 생성: MainViewModel.cs:43-44
      - 시작/중지: MainViewModel.cs:137-149
      - 작업 스레드 생성: AlphaBotBiz.cs:290, 내부 재스레드 AlphaBotBiz.cs:325-331
  - Finance:
      - 타이머 생성: MainViewModel.cs:42-43
      - 작업 스레드: AlphaBotBiz.cs:271, 내부 재스레드 AlphaBotBiz.cs:306-312
  - Radar:
      - 타이머 생성: MainWindow.xaml.cs:123-139
      - 작업 스레드: MainWindow.xaml.cs:454, 내부 재스레드 MainWindow.xaml.cs:712-718
  - Stock:
      - 타이머 생성: MainWindow.xaml.cs:80-90
      - 작업 스레드: MainWindow.xaml.cs:335
      - Alive: MainWindow.xaml.cs:269-287, 시작 MainWindow.xaml.cs:912-918

  ———

  ## 4. DB 처리 흐름

  ### 공통 Operation 조회 흐름

  T_Operation + T_OperationTerm 조회
  → Active / TermType / LoopInterval / OnceTime / LoopStartTime / LoopEndTime / StockOpen / OffDay 로 실행 여부 판단
  → LastExecDT 업데이트
  → 작업 실행
  → OperationTermHistory START / ERROR / STOP 또는 END 기록

  | 프로젝트    | 조회 SQL/SP                                  | 조회 조건                                       | 상태/이력 SP                                                         |
  | ----------- | -------------------------------------------- | ----------------------------------------------- | -------------------------------------------------------------------- |
  | CollectData | SqlOperationDac.ListOperationTerm("Data")    | TOT.DisplayAlphabot = 1, TOT.SvcType = @SvcType | SystemData.dbo.USP_Operation_Update, USP_OperationTermHistory_Insert |
  | Finance     | SqlOperationDao.ListOperationTerm("Finance") | 동일, SvcType = @SvcType                        | 동일                                                                 |
  | Radar       | SqlOperation.ListOperationTerm()             | TOT.SvcType = 'ThemeRadar'                      | 동일                                                                 |
  | Stock       | SqlSender.ListOperationTerm()                | TOT.SvcType = 'StockPoint'                      | 동일                                                                 |

  근거

  - CollectData DAO:
      - FinUp.Core.DS.Dac/.../SqlOperationDac.cs:15-49
      - 상태/이력 SP: SqlOperationDac.cs:57-90
  - Finance DAO:
      - SqlOperationDao.cs:19-54
      - 상태/이력 SP: SqlOperationDao.cs:61-94
  - Radar SQL:
      - FinUp.Radar/Sql/SqlOperation.cs:11-47
      - 이력/업데이트: SqlOperation.cs:90-136
  - Stock SQL:
      - FinUp.Stock.App/Sql/SqlSender.cs:12-47
      - 업데이트: SqlSender.cs:82-102
      - 이력: SqlSender.cs:382-405

  ———

  ## 5. 반복 업무 상태 흐름

  ### 확인된 상태 흐름

  DB 설정 조회
  → 메모리 상태 Stop
  → 실행 조건 충족
  → LastExecDT 선 업데이트
  → actionState = Running
  → 업무 실행
  → 성공: OperationTermHistory STOP/END
  → 실패: OperationTermHistory ERROR 후 STOP/END
  → actionState = Stop

  | 프로젝트    | 상태 저장                                             | 처리 전 상태 변경                                  | 처리 후 상태 변경 | 실패 기록  |
  | ----------- | ----------------------------------------------------- | -------------------------------------------------- | ----------------- | ---------- |
  | CollectData | 메모리 member.actionState, DB LastExecDT, 이력 테이블 | LastExecDT 먼저 업데이트                           | STOP 이력         | ERROR 이력 |
  | Finance     | 동일                                                  | LastExecDT 먼저 업데이트                           | STOP 이력         | ERROR 이력 |
  | Radar       | 동일                                                  | LastExecDT 먼저 업데이트                           | STOP 이력         | ERROR 이력 |
  | Stock       | 동일                                                  | ProcessStart 내부에서 START 후 LastExecDT 업데이트 | END 이력          | ERROR 이력 |

  근거

  - CollectData: AlphaBotBiz.cs:263-290, 337-368
  - Finance: AlphaBotBiz.cs:244-271, 318-348
  - Radar: MainWindow.xaml.cs:424-454, 1001-1031
  - Stock: MainWindow.xaml.cs:678-730

  ———

  ## 6. 중복 처리 위험

  | 위험도   | 위치                        | 시나리오                                                                            | 원인                                                                                                           |
  | -------- | --------------------------- | ----------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------- |
  | Critical | 4개 공통                    | 같은 DB 설정을 여러 앱 인스턴스가 동시에 읽고 같은 작업 실행                        | T_Operation.LastExecDT 업데이트가 원자적 선점이 아님. WHERE LastExecDT = 이전값 같은 경쟁 방지 조건 확인 안 됨 |
  | High     | CollectData/Finance/Radar   | Timer tick 또는 ManualExec가 작업 시작 직전/중간에 중복 실행                        | actionState는 메모리 값이며 lock/interlocked 없음                                                              |
  | High     | CollectData/Finance/Radar   | 작업 실패/프로세스 종료 후 LastExecDT만 갱신되어 실제 처리가 누락                   | 작업 실행 전에 LastExecDT 업데이트                                                                             |
  | Medium   | Stock                       | 작업 중 UI Stop을 눌러도 실행 중 Thread는 취소되지 않음                             | CancellationToken 없음                                                                                         |
  | Medium   | CollectData/Radar 일부 Unit | Task.Run(async...) fire-and-forget 후 외부 전송 실패가 본 처리 결과와 분리될 가능성 | await 없이 비동기 작업 분리                                                                                    |

  근거

  - 실행 전 LastExecDT 업데이트:
      - CollectData: AlphaBotBiz.cs:284-290
      - Finance: AlphaBotBiz.cs:265-271
      - Radar: MainWindow.xaml.cs:447-454
  - 메모리 상태만 확인:
      - CollectData: AlphaBotBiz.cs:227-230
      - Finance: AlphaBotBiz.cs:208-211
      - Radar: MainWindow.xaml.cs:388-391
      - Stock: MainWindow.xaml.cs:300-303
  - fire-and-forget 예:
      - CollectData CrawlerSite.cs에서 다수 Task.Run(async...) 검색됨
      - Radar NewsTelegramMessage.cs, ThemeLogSendMessage.cs에서 Task.Run(async...) 검색됨

  ———

  ## 7. 예외/복구 구조

  | 프로젝트    | 예외 처리                                    | 루프 지속 여부                    | 문제점                                                |
  | ----------- | -------------------------------------------- | --------------------------------- | ----------------------------------------------------- |
  | CollectData | 다수 catch { }, RunTask는 NLog/Console 기록  | Timer 자체는 계속 돌 가능성 높음  | 예외 삼킴, 원인 추적 어려움                           |
  | Finance     | 다수 catch { }, Console 출력                 | Timer 자체는 계속 돌 가능성 높음  | 영구 로그 부족                                        |
  | Radar       | 일부 Trace/화면 로그, App 전역 예외 핸들러   | UI Dispatcher 예외는 handled 처리 | 작업 Thread 내부 예외는 이력 누락 가능                |
  | Stock       | 전역 예외 Telegram, 작업은 try/catch/finally | 상대적으로 복구 구조 명확         | 일부 async void/fire-and-forget 작업은 완료 추적 약함 |

  근거

  - CollectData catch { }: MainViewModel.cs:64-66, 76-90, AlphaBotBiz.cs:301-305
  - Finance catch { }: MainViewModel.cs:63-65, AlphaBotBiz.cs:283-286
  - Radar 전역 예외 처리: App.xaml.cs:24-54
  - Stock 전역 예외 처리: App.xaml.cs:20-48
  - Stock 작업 finally 복구: MainWindow.xaml.cs:707-730

  ———

  ## 8. DB 부하 위험

  | 위험도 | 위치                             | 근거                                                       | 설명                                                           |
  | ------ | -------------------------------- | ---------------------------------------------------------- | -------------------------------------------------------------- |
  | High   | 4개 공통 Operation 조회          | 5초마다 T_Operation, T_OperationTerm, T_StockCalendar 조회 | 앱 인스턴스가 늘면 공통 메타 DB 부하 증가                      |
  | High   | WITH(NOLOCK) 사용                | Collect/Finance/Radar/Stock Operation 조회 SQL             | Dirty read로 잘못된 실행 조건을 읽을 수 있음                   |
  | Medium | DBUtil 재사용/수동 Close         | DBUtil은 SqlConnection 필드 보유 후 메서드마다 Open/Close  | Dispose 패턴 일관성 및 예외 시 리더 null 가능성 추가 점검 필요 |
  | Medium | 장시간 작업 중 DB 상태 선점 부재 | LastExecDT만 갱신                                          | 장애 시 재처리/누락 판단 어려움                                |

  근거

  - WITH(NOLOCK):
      - Collect/Finance: SqlOperationDac.cs:36-43, SqlOperationDao.cs:40-47
      - Radar: SqlOperation.cs:33-40
      - Stock: SqlSender.cs:34-40
  - DBUtil Close:
      - Core DBUtil ExecQuery: FinUp.Core.Data/Util/DBUtil.cs:100-131
      - Stock DBUtil ExecQuery: FinUp.Stock.App/Util/DBUtil.cs:110-145

  ———

  ## 9. 운영 장애 가능성이 높은 코드

  1. 중복 실행 방지 부재
      - DB 원자 선점 없이 LastExecDT 업데이트 후 Thread 실행.
      - 다중 인스턴스/수동 실행/Timer 경합에서 중복 또는 누락 가능.
  2. 예외 삼킴
      - catch { }가 많아 장애 원인 추적이 어렵다.
      - 특히 CollectData/Finance는 화면 로그 외 영구 로그 근거가 약한 부분 존재.
  3. Thread 직접 생성
      - new Thread 반복 생성, 취소/조인/백오프 없음.
      - Stop 버튼은 Timer만 멈추며 실행 중 작업 종료 보장 없음.
  4. 작업 전 LastExecDT 갱신
      - 외부 연동/DB 작업 실패 전 이미 실행 완료처럼 다음 실행이 밀릴 수 있음.
  5. 설정 파일 민감정보
      - Stock App.config에 AWS/Naver/API/DB 관련 키가 설정값으로 존재.
      - 근거: FinUp.Stock.App.AlphaBot/App.config:66-86
      - 보고서에는 값은 재기재하지 않음.

  ———

  ## 10. 리팩터링 우선순위

  | 우선순위 | 개선안                                                                                      | 운영 영향             | 롤백 가능성                                     |
  | -------: | ------------------------------------------------------------------------------------------- | --------------------- | ----------------------------------------------- |
  |        1 | DB 기반 원자적 선점 추가: Pending → Running → Done/Error 상태 컬럼 또는 USP_Operation_Claim | 중복 실행 방지 핵심   | SP/컬럼 추가 필요, 기능 플래그로 점진 적용 권장 |
  |        2 | LastExecDT 갱신 시점을 “작업 시작”과 “작업 완료”로 분리                                     | 누락/재처리 판단 개선 | 이력 테이블 활용 가능                           |
  |        3 | catch { } 제거 후 공통 로그 기록                                                            | 장애 추적성 향상      | 코드 변경 범위 작음                             |
  |        4 | new Thread → Task + CancellationToken + 실행 registry                                       | 종료/중복 제어 개선   | 단계적 적용 필요                                |
  |        5 | 5초 Polling 메타 조회 캐시/변경 감지                                                        | DB 부하 감소          | 캐시 TTL로 안전 적용 가능                       |
  |        6 | 설정 민감정보 분리                                                                          | 보안 위험 감소        | 배포 파이프라인 영향 확인 필요                  |

  ———

  ## 11. 다음 분석 단계

  추가 확인 필요 항목입니다.

  1. DB 스키마/SP 확인
      - SystemData.dbo.USP_Operation_Update
      - SystemData.dbo.USP_OperationTermHistory_Insert
      - SystemData.dbo.T_Operation
      - SystemData.dbo.T_OperationTerm
      - SystemData.dbo.T_OperationTermHistory
  2. 실제 운영 배포 구조
      - 동일 AlphaBot을 여러 서버/인스턴스에서 동시에 실행하는지.
      - Server, ServerType, SvcType 분리 기준.
  3. 작업 단위별 상세 데이터 상태
      - 주문/결제/푸시/크롤링 Unit 내부에서 대상 데이터가 대기 → 처리중 → 완료/실패 상태를 갖는지 추가 추적 필요.
  4. 운영 로그 샘플
      - OperationTermHistory START/ERROR/STOP/END가 실제로 쌍을 이루는지.
      - ERROR 후 재시도 정책이 있는지.
  5. 성능/락 확인
      - T_Operation, T_OperationTerm, 각 Queue 테이블의 인덱스.
      - WITH(NOLOCK) 제거 가능성 및 영향.