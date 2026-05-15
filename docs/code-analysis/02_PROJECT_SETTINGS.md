# 프로젝트 설정 분석

## `.sln`

| 항목 | 내용 |
|---|---|
| 솔루션 파일 | 현재 폴더에서 발견되지 않음 |
| 확인 결과 | `.csproj` 단독 또는 상위 솔루션에서 포함될 가능성 `확인 필요` |

## `.csproj` 기본 설정

| 설정 | 값 | 근거 |
| --- | --- | --- |
| ProjectGuid | {C303E817-746D-4E25-AACF-D07066CEA394} | csproj |
| OutputType | WinExe | csproj |
| RootNamespace | FinUp.Stock.App.AlphaBot | csproj |
| AssemblyName | FinUp.Stock.App.AlphaBot | csproj |
| TargetFrameworkVersion | v4.7 | csproj |
| StartupObject | (명시 없음) | csproj |
| ProjectTypeGuids | {60dc8134-eba5-43b8-bcc9-bb4bc16c2548};{FAE04EC0-301F-11D3-BF4B-00C04F79EFBC} | WPF + C# 프로젝트 GUID |
| SignManifests | true | ClickOnce/매니페스트 서명 |
| ManifestKeyFile | FinUp.Stock.App.AlphaBot_TemporaryKey.pfx | 민감 파일명으로 취급 |
| PublishUrl | C:\00_배포\publish\FinUp.Stock.App.Alphabot\ | 배포 경로 설정 |

## 빌드 구성/플랫폼

| Condition | PlatformTarget | OutputPath | DefineConstants | Optimize | Prefer32Bit |
| --- | --- | --- | --- | --- | --- |
| '$(Configuration)|$(Platform)' == 'Debug|AnyCPU' | AnyCPU | bin\Debug\ | DEBUG;TRACE | false |  |
| '$(Configuration)|$(Platform)' == 'Release|AnyCPU' | AnyCPU | bin\Release\ | TRACE | true |  |
| '$(Configuration)|$(Platform)' == 'Debug|x64' | x64 | bin\x64\Debug\ | DEBUG;TRACE |  | true |
| '$(Configuration)|$(Platform)' == 'Release|x64' | x64 | bin\x64\Release\ | TRACE | true | true |

## App.config

| 항목 | 내용 |
|---|---|
| supportedRuntime | `v4.0 .NETFramework,Version=v4.5.2` |
| connectionStrings | `없음` |

### appSettings (값 마스킹 적용)

| Key | Value |
| --- | --- |
| Server | REAL |
| StockPoint | http://www.stockpoint.co.kr |
| DBStockPoint | [REDACTED] |
| StockRadarPath | D:\APP\StockPoint.App.StockRadar\StockPoint.App.StockWatch.exe |
| XingDataPath | D:\APP\StockPoint.App.XingData\StockPoint.App.XingData.exe |
| ServerID | [REDACTED] |
| ServerPWD | [REDACTED] |
| ObserveStockRadar | 60 |
| ApiDBStockPoint | [REDACTED] |
| RealExtComm | [REDACTED] |
| DBMessageServiceLgu | [REDACTED] |
| DBMessageServiceDanal | [REDACTED] |
| ChatCacheLoadUrl | https://pre-chatapi.finup.co.kr/api/v1/cache |
| ChatApiKey | [REDACTED] |
| ChatApiUrl | https://pre-chatapi.finup.co.kr |
| ChatApiEnable | N |
| StockDataApi | https://stockdata.finup.co.kr/api |
| StockPointApi | https://pre-apichat.finup.co.kr/api |
| FinUpImgUrl | https://pre-img.finup.co.kr |
| FinUpStockUrl | https://pre-stock.finup.co.kr |
| MentorStockUrl | https://pre-mentorstock.finup.co.kr |
| ThemeRadarApiUrl | https://apiradar.finup.co.kr |
| WiseInvestLguUrl | http://loc-wiseinvest.danal.co.kr/ |
| AWSAccessKey | [REDACTED] |
| AWSSecretKey | [REDACTED] |
| NaverApiClientId | [REDACTED] |
| NaverApiClientSecretId | [REDACTED] |
| NaverLoginId | [REDACTED] |
| NaverLoginPw | [REDACTED] |
| NaverApiRedirectUrl | https://cafe.naver.com/withstock |
| NaverCafeId | 12323151 |
| NaverCafeMenuId | 350 |
| NaverCafeMentorMarketMenuId | 309 |
| NaverCafeUploadLimitMB | 2 |
| NaverCafeAttendBoardMenuId | 384 |
| bitlyToken | [REDACTED] |
| YoutubeDataAPIKey | [REDACTED] |
| ApiLogUrl | https://apilog.finup.co.kr/Log/System |
| ApiLogSender | FinUp.Stock.App.AlphaBot |
| UseApiLog | true |

### assemblyBinding redirects

| Assembly | oldVersion | newVersion |
| --- | --- | --- |
| Newtonsoft.Json | 0.0.0.0-13.0.0.0 | 13.0.0.0 |
| NLog | 0.0.0.0-4.0.0.0 | 4.0.0.0 |
| Google.Apis | 0.0.0.0-1.67.0.0 | 1.67.0.0 |
| Google.Apis.Core | 0.0.0.0-1.67.0.0 | 1.67.0.0 |
| System.Runtime.CompilerServices.Unsafe | 0.0.0.0-6.0.0.0 | 6.0.0.0 |
| System.Threading.Tasks.Extensions | 0.0.0.0-4.2.0.1 | 4.2.0.1 |
| System.Memory | 0.0.0.0-4.0.1.2 | 4.0.1.2 |
| System.Buffers | 0.0.0.0-4.0.3.0 | 4.0.3.0 |

## NuGet packages.config

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

## Assembly/DLL References

| Reference | HintPath | Private |
| --- | --- | --- |
| AWSSDK.CloudWatch | ..\Solutions\packages\AWSSDK.CloudWatch.3.3.104.3\lib\net45\AWSSDK.CloudWatch.dll |  |
| AWSSDK.Core | ..\Solutions\packages\AWSSDK.Core.3.3.104\lib\net45\AWSSDK.Core.dll |  |
| AWSSDK.EC2 | ..\Solutions\packages\AWSSDK.EC2.3.3.142\lib\net45\AWSSDK.EC2.dll |  |
| AWSSDK.RDS | ..\Solutions\packages\AWSSDK.RDS.3.3.114\lib\net45\AWSSDK.RDS.dll |  |
| FirebaseAdmin | ..\Solutions\packages\FirebaseAdmin.3.0.0\lib\net462\FirebaseAdmin.dll |  |
| Google.Api.Gax | ..\Solutions\packages\Google.Api.Gax.4.8.0\lib\net462\Google.Api.Gax.dll |  |
| Google.Api.Gax.Rest | ..\Solutions\packages\Google.Api.Gax.Rest.4.8.0\lib\net462\Google.Api.Gax.Rest.dll |  |
| Google.Apis | ..\Solutions\packages\Google.Apis.1.67.0\lib\net462\Google.Apis.dll |  |
| Google.Apis.Auth | ..\Solutions\packages\Google.Apis.Auth.1.67.0\lib\net462\Google.Apis.Auth.dll |  |
| Google.Apis.Core | ..\Solutions\packages\Google.Apis.Core.1.67.0\lib\net462\Google.Apis.Core.dll |  |
| Google.Apis.YouTube.v3 | ..\Solutions\packages\Google.Apis.YouTube.v3.1.43.0.1834\lib\net45\Google.Apis.YouTube.v3.dll |  |
| HtmlAgilityPack | ..\Solutions\packages\HtmlAgilityPack.1.11.17\lib\Net45\HtmlAgilityPack.dll |  |
| Interop.DANALCOMLib | DLL\Interop.DANALCOMLib.dll |  |
| M2Mqtt.Net | DLL\M2Mqtt.Net.dll |  |
| Microsoft.Bcl.AsyncInterfaces | ..\Solutions\packages\Microsoft.Bcl.AsyncInterfaces.6.0.0\lib\net461\Microsoft.Bcl.AsyncInterfaces.dll |  |
| Microsoft.Extensions.DependencyInjection.Abstractions | ..\Solutions\packages\Microsoft.Extensions.DependencyInjection.Abstractions.6.0.0\lib\net461\Microsoft.Extensions.DependencyInjection.Abstractions.dll |  |
| MoonAPNS | ..\Solutions\packages\MoonAPNS.0.0.4.188\lib\net451\MoonAPNS.dll | True |
| Newtonsoft.Json | ..\Solutions\packages\Newtonsoft.Json.13.0.3\lib\net45\Newtonsoft.Json.dll |  |
| NLog | ..\Solutions\packages\NLog.4.4.12\lib\net45\NLog.dll | True |
| System | (Framework/GAC) |  |
| System.Buffers | ..\Solutions\packages\System.Buffers.4.5.1\lib\net461\System.Buffers.dll |  |
| System.CodeDom | ..\Solutions\packages\System.CodeDom.7.0.0\lib\net462\System.CodeDom.dll |  |
| System.Collections.Immutable | ..\Solutions\packages\System.Collections.Immutable.8.0.0\lib\net462\System.Collections.Immutable.dll |  |
| System.ComponentModel.DataAnnotations | (Framework/GAC) |  |
| System.configuration | (Framework/GAC) |  |
| System.Configuration.Install | (Framework/GAC) |  |
| System.Data | (Framework/GAC) |  |
| System.Drawing | (Framework/GAC) |  |
| System.Management | (Framework/GAC) |  |
| System.Memory | ..\Solutions\packages\System.Memory.4.5.5\lib\net461\System.Memory.dll |  |
| System.Numerics | (Framework/GAC) |  |
| System.Numerics.Vectors | ..\Solutions\packages\System.Numerics.Vectors.4.5.0\lib\net46\System.Numerics.Vectors.dll |  |
| System.Runtime.CompilerServices.Unsafe | ..\Solutions\packages\System.Runtime.CompilerServices.Unsafe.6.0.0\lib\net461\System.Runtime.CompilerServices.Unsafe.dll |  |
| System.Threading.Tasks.Extensions | ..\Solutions\packages\System.Threading.Tasks.Extensions.4.5.4\lib\net461\System.Threading.Tasks.Extensions.dll |  |
| System.Transactions | (Framework/GAC) |  |
| System.ValueTuple | ..\Solutions\packages\System.ValueTuple.4.5.0\lib\net47\System.ValueTuple.dll |  |
| System.Web | (Framework/GAC) |  |
| System.Web.Extensions | (Framework/GAC) |  |
| System.Windows.Forms | (Framework/GAC) |  |
| System.Xml | (Framework/GAC) |  |
| Microsoft.CSharp | (Framework/GAC) |  |
| System.Core | (Framework/GAC) |  |
| System.Xml.Linq | (Framework/GAC) |  |
| System.Data.DataSetExtensions | (Framework/GAC) |  |
| System.Net.Http | (Framework/GAC) |  |
| System.Xaml | (Framework/GAC) |  |
| WindowsBase | (Framework/GAC) |  |
| PresentationCore | (Framework/GAC) |  |
| PresentationFramework | (Framework/GAC) |  |

## ProjectReference

| From | To | 경로 |
| --- | --- | --- |
| FinUp.Stock.App.AlphaBot | FinUp.Core.Fundamentals | ..\FinUp.Core.Fundamentals\FinUp.Core.Fundamentals.csproj |
| FinUp.Stock.App.AlphaBot | FinUp.Stock.App | ..\FinUp.Stock.App\FinUp.Stock.App.csproj |

## 확인 필요

- `App.config`의 supportedRuntime은 .NETFramework v4.5.2로 표시되지만 csproj TargetFrameworkVersion은 v4.7이다. 실제 런타임 바인딩 영향 확인 필요.
- `ManifestKeyFile`, `PushCertify` 파일, DB/API/토큰 관련 appSettings는 보안 관리 방식 확인 필요.

## 분석 한계

- 현재 폴더의 소스와 프로젝트 파일을 기준으로 정적 분석했다. 런타임 DB 데이터, 실제 스케줄 설정값, 외부 API 응답, 배포 서버 상태는 실행 검증하지 않았다.
- `FinUp.Stock.App` 및 `FinUp.Core.Fundamentals`는 프로젝트 참조로 확인되지만 본 리포트의 세부 클래스/메소드 분석 범위는 현재 폴더의 `FinUp.Stock.App.AlphaBot` 소스에 한정했다.
- `DBUtil`, `SqlSender`, `LogWriter`, `NetUtil` 등 핵심 구현 일부는 참조 프로젝트에 있어 커넥션 해제/SQL 생성/로그 경로의 최종 동작은 `확인 필요`로 표시했다.
- 민감값은 원문 대신 `[REDACTED]`로 마스킹했다.
