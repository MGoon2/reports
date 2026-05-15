# FinUp API Endpoint Inventory

> Design system: MiniMax (`/home/kmyoon/.codex/skills/codex-design/minimax/DESIGN.md`)

- 조사 대상 프로젝트: 18개
- 추출 엔드포인트: 421개
- URL은 Attribute Route를 우선 사용했고, `[controller]`, `[action]`, `v{version:apiVersion}`는 코드의 controller/action/API version 값으로 치환했습니다.
- 레거시 Web API에서 `Route`는 있으나 HTTP verb attribute가 없는 경우 HTTP는 `(unspecified)`로 보존했습니다.

## 프로젝트별 요약

| 프로젝트 명 | 엔드포인트 수 |
|---|---:|
| `FinUp.Auth.Api` | 10 |
| `FinUp.Chat.Api` | 35 |
| `FinUp.Chat.Api.Badge` | 4 |
| `FinUp.Chat.Api.Channel` | 4 |
| `FinUp.Chat.NET.Api` | 136 |
| `FinUp.Chat.NET.Api.Badge` | 2 |
| `FinUp.Chat.NET.Api.Channel` | 4 |
| `FinUp.Chat.NET.Api.ChannerView` | 5 |
| `FinUp.Chat.NET.Api.Push` | 1 |
| `FinUp.General.Api` | 5 |
| `FinUp.LogData.Api` | 6 |
| `FinUp.Mars.Api` | 14 |
| `FinUp.Radar.Api` | 23 |
| `FinUp.Stock.Api` | 56 |
| `FinUp.Stock.Scraper.Api` | 3 |
| `FinUp.StockData.Price.Api` | 93 |
| `FinUp.StockData.Price.Api.Channel` | 2 |
| `FinUp.StockData.Price.Api.RealTime` | 18 |

## 엔드포인트 전수 목록

| 프로젝트 명 | 엔드포인트 URL | 엔드포인트 클래스 | 엔드포인트 메소드 |
|---|---|---|---|
| `FinUp.Auth.Api` | `api/auth/active` | `AuthController` | `GET IsActive` |
| `FinUp.Auth.Api` | `api/auth/app` | `AuthController` | `POST GetAuthApp` |
| `FinUp.Auth.Api` | `api/auth/app/apptoken` | `AuthController` | `POST GetAuthAppToken` |
| `FinUp.Auth.Api` | `api/auth/app/jwt` | `AuthController` | `POST GetAuthSimpleJwt` |
| `FinUp.Auth.Api` | `api/auth/autologin` | `AuthController` | `POST GetAuthAutoLogin` |
| `FinUp.Auth.Api` | `api/auth/logout` | `AuthController` | `GET Logout` |
| `FinUp.Auth.Api` | `api/auth/refresh` | `AuthController` | `POST GetAuthRefresh` |
| `FinUp.Auth.Api` | `api/auth/test` | `AuthController` | `GET TestToken` |
| `FinUp.Auth.Api` | `api/check/health` | `CheckController` | `GET Check` |
| `FinUp.Auth.Api` | `api/Home` | `HomeController` | `GET Index` |
| `FinUp.Chat.Api` | `api/app/chat` | `AppController` | `ChatNoneAuth` |
| `FinUp.Chat.Api` | `api/app/chat/alarmlist` | `AppController` | `Alarm` |
| `FinUp.Chat.Api` | `api/app/chat/auth` | `AppController` | `ChatAuth` |
| `FinUp.Chat.Api` | `api/app/chat/auth/last/signal` | `AppController` | `ChatAuthLastSignalProcess` |
| `FinUp.Chat.Api` | `api/app/chat/auth/signal/edit` | `AppController` | `ChatAuthSignalEditProcess` |
| `FinUp.Chat.Api` | `api/app/chat/auth/signal/edit/preprocess` | `AppController` | `ChatAuthSignalEditPreprocess` |
| `FinUp.Chat.Api` | `api/app/chat/bannedword/refresh` | `AppController` | `GET RefreshChatBannedWord` |
| `FinUp.Chat.Api` | `api/app/chat/banner` | `AppController` | `ChatBannerList` |
| `FinUp.Chat.Api` | `api/app/chat/cacheload` | `AppController` | `GET ChatCacheReload` |
| `FinUp.Chat.Api` | `api/app/chat/cacheload` | `AppController` | `GET ChatCacheReloadChat` |
| `FinUp.Chat.Api` | `api/app/chat/device` | `AppController` | `ChatDevice` |
| `FinUp.Chat.Api` | `api/app/chat/emoticon` | `AppController` | `GET Emoticon` |
| `FinUp.Chat.Api` | `api/app/chat/favorite` | `AppController` | `ChatFavorite` |
| `FinUp.Chat.Api` | `api/app/chat/filedownload` | `AppController` | `GET FileDownload` |
| `FinUp.Chat.Api` | `api/app/chat/files` | `AppController` | `ChatAuthFiles` |
| `FinUp.Chat.Api` | `api/app/chat/filespaging` | `AppController` | `ChatAuthFilesPaging` |
| `FinUp.Chat.Api` | `api/app/chat/fileupload` | `AppController` | `FileUpload` |
| `FinUp.Chat.Api` | `api/app/chat/fileuploaddoc` | `AppController` | `FileUploadDoc` |
| `FinUp.Chat.Api` | `api/app/chat/homelogin` | `AppController` | `ChatMentorWebLogin` |
| `FinUp.Chat.Api` | `api/app/chat/hostroute` | `AppController` | `POST HostRoute` |
| `FinUp.Chat.Api` | `api/app/chat/log` | `AppController` | `ChatLog` |
| `FinUp.Chat.Api` | `api/app/chat/logout` | `AppController` | `GET Logout` |
| `FinUp.Chat.Api` | `api/app/chat/mentor` | `AppController` | `ChatMentor` |
| `FinUp.Chat.Api` | `api/app/chat/profile` | `AppController` | `ChstUserProfile` |
| `FinUp.Chat.Api` | `api/app/chat/subscribe/{userIdx}/{cIdx}` | `AppController` | `GET AddSubscribe` |
| `FinUp.Chat.Api` | `api/app/chat/subscribecancel/{userIdx}/{chatIdx}` | `AppController` | `GET CacnelSubscribe` |
| `FinUp.Chat.Api` | `api/app/chat/update` | `AppController` | `GET Update` |
| `FinUp.Chat.Api` | `api/app/chat/version` | `AppController` | `GET Version` |
| `FinUp.Chat.Api` | `api/app/chat/weblogin` | `AppController` | `ChatUserWebLogin` |
| `FinUp.Chat.Api` | `api/check/health` | `CheckController` | `GET HealthCheck` |
| `FinUp.Chat.Api` | `api/contents/freechatout` | `ContentsController` | `POST FreeChatOut` |
| `FinUp.Chat.Api` | `api/contents/freechatsubscribe` | `ContentsController` | `POST FreeChatSubscribe` |
| `FinUp.Chat.Api` | `api/popup/list` | `PopupController` | `POST GetPopupListAsync` |
| `FinUp.Chat.Api` | `api/report` | `ReportController` | `POST PostReport` |
| `FinUp.Chat.Api` | `api/room/refresh/{chatIdx}` | `RoomController` | `GET RefreshChatRoomAsync` |
| `FinUp.Chat.Api.Badge` | `api/badge/count` | `BadgeController` | `Count` |
| `FinUp.Chat.Api.Badge` | `api/badge/init` | `BadgeController` | `Init` |
| `FinUp.Chat.Api.Badge` | `api/check/health` | `CheckController` | `GET Check` |
| `FinUp.Chat.Api.Badge` | `api/Home` | `HomeController` | `GET Index` |
| `FinUp.Chat.Api.Channel` | `api/Chat/Connect` | `ChatController` | `GET Connect` |
| `FinUp.Chat.Api.Channel` | `api/Chat/ConnectByGet` | `ChatController` | `GET ConnectByGet` |
| `FinUp.Chat.Api.Channel` | `api/Chat/Count` | `ChatController` | `GET Count` |
| `FinUp.Chat.Api.Channel` | `WeatherForecast` | `WeatherForecastController` | `GET Get` |
| `FinUp.Chat.NET.Api` | `api/Check` | `CheckController` | `GET CheckDB` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Auth` | `AuthController` | `POST GetAuth` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Auth/refresh` | `AuthController` | `POST GetAuthRefresh` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Auth/refresh:noneactive` | `AuthController` | `POST GetAuthRefreshNoneActive` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Auth/token` | `AuthController` | `POST GetAuthToken` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Banner` | `BannerController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/banword:refresh` | `BanwordController` | `PATCH RefreshAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Cache` | `CacheController` | `GET Load` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Cache/chat/{chatidx}/messages` | `CacheController` | `GET LoadChatMessage` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Cache/publish` | `CacheController` | `POST PublishAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Cache/state` | `CacheController` | `GET State` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Chat` | `ChatController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Chat` | `ChatController` | `POST Insert` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Chat/update` | `ChatController` | `GET Update` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Chat/{chatidx}` | `ChatController` | `DELETE DeleteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Chat/{chatidx}` | `ChatController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Chat/{chatidx}` | `ChatController` | `PATCH PatchAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/files` | `ChatFilesController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/files/{chatfileidx}` | `ChatFilesController` | `DELETE DeleteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/files/{chatfileidx}:download` | `ChatFilesController` | `GET DownloadFileAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/files/{chatfileidx}:download-app` | `ChatFilesController` | `GET DownloadAppFileAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/files:upload` | `ChatFilesController` | `POST UploadAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/files:upload-robo` | `ChatFilesController` | `POST UploadRoboAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages` | `ChatMessageController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages` | `ChatMessageController` | `POST PostAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages-system` | `ChatMessageController` | `POST PostAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages-url` | `ChatMessageController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages/{chatmessageidx}` | `ChatMessageController` | `DELETE DeleteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages/{chatmessageidx}` | `ChatMessageController` | `GET Get` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages/{chatmessageidx}` | `ChatMessageController` | `PATCH PatchAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages:free` | `ChatMessageController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages:history` | `ChatMessageController` | `GET Get` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages:history-date` | `ChatMessageController` | `GET Get` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages:robo` | `ChatMessageController` | `POST PostRoboAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages:search` | `ChatMessageController` | `GET Get` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/messages:signal` | `ChatMessageController` | `POST PostApiKeyAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/notice` | `NoticeController` | `GET GetNotice` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/notice` | `NoticeController` | `POST PostNoticeAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/notice/{boardidx}` | `NoticeController` | `DELETE DeleteNotice` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/notice/{boardidx}` | `NoticeController` | `GET GetNoticeDetailAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/notice/{boardidx}:admin` | `NoticeController` | `DELETE DeleteNoticeAdmin` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/notice/{boardidx}:admin` | `NoticeController` | `PATCH PatchAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users` | `ChatUsersController` | `GET GetListAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users` | `ChatUsersController` | `POST PostAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}` | `ChatUsersController` | `DELETE DeleteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}` | `ChatUsersController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}` | `ChatUsersController` | `PATCH PatchAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}/favorites` | `ChatUsersController` | `DELETE DeleteFavoriteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}/favorites` | `ChatUsersController` | `POST InsertFavoriteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}:ban` | `ChatUsersController` | `POST BanAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}:enter` | `ChatUsersController` | `POST EnterAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}:enter-Admin` | `ChatUsersController` | `POST EnterAsAdminAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}:out` | `ChatUsersController` | `POST OutAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}:push` | `ChatUsersController` | `POST UpdatePushAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users/{chatuseridx}:writable` | `ChatUsersController` | `POST UpdateWritableAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users:cancel` | `ChatUsersController` | `POST CancelAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users:upsert` | `ChatUsersController` | `POST UpsertAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/chat/{chatidx}/users:writable` | `ChatUsersController` | `POST UpdateWritableAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Emoticon` | `EmoticonController` | `GET GetEmoticon` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Reports` | `ReportsController` | `POST PostReport` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Routing` | `RoutingController` | `GET Get` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Session/api/app/chat/log` | `SessionController` | `POST LegacyLog` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Session/close` | `SessionController` | `GET Close` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Session/enter` | `SessionController` | `GET Enter` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Session/log` | `SessionController` | `POST Log` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Users` | `UsersController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Users` | `UsersController` | `POST PostAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Users/{appuserkey}/profile:sys` | `UsersController` | `POST PostProfileAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Users/{appuserkey}:sys` | `UsersController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Users/{useridx}` | `UsersController` | `DELETE DeleteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Users/{useridx}` | `UsersController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.0/Users/{useridx}` | `UsersController` | `PATCH PatchAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.1/chat/{chatidx}/files` | `ChatFilesController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.1/chat/{chatidx}/files-debug` | `ChatFilesController` | `GET GetDebugAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.1/chat/{chatidx}/files-debug:direction` | `ChatFilesController` | `GET GetDebugDirectionAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.1/chat/{chatidx}/files:direction` | `ChatFilesController` | `GET GetDirectionAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.1/Reports` | `ReportsController` | `GET Get` |
| `FinUp.Chat.NET.Api` | `api/v1.2/chat/{chatidx}/files` | `ChatFilesController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/chat/{chatidx}/files:direction` | `ChatFilesController` | `GET GetDirectionAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/chat/{chatidx}/files:upload` | `ChatFilesController` | `POST UploadAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/chat/{chatidx}/messages` | `ChatMessageController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/chat/{chatidx}/messages` | `ChatMessageController` | `POST PostAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/Common` | `CommonController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/users/{targetuseridx}/report/count:target` | `UserReportController` | `GET GetTargetUserReportCountAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/users/{targetuseridx}/report:target` | `UserReportController` | `GET GetPageAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/users/{useridx}/ban` | `UserBanController` | `GET GetUserBanListAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/users/{useridx}/ban` | `UserBanController` | `POST InsertAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/users/{useridx}/ban/{userbanidx}` | `UserBanController` | `DELETE DeleteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.2/users/{useridx}/report` | `UserReportController` | `POST InsertAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Auth/token:apikey` | `AuthController` | `POST GetAuthFromApikey` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Auth/token:cookie` | `AuthController` | `POST GetAuthFromCookie` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Banner` | `BannerController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/banword:refresh` | `BanwordController` | `PATCH RefreshAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Chat` | `ChatController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Chat` | `ChatController` | `POST Insert` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Chat/openchat/display/{display}` | `ChatController` | `GET GetChatMessageCount` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Chat/{appcode}/list` | `ChatController` | `GET GetAppcodeChatList` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Chat/{appcode}/message-count` | `ChatController` | `GET GetChatMessageCount` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Chat/{appcode}/openchat:theme` | `ChatController` | `POST InsertOpenChatTheme` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Chat/{appcode}/{keywordidx}/info` | `ChatController` | `GET GetChatbyKeyword` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/files` | `ChatFilesController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/files/{chatfileidx}:download` | `ChatFilesController` | `GET DownloadFileAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/files:direction` | `ChatFilesController` | `GET GetDirectionAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/files:upload` | `ChatFilesController` | `POST UploadAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/messages` | `ChatMessageController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/messages` | `ChatMessageController` | `POST PostAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/messages/{appcode}:unauth` | `ChatMessageController` | `GET GetUnAuthAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/messages/{chatmessageidx}/openchat:admin` | `ChatMessageController` | `DELETE DeleteOpenChatAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/messages:system` | `ChatMessageController` | `POST PostApiKeyAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Chat/{chatidx}/openchat` | `ChatController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users` | `ChatUsersController` | `GET GetListAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users` | `ChatUsersController` | `POST PostAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/openchat:enter` | `ChatUsersController` | `POST EnterOpenChatAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}` | `ChatUsersController` | `DELETE DeleteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}` | `ChatUsersController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}` | `ChatUsersController` | `PATCH PatchAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}/favorites` | `ChatUsersController` | `DELETE DeleteFavoriteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}/favorites` | `ChatUsersController` | `POST InsertFavoriteAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}:ban` | `ChatUsersController` | `POST BanAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}:enter` | `ChatUsersController` | `POST EnterAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}:enter-Admin` | `ChatUsersController` | `POST EnterAsAdminAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}:out` | `ChatUsersController` | `POST OutAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}:push` | `ChatUsersController` | `POST UpdatePushAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users/{chatuseridx}:writable` | `ChatUsersController` | `POST UpdateWritableAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users:cancel` | `ChatUsersController` | `POST CancelAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users:upsert` | `ChatUsersController` | `POST UpsertAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{chatidx}/users:writable` | `ChatUsersController` | `POST UpdateWritableAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/chat/{useridx}/{appcode}/messages/delete-all-message` | `ChatMessageController` | `DELETE DeleteServiceBlockUserMessageAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Users` | `UsersController` | `GET GetAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Users` | `UsersController` | `POST PostAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Users/service-block` | `UsersController` | `GET GetUserServiceBlockAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Users/service-block` | `UsersController` | `POST PostUserServiceBlockAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Users/service-block/{blockidx}` | `UsersController` | `DELETE DeleteUserServiceBlockAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/Users/user-alarm` | `UsersController` | `POST GetUserAlarmList` |
| `FinUp.Chat.NET.Api` | `api/v1.9/users/{useridx}/ban` | `UserBanController` | `GET GetUserBanListAsync` |
| `FinUp.Chat.NET.Api` | `api/v1.9/users/{useridx}/ban` | `UserBanController` | `POST InsertAsync` |
| `FinUp.Chat.NET.Api.Badge` | `api/Check` | `CheckController` | `GET CheckDB` |
| `FinUp.Chat.NET.Api.Badge` | `api/v1.0/chat/{chatIdx}/users/{chatuseridx}/badge:init` | `BadgeController` | `POST Init` |
| `FinUp.Chat.NET.Api.Channel` | `api/v{version:apiVersion}/Chat` | `ChatController` | `GET Connect` |
| `FinUp.Chat.NET.Api.Channel` | `api/v{version:apiVersion}/Chat/client/count` | `ChatController` | `GET Count` |
| `FinUp.Chat.NET.Api.Channel` | `api/v{version:apiVersion}/Chat/connect` | `ChatController` | `GET ConnectByGet` |
| `FinUp.Chat.NET.Api.Channel` | `api/v{version:apiVersion}/Chat/sse/connect/{chatIdx}` | `ChatController` | `GET SeeConnectAsync` |
| `FinUp.Chat.NET.Api.ChannerView` | `api/v{version:apiVersion}/Auth/VerifyJwtToken` | `AuthController` | `POST VerifyJwtToken` |
| `FinUp.Chat.NET.Api.ChannerView` | `api/v{version:apiVersion}/Auth/VerifyRecaptcha` | `AuthController` | `POST VerifyRecaptcha` |
| `FinUp.Chat.NET.Api.ChannerView` | `api/v{version:apiVersion}/Url/GetUrlDelay` | `UrlController` | `GET GetUrlDelay` |
| `FinUp.Chat.NET.Api.ChannerView` | `api/v{version:apiVersion}/Url/GetUrlParsingResult` | `UrlController` | `POST GetUrlParsingResult` |
| `FinUp.Chat.NET.Api.ChannerView` | `chat/v{version:apiVersion}/ProcessChatWebsocket` | `WebSocketController` | `GET ProcessChatWebsocket` |
| `FinUp.Chat.NET.Api.Push` | `api/Check` | `CheckController` | `GET CheckDB` |
| `FinUp.General.Api` | `api/App` | `AppController` | `POST Post` |
| `FinUp.General.Api` | `api/check/health` | `CheckController` | `GET HealthCheck` |
| `FinUp.General.Api` | `api/oorione/checkreward` | `OorioneController` | `POST CheckReward` |
| `FinUp.General.Api` | `api/oorione/checkuser` | `OorioneController` | `POST CheckUser` |
| `FinUp.General.Api` | `api/oorione/orderuser` | `OorioneController` | `POST OrderUser` |
| `FinUp.LogData.Api` | `Log` | `LogController` | `GET Get` |
| `FinUp.LogData.Api` | `Log/Logging` | `LogController` | `POST Logging` |
| `FinUp.LogData.Api` | `Log/Ping` | `LogController` | `POST Ping` |
| `FinUp.LogData.Api` | `Log/PushResponse` | `LogController` | `POST PushResponse` |
| `FinUp.LogData.Api` | `Log/System` | `LogController` | `POST System` |
| `FinUp.LogData.Api` | `Log/SystemList` | `LogController` | `POST SystemList` |
| `FinUp.Mars.Api` | `api/v1.0/Expression` | `ExpressionController` | `GET Get` |
| `FinUp.Mars.Api` | `api/v1.0/Home` | `HomeController` | `GET Index` |
| `FinUp.Mars.Api` | `api/v1.0/Images/themeus` | `ImagesController` | `GET Index` |
| `FinUp.Mars.Api` | `api/v1.0/Search/history` | `SearchController` | `GET GetUserSearchHistory` |
| `FinUp.Mars.Api` | `api/v1.0/Search/history/exp/{expressionIdx}` | `SearchController` | `GET GetUserSearchHistory` |
| `FinUp.Mars.Api` | `api/v1.0/Search/history/{userStockSearchIdx}` | `SearchController` | `DELETE DeleteUserSearchHistory` |
| `FinUp.Mars.Api` | `api/v1.0/Search/stock/{code}` | `SearchController` | `GET GetStock` |
| `FinUp.Mars.Api` | `api/v1.0/Search/stock/{code}/exp/{expressoinIdx}` | `SearchController` | `GET GetExpressionResultStock` |
| `FinUp.Mars.Api` | `api/v1.0/Search/ticker/{code}` | `SearchController` | `GET GetTicker` |
| `FinUp.Mars.Api` | `api/v1.0/Search/ticker/{code}/exp/{expressoinIdx}` | `SearchController` | `GET GetExpressionResultTicker` |
| `FinUp.Mars.Api` | `api/v1.0/Search/{name}` | `SearchController` | `GET Search` |
| `FinUp.Mars.Api` | `api/v1.0/Video` | `VideoController` | `POST Get` |
| `FinUp.Mars.Api` | `api/v1.0/WeatherForecast` | `WeatherForecastController` | `GET Get` |
| `FinUp.Mars.Api` | `api/v1.0/WeatherForecast` | `WeatherForecastController` | `POST Post` |
| `FinUp.Radar.Api` | `api/App` | `AppController` | `OPTIONS Option` |
| `FinUp.Radar.Api` | `api/App` | `AppController` | `POST Post` |
| `FinUp.Radar.Api` | `api/App` | `AppController` | `GET setCache` |
| `FinUp.Radar.Api` | `api/App` | `AppController` | `GET setCacheData` |
| `FinUp.Radar.Api` | `api/Web` | `WebController` | `GET getIssueKeyword` |
| `FinUp.Radar.Api` | `api/Web` | `WebController` | `GET getKeywordPriceDetail` |
| `FinUp.Radar.Api` | `Cache/CacheCheck` | `CacheController` | `GET SetCache` |
| `FinUp.Radar.Api` | `Cache/Keyword` | `CacheController` | `GET SetCacheKeyword` |
| `FinUp.Radar.Api` | `cache/setcache` | `CacheController` | `POST setCache` |
| `FinUp.Radar.Api` | `Cache/setCacheGet` | `CacheController` | `GET setCacheGet` |
| `FinUp.Radar.Api` | `cache/setcacheindustry` | `CacheController` | `POST SetCacheIndustry` |
| `FinUp.Radar.Api` | `Cache/Update` | `CacheController` | `GET Update` |
| `FinUp.Radar.Api` | `Cache/WordFilter` | `CacheController` | `GET SetCacheWordFilter` |
| `FinUp.Radar.Api` | `Data/IndustryDiff` | `DataController` | `GET GetDiff` |
| `FinUp.Radar.Api` | `Engine/KeywordData` | `EngineController` | `GET GetKeywordData` |
| `FinUp.Radar.Api` | `getHealthCheck` | `AppController` | `GET getHealthCheck` |
| `FinUp.Radar.Api` | `getThemeLogTopTheme` | `AppController` | `GET getThemeLogTopTheme` |
| `FinUp.Radar.Api` | `getUserIp` | `AppController` | `GET getUserIp` |
| `FinUp.Radar.Api` | `sendThemeLogToTelegram` | `AppController` | `GET sendThemeLogToTelegram` |
| `FinUp.Radar.Api` | `sendThemeLogToTelegramTest` | `AppController` | `GET sendThemeLogToTelegramTest` |
| `FinUp.Radar.Api` | `setAttentionNews` | `AppController` | `GET setAttentionNews` |
| `FinUp.Radar.Api` | `setScheduleNewsBriefing` | `AppController` | `GET setScheduleNewsBriefing` |
| `FinUp.Radar.Api` | `setThemeLogCache` | `AppController` | `GET setThemeLogCache` |
| `FinUp.Stock.Api` | `api/App` | `AppController` | `GET RemoveChatUser` |
| `FinUp.Stock.Api` | `api/App` | `AppController` | `GET SetPushLog` |
| `FinUp.Stock.Api` | `api/App` | `AppController` | `GET SetPushLogUserIdx` |
| `FinUp.Stock.Api` | `api/ban/banuser` | `ReportController` | `POST BanUser` |
| `FinUp.Stock.Api` | `api/ban/cancelbanuser` | `ReportController` | `POST CancelBanUser` |
| `FinUp.Stock.Api` | `api/chat/homelogin` | `ChatController` | `GET GetHomeLogin` |
| `FinUp.Stock.Api` | `api/chat/mentors` | `ChatController` | `GET GetChatMentorList` |
| `FinUp.Stock.Api` | `api/chat/portfolio` | `ChatController` | `GET GetPortfolio` |
| `FinUp.Stock.Api` | `api/chat/portfolio/signals` | `ChatController` | `GET GetPortfolioSignals` |
| `FinUp.Stock.Api` | `api/chat/portfolioas` | `ChatController` | `DELETE DeletePortfolioAs` |
| `FinUp.Stock.Api` | `api/chat/portfolioas` | `ChatController` | `GET GetAsDetail` |
| `FinUp.Stock.Api` | `api/chat/portfolioas` | `ChatController` | `POST InsertAsAsync` |
| `FinUp.Stock.Api` | `api/chat/portfolioas` | `ChatController` | `PATCH UpdateAsAsync` |
| `FinUp.Stock.Api` | `api/chat/portfolioas/list` | `ChatController` | `GET GetAsListPaging` |
| `FinUp.Stock.Api` | `api/chat/robo-popup` | `ChatController` | `GET GetRoboPopupAsync` |
| `FinUp.Stock.Api` | `api/chat/robo/favorite` | `ChatController` | `GET GetRoboFavoriteList` |
| `FinUp.Stock.Api` | `api/chat/robo/favorite` | `ChatController` | `POST ProcessRoboRecommandFavorite` |
| `FinUp.Stock.Api` | `api/chat/robo/search` | `ChatController` | `GET SearchRoboRecommandList` |
| `FinUp.Stock.Api` | `api/chat/signal` | `ChatController` | `POST PostSignalAsync` |
| `FinUp.Stock.Api` | `api/chat/signal/edit` | `ChatController` | `PATCH UpdateLastSignal` |
| `FinUp.Stock.Api` | `api/chat/signal/edit/preprocess` | `ChatController` | `GET CheckLastSignal` |
| `FinUp.Stock.Api` | `api/chat/signal/last` | `ChatController` | `POST PostLastSignalAsync` |
| `FinUp.Stock.Api` | `api/chat/signal/list` | `ChatController` | `GET GetSignalList` |
| `FinUp.Stock.Api` | `api/chat/signal/process` | `ChatController` | `PATCH ProcessSignal` |
| `FinUp.Stock.Api` | `api/chat/signal/process/nonauth` | `ChatController` | `PATCH ProcessSignalNoneAuth` |
| `FinUp.Stock.Api` | `api/chat/signal/robo` | `ChatController` | `POST InsertRoboSignalAsync` |
| `FinUp.Stock.Api` | `api/chat/signal/robo/list` | `ChatController` | `GET GetRoboSignalsAsync` |
| `FinUp.Stock.Api` | `api/chat/signalcodes` | `ChatController` | `GET GetStockSignalCodes` |
| `FinUp.Stock.Api` | `api/chat/update` | `ChatController` | `GET UpdateChat` |
| `FinUp.Stock.Api` | `api/chat/user` | `ChatController` | `GET GetChatUserAsync` |
| `FinUp.Stock.Api` | `api/chat/user/coupon` | `ChatController` | `GET GetUserChatCouponStatus` |
| `FinUp.Stock.Api` | `api/chat/version` | `ChatController` | `GET GetVersion` |
| `FinUp.Stock.Api` | `api/chat/weblogin` | `ChatController` | `GET GetUserWebLogin` |
| `FinUp.Stock.Api` | `api/check/health` | `CheckController` | `GET HealthCheck` |
| `FinUp.Stock.Api` | `api/contents/freechat` | `ChatController` | `POST JoinFreeChat` |
| `FinUp.Stock.Api` | `api/contents/freechat` | `ChatController` | `DELETE OutFreeChat` |
| `FinUp.Stock.Api` | `api/Home` | `HomeController` | `GET Index` |
| `FinUp.Stock.Api` | `api/Join` | `JoinController` | `POST GetCertify` |
| `FinUp.Stock.Api` | `api/Join` | `JoinController` | `GET GetPhoneCount` |
| `FinUp.Stock.Api` | `api/Join` | `JoinController` | `GET SendCertifyEmail` |
| `FinUp.Stock.Api` | `api/Join` | `JoinController` | `GET SendCertifyEmailUser` |
| `FinUp.Stock.Api` | `api/Pay` | `PayController` | `POST PointPay` |
| `FinUp.Stock.Api` | `api/report/user` | `ReportController` | `POST ReportUser` |
| `FinUp.Stock.Api` | `api/Tag` | `TagController` | `GET AutoComplete` |
| `FinUp.Stock.Api` | `api/User` | `UserController` | `GET SetUserAppKeyUpdate` |
| `FinUp.Stock.Api` | `api/user/alarmlist` | `UserController` | `GET GetUserAlarmList` |
| `FinUp.Stock.Api` | `api/vms/schedules/{id}/vods` | `VMSController` | `POST schedulesVod` |
| `FinUp.Stock.Api` | `api/Vod` | `VodController` | `GET SetVodPlay` |
| `FinUp.Stock.Api` | `api/Vod` | `VodController` | `POST SetVodPlay` |
| `FinUp.Stock.Api` | `api/Vod` | `VodController` | `GET SetVodRec` |
| `FinUp.Stock.Api` | `api/Vod` | `VodController` | `POST SetVodRec` |
| `FinUp.Stock.Api` | `api/Vod` | `VodController` | `GET VideoAuth` |
| `FinUp.Stock.Api` | `api/Vod` | `VodController` | `POST accounts` |
| `FinUp.Stock.Api` | `api/Vod` | `VodController` | `POST schedules` |
| `FinUp.Stock.Api` | `api/vod/accounts/{id}/checking_paid` | `VodController` | `POST accountsCheckingPaid` |
| `FinUp.Stock.Api` | `api/vod/schedules/{id}/vods` | `VodController` | `POST schedulesVod` |
| `FinUp.Stock.Scraper.Api` | `Url/Delay` | `UrlController` | `POST Delay` |
| `FinUp.Stock.Scraper.Api` | `Url/List/Parse` | `UrlController` | `POST ParseList` |
| `FinUp.Stock.Scraper.Api` | `Url/Parse` | `UrlController` | `POST Parse` |
| `FinUp.StockData.Price.Api` | `api/alarm/alarm-history-issue-theme` | `RadarAlarmController` | `GET GetIssueThemeList` |
| `FinUp.StockData.Price.Api` | `api/alarm/alarm-history-stock-signal/{type}` | `RadarAlarmController` | `GET GetStockSignalList` |
| `FinUp.StockData.Price.Api` | `api/alarm/alarm-list` | `RadarAlarmController` | `GET GetServiceList` |
| `FinUp.StockData.Price.Api` | `api/chart/capture` | `ChartController` | `GET Capture` |
| `FinUp.StockData.Price.Api` | `api/chart/capture` | `ChartController` | `GET Capture` |
| `FinUp.StockData.Price.Api` | `api/chart/capture/theme` | `ChartController` | `GET CaptureTheme` |
| `FinUp.StockData.Price.Api` | `api/chart/lw/theme` | `ChartController` | `GET GetThemeChartAsync` |
| `FinUp.StockData.Price.Api` | `api/chart/nvd3/minutes/{code}/{minutes}` | `PriceController` | `GET GetCandleAllChart` |
| `FinUp.StockData.Price.Api` | `api/chart/nvd3/{code}` | `PriceController` | `GET GetNvd3Chart` |
| `FinUp.StockData.Price.Api` | `api/chart/stockDeposit` | `ChartController` | `GET StockDepositTrend` |
| `FinUp.StockData.Price.Api` | `api/chart/themeday` | `ChartController` | `GET ThemeDay` |
| `FinUp.StockData.Price.Api` | `api/check/health` | `CheckController` | `GET HealthCheck` |
| `FinUp.StockData.Price.Api` | `api/data/currenthoga/{code}` | `DataController` | `GET GetCurrentHoga` |
| `FinUp.StockData.Price.Api` | `api/data/currenttrader/{code}` | `DataController` | `GET GetCurrentTrader` |
| `FinUp.StockData.Price.Api` | `api/data/financial/{code}/{pageNo?}/{pageSize?}/{isQuarter?}` | `DataController` | `GET GetFinancialDetail` |
| `FinUp.StockData.Price.Api` | `api/data/hoga/last/{code}/{day}/{time}/{count}` | `DataController` | `GET GetLastHoga` |
| `FinUp.StockData.Price.Api` | `api/data/hoga/{code}/{day}/{start}/{end}` | `DataController` | `GET GetHoga` |
| `FinUp.StockData.Price.Api` | `api/data/marketopen/{isRealTime}` | `DataController` | `GET IsTodayMarketOpen` |
| `FinUp.StockData.Price.Api` | `api/data/price/last/{code}/{day}/{time}/{count}` | `DataController` | `GET GetLastPrice` |
| `FinUp.StockData.Price.Api` | `api/data/price/{code}/{day}/{start}/{end}` | `DataController` | `GET GetPrice` |
| `FinUp.StockData.Price.Api` | `api/data/stock/{code}` | `DataController` | `GET GetStockDetailAsync` |
| `FinUp.StockData.Price.Api` | `api/data/trader/last/{code}/{day}/{time}/{count}` | `DataController` | `GET GetLastTrader` |
| `FinUp.StockData.Price.Api` | `api/data/trader/{code}/{day}/{start}/{end}` | `DataController` | `GET GetTrader` |
| `FinUp.StockData.Price.Api` | `api/data/traderday/{code}/{startday}/{endday}` | `DataController` | `GET GetTraderDay` |
| `FinUp.StockData.Price.Api` | `api/data/traderlast/{code}/{day}/{end}` | `DataController` | `GET GetTraderLast` |
| `FinUp.StockData.Price.Api` | `api/data/vi/{code}/{date}` | `DataController` | `GET GetStockVIs` |
| `FinUp.StockData.Price.Api` | `api/dayprice/paging/{code}/{pageNo?}/{pageSize?}` | `PriceController` | `GET GetDayPrice` |
| `FinUp.StockData.Price.Api` | `api/dayprice/{code}/{from}/{to}` | `PriceController` | `GET GetDayPrice` |
| `FinUp.StockData.Price.Api` | `api/index/last` | `IndexController` | `GET GetIndexLast` |
| `FinUp.StockData.Price.Api` | `api/keyword/news` | `KeywordController` | `GET GetKeywordNewsAsync` |
| `FinUp.StockData.Price.Api` | `api/keyword/news/summary-search` | `KeywordController` | `POST GetThemeNewsSummarySearch` |
| `FinUp.StockData.Price.Api` | `api/keyword/stock/golden-signal-form/{stockCode}` | `KeywordController` | `GET GetGoldenSignalStockData` |
| `FinUp.StockData.Price.Api` | `api/keyword/stock/holder/{stockCode}` | `KeywordController` | `GET GetStockHolder` |
| `FinUp.StockData.Price.Api` | `api/keyword/stock/industry/stock/{stockCode}` | `KeywordController` | `GET GetStockRelationIndustry` |
| `FinUp.StockData.Price.Api` | `api/keyword/stock/industry/{industryidx}/{stockcode}` | `KeywordController` | `GET GetIndustryRelationStockAsync` |
| `FinUp.StockData.Price.Api` | `api/keyword/stock/ranking/{type}` | `KeywordController` | `GET GetStockRanking` |
| `FinUp.StockData.Price.Api` | `api/keyword/stock/theme/{stockCode}` | `KeywordController` | `GET GetStockRelationTheme` |
| `FinUp.StockData.Price.Api` | `api/keyword/theme/diff/{keywordidx}` | `KeywordController` | `GET GetThemeDiff` |
| `FinUp.StockData.Price.Api` | `api/keyword/theme/similarity/{keywordidx}` | `KeywordController` | `GET GetKeywordSimilarityTheme` |
| `FinUp.StockData.Price.Api` | `api/keyword/theme/stock/{keywordidx}` | `KeywordController` | `GET GetThemeRelationStock` |
| `FinUp.StockData.Price.Api` | `api/keyword/{keywordidx}` | `KeywordController` | `GET GetKeywordDetailPrice` |
| `FinUp.StockData.Price.Api` | `api/market/{from}/{to}/{offday?}` | `PriceController` | `GET GetMarket` |
| `FinUp.StockData.Price.Api` | `api/news-contents/board` | `NewsContentsController` | `GET UploadNewsContentsBoard` |
| `FinUp.StockData.Price.Api` | `api/news/news_market_issue/{type}` | `RadarAlarmController` | `GET GetServiceList` |
| `FinUp.StockData.Price.Api` | `api/news/NewsListPage` | `NewsController` | `POST NewsListPage` |
| `FinUp.StockData.Price.Api` | `api/news/stock` | `NewsController` | `POST NewsListPageStock` |
| `FinUp.StockData.Price.Api` | `api/news/theme` | `NewsController` | `POST NewsListPageTheme` |
| `FinUp.StockData.Price.Api` | `api/prevday/{date}/{code}` | `PriceController` | `GET GetPrevDay` |
| `FinUp.StockData.Price.Api` | `api/price/diff` | `PriceController` | `POST GetPriceDiffList` |
| `FinUp.StockData.Price.Api` | `api/price/highlow/{code}/{from}` | `PriceController` | `GET GetHighLow` |
| `FinUp.StockData.Price.Api` | `api/price/highlowlist` | `PriceController` | `POST GetHighLowList` |
| `FinUp.StockData.Price.Api` | `api/price/highlowvalue/{code}/{from}` | `PriceController` | `GET GetHighLowValue` |
| `FinUp.StockData.Price.Api` | `api/price/limitprice/{code}` | `PriceController` | `GET GetLimitPrice` |
| `FinUp.StockData.Price.Api` | `api/price/minutes/{code}/{from}/{to}` | `PriceController` | `GET GetMinutes` |
| `FinUp.StockData.Price.Api` | `api/price/quote/{code}` | `PriceController` | `GET GetQuoteAsync` |
| `FinUp.StockData.Price.Api` | `api/price/search-history` | `PriceController` | `POST GetSearchHistoryPrice` |
| `FinUp.StockData.Price.Api` | `api/price/tradesummary/{code}/{from}/{to}` | `PriceController` | `GET GetPriceSummary` |
| `FinUp.StockData.Price.Api` | `api/price/{code}` | `PriceController` | `GET GetPrice` |
| `FinUp.StockData.Price.Api` | `api/pricelist` | `PriceController` | `POST GetPriceList` |
| `FinUp.StockData.Price.Api` | `api/priceliststock/{code}` | `PriceController` | `GET GetPriceListStock` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/chart/count` | `PriceMonitorController` | `POST GetStockCountChart` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/chart/price` | `PriceMonitorController` | `POST GetStockPriceChart` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/list/paging` | `PriceMonitorController` | `POST GetPriceMonitorListPaging` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/paging` | `PriceMonitorController` | `POST GetPriceMonitorPaging` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/preopen` | `PriceMonitorController` | `GET IsPreMarketOpen` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/rank` | `PriceMonitorController` | `POST GetPriceMonitorRank` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/stock` | `PriceMonitorController` | `POST GetPriceMonitorStockPaging` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/stock` | `PriceMonitorController` | `GET GetStock` |
| `FinUp.StockData.Price.Api` | `api/pricemonitor/stock/set` | `PriceMonitorController` | `GET SetStock` |
| `FinUp.StockData.Price.Api` | `api/profit` | `PriceController` | `GET GetItemStockProfit` |
| `FinUp.StockData.Price.Api` | `api/stock/calendar` | `KeywordController` | `GET GetStockOpenDateAsync` |
| `FinUp.StockData.Price.Api` | `api/ThemeCaptureChart` | `ThemeLogController` | `POST GetThemeCaptureChart` |
| `FinUp.StockData.Price.Api` | `api/themelog` | `ThemeLogController` | `POST GetThemeLog` |
| `FinUp.StockData.Price.Api` | `api/ThemeLog/Diff` | `ThemeLogController` | `POST GetThemeDiffList` |
| `FinUp.StockData.Price.Api` | `api/themelog/keyword/Diff` | `ThemeLogController` | `POST GetThemelogKeywordDiffList` |
| `FinUp.StockData.Price.Api` | `api/themelog/keyword/rank` | `ThemeLogController` | `GET GetThemelogKeywordRank` |
| `FinUp.StockData.Price.Api` | `api/themelog/keyword/relation-stocks` | `ThemeLogController` | `POST GetThemeLogRelationStocks` |
| `FinUp.StockData.Price.Api` | `api/ThemeLog/play` | `ThemeLogController` | `POST GetThemePlay` |
| `FinUp.StockData.Price.Api` | `api/ThemeLog/play/info` | `ThemeLogController` | `POST GetThemePlayInfo` |
| `FinUp.StockData.Price.Api` | `api/ThemeLog/ThemeRankingByDiff` | `ThemeLogController` | `GET GetThemeRankingByDiff` |
| `FinUp.StockData.Price.Api` | `api/ThemeRelationStock` | `ThemeLogController` | `POST GetThemeRelationStock` |
| `FinUp.StockData.Price.Api` | `api/tv/config` | `TradingViewController` | `GET GetConfig` |
| `FinUp.StockData.Price.Api` | `api/tv/history` | `TradingViewController` | `GET GetHistory` |
| `FinUp.StockData.Price.Api` | `api/tv/marks` | `TradingViewController` | `GET GetMarks` |
| `FinUp.StockData.Price.Api` | `api/tv/symbol_info` | `TradingViewController` | `GET GetSymbolInfo` |
| `FinUp.StockData.Price.Api` | `api/tv/symbols` | `TradingViewController` | `GET GetSymbols` |
| `FinUp.StockData.Price.Api` | `api/tv/time` | `TradingViewController` | `GET GetTime` |
| `FinUp.StockData.Price.Api` | `api/v2/chart/lw/theme` | `ChartController` | `GET GetThemeChartAsync_v2` |
| `FinUp.StockData.Price.Api` | `api/v2/tv/history` | `TradingViewController` | `GET GetHistoryV2` |
| `FinUp.StockData.Price.Api` | `api/v2/tv/marks` | `TradingViewController` | `GET GetMarks` |
| `FinUp.StockData.Price.Api` | `api/v2/tv/ticker/history` | `TradingViewTickerController` | `GET GetHistoryV2` |
| `FinUp.StockData.Price.Api` | `api/v3/tv/history` | `TradingViewController` | `GET GetHistoryV3` |
| `FinUp.StockData.Price.Api` | `api/v3/tv/marks` | `TradingViewController` | `GET GetMarks` |
| `FinUp.StockData.Price.Api.Channel` | `api/check/health` | `CheckController` | `GET HealthCheck` |
| `FinUp.StockData.Price.Api.Channel` | `api/price/connect` | `PriceController` | `GET ConnectByGet` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Cache/price` | `CacheController` | `GET GetAll` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Cache/price/schedule` | `CacheController` | `GET SchedulePrice` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Cache/price/{code}` | `CacheController` | `GET Get` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Policy/reset` | `PolicyController` | `GET Reset` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Policy/{path?}` | `PolicyController` | `GET Get` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Scope` | `ScopeController` | `GET GetAll` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Scope/count` | `ScopeController` | `GET GetScopeCount` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Scope/count/interval` | `ScopeController` | `GET GetScopeCountInterval` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Scope/count/realtime` | `ScopeController` | `GET GetScopeCountRealtime` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Scope/id/{id}` | `ScopeController` | `GET GetScope` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Scope/ip/{ip}` | `ScopeController` | `GET GetScopeIP` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Sse` | `SseController` | `GET Get` |
| `FinUp.StockData.Price.Api.RealTime` | `api/Sse/test/eventstream` | `SseController` | `GET TestEventstream` |
| `FinUp.StockData.Price.Api.RealTime` | `api/v1.0/Cache/price` | `CacheController` | `GET GetAll` |
| `FinUp.StockData.Price.Api.RealTime` | `api/v1.0/Cache/price/schedule` | `CacheController` | `GET SchedulePrice` |
| `FinUp.StockData.Price.Api.RealTime` | `api/v1.0/Cache/price/{code}` | `CacheController` | `GET Get` |
| `FinUp.StockData.Price.Api.RealTime` | `api/v1.0/Sse` | `SseController` | `GET Get` |
| `FinUp.StockData.Price.Api.RealTime` | `api/v1.0/Sse/price/{code}` | `SseController` | `GET Get` |

## 추출 근거 파일

| 프로젝트 명 | 소스 파일 수 | 주요 라우팅 근거 |
|---|---:|---|
| `FinUp.Auth.Api` | 13 | `FinUp.Auth.Api/Controllers/AuthController.cs:122`<br>`FinUp.Auth.Api/Controllers/AuthController.cs:192`<br>`FinUp.Auth.Api/Controllers/AuthController.cs:243`<br>`FinUp.Auth.Api/Controllers/AuthController.cs:252`<br>`FinUp.Auth.Api/Controllers/AuthController.cs:264`<br>… |
| `FinUp.Chat.Api` | 45 | `FinUp.Chat.Api/Controllers/AppController.Chat.cs:1005`<br>`FinUp.Chat.Api/Controllers/AppController.Chat.cs:1048`<br>`FinUp.Chat.Api/Controllers/AppController.Chat.cs:1057`<br>`FinUp.Chat.Api/Controllers/AppController.Chat.cs:109`<br>`FinUp.Chat.Api/Controllers/AppController.Chat.cs:373`<br>… |
| `FinUp.Chat.Api.Badge` | 11 | `FinUp.Chat.Api.Badge/Controllers/BadgeController.cs:21`<br>`FinUp.Chat.Api.Badge/Controllers/BadgeController.cs:43`<br>`FinUp.Chat.Api.Badge/Controllers/CheckController.cs:15`<br>`FinUp.Chat.Api.Badge/Controllers/HomeController.cs:12` |
| `FinUp.Chat.Api.Channel` | 2 | `FinUp.Chat.Api.Channel/Controllers/ChatController.cs:31`<br>`FinUp.Chat.Api.Channel/Controllers/ChatController.cs:61`<br>`FinUp.Chat.Api.Channel/Controllers/ChatController.cs:78`<br>`FinUp.Chat.Api.Channel/Controllers/WeatherForecastController.cs:27` |
| `FinUp.Chat.NET.Api` | 32 | `FinUp.Chat.NET.Api/Controllers/CheckController.cs:21`<br>`FinUp.Chat.NET.Api/Controllers/v1_0/AuthController.cs:34`<br>`FinUp.Chat.NET.Api/Controllers/v1_0/AuthController.cs:51`<br>`FinUp.Chat.NET.Api/Controllers/v1_0/AuthController.cs:68`<br>`FinUp.Chat.NET.Api/Controllers/v1_0/AuthController.cs:85`<br>… |
| `FinUp.Chat.NET.Api.Badge` | 2 | `FinUp.Chat.NET.Api.Badge/Controllers/CheckController.cs:18`<br>`FinUp.Chat.NET.Api.Badge/Controllers/v1_0/BadgeController.cs:28` |
| `FinUp.Chat.NET.Api.Channel` | 1 | `FinUp.Chat.NET.Api.Channel/Controllers/ChatController.cs:110`<br>`FinUp.Chat.NET.Api.Channel/Controllers/ChatController.cs:42`<br>`FinUp.Chat.NET.Api.Channel/Controllers/ChatController.cs:61`<br>`FinUp.Chat.NET.Api.Channel/Controllers/ChatController.cs:97` |
| `FinUp.Chat.NET.Api.ChannerView` | 3 | `FinUp.Chat.NET.Api.ChannerView/Controllers/v1_0/AuthController.cs:30`<br>`FinUp.Chat.NET.Api.ChannerView/Controllers/v1_0/AuthController.cs:45`<br>`FinUp.Chat.NET.Api.ChannerView/Controllers/v1_0/UrlController.cs:32`<br>`FinUp.Chat.NET.Api.ChannerView/Controllers/v1_0/UrlController.cs:43`<br>`FinUp.Chat.NET.Api.ChannerView/Controllers/v1_0/WebSocketController.cs:34` |
| `FinUp.Chat.NET.Api.Push` | 1 | `FinUp.Chat.NET.Api.Push/Controllers/CheckController.cs:19` |
| `FinUp.General.Api` | 29 | `FinUp.General.Api/Controllers/AppController.cs:22`<br>`FinUp.General.Api/Controllers/CheckController.cs:15`<br>`FinUp.General.Api/Controllers/OorioneController.cs:209`<br>`FinUp.General.Api/Controllers/OorioneController.cs:30`<br>`FinUp.General.Api/Controllers/OorioneController.cs:97` |
| `FinUp.LogData.Api` | 2 | `FinUp.LogData.Api/Controllers/LogController.cs:102`<br>`FinUp.LogData.Api/Controllers/LogController.cs:24`<br>`FinUp.LogData.Api/Controllers/LogController.cs:35`<br>`FinUp.LogData.Api/Controllers/LogController.cs:51`<br>`FinUp.LogData.Api/Controllers/LogController.cs:67`<br>… |
| `FinUp.Mars.Api` | 6 | `FinUp.Mars.Api/Controllers/v1_0/ExpressionController.cs:25`<br>`FinUp.Mars.Api/Controllers/v1_0/HomeController.cs:25`<br>`FinUp.Mars.Api/Controllers/v1_0/ImagesController.cs:16`<br>`FinUp.Mars.Api/Controllers/v1_0/SearchController.cs:105`<br>`FinUp.Mars.Api/Controllers/v1_0/SearchController.cs:116`<br>… |
| `FinUp.Radar.Api` | 85 | `FinUp.Radar.Api/Controllers/AppController.cs:238`<br>`FinUp.Radar.Api/Controllers/AppController.cs:248`<br>`FinUp.Radar.Api/Controllers/AppController.cs:274`<br>`FinUp.Radar.Api/Controllers/AppController.cs:301`<br>`FinUp.Radar.Api/Controllers/AppController.cs:308`<br>… |
| `FinUp.Stock.Api` | 105 | `FinUp.Stock.Api/Controllers/AppController.cs:236`<br>`FinUp.Stock.Api/Controllers/AppController.cs:58`<br>`FinUp.Stock.Api/Controllers/AppController.cs:76`<br>`FinUp.Stock.Api/Controllers/ChatController.cs:1091`<br>`FinUp.Stock.Api/Controllers/ChatController.cs:1127`<br>… |
| `FinUp.Stock.Scraper.Api` | 1 | `FinUp.Stock.Scraper/FinUp.Stock.Scraper.Api/Controllers/UrlController.cs:30`<br>`FinUp.Stock.Scraper/FinUp.Stock.Scraper.Api/Controllers/UrlController.cs:38`<br>`FinUp.Stock.Scraper/FinUp.Stock.Scraper.Api/Controllers/UrlController.cs:46` |
| `FinUp.StockData.Price.Api` | 31 | `FinUp.StockData.Price.Api/Controllers/ChartController.cs:108`<br>`FinUp.StockData.Price.Api/Controllers/ChartController.cs:145`<br>`FinUp.StockData.Price.Api/Controllers/ChartController.cs:155`<br>`FinUp.StockData.Price.Api/Controllers/ChartController.cs:165`<br>`FinUp.StockData.Price.Api/Controllers/ChartController.cs:238`<br>… |
| `FinUp.StockData.Price.Api.Channel` | 7 | `FinUp.StockData.Price.Api.Channel/Controllers/CheckController.cs:14`<br>`FinUp.StockData.Price.Api.Channel/Controllers/PriceController.cs:23` |
| `FinUp.StockData.Price.Api.RealTime` | 6 | `FinUp.StockData.Price.Api.RealTime/Controllers/Legacy/CacheController.cs:31`<br>`FinUp.StockData.Price.Api.RealTime/Controllers/Legacy/CacheController.cs:35`<br>`FinUp.StockData.Price.Api.RealTime/Controllers/Legacy/CacheController.cs:44`<br>`FinUp.StockData.Price.Api.RealTime/Controllers/Legacy/PolicyController.cs:23`<br>`FinUp.StockData.Price.Api.RealTime/Controllers/Legacy/PolicyController.cs:27`<br>… |