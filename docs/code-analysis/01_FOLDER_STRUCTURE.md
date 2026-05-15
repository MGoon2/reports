# 폴더 구조 분석

## 확인된 최상위 구조

| 폴더/파일 | 역할 | 파일 수 | C# 파일 수 | 주요 파일 예시 |
| --- | --- | --- | --- | --- |
| DLL | 로컬 외부 DLL 참조 | 4 | 0 | DLL/Interop.DANALCOMLib.dll, DLL/M2Mqtt.Net.dll, DLL/Newtonsoft.Json.dll, DLL/Telegram.Bot.dll |
| Operation | 배치/업무 처리 로직, 결제, 푸시, 외부 API 연동 | 21 | 14 | Operation/Process.cs, Operation/ProcessBase.cs, Operation/ProcessUnit.cs, Operation/Push.cs, Operation/Stock.cs |
| Properties | WPF/어셈블리 리소스 및 설정 디자이너 파일 | 5 | 3 | Properties/AssemblyInfo.cs, Properties/Resources.Designer.cs, Properties/Resources.resx, Properties/Settings.Designer.cs, Properties/Settings.settings |
| PushCertify | 푸시/FCM 인증서 및 키 파일(민감 파일) | 3 | 0 | PushCertify/firebase-stockpoint-firebase-adminsdk-iw1k8-dfc66935df.json, PushCertify/stockpoint_adhoc.p12, PushCertify/stockpoint_dev.p12 |
| Type | 업무 DTO/Enum/상태 모델 | 7 | 7 | Type/AlphaBotMember.cs, Type/ApiSiteHealthCheckMember.cs, Type/AWSMonitoringMember.cs, Type/ChatMember.cs, Type/OperationType.cs |
| Utils | HTTP/메일/네이버 로그인/영수증 검증 등 유틸리티 | 4 | 4 | Utils/CommonUtil.cs, Utils/EmailHelper.cs, Utils/NaverLogin.cs, Utils/ReceiptiOSVerification.cs |
| doc-spec | 분석 산출물 예시/템플릿 문서 | 4 | 0 | doc-spec/LOOP.md, doc-spec/NAMESPACE_CLASS_METHOD_REPORT.md, doc-spec/PROJECT_INVENTORY.json, doc-spec/PROJECT_RELATION.md |
| docs | 확인 필요 | 9 | 0 | docs/code-analysis/00_PROJECT_SUMMARY.md, docs/code-analysis/01_FOLDER_STRUCTURE.md, docs/code-analysis/02_PROJECT_SETTINGS.md, docs/code-analysis/03_CODE_STRUCTURE.md, docs/code-analysis/04_NAMESPACE_CLASS_METHOD_REPORT.md |

## 루트 주요 파일

| 파일 | 역할 | 근거/비고 |
| --- | --- | --- |
| FinUp.Stock.App.AlphaBot.csproj | WPF 프로젝트 정의, 참조/컴파일 항목 관리 | csproj |
| App.xaml / App.xaml.cs | 애플리케이션 시작점 및 전역 예외 처리 | App.xaml:5, App.xaml.cs |
| MainWindow.xaml / MainWindow.xaml.cs | 운영 UI, 타이머 스케줄러, 작업 실행 | MainWindow.xaml.cs |
| App.config | 런타임 설정, API URL, DB/인증 관련 설정 | 값은 마스킹 필요 |
| packages.config | NuGet 패키지 목록 | 26개 패키지 |
| DLL/*.dll | 로컬 DLL 참조 | Interop.DANALCOMLib, M2Mqtt.Net, Newtonsoft.Json, Telegram.Bot |
| PushCertify/* | 푸시/FCM 인증 관련 파일 | 민감 파일로 취급 |

## 실행 흐름상 중요한 파일

| 파일 | 중요 이유 |
| --- | --- |
| App.xaml | StartupUri로 MainWindow 지정 |
| MainWindow.xaml.cs | 타이머 생성/시작/중지, DB 스케줄 로딩, 작업 Thread 실행 |
| Operation/ProcessBase.cs | 설정 로딩, SQL/DB/Push 헬퍼 초기화 |
| Operation/Process.cs | AWS/FCM/Bitly/YouTube 등 공통 외부 연동 초기화 및 유틸 |
| Operation/ProcessUnit.cs | 대부분의 배치 업무 메소드 구현 |
| Operation/Payment/* | Danal 카드/휴대폰 결제 처리 |
| Operation/Push.cs | FCM/APNS/MQTT 푸시 발송 |
| Utils/* | HTTP, 메일, Naver 로그인, iOS 영수증 검증 유틸 |

## 분석 제외 대상

| 경로/패턴 | 사유 | 처리 |
| --- | --- | --- |
| bin/, obj/ | 빌드 산출물 | 분석 제외 |
| .vs/ | Visual Studio 캐시 | 분석 제외 |
| packages/, ../Solutions/packages | NuGet 패키지 산출물 | 소스 분석 제외, 참조 정보만 확인 |
| node_modules/ | Node 패키지 | 현재 없음/분석 제외 |
| *.log | 로그 파일 | 분석 제외 |
| docs/code-analysis/ | 이번 분석 산출물 | 생성 대상 |

## 생성된 분석 산출물

- `docs/code-analysis/` 하위 Markdown 8개 및 `PROJECT_INVENTORY.json`.

## 추정/확인 필요

- `doc-spec/`는 기존 분석 예시/템플릿으로 보이며 런타임 소스는 아니다(확인 필요).
- `Operation/MailForm`, `Operation/InactiveUser`, `Operation/PointDisappearanceUser`의 HTML 템플릿은 메일/알림 본문 템플릿으로 추정된다.

## 분석 한계

- 현재 폴더의 소스와 프로젝트 파일을 기준으로 정적 분석했다. 런타임 DB 데이터, 실제 스케줄 설정값, 외부 API 응답, 배포 서버 상태는 실행 검증하지 않았다.
- `FinUp.Stock.App` 및 `FinUp.Core.Fundamentals`는 프로젝트 참조로 확인되지만 본 리포트의 세부 클래스/메소드 분석 범위는 현재 폴더의 `FinUp.Stock.App.AlphaBot` 소스에 한정했다.
- `DBUtil`, `SqlSender`, `LogWriter`, `NetUtil` 등 핵심 구현 일부는 참조 프로젝트에 있어 커넥션 해제/SQL 생성/로그 경로의 최종 동작은 `확인 필요`로 표시했다.
- 민감값은 원문 대신 `[REDACTED]`로 마스킹했다.
