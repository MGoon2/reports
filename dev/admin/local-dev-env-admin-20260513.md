# front-admin / api-admin 로컬 실행 환경변수 가이드

> 작성일: 2026-05-13
> 대상: 로컬 PC 에서 `front-admin` + `api-admin` 을 직접 띄우는 개발자
> 기준: develop 브랜치 (= Jenkins dev 배포가 주입하는 값 기준)

Jenkins 가 dev/prod 배포 시 `withCredentials` 와 `withEnv` 로 자동 주입하는 모든 변수를, 로컬에서는 직접 채워줘야 한다. 누락이 많아 한 번에 잡기 위해 전수조사 결과를 정리한다.

---

## 0. TL;DR — 두 프로젝트가 짝맞춰야 하는 것

먼저 가장 자주 막히는 5가지:

1. **`FINUP_ADMIN_BFF_SHARED_SECRET`** 은 front-admin / api-admin 양쪽 동일값 필수. 다르면 모든 호출이 BFF HMAC 검증 단계에서 401.
2. **front-admin 의 `ADMIN_API_BASE_URL`** = api-admin 이 뜬 호스트. 로컬 api-admin 띄우면 `http://localhost:8086`, 아니면 `https://api-admin.internal.finup.co.kr` (VPN 필요).
3. **로그인 우회**: api-admin 에 `FINUP_ADMIN_AUTH_STUB_ENABLED=true` 만 켜면 front-admin 로그인 화면에서 id/pw = `admin`/`admin` 으로 통과 가능 (스텁 기본값).
4. **PG 주소 사고 방지**: api-admin `application.yml` 기본값이 **운영 PG (10.0.208.94)** 이라 반드시 `FINUP_PG_URL` 을 dev (`10.0.200.242`) 로 명시 덮어쓰기.
5. **api-radar 도메인**: `api-radar` (하이픈) 사용. 레거시 `apiradar` (하이픈 없음) 절대 사용 금지 — 404 함정 (CLAUDE 메모리에 기록된 재발 함정).

---

## 0-1. 🚨 api-admin 이 아예 부팅 안 되는 변수 (최우선)

application.yml 의 `${X:default}` 패턴과 빈 컨테이너 초기화 코드를 전수 분석한 결과, **빈 값으로 두면 Spring Boot ApplicationContext 가 죽는 변수**는 다음과 같다.

### (1) `FINUP_AUTH_ADMIN_JWT_SECRET` — ApplicationContext 초기화 실패

`AdminJwtTokenProvider.java:35-36` 생성자가 이렇게 동작한다:

```java
byte[] keyBytes = Decoders.BASE64.decode(properties.getSecret());
this.key = Keys.hmacShaKeyFor(keyBytes);
```

- 빈 문자열 또는 Base64 디코딩 결과가 32바이트 미만이면 → `Keys.hmacShaKeyFor` 가 **`WeakKeyException`** 던짐 → `@Component` 빈 생성 실패 → 부팅 실패.
- **반드시 Base64 인코딩 + 디코딩 시 32바이트(256bit) 이상** 의 값이어야 한다. HS256 최소 키 길이 요구사항.
- 평문 임의 문자열 (`local-dev-jwt-secret-...`) 은 Base64 디코드 결과가 의도와 달라 길이 부족할 가능성이 있음 — 권장하지 않음.

권장 생성 방법:

```bash
# Linux / Mac / WSL
openssl rand -base64 48

# Windows PowerShell
[Convert]::ToBase64String((1..48 | ForEach-Object { Get-Random -Maximum 256 }))
```

→ 결과(약 64자, Base64) 를 그대로 `FINUP_AUTH_ADMIN_JWT_SECRET` 에 넣을 것.

### (2) Hikari fail-fast — DB 4종 연결 실패 시 부팅 실패

`application.yml` 의 모든 DataSource 가 `minimum-idle: 5` + `connection-timeout: 30000`. Hikari 가 부팅 시 풀을 채우려 시도하고, 실패하면 fail-fast 로 죽는다.

| 변수 | 빠지면 / 도달 불가면 |
|---|---|
| `FINUP_MSSQL_FINUPADMIN_PASSWORD` | MSSQL master(FinUp) 연결 실패 → 부팅 실패 |
| `FINUP_MSSQL_GUIDE_PASSWORD` | MSSQL FinUpGuide 연결 실패 → 부팅 실패 |
| `FINUP_MSSQL_STOCKDATA_PASSWORD` | MSSQL StockData 연결 실패 → 부팅 실패 |
| `FINUP_PG_PASSWORD` | PG 연결 실패 → 부팅 실패 |
| `FINUP_MSSQL_HOST` (VPN 미접속 등 호스트 도달 불가) | MSSQL 3종 모두 실패 → 부팅 실패 |
| `FINUP_PG_URL` (기본값이 운영 10.0.208.94. dev 비번으론 인증 실패) | PG 연결 실패 → 부팅 실패 |

⚠️ 즉 **dev MSSQL/PG 까지 닿을 수 있는 VPN + 4개 비번** 이 없으면 로컬 api-admin 자체가 안 뜬다. 이게 가장 큰 진입장벽.
(MongoDB 클라이언트는 lazy 라서 부팅엔 영향 없음.)

### 결론: 로컬 부팅 최소 6종

```env
# 1) JWT — Base64 32바이트+ 필수
FINUP_AUTH_ADMIN_JWT_SECRET=<openssl rand -base64 48 결과>

# 2~5) DB 4종 비번 (dev pw)
FINUP_MSSQL_FINUPADMIN_PASSWORD=<dev mssql pw>
FINUP_MSSQL_GUIDE_PASSWORD=<dev mssql pw>
FINUP_MSSQL_STOCKDATA_PASSWORD=<dev mssql pw>
FINUP_PG_PASSWORD=<dev pg pw>

# 6) PG 주소를 dev 로 (기본값이 운영이라 반드시 덮음)
FINUP_PG_URL=jdbc:postgresql://10.0.200.242:1412/finup
```

여기에 VPN 으로 `db.internal.finup.co.kr:1412` (MSSQL) 와 `10.0.200.242:1412` (PG) 도달 가능해야 한다. 이게 충족되면 일단 부팅은 된다. 나머지는 부팅 후 해당 기능 호출 시점에만 실패하므로 화면 단위로 채워가면 된다 (§2.2 의 C/D/E 참고).

### 부팅은 되지만 기능 호출 시 실패 (graceful skip / 호출 실패)

| 변수 | 빠지면 / 동작 |
|---|---|
| `FINUP_ADMIN_BFF_SHARED_SECRET` | 부팅 OK. application.yml 주석 명시 — "미설정 시 BFF 인증은 항상 실패". front-admin BFF 호출 401 가능 |
| `FINUP_RADAR_API_URL` | api-radar 호출 시점에만 실패 |
| `FINUP_CHAT_API_URL` / `FINUP_CHAT_API_KEY` | application.yml:238-239 "미주입 시 호출부는 graceful skip + WARN 로그" |
| `FINUP_DANAL_*_KEY` / `_IV` | Danal 결제 시점에만 실패 |
| `FINUP_ADMIN_SETTLEBANK_CORP_ID` / `_WEB_ID` | SettleBank 실명조회 시점에만 실패 |
| `FINUP_ADMIN_YOUTUBE_API_KEY` | YouTube 검색 화면에서만 실패 |
| `FINUP_STOCK_API_INTERNAL_TOKEN` | 스톡 캐시 reload 호출 시점에만 실패 |
| `@Value` 직접 참조 중 default 없는 것 (`vms.api.*`, `stock.price.address`, `admin.lgu.partner-url`, `finup.web.domain` 등) | 부팅 OK. 해당 페이지 호출 시 NPE 또는 빈 값 호출 실패 |

---

## 1. front-admin (Next.js, port 3006)

### 1.1 .env.local 작성

프로젝트엔 이미 `.env.dev`, `.env.prod`, `.env.example` 가 있다. 로컬은 **`.env.local`** 을 새로 만들어 쓰는 게 가장 깔끔하다 (Next.js 가 자동 우선 적용).

```env
# ============================================================
# front-admin .env.local — 로컬 dev 실행용
# ============================================================

# === 필수: 인증 / BFF ===
# Jenkins 가 dev/prod 별로 주입하던 두 secret. front-admin 쪽은 NextAuth/HMAC 모두
# 평문 32자+ 면 충분 (Base64 강제 아님).
# 단 FINUP_ADMIN_BFF_SHARED_SECRET 은 api-admin 과 "반드시 동일 값" 이어야 함.
NEXTAUTH_SECRET=local-dev-nextauth-secret-min-32chars-xxxxxx
FINUP_ADMIN_BFF_SHARED_SECRET=local-dev-bff-shared-secret-min-32chars-xxxxxx

# === 필수: API 연결 ===
NEXTAUTH_URL=http://localhost:3006

# (A) api-admin 도 로컬에서 띄울 경우
ADMIN_API_BASE_URL=http://localhost:8086
# (B) api-admin 은 dev 인프라 그대로 쓸 경우 (VPN 필요)
# ADMIN_API_BASE_URL=https://api-admin.internal.finup.co.kr

NEXT_PUBLIC_BFF_URL=

# === Mock 끔 ===
USE_MOCK=false
NEXT_PUBLIC_USE_MOCK=false

# === URL (dev 환경값 그대로) ===
NEXT_PUBLIC_FINUP_ADMIN_URL=https://pre-biz.finup.co.kr
NEXT_PUBLIC_TSSA_ADMIN_URL=https://pre-biz.finup.co.kr
NEXT_PUBLIC_STOCK_ADMIN_URL=https://pre-bizstock.finup.co.kr
NEXT_PUBLIC_IMAGE_URL=https://img.internal.finup.co.kr/
NEXT_PUBLIC_STOCK_CACHE_RELOAD_URL=https://pre-stock.finup.co.kr/Common/LoadMainCache.aspx

# === 선택: TradingView 차트 백엔드 (기본값 OK) ===
STOCKDATA_CORE_API_BASE_URL=https://stockdata.finup.co.kr
NEXT_PUBLIC_STOCKDATA_CORE_API_BASE_URL=https://stockdata.finup.co.kr

# === 선택: 신뢰 프록시 (로컬은 127.0.0.1 만 있으면 됨) ===
FINUP_ADMIN_BFF_TRUSTED_PROXIES=127.0.0.1/32,::1/128
```

### 1.2 변수 전수 목록

#### A. 인증 / 보안

| 변수 | 사용처 | 기본값 | 용도 | NEXT_PUBLIC |
|---|---|---|---|---|
| `NEXTAUTH_SECRET` | `src/lib/auth/nextAuth.ts:235` | 없음 (필수) | NextAuth JWT 서명 | No |
| `FINUP_ADMIN_BFF_SHARED_SECRET` | `src/lib/auth/bffSign.ts:28` | 없음 (필수) | BFF ↔ api-admin HMAC 사전 공유 시크릿 | No |
| `FINUP_ADMIN_BFF_TRUSTED_PROXIES` | `src/lib/auth/clientIp.ts:18` | `10.0.0.0/8,172.16.0.0/12,192.168.0.0/16,127.0.0.1/32,::1/128` | X-Forwarded-For 체인 신뢰 CIDR | No |

#### B. API 연결

| 변수 | 사용처 | 기본값 | 용도 | NEXT_PUBLIC |
|---|---|---|---|---|
| `NEXTAUTH_URL` | NextAuth | 없음 | NextAuth 콜백 URL (= 프론트 자기 URL) | No |
| `ADMIN_API_BASE_URL` | `next.config.ts:19`, `src/lib/config/admin-api.ts:31` | 없음 | 서버사이드 api-admin 호출 URL | No |
| `NEXT_PUBLIC_BFF_URL` | `src/lib/config/admin-api.ts:31` | 빈 값 | 클라이언트사이드 BFF URL. 빈 값이면 Next rewrites 가 같은 origin 으로 프록시 | Yes |
| `BACKUP_ADMIN_API_URL` | `src/app/Common/[...path]/route.ts:8,10`, `src/app/api/download/route.ts:10,42` | 없음 | 주 API 실패 시 백업 | No |
| `DOWNLOAD_FALLBACK_ADMIN_API_URL` | `src/app/api/download/route.ts:12,44` | 없음 | 파일 다운로드 전용 폴백 | No |

#### C. 외부 서비스 URL (이미지 / 차트)

| 변수 | 사용처 | 기본값 | 용도 | NEXT_PUBLIC |
|---|---|---|---|---|
| `NEXT_PUBLIC_IMAGE_URL` | `src/lib/file-url.ts:95-96`, `src/app/api/editor/upload/route.ts:12` | 없음 | 이미지 CDN 기준 URL | Yes |
| `NEXT_PUBLIC_STOCK_IMAGE_URL` | `src/app/api/download/route.ts:11,43` | fallback → `NEXT_PUBLIC_IMAGE_URL` | 주식 이미지 전용 (없으면 자동 폴백) | Yes |
| `STOCKDATA_CORE_API_BASE_URL` | `src/app/api/stockchart/marks/route.ts:8`, `src/app/api/stockchart/history/route.ts:12` | `https://stockdata.finup.co.kr` | TradingView 차트 백엔드 (server) | No |
| `NEXT_PUBLIC_STOCKDATA_CORE_API_BASE_URL` | 같은 위치 (line 9, 13) | fallback | 클라이언트 폴백 | Yes |

#### D. 관리자 / 외부 어드민 URL

| 변수 | 사용처 | 기본값 (dev) | 용도 | NEXT_PUBLIC |
|---|---|---|---|---|
| `NEXT_PUBLIC_FINUP_ADMIN_URL` | `.env.dev`, `src/lib/config/admin-api.ts:23` | `https://pre-biz.finup.co.kr` | FinUp 관리자 페이지 링크 | Yes |
| `NEXT_PUBLIC_TSSA_ADMIN_URL` | `.env.dev`, `src/app/(admin)/stock/service/freeitemstocklist/page.tsx:189` | `https://pre-biz.finup.co.kr` | TSSA 관리자 페이지 | Yes |
| `NEXT_PUBLIC_STOCK_ADMIN_URL` | `.env.dev`, `src/components/stock/contents/FeatureVideoDetailContent.tsx:1706` | `https://pre-bizstock.finup.co.kr` | 주식 관리자 페이지 | Yes |
| `NEXT_PUBLIC_STOCK_CACHE_RELOAD_URL` | `.env.dev`, `src/app/(admin)/finup/management/contents/bannerlist/page.tsx:254` | `https://pre-stock.finup.co.kr/Common/LoadMainCache.aspx` | 주식 캐시 리로드 호출 | Yes |

#### E. Mock / 테스트 / 프레임워크

| 변수 | 사용처 | 기본값 | 용도 | NEXT_PUBLIC |
|---|---|---|---|---|
| `USE_MOCK` | `src/lib/auth/nextAuth.ts:41`, `src/lib/api/**/*.api.ts` | `false` | 서버사이드 mock 사용 | No |
| `NEXT_PUBLIC_USE_MOCK` | 동상 | `false` | 클라이언트사이드 mock | Yes |
| `NODE_ENV` | `src/lib/config/admin-api.ts:17` | auto | development/production | No |
| `NEXT_TELEMETRY_DISABLED` | `Dockerfile:13,20` | 없음 | Next.js 원격 분석 비활성화 (`1`) | No |
| `PORT` | `docker-compose.yml:9` | `3006` | 컨테이너 포트 | No |

#### F. Jenkins 가 빌드 시점에 추가 주입 (로컬은 .env.local 에서 직접 설정)

| 변수 | Jenkins Credential ID | 비고 |
|---|---|---|
| `NEXTAUTH_SECRET` | `FINUP_NEXTAUTH_SECRET_${DEPLOY_ENV}` | dev/prod 별 다른 값 |
| `FINUP_ADMIN_BFF_SHARED_SECRET` | `FINUP_ADMIN_BFF_SHARED_SECRET_${DEPLOY_ENV}` | api-admin 과 동일값 필수 |

### 1.3 실행

```bash
cd front-admin
npm run dev -- -p 3006
```

---

## 2. api-admin (Spring Boot, port 8086 / actuator 8186)

api-admin 은 `src/main/resources/application.yml` 하나에 모든 환경변수를 `${ENV:default}` 패턴으로 노출한다. Jenkins 가 주입하는 건 주로 **비밀번호 / secret / 외부 키**.

### 2.1 .env (또는 IDE Run Configuration) 작성

루트의 `api-admin/.env` 에 두고 `docker-compose up` 하거나, IDE Run Configuration 의 Environment Variables 에 그대로 붙여넣는다.

```env
# ============================================================
# api-admin .env — 로컬 dev 실행용
# ============================================================

# === DB: MSSQL (dev 인스턴스 사용, VPN 필요) ===
FINUP_MSSQL_HOST=db.internal.finup.co.kr:1412
FINUP_MSSQL_FINUPADMIN_USERNAME=developer
FINUP_MSSQL_FINUPADMIN_PASSWORD=<dev_mssql_pw>
FINUP_MSSQL_GUIDE_USERNAME=FinUpAdmin
FINUP_MSSQL_GUIDE_PASSWORD=<dev_mssql_pw>
FINUP_MSSQL_STOCKDATA_USERNAME=StockDataAdmin
FINUP_MSSQL_STOCKDATA_PASSWORD=<dev_mssql_pw>

# === DB: PG (dev = 10.0.200.242, 운영 = 10.0.208.94 — 절대 혼동 금지) ===
FINUP_PG_URL=jdbc:postgresql://10.0.200.242:1412/finup
FINUP_PG_USERNAME=finup
FINUP_PG_PASSWORD=<dev_pg_pw>

# === DB: MongoDB Lab (테마) ===
FINUP_MONGO_LAB_URI=mongodb://10.0.15.82:1412
FINUP_MONGO_LAB_DB=Lab

# === 인증 / BFF ===
# JWT_SECRET 은 반드시 Base64 인코딩 + 디코딩 시 32바이트 이상이어야 함 (HS256 최소).
# 빈 값/짧은 값이면 AdminJwtTokenProvider 가 WeakKeyException 으로 부팅 실패.
# 생성: openssl rand -base64 48
FINUP_AUTH_ADMIN_JWT_SECRET=<openssl rand -base64 48 결과 (약 64자 Base64)>
FINUP_ADMIN_BFF_SHARED_SECRET=<임의 32자+ 문자열, front-admin 과 동일>
FINUP_ADMIN_BFF_ENABLED=true
FINUP_ADMIN_JWT_ISSUER=https://devfinup.click
FINUP_ADMIN_AUTH_STUB_ENABLED=true   # 로컬 로그인 우회 (id/pw = admin/admin)

# === URL (dev 환경값) ===
FINUP_IMAGE_BASE_URL=https://img.internal.finup.co.kr
FINUP_STOCK_WEB_URL=https://pre-stock.finup.co.kr
FINUP_MEMBER_LOGIN_AUTH_PC_URL=https://pre.finup.co.kr
FINUP_MEMBER_LOGIN_AUTH_MOBILE_URL=https://pre-m.finup.co.kr
FINUP_RADAR_WEB_URL=https://pre-radar.finup.co.kr
FINUP_MENTOR_SUBDOMAIN=pre-mentorstock
FINUP_ADMIN_CHAT_BANNER_IMAGE_URL=https://pre-chatimg.finup.co.kr
FINUP_ADMIN_CHAT_WEB_ADMIN_URL=https://pre-chatweb.finup.co.kr/admin
FINUP_ADMIN_CHAT_CHANNEL_FINANCE_URL=https://finance.internal.finup.co.kr

# === Danal (테스트 CPID) ===
DANAL_CREDIT_CPID=9810030929
DANAL_AUTO_CREDIT_CPID=9810030929

# === S3 (로컬은 끄는 게 편함) ===
ADMIN_STORAGE_S3_ENABLED=false
FINUP_S3_BUCKET=finup-dev
FINUP_S3_HIDDEN_BUCKET=finup-hidden-dev-326539043145-ap-northeast-2-an

# === 내부 호출 (해당 기능 쓸 때만 채움) ===
# FINUP_RADAR_API_URL=https://api-radar.internal.finup.co.kr/app
# FINUP_CHAT_API_URL=<chat-api dev URL>
# FINUP_CHAT_API_KEY=<chat-api dev key>
# FINUP_CHAT_ROOM_SYNC_ENABLED=true
# FINUP_STOCK_API_INTERNAL_TOKEN=<stock internal dev token>

# === Spring profile ===
SPRING_PROFILES_ACTIVE=local
```

### 2.2 변수 전수 목록

#### A. Jenkins Credentials (Jenkinsfile 가 주입하던 것)

| ENV | Jenkins Credential | 기본값 | 용도 | 로컬값 |
|---|---|---|---|---|
| `FINUP_PG_URL` | `FINUP_PG_URL_{env}` | `jdbc:postgresql://10.0.208.94:1412/finup` (운영) | PG 연결 | `jdbc:postgresql://10.0.200.242:1412/finup` (dev) |
| `FINUP_PG_USERNAME` | `FINUP_PG_USERNAME_{env}` | `finup` | PG user | `finup` |
| `FINUP_PG_PASSWORD` | `FINUP_PG_PASSWORD_{env}` | 없음 | PG pw | dev PG pw |
| `FINUP_MSSQL_HOST` | `FINUP_MSSQL_HOST_{env}` | `db.internal.finup.co.kr:1412` | MSSQL host | 그대로 |
| `FINUP_MSSQL_FINUPADMIN_USERNAME` | 동상 | `developer` | FinUp DB user | `developer` |
| `FINUP_MSSQL_FINUPADMIN_PASSWORD` | 동상 | 없음 | FinUp DB pw | dev MSSQL pw |
| `FINUP_MSSQL_GUIDE_USERNAME` | 동상 | `FinUpAdmin` | FinUpGuide DB user | `FinUpAdmin` |
| `FINUP_MSSQL_GUIDE_PASSWORD` | 동상 | 없음 | FinUpGuide DB pw | dev MSSQL pw |
| `FINUP_MSSQL_STOCKDATA_USERNAME` | 동상 | `StockDataAdmin` | StockData DB user | `StockDataAdmin` |
| `FINUP_MSSQL_STOCKDATA_PASSWORD` | 동상 | 없음 | StockData DB pw | dev MSSQL pw |
| `FINUP_AUTH_ADMIN_JWT_SECRET` | `FINUP_AUTH_ADMIN_JWT_SECRET_{env}` | 없음 | JWT 서명 | 임의 32자+ |
| `FINUP_ADMIN_BFF_SHARED_SECRET` | `FINUP_ADMIN_BFF_SHARED_SECRET_{env}` | 없음 | BFF HMAC | **front-admin 과 동일** |
| `FINUP_ADMIN_SETTLEBANK_CORP_ID` | 동상 | 없음 | SettleBank 기업 ID | 로컬은 생략 가능 |
| `FINUP_ADMIN_SETTLEBANK_WEB_ID` | 동상 | 없음 | SettleBank 웹 ID | 로컬은 생략 가능 |
| `FINUP_DANAL_CREDIT_KEY` | 동상 | 없음 | Danal 단건결제 AES KEY | 로컬은 생략 가능 |
| `FINUP_DANAL_CREDIT_IV` | 동상 | 없음 | Danal 단건결제 AES IV | 로컬은 생략 가능 |
| `FINUP_DANAL_AUTO_CREDIT_KEY` | 동상 | 없음 | Danal 자동결제 AES KEY | 로컬은 생략 가능 |
| `FINUP_DANAL_AUTO_CREDIT_IV` | 동상 | 없음 | Danal 자동결제 AES IV | 로컬은 생략 가능 |
| `FINUP_STOCK_API_INTERNAL_TOKEN` | 동상 | 없음 | api-stock 캐시 reload | 해당 기능 쓸 때만 |
| `FINUP_RADAR_API_URL` | 동상 | 없음 | api-radar 내부 호출 | `https://api-radar.internal.finup.co.kr/app` (dev) |
| `FINUP_CHAT_API_URL` | 동상 | 없음 | service-chat 연동 URL | 해당 기능 쓸 때만 |
| `FINUP_CHAT_API_KEY` | 동상 | 없음 | service-chat 연동 키 | 해당 기능 쓸 때만 |

#### B. Jenkinsfile `withEnv` 하드코딩 (환경별 URL)

| 변수 | Prod | Dev | 로컬 dev 권장 |
|---|---|---|---|
| `IMAGE_BASE` / `FINUP_IMAGE_BASE_URL` | `https://img.finup.co.kr` | `https://img.internal.finup.co.kr` | dev 값 |
| `S3_BUCKET` / `FINUP_S3_BUCKET` | `finup-files-prod-326539043145-ap-northeast-2-an` | `finup-dev` | `finup-dev` |
| `S3_HIDDEN_BUCKET` / `FINUP_S3_HIDDEN_BUCKET` | `finup-hiddenfiles-prod-...` | `finup-hidden-dev-326539043145-ap-northeast-2-an` | dev 값 |
| `STOCK_WEB` / `FINUP_STOCK_WEB_URL` | `https://stock.finup.co.kr` | `https://pre-stock.finup.co.kr` | dev 값 |
| `CHAT_BANNER_IMG` / `FINUP_ADMIN_CHAT_BANNER_IMAGE_URL` | `https://chatimg.finup.co.kr` | `https://pre-chatimg.finup.co.kr` | dev 값 |
| `CHAT_WEB_ADMIN` / `FINUP_ADMIN_CHAT_WEB_ADMIN_URL` | `https://freechat.finup.co.kr/admin` | `https://pre-chatweb.finup.co.kr/admin` | dev 값 |
| `CHAT_CHANNEL_FINANCE` / `FINUP_ADMIN_CHAT_CHANNEL_FINANCE_URL` | `https://chatchannelfinance.finup.co.kr` | `https://finance.internal.finup.co.kr` | dev 값 |
| `PC_URL` / `FINUP_MEMBER_LOGIN_AUTH_PC_URL` | `https://www.finup.co.kr` | `https://pre.finup.co.kr` | dev 값 |
| `MOBILE_URL` / `FINUP_MEMBER_LOGIN_AUTH_MOBILE_URL` | `https://m.finup.co.kr` | `https://pre-m.finup.co.kr` | dev 값 |
| `RADAR_WEB` / `FINUP_RADAR_WEB_URL` | `https://radar.finup.co.kr` | `https://pre-radar.finup.co.kr` | dev 값 |
| `MENTOR_SUBDOMAIN` / `FINUP_MENTOR_SUBDOMAIN` | `mentorstock` | `pre-mentorstock` | dev 값 |
| `JWT_ISSUER` / `FINUP_ADMIN_JWT_ISSUER` | `https://finup.co.kr` | `https://devfinup.click` | dev 값 |
| `DANAL_CREDIT_CPID` | `6010030517` | `9810030929` (Test) | `9810030929` |
| `DANAL_AUTO_CREDIT_CPID` | `D010033582` | `9810030929` (Test) | `9810030929` |
| `FINUP_CHAT_ROOM_SYNC_ENABLED` | `false` | `true` | dev 만 `true` |

#### C. application.yml 토글 변수 (기본값으로 잘 돌아감)

| ENV | 기본 | 비고 |
|---|---|---|
| `FINUP_ADMIN_BFF_ENABLED` | `true` | 로컬에서 BFF 검증 끄려면 `false` (front-admin 우회 가능) |
| `FINUP_ADMIN_BFF_MAX_SKEW_MS` | `60000` | HMAC 타임스탬프 skew 한계 |
| `FINUP_ADMIN_JWT_ACCESS_EXPIRATION_MS` | `3600000` (1h) | 그대로 |
| `FINUP_ADMIN_JWT_REFRESH_EXPIRATION_MS` | `10800000` (3h) | 그대로 |
| `FINUP_ADMIN_JWT_ROLLING_THRESHOLD_MS` | `600000` (10분) | 자동갱신 임계 |
| `FINUP_ADMIN_JWT_AUDIENCE` | `admin` | 그대로 |
| `FINUP_ADMIN_AUTH_STUB_ENABLED` | `false` | **로컬은 `true` 추천** (로그인 우회) |
| `FINUP_ADMIN_AUTH_STUB_LOGIN_ID` | `admin` | 스텁 id |
| `FINUP_ADMIN_AUTH_STUB_PASSWORD` | `admin` | 스텁 pw |
| `FINUP_ADMIN_AUTH_STUB_NAME` | `admin` | 스텁 이름 |
| `FINUP_ADMIN_AUTH_STUB_ROLES` | `ADMIN` | 스텁 권한 |
| `FINUP_ADMIN_COMMUNITY_BOARD_DEFAULT_USER_IDX` | `139537` | 그대로 |
| `FINUP_ADMIN_OPERATION_UPLOAD_DIR` | `./uploads/admin-operation` | 그대로 |
| `FINUP_ADMIN_CHAT_BANNER_UPLOAD_DIR` | `D:/FinUpChat/Files` (Windows) | 로컬 경로로 변경 추천 |
| `FINUP_ADMIN_SETTLEBANK_URL` | `https://van.sbsvc.online/...` | 그대로 |
| `FINUP_FINANCE_REPORT_CF_IDX` | `287724` | 머니서퍼 PLUS 리포트 CFIdx |
| `FINUP_FINANCE_REPORT_C_IDX` | `148799` | 머니서퍼 PLUS 리포트 CIdx |
| `FINUP_FINANCE_REPORT_CATEGORY` | `83` | 카테고리 |
| `FINUP_CHAT_ROOM_SYNC_ENABLED` | `false` | dev 만 `true` |
| `MANAGEMENT_SERVER_PORT` | `8186` | actuator 포트 |

#### D. S3 관련

| ENV | 기본 | 로컬 권장 |
|---|---|---|
| `ADMIN_STORAGE_S3_ENABLED` / `FINUP_S3_ENABLED` | `true` | `false` (로컬 파일시스템) |
| `FINUP_S3_REGION` | `ap-northeast-2` | 그대로 |
| `FINUP_S3_BUCKET` | `finup-dev` | `finup-dev` |
| `FINUP_S3_ENDPOINT` | 없음 | 생략 |
| `FINUP_S3_PROFILE` | 없음 | S3 켤 거면 `finup` (`~/.aws/credentials` 의 프로필) |
| `FINUP_S3_KEY_PREFIX` | `Files` | 그대로 |
| `FINUP_S3_BASE_URL` | `https://img.internal.finup.co.kr` | 그대로 |
| `FINUP_S3_PRIVATE_ACCESS` | `true` | 그대로 |
| `FINUP_S3_PATH_STYLE_ACCESS` | `false` | 그대로 |
| `FINUP_S3_SSE` | `AES256` | 그대로 |
| `FINUP_S3_KMS_KEY_ID` | 없음 | 생략 |
| `FINUP_S3_DEFAULT_MAX_SIZE_BYTES` | `20971520` (20MB) | 그대로 |
| `FINUP_S3_HIDDEN_ENABLED` | `true` | `false` (로컬) |
| `FINUP_S3_HIDDEN_BUCKET` | `finup-hidden-dev-326539043145-ap-northeast-2-an` | 그대로 |
| `FINUP_S3_HIDDEN_KEY_PREFIX` | `Files` | 그대로 |

#### E. @Value 직접 참조 (해당 기능 쓸 때만 필요)

| ENV / 프로퍼티 | 사용처 | 기본값 | 용도 |
|---|---|---|---|
| `vms.api.url` | `VmsService:28` | 없음 | VMS 라이브 스트리밍 API URL |
| `vms.api.key` | `VmsService:30` | 없음 | VMS API Key |
| `admin.server-type` | `FinupAdminSiteService:35` | 없음 | 서버 타입 식별 (LOCAL/DEV/PROD) |
| `admin.stock.banner.cache-reload-urls` | `StockMemberBannerPopupService:30` | `https://api-stock.finup.co.kr/api/stock/internal/main/reload-cache` | 스톡 캐시 리로드 URL (콤마 구분) |
| `admin.stock.banner.cache-reload-token` | `StockMemberBannerPopupService:33` | 없음 | 캐시 리로드 토큰 (= `FINUP_STOCK_API_INTERNAL_TOKEN`) |
| `admin.youtube.api-key` / `FINUP_ADMIN_YOUTUBE_API_KEY` | `StockMemberService:111` | 없음 | YouTube API Key |
| `stock.price.address` | `StockMemberLeagueService:35` | 없음 | 주가 데이터 MTS 주소 |
| `admin.lgu.partner-url` | `StockMemberWiseInvestService:43` | 없음 | LGU+ 파트너 URL |
| `futurewiz.api-flag` | `StockMemberService:114` | `0` | FutureWiz API 플래그 |
| `futurewiz.sdk-flag` | `StockMemberService:117` | `0` | FutureWiz SDK 플래그 |
| `futurewiz.value-id` | `StockMemberService:120` | `STPOINT` | FutureWiz 값 ID |
| `futurewiz.value-type` | `StockMemberService:123` | `P` | FutureWiz 값 타입 |
| `futurewiz.value-ad-url` | `StockMemberService:126` | `http://www.stockpoint.co.kr/Images/sp_logo.png` | FutureWiz 광고 |
| `futurewiz.url.live-create` | `StockMemberService:129` | `http://web2.fnup.com/LiveService/bStart.asp` | FutureWiz 라이브 생성 |
| `futurewiz.url.live-join` | `StockMemberService:132` | `http://web2.fnup.com/LiveService/STPOINT/Player.asp` | FutureWiz 라이브 참여 |
| `futurewiz.url.vod-play` | `StockMemberService:135` | `http://web2.fnup.com/LiveService/STPOINT/vodPlayinfo.asp` | FutureWiz VOD |
| `futurewiz.url.mobile-live` | `StockMemberService:138` | `stockpoint://...` | FutureWiz 모바일 라이브 |
| `futurewiz.streamer.api-base-url` | `StockMemberMentorService:77` | `https://united-player-test.fnup.com/api/v1` | FutureWiz 스트리머 |
| `futurewiz.streamer.secret-key` | `StockMemberMentorService:80` | (해시 기본값) | FutureWiz 스트리머 시크릿 |
| `stock.mentor.web.domain` | `StockMemberMentorService:83` | `finup.co.kr` | 멘토 웹 도메인 |
| `stock.mentor.web.subdomain.{real,staging,dev,local}` | `StockMemberMentorService:86~95` | `mentorstock` / `pre-mentorstock` / `dev-mentorstock` / `pre-mentorstock` | 환경별 멘토 서브도메인 |
| `finup.web.domain` / `pc-subdomain` / `mobile-subdomain` | `FinupMemberService:131~135` | 없음 | FinUp 웹 도메인 (없으면 NPE 가능) |
| `finup.radar.themelog.cache.url1/url2` | `FinupMemberService:159,161` | 없음 | 테마로그 캐시 리로드 |

#### F. Dockerfile / docker-compose 기본

| 설정 | 위치 | 값 |
|---|---|---|
| `TZ` | Dockerfile:3 / docker-compose:14 | `Asia/Seoul` |
| `JAVA_OPTS` | Dockerfile:13 | `-Duser.timezone=Asia/Seoul` |
| `JAVA_TOOL_OPTIONS` | docker-compose:15 | `-Duser.timezone=Asia/Seoul` |
| 포트 | docker-compose:6~10 | `8086:8086` (app) / `8186:8186` (actuator) |

#### G. Gradle bootRun system property (build.gradle:63~68)

| 프로퍼티 | 매핑 ENV | 기본 | 비고 |
|---|---|---|---|
| `spring.profiles.active` | `SPRING_PROFILES_ACTIVE` | `local` | 그대로 |
| `admin.storage.s3.enabled` | `ADMIN_STORAGE_S3_ENABLED` | `true` | 로컬 `false` |
| `admin.storage.s3.profile` | `ADMIN_STORAGE_S3_PROFILE` | `finup` | S3 끄면 무시 |
| `admin.auth.stub-enabled` | `FINUP_ADMIN_AUTH_STUB_ENABLED` | `false` | 로컬 `true` |

### 2.3 실행

```bash
cd api-admin
./gradlew bootRun
```

또는 Docker:

```bash
cd api-admin
IMAGE=finup/api-admin:local docker-compose up -d
```

---

## 3. 체크리스트 (실패 빠르게 잡는 순서)

1. ☐ **`FINUP_ADMIN_BFF_SHARED_SECRET`** 양쪽 동일?
2. ☐ **`NEXTAUTH_SECRET`** 32자 이상?
3. ☐ **front-admin `ADMIN_API_BASE_URL`** 이 실제 api-admin 호스트 가리킴?
4. ☐ **api-admin `FINUP_PG_URL`** 이 운영(10.0.208.94) 아닌 dev(10.0.200.242) 가리킴?
5. ☐ **api-admin MSSQL 3개 pw** 모두 채움? (`FINUPADMIN`, `GUIDE`, `STOCKDATA`)
6. ☐ **`FINUP_AUTH_ADMIN_JWT_SECRET`** 채움?
7. ☐ **로그인 우회 원하면** api-admin `FINUP_ADMIN_AUTH_STUB_ENABLED=true`?
8. ☐ **S3** 안 쓸 거면 `ADMIN_STORAGE_S3_ENABLED=false` + `FINUP_S3_HIDDEN_ENABLED=false`?
9. ☐ **VPN** 또는 인프라 접근 (dev MSSQL/PG/Mongo) 연결 확인?
10. ☐ **api-radar 도메인** `api-radar` 하이픈 포함? (`apiradar` 금지)

---

## 4. 참조

- front-admin `.env.dev`: 같은 레포 `front-admin/.env.dev`
- front-admin `.env.example`: 같은 레포 `front-admin/.env.example`
- api-admin `application.yml`: `api-admin/src/main/resources/application.yml`
- api-admin BFF 보안 강화: `api-admin/.claude/skills/auth-hardening.md` (CLAUDE 메모리: `project_admin_auth_hardening_20260508.md`)
- PG 주소 함정: CLAUDE 메모리 `reference_pg_addresses.md` (dev=10.0.200.242, 운영=10.0.208.94)
- api-radar 함정: CLAUDE 메모리 `feedback_apiradar_vs_api_dash_radar_trap.md`
