---
name: trailbase
description: TrailBase project guide for installing and running the single-executable backend, configuring traildepot/config.textproto and migrations, exposing Record APIs, using auth and token flows, integrating first-party SDKs for TypeScript/JavaScript, Dart/Flutter, Rust, C#/.NET, Swift, Kotlin, Go, and Python, calling HTTP APIs directly, implementing WASM custom endpoints, and locating relevant source/docs in the trailbase repository. Use when Codex needs to answer or implement TrailBase setup, SDK, REST/HTTP API, auth, realtime, configuration, migration, deployment, or custom endpoint work.
---

# TrailBase

Use this skill to work with TrailBase as an application platform: install it, start it, configure `traildepot`, expose data through Record APIs, call HTTP APIs directly, or integrate a first-party SDK.

Prefer current repo files over memory. If the user asks about the public/latest release, package version, Docker tag, or external docs, verify online or from the package registry before giving version-specific advice.

## Workflow

1. Identify the task surface:
   - Install/run/deploy: read `references/install-run.md`.
   - `config.textproto`, migrations, Record API setup, ACLs: read `references/config-and-migrations.md`.
   - Direct HTTP/Auth/Record API calls: read `references/http-api.md`.
   - OAuth, OIDC, PKCE, or "TrailBase as SSO" questions: read `references/oauth-sso.md`.
   - SDK integration: read `references/sdk.md`, then inspect the language-specific client source if precision matters.
   - WASM custom endpoints: read `references/custom-wasm-apis.md`.
   - Repo navigation or implementation changes: read `references/source-map.md`.
2. Verify against source for nontrivial answers. TrailBase has generated docs and multiple clients; source can drift from docs.
3. For code examples, use localhost `http://localhost:4000` unless the user gives another base URL.
4. For auth-sensitive examples, never invent tokens. Show placeholders such as `${AUTH_TOKEN}` or obtain tokens from a real login command if credentials are provided.

## Core Facts

- TrailBase is a single executable named `trail`; `trail run` starts a local server on `localhost:4000` and bootstraps `./traildepot`.
- Admin UI is at `/_/admin/`; optional auth UI is added with `trail components add trailbase/auth_ui` and then lives under `/_/auth/login`.
- Record APIs expose `STRICT` SQLite `TABLE`s or `VIEW`s with an `INTEGER`, UUIDv4, or UUIDv7 primary key.
- Main public Record API path is `/api/records/v1/<api-name>`.
- Main auth path is `/api/auth/v1`.
- Auth tokens are sent with `Authorization: Bearer <auth_token>`; refresh and CSRF tokens may also be represented as `Refresh-Token` and `CSRF-Token` headers by SDKs.
- TrailBase can broker sign-in through configured external OAuth/OIDC providers and supports an auth-code + PKCE handoff to native or different-origin apps. Do not describe it as a full OAuth/OIDC identity provider unless the current source has added standard IdP endpoints such as authorization, discovery, JWKS, and userinfo.
- Realtime subscriptions are exposed under `/api/records/v1/<api-name>/subscribe/<id-or-*>`.

## Validation

When changing a TrailBase repo checkout, prefer focused validation:

```sh
cargo test -p trailbase-client
pnpm --filter trailbase test
trail help
trail run
```

Pick commands that match the files touched. If commands require missing dependencies, report the exact blocker and still provide source-backed reasoning.
