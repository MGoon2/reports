# FinUp 비-Api 프로젝트 API Endpoint 사용 분석

- 생성시각: `2026-05-15T11:51:54+09:00`
- 기준 CSV: `/mnt/c/reports/code-research/api-endpoint/finup_api_endpoints.csv`
- 제외 기준: `FinUp.*Api*` 프로젝트와 프로젝트명에 `UnitTest`가 포함된 사용 프로젝트 제외
- 매칭 기준: CSV `url` 정적 문자열 exact match + `{param}` route의 고정 literal/prefix match

## 1. 요약

|항목|값|
|---|---:|
|CSV endpoint row|421|
|고유 URL|358|
|분석한 비-Api 프로젝트(UnitTest 제외)|100|
|사용처 hit(UnitTest 제외)|492|
|UnitTest 사용처 제거 행|54|
|사용 확인 endpoint row|122|
|정적 미사용 endpoint row|299|

## 2. API 프로젝트별 사용 확인 현황

|API 프로젝트|Endpoint 수|사용 확인 Endpoint|사용처 Hit|정적 미사용 Endpoint|
|---|---:|---:|---:|---:|
|FinUp.Auth.Api|10|5|14|5|
|FinUp.Chat.Api|35|9|23|26|
|FinUp.Chat.Api.Badge|4|1|2|3|
|FinUp.Chat.Api.Channel|4|0|0|4|
|FinUp.Chat.NET.Api|136|40|129|96|
|FinUp.Chat.NET.Api.Badge|2|1|6|1|
|FinUp.Chat.NET.Api.Channel|4|3|49|1|
|FinUp.Chat.NET.Api.ChannerView|5|0|0|5|
|FinUp.Chat.NET.Api.Push|1|1|6|0|
|FinUp.General.Api|5|2|12|3|
|FinUp.LogData.Api|6|3|86|3|
|FinUp.Mars.Api|14|0|0|14|
|FinUp.Radar.Api|23|14|63|9|
|FinUp.Stock.Api|56|9|43|47|
|FinUp.Stock.Scraper.Api|3|0|0|3|
|FinUp.StockData.Price.Api|93|33|57|60|
|FinUp.StockData.Price.Api.Channel|2|1|2|1|
|FinUp.StockData.Price.Api.RealTime|18|0|0|18|

## 3. 사용 프로젝트 상위(UnitTest 제외)

|사용 프로젝트|Hit 수|
|---|---:|
|Finup.Chat.NET.Blazor.Core|122|
|FinUp.Stock.App.AlphaBot|38|
|FinUp.Stock.Admin|32|
|FinUp.Finance|31|
|FinUp.Stock.MobileWeb|28|
|FinUp.Stock.Mentor|26|
|FinUp.Radar.App.AlphaBot|25|
|FinUp.Stock.Web|18|
|FinUp.Finance.Admin|15|
|FinUp.General.Admin|14|
|FinUp.General|13|
|FinUp.StockData.ChartCapture.App|12|
|FinUp.Radar.Web.Admin|12|
|FinUp.Chat.Web|11|
|FinUp.Stock|11|
|Finup.Chat.NET.Blazor.WASM|10|
|FinUp.Chat.Admin|9|
|FinUp.General.MobileWeb|6|
|FinUp.General.Web|6|
|FinUp.Guide.Admin|5|
|FinUp.Tssa.Admin|5|
|FinUP.Mars|5|
|FinUp.StockData.Price.Middleware.App|4|
|FinUp.Radar.Web|4|
|FinUp.Tssa.MobileWeb|4|
|FinUp.Tssa.Web|4|
|FinUp.StockData.RoboAnalysis.App|4|
|FinUp.Stock.App|3|
|FinUp.StockData.SignalQueue.App|3|
|FinUp.Company.Web|2|

## 4. Endpoint 사용처 표 (상위 220건, 전체는 CSV/HTML 참조)

|프로젝트 명|엔드포인트 URL|엔드포인트 클래스|엔드포인트 메소드|사용 프로젝트 명|클래스|메소드(라인)|메소드 분석|
|---|---|---|---|---|---|---|---|
|FinUp.Auth.Api|api/auth/app|AuthController|GetAuthApp|Finup.Chat.NET.Blazor.Core|ChatApiAuth|RequestUserJwtFromStockService (Finup.Chat.NET.Blazor.Core/Protocols/ChatApiAuth.cs:41)|서버-side HTTP 호출 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/app|AuthController|GetAuthApp|FinUp.Chat.Web|Config|설정/상수 영역 (FinUp.Chat.Web/appsettings.json:25)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/app|AuthController|GetAuthApp|FinUp.Stock.Admin|View/Markup|View/Markup 영역 (Finup.Stock.Admin/Chat/ChatRoom.aspx:80)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/app|AuthController|GetAuthApp|FinUp.Stock.App.AlphaBot|ProcessUnit|AuthAppHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3404)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/app|AuthController|GetAuthApp|FinUp.Stock.Mentor|View/Markup|View/Markup 영역 (FinUp.Stock.Mentor/Chat/ChatRoom.aspx:84)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/app/jwt|AuthController|GetAuthSimpleJwt|FinUp.Stock.Admin|View/Markup|View/Markup 영역 (Finup.Stock.Admin/Chat/ChatRoom.aspx:80)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/app/jwt|AuthController|GetAuthSimpleJwt|FinUp.Stock.Mentor|View/Markup|View/Markup 영역 (FinUp.Stock.Mentor/Chat/ChatRoom.aspx:84)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/autologin|AuthController|GetAuthAutoLogin|FinUp.Stock.App.AlphaBot|ProcessUnit|AuthRefreshHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3446)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/refresh|AuthController|GetAuthRefresh|FinUp.Chat.Web|Config|설정/상수 영역 (FinUp.Chat.Web/appsettings.json:26)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/refresh|AuthController|GetAuthRefresh|FinUp.Stock.Admin|View/Markup|View/Markup 영역 (Finup.Stock.Admin/Chat/ChatRoom.aspx:81)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/refresh|AuthController|GetAuthRefresh|FinUp.Stock.App.AlphaBot|ProcessUnit|AuthRefreshHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3447)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/auth/refresh|AuthController|GetAuthRefresh|FinUp.Stock.Mentor|View/Markup|View/Markup 영역 (FinUp.Stock.Mentor/Chat/ChatRoom.aspx:85)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/check/health|CheckController|Check|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3358)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Auth.Api|api/check/health|CheckController|Check|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3359)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.Chat.Web|Config|설정/상수 영역 (FinUp.Chat.Web/appsettings.json:24)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.General.Admin|UserDetailSubscribeList.aspx|RemoveChatCache (FinUp.General.Admin/Member/UserDetail/UserDetailSubscribeList.aspx.cs:1231)|서버-side HTTP 호출 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.Stock.Admin|View/Markup|View/Markup 영역 (Finup.Stock.Admin/Chat/ChatRoom.aspx:79)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.Stock.Admin|View/Markup|View/Markup 영역 (Finup.Stock.Admin/Chat/ChatRoom.aspx:84)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.Stock.Mentor|View/Markup|View/Markup 영역 (FinUp.Stock.Mentor/Chat/ChatRoom.aspx:83)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.Stock.Mentor|View/Markup|View/Markup 영역 (FinUp.Stock.Mentor/Chat/ChatRoom.aspx:88)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.Stock.MobileWeb|InsightStockView.aspx|btnVideoJoinAction_Click (FinUp.Stock.MobileWeb/Insight/InsightStockView.aspx.cs:1118)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.Stock.MobileWeb|BackupLeadingView.aspx|btnJoinChat_ServerClick (FinUp.Stock.MobileWeb/Leading/BackupLeadingView.aspx.cs:1472)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.Stock.Web|BackUpLeadingView.aspx|btnJoinChat_ServerClick (FinUp.Stock.Web/Leading/BackUpLeadingView.aspx.cs:1505)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat|AppController|ChatNoneAuth|FinUp.StockData.ChartCapture.App|Config|설정/상수 영역 (FinUp.StockData.ChartCapture.App/App.config:23)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat/auth|AppController|ChatAuth|FinUp.Stock.Admin|View/Markup|View/Markup 영역 (Finup.Stock.Admin/Chat/ChatRoom.aspx:79)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat/auth|AppController|ChatAuth|FinUp.Stock.Mentor|View/Markup|View/Markup 영역 (FinUp.Stock.Mentor/Chat/ChatRoom.aspx:83)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat/cacheload|AppController|ChatCacheReload|FinUp.StockData.ChartCapture.App|Config|설정/상수 영역 (FinUp.StockData.ChartCapture.App/App.config:23)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat/cacheload|AppController|ChatCacheReloadChat|FinUp.StockData.ChartCapture.App|Config|설정/상수 영역 (FinUp.StockData.ChartCapture.App/App.config:23)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat/fileupload|AppController|FileUpload|FinUp.Stock.Admin|View/Markup|View/Markup 영역 (Finup.Stock.Admin/Chat/ChatRoom.aspx:84)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat/fileupload|AppController|FileUpload|FinUp.Stock.Mentor|View/Markup|View/Markup 영역 (FinUp.Stock.Mentor/Chat/ChatRoom.aspx:88)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/app/chat/subscribe/{userIdx}/{cIdx}|AppController|AddSubscribe|FinUp.Stock.MobileWeb|InsightStockView.aspx|btnVideoJoinAction_Click (FinUp.Stock.MobileWeb/Insight/InsightStockView.aspx.cs:1118)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.Api|api/app/chat/subscribe/{userIdx}/{cIdx}|AppController|AddSubscribe|FinUp.Stock.MobileWeb|BackupLeadingView.aspx|btnJoinChat_ServerClick (FinUp.Stock.MobileWeb/Leading/BackupLeadingView.aspx.cs:1472)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.Api|api/app/chat/subscribe/{userIdx}/{cIdx}|AppController|AddSubscribe|FinUp.Stock.Web|BackUpLeadingView.aspx|btnJoinChat_ServerClick (FinUp.Stock.Web/Leading/BackUpLeadingView.aspx.cs:1505)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.Api|api/app/chat/subscribecancel/{userIdx}/{chatIdx}|AppController|CacnelSubscribe|FinUp.General.Admin|UserDetailSubscribeList.aspx|RemoveChatCache (FinUp.General.Admin/Member/UserDetail/UserDetailSubscribeList.aspx.cs:1231)|서버-side HTTP 호출 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.Api|api/check/health|CheckController|HealthCheck|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3358)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/check/health|CheckController|HealthCheck|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3359)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api|api/room/refresh/{chatIdx}|RoomController|RefreshChatRoomAsync|FinUp.Stock.Admin|FeatureChatRoom.aspx|메소드 식별 필요 (Finup.Stock.Admin/Feature/FeatureChatRoom.aspx.cs:586)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.Api.Badge|api/check/health|CheckController|Check|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3358)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.Api.Badge|api/check/health|CheckController|Check|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3359)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3354)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3355)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3356)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3357)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3358)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3359)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.2/Common|CommonController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestCommonInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:508)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.2/users/{targetuseridx}/report/count:target|UserReportController|GetTargetUserReportCountAsync|FinUp.General|FUApi.ChatApi|ChatUserReportCount (FinUp.General/FUApi.ChatApi.cs:667)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.2/users/{targetuseridx}/report:target|UserReportController|GetPageAsync|FinUp.General|FUApi.ChatApi|ChatUserReportList (FinUp.General/FUApi.ChatApi.cs:708)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.2/users/{useridx}/ban|UserBanController|GetUserBanListAsync|FinUp.General|FUApi.ChatApi|ChatApiCancelUserBan (FinUp.General/FUApi.ChatApi.cs:625)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.2/users/{useridx}/ban|UserBanController|InsertAsync|FinUp.General|FUApi.ChatApi|ChatApiCancelUserBan (FinUp.General/FUApi.ChatApi.cs:625)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.2/users/{useridx}/ban/{userbanidx}|UserBanController|DeleteAsync|FinUp.General|FUApi.ChatApi|ChatApiCancelUserBan (FinUp.General/FUApi.ChatApi.cs:625)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.2/users/{useridx}/report|UserReportController|InsertAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserReport (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:569)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.2/users/{useridx}/report|UserReportController|InsertAsync|FinUp.General|FUApi.ChatApi|ChatUserReportCount (FinUp.General/FUApi.ChatApi.cs:667)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.2/users/{useridx}/report|UserReportController|InsertAsync|FinUp.General|FUApi.ChatApi|ChatUserReportList (FinUp.General/FUApi.ChatApi.cs:708)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/Auth/token:apikey|AuthController|GetAuthFromApikey|Finup.Chat.NET.Blazor.Core|ChatApiAuth|RequestUserJwtByApiKey (Finup.Chat.NET.Blazor.Core/Protocols/ChatApiAuth.cs:159)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Auth/token:cookie|AuthController|GetAuthFromCookie|Finup.Chat.NET.Blazor.Core|ChatApiAuth|RequestUserJwtByCookie (Finup.Chat.NET.Blazor.Core/Protocols/ChatApiAuth.cs:128)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatList (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:113)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatList (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:113)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:146)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:146)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:178)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:178)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfoByKeywordIdx (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:204)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfoByKeywordIdx (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:204)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestOpenchatDiplayUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:230)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestOpenchatDiplayUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:230)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageList (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:428)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageList (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:428)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:477)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:477)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:680)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:680)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestAllMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:707)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|RequestAllMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:707)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|SendMessage (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:725)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|SendMessage (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:725)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|SetDefaultHeader (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:767)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|SetDefaultHeader (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:767)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|DownloadFile (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:789)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|Finup.Chat.NET.Blazor.Core|ChatApi|DownloadFile (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:789)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|FinUp.Finance|ChatApiService|GetThemeChatMessageRanks (FinUp.Finance/Service/ChatApiService.cs:30)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|FinUp.Finance|ChatApiService|GetThemeChatMessageRanks (FinUp.Finance/Service/ChatApiService.cs:30)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|GetAsync|FinUp.Finance.Admin|Config|설정/상수 영역 (FinUp.Finance.Admin/Web.config:49)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat|ChatController|Insert|FinUp.Finance.Admin|Config|설정/상수 영역 (FinUp.Finance.Admin/Web.config:49)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat/openchat/display/{display}|ChatController|GetChatMessageCount|Finup.Chat.NET.Blazor.Core|ChatApi|RequestOpenchatDiplayUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:230)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat/{appcode}/list|ChatController|GetAppcodeChatList|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:146)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat/{appcode}/message-count|ChatController|GetChatMessageCount|FinUp.Finance|ChatApiService|GetThemeChatMessageRanks (FinUp.Finance/Service/ChatApiService.cs:30)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/Chat/{appcode}/{keywordidx}/info|ChatController|GetChatbyKeyword|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfoByKeywordIdx (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:204)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/files|ChatFilesController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|SetDefaultHeader (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:767)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/files|ChatFilesController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|DownloadFile (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:789)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/files/{chatfileidx}:download|ChatFilesController|DownloadFileAsync|Finup.Chat.NET.Blazor.Core|ChatApi|DownloadFile (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:789)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/files:upload|ChatFilesController|UploadAsync|Finup.Chat.NET.Blazor.Core|ChatApi|SetDefaultHeader (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:767)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageList (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:428)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageList (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:428)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:477)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:477)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:680)|설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:680)|설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestAllMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:707)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestAllMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:707)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|SendMessage (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:725)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|SendMessage (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:725)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|GetAsync|FinUp.Finance.Admin|Config|설정/상수 영역 (FinUp.Finance.Admin/Web.config:49)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages|ChatMessageController|PostAsync|FinUp.Finance.Admin|Config|설정/상수 영역 (FinUp.Finance.Admin/Web.config:49)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages/{appcode}:unauth|ChatMessageController|GetUnAuthAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:477)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages/{chatmessageidx}/openchat:admin|ChatMessageController|DeleteOpenChatAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:680)|설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/messages:system|ChatMessageController|PostApiKeyAsync|FinUp.Finance.Admin|Config|설정/상수 영역 (FinUp.Finance.Admin/Web.config:49)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/Chat/{chatidx}/openchat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:178)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Chat/{chatidx}/openchat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestOpenchatDiplayUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:230)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/Chat/{chatidx}/openchat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/Chat/{chatidx}/openchat|ChatController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:680)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|GetListAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|GetListAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|GetListAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|GetListAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|GetListAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users|ChatUsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/openchat:enter|ChatUsersController|EnterOpenChatAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|DeleteAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|PatchAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|DeleteAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|PatchAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|DeleteAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|PatchAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|DeleteAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|PatchAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|DeleteAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}|ChatUsersController|PatchAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}:enter|ChatUsersController|EnterAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{chatidx}/users/{chatuseridx}:out|ChatUsersController|OutAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/chat/{useridx}/{appcode}/messages/delete-all-message|ChatMessageController|DeleteServiceBlockUserMessageAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestAllMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:707)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserInfoByJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:248)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserInfoByJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:248)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserBan (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:539)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserBan (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:539)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestServiceBlockUser (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:607)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestServiceBlockUser (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:607)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|GetAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestGetServiceBlock (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:639)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|PostAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestGetServiceBlock (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:639)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|GetAsync|FinUp.General|FUApi.ChatApi|ChatApiGetUserBanList (FinUp.General/FUApi.ChatApi.cs:579)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users|UsersController|PostAsync|FinUp.General|FUApi.ChatApi|ChatApiGetUserBanList (FinUp.General/FUApi.ChatApi.cs:579)|설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users/service-block|UsersController|GetUserServiceBlockAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestServiceBlockUser (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:607)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users/service-block|UsersController|PostUserServiceBlockAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestServiceBlockUser (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:607)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users/service-block|UsersController|GetUserServiceBlockAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestGetServiceBlock (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:639)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/Users/service-block|UsersController|PostUserServiceBlockAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestGetServiceBlock (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:639)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/users/{useridx}/ban|UserBanController|GetUserBanListAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserBan (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:539)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/users/{useridx}/ban|UserBanController|InsertAsync|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserBan (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:539)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 템플릿과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api|api/v1.9/users/{useridx}/ban|UserBanController|GetUserBanListAsync|FinUp.General|FUApi.ChatApi|ChatApiGetUserBanList (FinUp.General/FUApi.ChatApi.cs:579)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api|api/v1.9/users/{useridx}/ban|UserBanController|InsertAsync|FinUp.General|FUApi.ChatApi|ChatApiGetUserBanList (FinUp.General/FUApi.ChatApi.cs:579)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Badge|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3354)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api.Badge|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3355)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api.Badge|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3356)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api.Badge|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3357)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api.Badge|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3358)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api.Badge|api/Check|CheckController|CheckDB|FinUp.Stock.App.AlphaBot|ProcessUnit|ApiSiteHealthCheck (FinUp.Stock.App.AlphaBot/Operation/ProcessUnit.cs:3359)|문자열/경로 참조 후보. 매칭=CSV URL과 동일한 정적 문자열, 신뢰도=High.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Chat.Admin|View/Markup|View/Markup 영역 (FinUp.Chat.Admin/Views/ThemeChat/Monitoring.cshtml:43)|문자열/경로 참조 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatList (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:113)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:146)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:178)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfoByKeywordIdx (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:204)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestOpenchatDiplayUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:230)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageList (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:428)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageListNonJWT (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:477)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:680)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|RequestAllMessageDelete (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:707)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|SendMessage (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:725)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|SetDefaultHeader (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:767)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.Core|ChatApi|DownloadFile (Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:789)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.WASM|Config|설정/상수 영역 (Finup.Chat.NET.Blazor.WASM/wwwroot/appsettings.Staging.json:7)|SignalR/실시간 연결 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.WASM|Config|설정/상수 영역 (Finup.Chat.NET.Blazor.WASM/wwwroot/appsettings.Staging.json:8)|SignalR/실시간 연결 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.WASM|Config|설정/상수 영역 (Finup.Chat.NET.Blazor.WASM/wwwroot/appsettings.json:7)|SignalR/실시간 연결 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.WASM|Config|설정/상수 영역 (Finup.Chat.NET.Blazor.WASM/wwwroot/appsettings.json:8)|SignalR/실시간 연결 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|Finup.Chat.NET.Blazor.WASM|Config|설정/상수 영역 (Finup.Chat.NET.Blazor.WASM/wwwroot/appsettings.publish.json:6)|SignalR/실시간 연결 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Chat.Web.React|ChatRepository|GetChatMessageAsync (FinUp.Chat.Web.React/Repository/ChatRepository.cs:55)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Finance|ChatApiService|GetThemeChatMessageRanks (FinUp.Finance/Service/ChatApiService.cs:30)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Finance.Admin|Config|설정/상수 영역 (FinUp.Finance.Admin/Web.config:48)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Finance.Admin|Config|설정/상수 영역 (FinUp.Finance.Admin/Web.config:49)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.General|FUApi.ChatApi|ChatApiChatUserInsert (FinUp.General/FUApi.ChatApi.cs:410)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.General|FUApi.ChatApi|ChatApiChatUserUpdate (FinUp.General/FUApi.ChatApi.cs:459)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ExecChatApiChatFilesDownLoad (FinUp.Stock/SPApi.ChatApi.cs:529)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserInsert (FinUp.Stock/SPApi.ChatApi.cs:820)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserInsert (FinUp.Stock/SPApi.ChatApi.cs:826)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserUpdate (FinUp.Stock/SPApi.ChatApi.cs:875)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserUpdate (FinUp.Stock/SPApi.ChatApi.cs:881)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserOutAll (FinUp.Stock/SPApi.ChatApi.cs:906)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ChatApiChatMessageHistoryDate (FinUp.Stock/SPApi.ChatApi.cs:949)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ChatApiChatMessageHistory (FinUp.Stock/SPApi.ChatApi.cs:992)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock|SPApi.ChatApi|ChatApiRoboAIDescChange (FinUp.Stock/SPApi.ChatApi.cs:1016)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock.App|ChatApi|ChatApiChatUserInsert (FinUp.Stock.App/Util/ChatApi.cs:259)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock.App|ChatApi|ChatApiChatUserCancel (FinUp.Stock.App/Util/ChatApi.cs:365)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.Stock.App|ChatApi|ChatApiChatUserOutAll (FinUp.Stock.App/Util/ChatApi.cs:694)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.StockData.ChartCapture.App|TcpListenerRobo|UploadFileAsync (FinUp.StockData.ChartCapture.App/TcpListenerRobo.cs:141)|서버-side HTTP 호출 후보; 설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat|ChatController|Connect|FinUp.StockData.Price.Middleware.App|Config|설정/상수 영역 (FinUp.StockData.Price.Middleware.App/App.config:45)|설정/상수 URL 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat/client/count|ChatController|Count|FinUp.Chat.Admin|View/Markup|View/Markup 영역 (FinUp.Chat.Admin/Views/ThemeChat/Monitoring.cshtml:43)|문자열/경로 참조 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat/connect|ChatController|ConnectByGet|Finup.Chat.NET.Blazor.WASM|Config|설정/상수 영역 (Finup.Chat.NET.Blazor.WASM/wwwroot/appsettings.Staging.json:7)|SignalR/실시간 연결 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|
|FinUp.Chat.NET.Api.Channel|api/v{version:apiVersion}/Chat/connect|ChatController|ConnectByGet|Finup.Chat.NET.Blazor.WASM|Config|설정/상수 영역 (Finup.Chat.NET.Blazor.WASM/wwwroot/appsettings.Staging.json:8)|SignalR/실시간 연결 후보. 매칭=CSV 파라미터 URL의 고정 구간 순차 매칭, 신뢰도=Medium.|

## 5. 산출물

- 전체 상세 CSV: `/mnt/c/reports/code-research/api-endpoint/finup_endpoint_usage_detail.csv`
- 정적 미사용 Endpoint CSV: `/mnt/c/reports/code-research/api-endpoint/finup_endpoint_unused.csv`
- HTML: `/mnt/c/reports/code-research/api-endpoint/finup_endpoint_usage_report.html`
- 요약 JSON: `/mnt/c/reports/code-research/api-endpoint/finup_endpoint_usage_summary.json`