# HTTP API

Use this for raw curl/fetch integration, auth endpoints, Record API endpoints, list query parameters, file endpoints, and realtime subscriptions.

## Paths

Base examples assume:

```text
http://localhost:4000
```

Auth base:

```text
/api/auth/v1
```

Record API base:

```text
/api/records/v1
```

## Auth

Password login:

```sh
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"email": "admin@localhost", "password": "secret"}' \
  http://localhost:4000/api/auth/v1/login
```

The response contains tokens such as:

```json
{
  "auth_token": "...",
  "refresh_token": "...",
  "csrf_token": "..."
}
```

Use the auth token:

```sh
--header "Authorization: Bearer ${AUTH_TOKEN}"
```

SDKs also build `Refresh-Token` and `CSRF-Token` headers when those token values exist.

Other important auth endpoints implemented by SDKs include:

- `POST /api/auth/v1/refresh`
- `POST /api/auth/v1/logout`
- `GET /api/auth/v1/status`
- `POST /api/auth/v1/token`
- `POST /api/auth/v1/login_mfa`
- `POST /api/auth/v1/otp/request`
- `POST /api/auth/v1/otp/login`
- `POST /api/auth/v1/change_email`
- `GET /api/auth/v1/avatar/<user-id>`
- `GET /api/auth/v1/oauth/providers`
- OAuth login/callback under `/api/auth/v1/oauth/<provider>/...`

For native/different-origin auth UI flows, TrailBase supports auth-code flow with PKCE: pass `response_type=code`, `pkce_code_challenge=<url-safe-base64-sha256-verifier>`, and `redirect_uri=<target>` to login/OAuth login, then exchange the auth code at `/api/auth/v1/token`.

For OAuth/OIDC SSO boundaries, see `references/oauth-sso.md`. In current source, TrailBase acts as an app auth service and external OAuth/OIDC login broker; do not assume standard OIDC provider endpoints are present.

## Record CRUD

Create:

```sh
curl \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer ${AUTH_TOKEN}" \
  --request POST \
  --data '{"text_not_null": "test"}' \
  http://localhost:4000/api/records/v1/simple_strict_table
```

Read:

```sh
curl \
  --header "Authorization: Bearer ${AUTH_TOKEN}" \
  http://localhost:4000/api/records/v1/simple_strict_table/<RECORD_ID>
```

Update:

```sh
curl \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer ${AUTH_TOKEN}" \
  --request PATCH \
  --data '{"text_not_null": "updated"}' \
  http://localhost:4000/api/records/v1/simple_strict_table/<RECORD_ID>
```

Delete:

```sh
curl \
  --header "Authorization: Bearer ${AUTH_TOKEN}" \
  --request DELETE \
  http://localhost:4000/api/records/v1/simple_strict_table/<RECORD_ID>
```

Schema:

```text
GET /api/records/v1/<api-name>/schema
```

## List And Filters

List endpoint:

```text
GET /api/records/v1/<api-name>?<search_params>
```

Example:

```sh
curl --globoff \
  --header "Content-Type: application/json" \
  --header "Authorization: Bearer ${AUTH_TOKEN}" \
  --request GET \
  'http://localhost:4000/api/records/v1/movies?limit=3&order=rank&filter[watch_time][$lt]=120&filter[description][$like]=%love%'
```

Operators used by the TypeScript client:

```text
$eq, $ne, $lt, $lte, $gt, $gte, $like, $re, @within, @intersects, @contains
```

Common list options include `limit`, `cursor`, `order`, `count`, `expand`, `geojson`, and nested `filter[...]` expressions.

## Realtime

Subscribe to one record:

```text
GET /api/records/v1/<api-name>/subscribe/<record-id>
```

Subscribe to all visible changes:

```text
GET /api/records/v1/<api-name>/subscribe/*
```

Subscriptions are SSE-style streams in HTTP clients and have WebSocket support in the TypeScript client implementation.

## Files

The TypeScript client exposes file path helpers:

```text
/api/records/v1/<api-name>/<record-id>/file/<column-name>
/api/records/v1/<api-name>/<record-id>/files/<column-name>/<filename>
```

File columns are modeled with JSON metadata such as `filename`, `mime_type`, `content_type`, and `objectstore_path`.
