# 런타임 흐름 분석

## 프로그램 시작점

| 위치 | 확인된 사실 |
| --- | --- |
| App.xaml:5 | StartupUri="MainWindow.xaml"로 WPF 메인 창을 지정 |
| MainWindow.xaml.cs:60-67 | MainWindow 생성자에서 Loaded 이벤트에 InitializeMember 연결 |
| MainWindow.xaml.cs:73-107 | InitializeMember에서 타이머/DB/Process 객체 초기화 후 Load 호출 |

## 초기화 순서

| 순서 | 단계 | 위치 | 내용 |
| --- | --- | --- | --- |
| 1 | App 생성 | App.xaml.cs:20-29 | TelegramSender 생성, Dispatcher/AppDomain 예외 이벤트 등록 |
| 2 | MainWindow 로드 | MainWindow.xaml.cs:60-67 | Loaded 이벤트에서 InitializeMember 실행 |
| 3 | 멤버 초기화 | MainWindow.xaml.cs:73-107 | Process, Timer, SqlSender 생성 및 Dispatcher 예외 핸들러 설정 |
| 4 | 설정/DB 로딩 | MainWindow.xaml.cs:123-191 | ListOperationTerm 조회, AlphaBotMember/OperationType 구성 |
| 5 | 관찰 타이머 시작 | MainWindow.xaml.cs:190 | tObserveTimer 즉시 시작 |
| 6 | 사용자 시작 | MainWindow.xaml.cs:912-919 | 시작 버튼이 tMainTimer/tAlphaBotTimer 시작 |
| 7 | 주기 확인 | MainWindow.xaml.cs:293-335 | DB 설정 업데이트 후 Loop/Once 조건 판단 |
| 8 | 작업 실행 | MainWindow.xaml.cs:678-730 | 새 Thread에서 START/END/ERROR 히스토리 기록, actionOperation 호출 |
| 9 | 업무 처리 | Operation/ProcessUnit.cs | DB 큐 처리, 외부 API/푸시/메일/결제 수행 |
| 10 | 종료/중지 | MainWindow.xaml.cs:928-934, App.xaml.cs:50-57 | 버튼은 타이머 중지, App 종료 시 Sleep 후 Shutdown |

## 설정 로딩

| 설정 소스 | 사용 위치 | 내용 |
| --- | --- | --- |
| App.config appSettings | MainWindow.xaml.cs:29-31 | DBStockPoint 복호화, Server, ObserveTime 상수 |
| App.config appSettings | Operation/ProcessBase.cs:74-95 | DB/API/경로/키/토큰/푸시/YouTube 설정 로딩 |
| DB OperationTerm | MainWindow.xaml.cs:127-177, 356-395 | 활성 작업, 반복/1회성 주기, 개장일 조건 로딩 |
| PushCertify/firebase*.json | Operation/Process.cs:69, 83-86 | FirebaseApp Credential 파일 |

## 반복 루프 진입점/스케줄 판단

| 항목 | 위치 | 확인된 동작 |
| --- | --- | --- |
| Main Timer | MainWindow.xaml.cs:80-82, 914 | 5초마다 ProcessConfirm 실행 |
| Observe Timer | MainWindow.xaml.cs:84-86, 190 | 1초마다 UI 상태/다음 실행 시간 표시 |
| AlphaBot Alive Timer | MainWindow.xaml.cs:88-90, 915 | 1분마다 ALIVE 히스토리 기록 |
| Loop 조건 | MainWindow.xaml.cs:742-757 | LastExcute + LoopInterval <= 현재시각이면 실행 |
| Once 조건 | MainWindow.xaml.cs:787-827 | 설정 시각 ±5초, 당일 중복 실행 방지 |
| 중복 방지 | MainWindow.xaml.cs:302-303, 702, 720 | member.actionState가 Running이면 skip, finally에서 Stop |

## DB 조회/처리 흐름

| 단계 | 위치 | 설명 |
| --- | --- | --- |
| 스케줄 조회 | MainWindow.xaml.cs:127-128, 356-357 | ListOperationTerm SQL을 DBUtil.GetDataTable로 실행 |
| 작업 시작 기록 | MainWindow.xaml.cs:693-703 | OperationTermHistory START 기록 및 LastExecDT 업데이트 |
| 작업별 큐 조회/처리 | Operation/ProcessUnit.cs | 결제/푸시/SMS/API 등 각 메소드에서 DB 큐 조회 후 처리 |
| 작업 종료/오류 기록 | MainWindow.xaml.cs:707-729 | ERROR/END 히스토리 기록 |
| 로그 기록 | MainWindow.xaml.cs:840-870 | 화면/Telegram/LogWriter 기록 |

## 외부 호출 흐름

| 분류 | 주요 위치 | 내용 |
| --- | --- | --- |
| 결제 | Operation/Payment/*.cs, Operation/ProcessUnit.cs:51-156 | Danal 카드/휴대폰 자동결제 |
| 푸시 | Operation/Push.cs, Operation/ProcessUnit.cs:167-337 | Android/iOS FCM/APNS/MQTT 발송 |
| SMS | Operation/ProcessUnit.cs:348-388 | 외부 메시지 DB로 SMS insert |
| API 큐 | Operation/ProcessUnit.cs:823 이후 다수 | Kakao/Futurewiz/StockData/StockPoint/Chat API 연동 |
| AWS | Operation/Process.cs:80-88, ProcessUnit.cs:3488-4056 | CloudWatch/EC2/RDS 모니터링 |
| 외부 프로세스 | Operation/ProcessUnit.cs:784-808, 1712-1723 | StockRadar/XingData 실행 |
| YouTube/Bitly/Naver | Operation/Process.cs:233-302, Utils/NaverLogin.cs | 단축 URL, 라이브 상태, 네이버 카페/로그인 |

## 예외 처리/종료 조건

| 항목 | 위치 | 확인된 동작/리스크 |
| --- | --- | --- |
| 전역 Dispatcher 예외 | App.xaml.cs:43-48 | Telegram 전송 후 e.Handled=true |
| ProcessStart 예외 | MainWindow.xaml.cs:707-717 | ERROR 히스토리 기록 후 finally에서 END 기록 |
| 작업 메소드 예외 | Operation/ProcessUnit.cs 전반 | SetLogProcess 후 throw ex 또는 continue 혼재 |
| 로그 없는 catch | MainWindow.xaml.cs:266, 754, 777, 826, 872, 900 | 예외 삼킴 위험 |
| 중지 버튼 | MainWindow.xaml.cs:928-934 | 타이머만 중지, 이미 실행 중인 Thread 취소는 확인되지 않음 |
| 앱 종료 | App.xaml.cs:50-57 | Thread.Sleep(1000) 후 Shutdown |

## 확인 필요

- 작업 Thread가 장시간 실행 중일 때 앱 종료/중지 버튼이 실제 작업을 중단하는지 확인 필요.
- DB 스케줄 값이 비정상(null/음수/과도한 interval)일 때 안전 동작 확인 필요.

## 분석 한계

- 현재 폴더의 소스와 프로젝트 파일을 기준으로 정적 분석했다. 런타임 DB 데이터, 실제 스케줄 설정값, 외부 API 응답, 배포 서버 상태는 실행 검증하지 않았다.
- `FinUp.Stock.App` 및 `FinUp.Core.Fundamentals`는 프로젝트 참조로 확인되지만 본 리포트의 세부 클래스/메소드 분석 범위는 현재 폴더의 `FinUp.Stock.App.AlphaBot` 소스에 한정했다.
- `DBUtil`, `SqlSender`, `LogWriter`, `NetUtil` 등 핵심 구현 일부는 참조 프로젝트에 있어 커넥션 해제/SQL 생성/로그 경로의 최종 동작은 `확인 필요`로 표시했다.
- 민감값은 원문 대신 `[REDACTED]`로 마스킹했다.
