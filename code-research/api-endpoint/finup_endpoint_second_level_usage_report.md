# FinUp Endpoint 사용 메소드 2차 호출 연결 분석

- 생성시각: `2026-05-15T13:44:55+09:00`
- 기준 1차 CSV: `/mnt/c/reports/code-research/api-endpoint/finup_endpoint_usage_detail.csv`
- 대상 프로젝트: `Finup.Chat.NET.Blazor.Core, FinUp.Finance, FinUp.General, FinUp.Stock`
- 제외: `.Api` 프로젝트, `UnitTest` 프로젝트, 대상 프로젝트 내부 self-call
- 매칭: endpoint 호출 메소드명 정적 호출 검색 + ProjectReference/대상 클래스명 근거로 신뢰도 부여

## 요약

|항목|값|
|---|---:|
|Endpoint 호출 메소드|60|
|외부 호출 연결 row|14|
|외부 호출 미발견 메소드|54|

## 대상 프로젝트별 외부 호출 연결 수

|대상 프로젝트|연결 수|
|---|---:|
|FinUp.General|5|
|FinUp.Stock|9|

## 외부 호출 프로젝트별 연결 수

|외부 호출 프로젝트|연결 수|
|---|---:|
|FinUp.Stock.Web|3|
|FinUp.General.MobileWeb|2|
|FinUp.General.Web|2|
|FinUp.Stock.Admin|2|
|FinUp.Stock.App|2|
|FinUp.Stock.MobileWeb|2|
|FinUp.General.Admin|1|

## 상세 연결 표

|대상 사용 프로젝트|Endpoint 호출 클래스|Endpoint 호출 메소드|Endpoint 호출 메소드 위치|호출 Endpoint 목록|외부 호출 프로젝트|외부 호출 클래스|외부 호출 메소드(라인)|신뢰도|분석|
|---|---|---|---|---|---|---|---|---|---|
|FinUp.Finance|ChatApiService|GetThemeChatMessageRanks|FinUp.Finance/Service/ChatApiService.cs:30|api/v1.9/Chat \| api/v1.9/Chat/{appcode}/message-count \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetCurrentTraderAsync|FinUp.Finance/Service/StockDataApiService.cs:30|api/data/currenttrader/{code}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetIndexAsync|FinUp.Finance/Service/StockDataApiService.cs:64|api/index/last|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetLimitPrice|FinUp.Finance/Service/StockDataApiService.cs:100|api/price/limitprice/{code} \| api/price/{code}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetMarketInfoListAsync|FinUp.Finance/Service/StockDataApiService.cs:156|api/market/{from}/{to}/{offday?}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetNewsListPage|FinUp.Finance/Service/StockDataApiService.cs:107|api/news/NewsListPage|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetNewsListPageStock|FinUp.Finance/Service/StockDataApiService.cs:136|api/news/stock|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetNewsListPageTheme|FinUp.Finance/Service/StockDataApiService.cs:122|api/news/theme|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetPriceMonitorRankAsync|FinUp.Finance/Service/StockDataApiService.cs:48|api/pricemonitor/rank|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetQuote|FinUp.Finance/Service/StockDataApiService.cs:94|api/price/quote/{code} \| api/price/{code}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetSearchHistroyPrice|FinUp.Finance/Service/StockDataApiService.cs:186|api/price/search-history \| api/price/{code}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetStockDayPagingAsync|FinUp.Finance/Service/StockDataApiService.cs:81|api/dayprice/paging/{code}/{pageNo?}/{pageSize?} \| api/dayprice/{code}/{from}/{to}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetStockFinancialPagingAsync|FinUp.Finance/Service/StockDataApiService.cs:25|api/data/financial/{code}/{pageNo?}/{pageSize?}/{isQuarter?}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetStockInfoAsync|FinUp.Finance/Service/StockDataApiService.cs:87|api/data/stock/{code}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetStockPriceList|FinUp.Finance/Service/StockDataApiService.cs:162|api/price/diff \| api/price/{code}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetStockPriceMonitorChartAsync|FinUp.Finance/Service/StockDataApiService.cs:70|api/pricemonitor/chart/count|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetStockPriceMonitorPagingAsync|FinUp.Finance/Service/StockDataApiService.cs:36|api/pricemonitor/list/paging|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetThemeDiffList|FinUp.Finance/Service/StockDataApiService.cs:175|Log \| api/ThemeLog/Diff \| api/themelog|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Finance|StockDataApiService|GetThemeRankingByDiff|FinUp.Finance/Service/StockDataApiService.cs:150|Log \| api/ThemeLog/ThemeRankingByDiff \| api/themelog|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.General|FUApi.ChatApi|ChatApiCancelUserBan|FinUp.General/FUApi.ChatApi.cs:625|api/v1.2/users/{useridx}/ban \| api/v1.2/users/{useridx}/ban/{userbanidx}|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.General|FUApi.ChatApi|ChatApiChatUserInsert|FinUp.General/FUApi.ChatApi.cs:410|api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.General|FUApi.ChatApi|ChatApiChatUserUpdate|FinUp.General/FUApi.ChatApi.cs:459|api/v{version:apiVersion}/Chat|FinUp.General.Admin|UserDetail.aspx|btnUpdateNickName_Click (FinUp.General.Admin/Member/UserDetail/UserDetail.aspx.cs:600)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.General|FUApi.ChatApi|ChatApiChatUserUpdate|FinUp.General/FUApi.ChatApi.cs:459|api/v{version:apiVersion}/Chat|FinUp.General.MobileWeb|MemberInfo.aspx|btnNickNameChk_Click (FinUp.General.MobileWeb/MyPage/MemberInfo.aspx.cs:534)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.General|FUApi.ChatApi|ChatApiChatUserUpdate|FinUp.General/FUApi.ChatApi.cs:459|api/v{version:apiVersion}/Chat|FinUp.General.MobileWeb|MemberInfoSNS.aspx|btnNickNameChk_Click (FinUp.General.MobileWeb/MyPage/MemberInfoSNS.aspx.cs:486)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.General|FUApi.ChatApi|ChatApiChatUserUpdate|FinUp.General/FUApi.ChatApi.cs:459|api/v{version:apiVersion}/Chat|FinUp.General.Web|MemberInfo.aspx|btnNickNameChk_Click (FinUp.General.Web/MyPage/MemberInfo.aspx.cs:523)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.General|FUApi.ChatApi|ChatApiChatUserUpdate|FinUp.General/FUApi.ChatApi.cs:459|api/v{version:apiVersion}/Chat|FinUp.General.Web|MemberInfoSNS.aspx|btnNickNameChk_Click (FinUp.General.Web/MyPage/MemberInfoSNS.aspx.cs:476)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.General|FUApi.ChatApi|ChatApiGetUserBanList|FinUp.General/FUApi.ChatApi.cs:579|api/v1.9/Users \| api/v1.9/users/{useridx}/ban|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.General|FUApi.ChatApi|ChatUserReportCount|FinUp.General/FUApi.ChatApi.cs:667|api/v1.2/users/{targetuseridx}/report/count:target \| api/v1.2/users/{useridx}/report|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.General|FUApi.ChatApi|ChatUserReportList|FinUp.General/FUApi.ChatApi.cs:708|api/v1.2/users/{targetuseridx}/report:target \| api/v1.2/users/{useridx}/report|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Stock|SPApi.ChatApi|ChatApiChatMessageHistory|FinUp.Stock/SPApi.ChatApi.cs:992|api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Stock|SPApi.ChatApi|ChatApiChatMessageHistoryDate|FinUp.Stock/SPApi.ChatApi.cs:949|api/v{version:apiVersion}/Chat|FinUp.Stock.Web|APITest|InitPage (FinUp.Stock.Web/APITest.aspx.cs:26)|Medium|caller 프로젝트가 target 프로젝트를 참조하고 메소드명이 호출됨|
|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserInsert|FinUp.Stock/SPApi.ChatApi.cs:820|api/v{version:apiVersion}/Chat|FinUp.Stock.App|ChatApi|ExecChatApiChatUserInsert (FinUp.Stock.App/Util/ChatApi.cs:50)|Medium|caller 프로젝트가 target 프로젝트를 참조하고 메소드명이 호출됨|
|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserInsert|FinUp.Stock/SPApi.ChatApi.cs:826|Log \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserOutAll|FinUp.Stock/SPApi.ChatApi.cs:906|api/v{version:apiVersion}/Chat|FinUp.Stock.App|ChatApi|ExecChatApiChatUserOutAll (FinUp.Stock.App/Util/ChatApi.cs:651)|Medium|caller 프로젝트가 target 프로젝트를 참조하고 메소드명이 호출됨|
|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserUpdate|FinUp.Stock/SPApi.ChatApi.cs:875|api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Stock|SPApi.ChatApi|ChatApiChatUserUpdate|FinUp.Stock/SPApi.ChatApi.cs:881|Log \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|FinUp.Stock|SPApi.ChatApi|ChatApiRoboAIDescChange|FinUp.Stock/SPApi.ChatApi.cs:1016|api/v{version:apiVersion}/Chat|FinUp.Stock.Admin|FeatureRobo.aspx|btnAIDescChange_Click (Finup.Stock.Admin/Feature/FeatureRobo.aspx.cs:486)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.Stock|SPApi.ChatApi|ExecChatApiChatFilesDownLoad|FinUp.Stock/SPApi.ChatApi.cs:529|api/v{version:apiVersion}/Chat|FinUp.Stock.Admin|ChatHistory|btnFileDownload_Click (Finup.Stock.Admin/Chat/ChatHistory.aspx.cs:178)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.Stock|SPApi.ChatApi|ExecChatApiChatFilesDownLoad|FinUp.Stock/SPApi.ChatApi.cs:529|api/v{version:apiVersion}/Chat|FinUp.Stock.MobileWeb|ChatFileDownload|InitPage (FinUp.Stock.MobileWeb/Common/ChatFileDownload.aspx.cs:90)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.Stock|SPApi.ChatApi|ExecChatApiChatFilesDownLoad|FinUp.Stock/SPApi.ChatApi.cs:529|api/v{version:apiVersion}/Chat|FinUp.Stock.MobileWeb|ChatHistory.aspx|btnFileDownload_Click (FinUp.Stock.MobileWeb/Common/ChatHistory.aspx.cs:316)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.Stock|SPApi.ChatApi|ExecChatApiChatFilesDownLoad|FinUp.Stock/SPApi.ChatApi.cs:529|api/v{version:apiVersion}/Chat|FinUp.Stock.Web|ChatFileDownload|InitPage (FinUp.Stock.Web/Common/ChatFileDownload.aspx.cs:95)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|FinUp.Stock|SPApi.ChatApi|ExecChatApiChatFilesDownLoad|FinUp.Stock/SPApi.ChatApi.cs:529|api/v{version:apiVersion}/Chat|FinUp.Stock.Web|ChatHistory.aspx|btnFileDownload_Click (FinUp.Stock.Web/Common/ChatHistory.aspx.cs:313)|High|동일 라인에 대상 전체 클래스명과 메소드 호출이 함께 존재|
|Finup.Chat.NET.Blazor.Core|ChatApi|DownloadFile|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:789|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/files \| api/v1.9/chat/{chatidx}/files/{chatfileidx}:download \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestAllMessageDelete|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:707|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/messages \| api/v1.9/chat/{useridx}/{appcode}/messages/delete-all-message \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatEnter|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:287|api/v1.9/Chat \| api/v1.9/Chat/{chatidx}/openchat \| api/v1.9/chat/{chatidx}/users \| api/v1.9/chat/{chatidx}/users/openchat:enter \| api/v1.9/chat/{chatidx}/users/{chatuseridx} \| api/v1.9/chat/{chatidx}/users/{chatuseridx}:enter \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfo|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:178|api/v1.9/Chat \| api/v1.9/Chat/{chatidx}/openchat \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatInfoByKeywordIdx|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:204|api/v1.9/Chat \| api/v1.9/Chat/{appcode}/{keywordidx}/info \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatList|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:113|api/v1.9/Chat \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatListNonJWT|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:146|api/v1.9/Chat \| api/v1.9/Chat/{appcode}/list \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageList|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:428|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/messages \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatMessageListNonJWT|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:477|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/messages \| api/v1.9/chat/{chatidx}/messages/{appcode}:unauth \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatOut|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:356|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/users \| api/v1.9/chat/{chatidx}/users/{chatuseridx} \| api/v1.9/chat/{chatidx}/users/{chatuseridx}:out \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserInfo|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:385|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/users \| api/v1.9/chat/{chatidx}/users/{chatuseridx} \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:324|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/users \| api/v1.9/chat/{chatidx}/users/{chatuseridx} \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestChatUserUpdate|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:326|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/users \| api/v1.9/chat/{chatidx}/users/{chatuseridx} \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestCommonInfo|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:508|api/v1.2/Common|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestGetServiceBlock|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:639|api/v1.9/Users \| api/v1.9/Users/service-block|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestMessageDelete|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:680|api/v1.9/Chat \| api/v1.9/Chat/{chatidx}/openchat \| api/v1.9/chat/{chatidx}/messages \| api/v1.9/chat/{chatidx}/messages/{chatmessageidx}/openchat:admin \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestOpenchatDiplayUpdate|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:230|api/v1.9/Chat \| api/v1.9/Chat/openchat/display/{display} \| api/v1.9/Chat/{chatidx}/openchat \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestServiceBlockUser|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:607|api/v1.9/Users \| api/v1.9/Users/service-block|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserBan|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:539|api/v1.9/Users \| api/v1.9/users/{useridx}/ban|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserInfoByJWT|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:248|api/v1.9/Users|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|RequestUserReport|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:569|api/v1.2/users/{useridx}/report|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|SendMessage|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:725|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/messages \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApi|SetDefaultHeader|Finup.Chat.NET.Blazor.Core/Protocols/ChatApi.cs:767|api/v1.9/Chat \| api/v1.9/chat/{chatidx}/files \| api/v1.9/chat/{chatidx}/files:upload \| api/v{version:apiVersion}/Chat|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApiAuth|RequestUserJwtByApiKey|Finup.Chat.NET.Blazor.Core/Protocols/ChatApiAuth.cs:159|api/v1.9/Auth/token:apikey|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApiAuth|RequestUserJwtByCookie|Finup.Chat.NET.Blazor.Core/Protocols/ChatApiAuth.cs:128|api/v1.9/Auth/token:cookie|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
|Finup.Chat.NET.Blazor.Core|ChatApiAuth|RequestUserJwtFromStockService|Finup.Chat.NET.Blazor.Core/Protocols/ChatApiAuth.cs:41|api/auth/app|정적 외부 호출 없음|||N/A|대상 외부 프로젝트 소스에서 해당 endpoint 호출 메소드명 호출을 찾지 못함.|
## 외부 프로젝트 참조 관계(비-Api/비-UnitTest)

- CSV: `/mnt/c/reports/code-research/api-endpoint/finup_endpoint_second_level_project_refs.csv`

|대상 프로젝트|참조 프로젝트|분석|
|---|---|---|
|FinUp.Finance|FinUp.Finance.Admin|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.General|FinUp.Core.HealthCheck|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.General|FinUp.General.Admin|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.General|FinUp.General.MobileWeb|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.General|FinUp.General.Web|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Finance.Admin|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Radar.App.AlphaBot|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.Admin|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.App.AlphaBot|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.App.AlphaBot.Test|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.Challenger|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.ChallengerWeb|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.Mentor|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.MobileWeb|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.Stock.Web|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Biz|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Biz.Mapper|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Biz.MongoDB|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Biz.Redis|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.ChartCapture.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Fundamentals|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Log|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Model|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Price.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Price.DataMapper|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Price.Kiwoom|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Price.Middleware.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Price.eBest|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Price.eBest.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.RoboAnalysis.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.Signal.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.SignalQueue.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|FinUp.Stock|FinUp.StockData.StockWatch.App|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
|Finup.Chat.NET.Blazor.Core|Finup.Chat.NET.Blazor.WASM|csproj에서 대상 프로젝트 문자열/ProjectReference 확인. endpoint 호출 메소드 직접 호출 여부는 상세 연결 표 참조.|
