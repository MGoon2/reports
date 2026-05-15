# 프로젝트 간 참조 관계

## 전체 프로젝트 목록

| 프로젝트 | 타입 | 역할 |
| --- | --- | --- |
| FinUp.Stock.App.AlphaBot | WPF WinExe | 실행 진입점/스케줄러/업무 배치 |
| FinUp.Stock.App | Class Library(참조) | DB/SQL/Log/Entity/Util 제공으로 추정 |
| FinUp.Core.Fundamentals | Class Library(참조) | 기반 공통 기능 제공으로 추정 |

## 참조 관계

| From | To | 경로 | 파일 존재 | 관계 설명 |
| --- | --- | --- | --- | --- |
| FinUp.Stock.App.AlphaBot | FinUp.Core.Fundamentals | ..\FinUp.Core.Fundamentals\FinUp.Core.Fundamentals.csproj | 존재 | 기반 공통 기능 라이브러리(세부 확인 필요) |
| FinUp.Stock.App.AlphaBot | FinUp.Stock.App | ..\FinUp.Stock.App\FinUp.Stock.App.csproj | 존재 | DBUtil, SqlSender, LogWriter, Entity, NetUtil 등으로 보이는 공통 앱 라이브러리 |

## 의존성 방향

```text
FinUp.Stock.App.AlphaBot (WinExe)
  ├── FinUp.Stock.App (참조 프로젝트)
  ├── FinUp.Core.Fundamentals (참조 프로젝트)
  ├── NuGet packages.config 기반 외부 패키지
  └── DLL/ 로컬 DLL
```

## 순환 참조 여부

| 항목 | 결과 |
|---|---|
| 현재 `.csproj` 내부 순환 | 단일 프로젝트 기준 순환 없음 |
| 참조 프로젝트가 AlphaBot을 역참조하는지 | 확인 필요(참조 프로젝트 세부 분석 범위 밖) |
| 실행 프로젝트와 보조 프로젝트 구분 | AlphaBot은 WinExe 실행 프로젝트, 나머지 2개는 보조 Class Library로 추정 |

## NuGet 참조

| Package | Version | TargetFramework |
| --- | --- | --- |
| AWSSDK.CloudWatch | 3.3.104.3 | net452 |
| AWSSDK.Core | 3.3.104 | net452 |
| AWSSDK.EC2 | 3.3.142 | net452 |
| AWSSDK.RDS | 3.3.114 | net452 |
| FirebaseAdmin | 3.0.0 | net47 |
| Google.Api.Gax | 4.8.0 | net47 |
| Google.Api.Gax.Rest | 4.8.0 | net47 |
| Google.Apis | 1.67.0 | net47 |
| Google.Apis.Auth | 1.67.0 | net47 |
| Google.Apis.Core | 1.67.0 | net47 |
| Google.Apis.YouTube.v3 | 1.43.0.1834 | net47 |
| HtmlAgilityPack | 1.11.17 | net452 |
| Microsoft.Bcl.AsyncInterfaces | 6.0.0 | net47 |
| Microsoft.Extensions.DependencyInjection.Abstractions | 6.0.0 | net47 |
| MoonAPNS | 0.0.4.188 | net452 |
| Newtonsoft.Json | 13.0.3 | net47 |
| NLog | 4.4.12 | net452 |
| System.Buffers | 4.5.1 | net47 |
| System.CodeDom | 7.0.0 | net47 |
| System.Collections.Immutable | 8.0.0 | net47 |
| System.Management | 7.0.2 | net47 |
| System.Memory | 4.5.5 | net47 |
| System.Numerics.Vectors | 4.5.0 | net47 |
| System.Runtime.CompilerServices.Unsafe | 6.0.0 | net47 |
| System.Threading.Tasks.Extensions | 4.5.4 | net47 |
| System.ValueTuple | 4.5.0 | net47 |

## Assembly/DLL 참조

| Reference | HintPath | 비고 |
| --- | --- | --- |
| AWSSDK.CloudWatch | ..\Solutions\packages\AWSSDK.CloudWatch.3.3.104.3\lib\net45\AWSSDK.CloudWatch.dll | NuGet/Framework |
| AWSSDK.Core | ..\Solutions\packages\AWSSDK.Core.3.3.104\lib\net45\AWSSDK.Core.dll | NuGet/Framework |
| AWSSDK.EC2 | ..\Solutions\packages\AWSSDK.EC2.3.3.142\lib\net45\AWSSDK.EC2.dll | NuGet/Framework |
| AWSSDK.RDS | ..\Solutions\packages\AWSSDK.RDS.3.3.114\lib\net45\AWSSDK.RDS.dll | NuGet/Framework |
| FirebaseAdmin | ..\Solutions\packages\FirebaseAdmin.3.0.0\lib\net462\FirebaseAdmin.dll | NuGet/Framework |
| Google.Api.Gax | ..\Solutions\packages\Google.Api.Gax.4.8.0\lib\net462\Google.Api.Gax.dll | NuGet/Framework |
| Google.Api.Gax.Rest | ..\Solutions\packages\Google.Api.Gax.Rest.4.8.0\lib\net462\Google.Api.Gax.Rest.dll | NuGet/Framework |
| Google.Apis | ..\Solutions\packages\Google.Apis.1.67.0\lib\net462\Google.Apis.dll | NuGet/Framework |
| Google.Apis.Auth | ..\Solutions\packages\Google.Apis.Auth.1.67.0\lib\net462\Google.Apis.Auth.dll | NuGet/Framework |
| Google.Apis.Core | ..\Solutions\packages\Google.Apis.Core.1.67.0\lib\net462\Google.Apis.Core.dll | NuGet/Framework |
| Google.Apis.YouTube.v3 | ..\Solutions\packages\Google.Apis.YouTube.v3.1.43.0.1834\lib\net45\Google.Apis.YouTube.v3.dll | NuGet/Framework |
| HtmlAgilityPack | ..\Solutions\packages\HtmlAgilityPack.1.11.17\lib\Net45\HtmlAgilityPack.dll | NuGet/Framework |
| Interop.DANALCOMLib | DLL\Interop.DANALCOMLib.dll | 로컬 DLL |
| M2Mqtt.Net | DLL\M2Mqtt.Net.dll | 로컬 DLL |
| Microsoft.Bcl.AsyncInterfaces | ..\Solutions\packages\Microsoft.Bcl.AsyncInterfaces.6.0.0\lib\net461\Microsoft.Bcl.AsyncInterfaces.dll | NuGet/Framework |
| Microsoft.Extensions.DependencyInjection.Abstractions | ..\Solutions\packages\Microsoft.Extensions.DependencyInjection.Abstractions.6.0.0\lib\net461\Microsoft.Extensions.DependencyInjection.Abstractions.dll | NuGet/Framework |
| MoonAPNS | ..\Solutions\packages\MoonAPNS.0.0.4.188\lib\net451\MoonAPNS.dll | NuGet/Framework |
| Newtonsoft.Json | ..\Solutions\packages\Newtonsoft.Json.13.0.3\lib\net45\Newtonsoft.Json.dll | NuGet/Framework |
| NLog | ..\Solutions\packages\NLog.4.4.12\lib\net45\NLog.dll | NuGet/Framework |
| System | (Framework/GAC) | NuGet/Framework |
| System.Buffers | ..\Solutions\packages\System.Buffers.4.5.1\lib\net461\System.Buffers.dll | NuGet/Framework |
| System.CodeDom | ..\Solutions\packages\System.CodeDom.7.0.0\lib\net462\System.CodeDom.dll | NuGet/Framework |
| System.Collections.Immutable | ..\Solutions\packages\System.Collections.Immutable.8.0.0\lib\net462\System.Collections.Immutable.dll | NuGet/Framework |
| System.ComponentModel.DataAnnotations | (Framework/GAC) | NuGet/Framework |
| System.configuration | (Framework/GAC) | NuGet/Framework |
| System.Configuration.Install | (Framework/GAC) | NuGet/Framework |
| System.Data | (Framework/GAC) | NuGet/Framework |
| System.Drawing | (Framework/GAC) | NuGet/Framework |
| System.Management | (Framework/GAC) | NuGet/Framework |
| System.Memory | ..\Solutions\packages\System.Memory.4.5.5\lib\net461\System.Memory.dll | NuGet/Framework |
| System.Numerics | (Framework/GAC) | NuGet/Framework |
| System.Numerics.Vectors | ..\Solutions\packages\System.Numerics.Vectors.4.5.0\lib\net46\System.Numerics.Vectors.dll | NuGet/Framework |
| System.Runtime.CompilerServices.Unsafe | ..\Solutions\packages\System.Runtime.CompilerServices.Unsafe.6.0.0\lib\net461\System.Runtime.CompilerServices.Unsafe.dll | NuGet/Framework |
| System.Threading.Tasks.Extensions | ..\Solutions\packages\System.Threading.Tasks.Extensions.4.5.4\lib\net461\System.Threading.Tasks.Extensions.dll | NuGet/Framework |
| System.Transactions | (Framework/GAC) | NuGet/Framework |
| System.ValueTuple | ..\Solutions\packages\System.ValueTuple.4.5.0\lib\net47\System.ValueTuple.dll | NuGet/Framework |
| System.Web | (Framework/GAC) | NuGet/Framework |
| System.Web.Extensions | (Framework/GAC) | NuGet/Framework |
| System.Windows.Forms | (Framework/GAC) | NuGet/Framework |
| System.Xml | (Framework/GAC) | NuGet/Framework |
| Microsoft.CSharp | (Framework/GAC) | NuGet/Framework |
| System.Core | (Framework/GAC) | NuGet/Framework |
| System.Xml.Linq | (Framework/GAC) | NuGet/Framework |
| System.Data.DataSetExtensions | (Framework/GAC) | NuGet/Framework |
| System.Net.Http | (Framework/GAC) | NuGet/Framework |
| System.Xaml | (Framework/GAC) | NuGet/Framework |
| WindowsBase | (Framework/GAC) | NuGet/Framework |
| PresentationCore | (Framework/GAC) | NuGet/Framework |
| PresentationFramework | (Framework/GAC) | NuGet/Framework |

## 위험 요소

- 순환 참조 여부: 현재 프로젝트 파일만 보면 없음. 참조 프로젝트의 역참조는 `확인 필요`.
- 실행 프로젝트가 Data Layer를 직접 참조하는지: `FinUp.Stock.App.Sql`, `FinUp.Stock.App.Util.DBUtil`을 직접 사용하므로 직접 접근으로 확인된다.
- Common 프로젝트가 업무 프로젝트를 참조하는지: `확인 필요`.

## 분석 한계

- 현재 폴더의 소스와 프로젝트 파일을 기준으로 정적 분석했다. 런타임 DB 데이터, 실제 스케줄 설정값, 외부 API 응답, 배포 서버 상태는 실행 검증하지 않았다.
- `FinUp.Stock.App` 및 `FinUp.Core.Fundamentals`는 프로젝트 참조로 확인되지만 본 리포트의 세부 클래스/메소드 분석 범위는 현재 폴더의 `FinUp.Stock.App.AlphaBot` 소스에 한정했다.
- `DBUtil`, `SqlSender`, `LogWriter`, `NetUtil` 등 핵심 구현 일부는 참조 프로젝트에 있어 커넥션 해제/SQL 생성/로그 경로의 최종 동작은 `확인 필요`로 표시했다.
- 민감값은 원문 대신 `[REDACTED]`로 마스킹했다.
