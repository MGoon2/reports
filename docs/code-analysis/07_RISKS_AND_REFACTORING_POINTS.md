# 리스크 및 리팩터링 포인트

## 리스크 요약

| 심각도 | 유형 | 위치 | 근거/영향 | 권고 |
| --- | --- | --- | --- | --- |
| 높음 | 민감정보/자격증명 노출 | App.config, Operation/ProcessBase.cs:27-35, PushCertify/*, *.pfx/*.p12 | DB 연결 문자열/서버 계정/API 키/토큰/인증서 파일이 설정 또는 소스/프로젝트 콘텐츠로 포함되어 있다. 값은 리포트에서 마스킹했다. | 비밀 저장소/환경 변수로 이동하고 저장소 이력 내 노출 여부를 점검한다. |
| 높음 | 예외 삼킴 | MainWindow.xaml.cs:266, 754, 777, 826, 872, 900; Operation/Process.cs:161; Operation/Push.cs 다수 | catch { } 또는 예외 객체 미사용 catch가 있어 장애 원인 추적이 어려울 수 있다. | 최소 ERROR 로그/컨텍스트 기록 후 재시도·스킵·중단 정책을 명시한다. |
| 높음 | Thread 기반 동시성/중복 실행 | MainWindow.xaml.cs:293-335, 352-400, 678-730 | 타이머 Tick에서 새 Thread를 생성하고 actionState로 중복 방지하지만 상태 변경 전후 원자성/락이 없다. 수동 실행과 자동 실행이 경합할 수 있다. | 작업별 lock/SemaphoreSlim/중앙 스케줄러와 CancellationToken 기반 실행 상태 전이를 사용한다. |
| 중간 | Thread.Sleep 기반 대기 | Operation/ProcessUnit.cs:671-672, App.xaml.cs:54 | 작업 스레드를 Sleep으로 점유하며 취소/종료 신호를 확인하지 않는다. | Task.Delay + CancellationToken 또는 스케줄러 재진입 방식으로 변경한다. |
| 중간 | DB 커넥션 Dispose 확인 필요 | MainWindow.xaml.cs:115-128, Operation/ProcessBase.cs:140-157 및 ProcessUnit 전반 | DBUtil/DBUtilMySQL 인스턴스를 즉시 생성해 사용하지만 이 타입의 Dispose/connection 관리 구현은 현재 폴더 외부 참조 프로젝트에 있어 확인 필요하다. | 참조 프로젝트의 DBUtil 구현을 확인하고 IDisposable/using 또는 커넥션 풀 정책을 명확히 한다. |
| 중간 | 트랜잭션 경계/외부 호출 혼재 가능성 | Operation/ProcessUnit.cs:4646-4699 | TransactionScope 내부에서 여러 DB 작업을 수행한다. 외부 호출은 해당 블록 내에서 확인되지 않았지만 범위와 타임아웃 정책은 확인 필요하다. | 트랜잭션 범위를 최소화하고 타임아웃/격리수준/실패 보상 정책을 명시한다. |
| 중간 | 하드코딩된 엔드포인트/경로 | Operation/ProcessBase.cs:33-44, App.config, Operation/ProcessUnit.cs:807/1722 | 운영 API URL, 외부 실행 파일 경로, 일부 토큰/엔드포인트가 코드/설정에 고정되어 있다. | 환경별 설정 파일/배포 파이프라인 변수로 분리하고 검증 로직을 추가한다. |
| 중간 | async void 오류 전파 | Operation/ProcessUnit.cs:3200, 5073, 6168, 7468 | async void 메소드가 작업 메소드로 사용되어 호출자가 완료/실패를 기다릴 수 없다. | Task 반환으로 바꾸고 ProcessStart가 비동기 작업을 관찰하도록 설계한다. |
| 중간 | 외부 프로세스 중복 실행/수명 관리 | Operation/ProcessUnit.cs:784-808, 1712-1723 | StockRadar/XingData 실행 시 기존 프로세스 확인, 종료, 헬스체크가 명확하지 않다. | 프로세스 존재 확인, PID 기록, 종료/재시작 정책을 추가한다. |
| 중간 | 스케줄 설정 DB 의존/검증 부족 | MainWindow.xaml.cs:123-191, 293-335, 742-828 | LoopInterval/OnceTime 등 DB 설정값을 신뢰하며 null/범위 오류는 일부 catch에서 삼켜질 수 있다. | 설정값 유효성 검사와 실패 시 안전 기본값/알림을 추가한다. |

## 필수 점검 항목별 판정

| 점검 항목 | 판정 | 근거 |
| --- | --- | --- |
| 무한 루프 위험 | 낮음~중간 | while(true) 기반 메인 루프는 확인되지 않지만 타이머 기반 지속 실행 구조이며 중지 시 실행 중 Thread 취소는 확인 필요 |
| 예외 삼킴 | 높음 | MainWindow.xaml.cs와 Push/Process 일부에 catch {{ }} 또는 미사용 catch 존재 |
| DB 커넥션 누수 가능성 | 확인 필요 | DBUtil 구현이 참조 프로젝트에 있어 Dispose/using 확인 필요 |
| 트랜잭션 장시간 유지 | 중간 | TransactionScope 사용 구간 존재. 외부 호출 포함은 확인되지 않으나 범위/타임아웃 확인 필요 |
| Thread.Sleep 대기 | 중간 | Operation/ProcessUnit.cs:671-672, App.xaml.cs:54 |
| 동시성 문제 | 높음 | DispatcherTimer Tick + new Thread + actionState 플래그만으로 중복 방지 |
| 하드코딩 설정 | 높음 | ProcessBase의 API URL/토큰성 상수, App.config의 경로/계정/키 |
| 로그 부족 | 중간~높음 | 로그 없는 catch와 throw ex 사용으로 원인 추적/스택 보존 저하 |
| 장애 복구 불명확 | 중간 | 작업별 재시도/중단/스킵 정책이 일관되지 않음 |

## 리팩터링 우선순위

| 우선순위 | 대상 | 개선 방향 |
| --- | --- | --- |
| P0 | 비밀/인증 정보 | 소스/설정/인증서 저장소 분리, 저장소 이력 점검, 배포 시 Secret 주입 |
| P1 | 스케줄러/Thread 실행 | Thread 직접 생성 대신 작업 큐, SemaphoreSlim, CancellationToken, Task 기반 실행으로 전환 |
| P1 | 예외/로그 정책 | catch {{ }} 제거, 컨텍스트 포함 구조화 로그, throw; 사용 |
| P2 | DB 접근 | DBUtil IDisposable 확인, using 적용, 커넥션/트랜잭션 범위 축소 |
| P2 | 외부 호출 | HttpClient 재사용, 타임아웃/재시도/서킷브레이커, API 오류 코드 표준화 |
| P3 | 대형 ProcessUnit 분리 | 결제/푸시/API/AWS/메일/포인트 등 기능별 서비스로 분할 |
| P3 | 설정 검증 | 시작 시 필수 설정/경로/API URL/스케줄 값 검증 및 실패 알림 |

## 확인 필요

- 실제 운영 DB의 Operation/OperationTerm 설정값과 중복 실행 사례.
- 외부 프로젝트의 `DBUtil`, `LogWriter`, `NetUtil`, `SqlSender` 구현 세부.
- 배포 환경에서 인증서/키 파일 접근 권한과 회전 정책.

## 분석 한계

- 현재 폴더의 소스와 프로젝트 파일을 기준으로 정적 분석했다. 런타임 DB 데이터, 실제 스케줄 설정값, 외부 API 응답, 배포 서버 상태는 실행 검증하지 않았다.
- `FinUp.Stock.App` 및 `FinUp.Core.Fundamentals`는 프로젝트 참조로 확인되지만 본 리포트의 세부 클래스/메소드 분석 범위는 현재 폴더의 `FinUp.Stock.App.AlphaBot` 소스에 한정했다.
- `DBUtil`, `SqlSender`, `LogWriter`, `NetUtil` 등 핵심 구현 일부는 참조 프로젝트에 있어 커넥션 해제/SQL 생성/로그 경로의 최종 동작은 `확인 필요`로 표시했다.
- 민감값은 원문 대신 `[REDACTED]`로 마스킹했다.
