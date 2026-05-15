# 프로젝트 요약

## 확인된 사실

| 항목 | 내용 | 근거 |
| --- | --- | --- |
| 프로젝트 루트 | mnt/c/Dev/FinUp.Stock.App.AlphaBot | 현재 작업 디렉터리 |
| 솔루션 파일 | 없음 | find 결과 `.sln` 0건 |
| 프로젝트 파일 | FinUp.Stock.App.AlphaBot.csproj | 현재 폴더 단일 `.csproj` |
| 프로젝트 유형 | WPF Windows App / WinExe | csproj OutputType=WinExe, WPF ProjectTypeGuids |
| 대상 프레임워크 | v4.7 | csproj TargetFrameworkVersion |
| 시작점 | App.xaml StartupUri=MainWindow.xaml | App.xaml:5 |
| 소스 파일 수 | 30 | csproj Compile 항목 기준 |
| NuGet 패키지 수 | 26 | packages.config |
| 프로젝트 참조 수 | 2 | csproj ProjectReference |

## 솔루션/프로젝트 목록

| 이름 | 경로 | 역할 |
| --- | --- | --- |
| (없음) | 현재 폴더에 `.sln` 파일 없음 | 확인된 사실 |
| FinUp.Stock.App.AlphaBot | FinUp.Stock.App.AlphaBot.csproj | WPF Windows 실행 프로젝트 |

## 주요 기능 요약

| 기능 | 근거 위치 | 설명 |
| --- | --- | --- |
| WPF 타이머 기반 배치 실행 | MainWindow.xaml.cs:80-90, 912-931 | DispatcherTimer로 주기 확인 및 ALIVE 기록 |
| DB 기반 작업 스케줄 로딩 | MainWindow.xaml.cs:123-191, 352-400 | ListOperationTerm 결과로 작업/주기/활성 상태 구성 |
| 작업별 Thread 실행 | MainWindow.xaml.cs:335, 400, 678-730 | ProcessStart가 히스토리 기록 후 ActionOperation 호출 |
| 결제/SMS/푸시/외부 API 연동 | Operation/ProcessUnit.cs, Operation/Payment/*, Operation/Push.cs | 다수 업무 메소드가 DB 큐와 외부 서비스 연동 |
| AWS/YouTube/Bitly/FCM/Naver 연동 | Operation/Process.cs, ProcessUnit.cs, Utils/NaverLogin.cs | 외부 SDK/API 사용 |

## 확인된 진입점

| 위치 | 설명 |
| --- | --- |
| App.xaml:5 | StartupUri="MainWindow.xaml"로 WPF 메인 창을 지정 |
| MainWindow.xaml.cs:60-67 | MainWindow 생성자에서 Loaded 이벤트에 InitializeMember 연결 |
| MainWindow.xaml.cs:73-107 | InitializeMember에서 타이머/DB/Process 객체 초기화 후 Load 호출 |

## 상위 아키텍처

| 영역 | 파일/폴더 | 역할 |
| --- | --- | --- |
| UI/스케줄러 | App.xaml, MainWindow.xaml(.cs) | WPF UI, 타이머, 작업 실행 스레드 관리 |
| Process 계층 | Operation/Process*.cs | 업무 배치/큐 처리/외부 연동 로직 |
| Payment/Push/Utils | Operation/Payment/*, Operation/Push.cs, Utils/* | 결제/알림/HTTP/메일/네이버/영수증 유틸 |
| Type | Type/*.cs | DTO/Enum/상태 모델 |
| 외부 공통 라이브러리 | ../FinUp.Stock.App, ../FinUp.Core.Fundamentals | DBUtil/SQL/Log/Entity 등 제공(세부 확인 필요) |

## 추정

- 프로젝트명과 작업 메소드명을 기준으로, 이 앱은 운영자가 WPF 화면에서 시작/중지하는 주기성 배치/알림/외부연동 봇으로 추정된다.
- 실제 수행 주기와 활성 작업 목록은 DB `ListOperationTerm()` 결과에 의해 결정되므로 런타임 DB 확인이 필요하다.

## 확인 필요

- 외부 참조 프로젝트의 DB 연결/SQL 생성/로그 구현 세부 동작.
- 배포 서버에서 `App.config`와 실제 DB 설정값이 현재 저장소와 동일한지 여부.

## 분석 한계

- 현재 폴더의 소스와 프로젝트 파일을 기준으로 정적 분석했다. 런타임 DB 데이터, 실제 스케줄 설정값, 외부 API 응답, 배포 서버 상태는 실행 검증하지 않았다.
- `FinUp.Stock.App` 및 `FinUp.Core.Fundamentals`는 프로젝트 참조로 확인되지만 본 리포트의 세부 클래스/메소드 분석 범위는 현재 폴더의 `FinUp.Stock.App.AlphaBot` 소스에 한정했다.
- `DBUtil`, `SqlSender`, `LogWriter`, `NetUtil` 등 핵심 구현 일부는 참조 프로젝트에 있어 커넥션 해제/SQL 생성/로그 경로의 최종 동작은 `확인 필요`로 표시했다.
- 민감값은 원문 대신 `[REDACTED]`로 마스킹했다.
