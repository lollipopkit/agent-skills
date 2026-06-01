# TrailBase Skill

Codex skill for working with TrailBase as an application platform: install and
run the `trail` executable, configure `traildepot`, expose Record APIs, use auth
and OAuth flows, call HTTP APIs directly, integrate first-party SDKs, and locate
implementation details in the TrailBase source tree.

## Install

```sh
npx skills add lollipopkit/trailbase.skill
```

## What This Covers

- Local install, Docker, `trail run`, admin UI, and optional auth UI.
- `traildepot/config.textproto`, migrations, Record API setup, ACLs, and access
  rules.
- Raw HTTP usage for auth, Record APIs, file endpoints, and realtime
  subscriptions.
- OAuth/OIDC login, PKCE handoff, and the practical boundary around using
  TrailBase as SSO.
- First-party SDK integration for TypeScript/JavaScript, Dart/Flutter, Rust,
  C#/.NET, Swift, Kotlin, Go, and Python.
- WASM custom endpoint setup.
- Source navigation for implementation or verification work.

## Entry Points

- `SKILL.md`: primary agent instructions and core facts.
- `references/install-run.md`: installation, startup, Docker, admin UI, and auth
  UI.
- `references/config-and-migrations.md`: config, migrations, Record APIs, ACLs,
  and authorization rules.
- `references/http-api.md`: direct HTTP endpoints and curl-style usage.
- `references/oauth-sso.md`: OAuth/OIDC/PKCE/SSO capabilities and limits.
- `references/sdk.md`: SDK integration notes by language.
- `references/custom-wasm-apis.md`: WASM custom endpoint workflow.
- `references/source-map.md`: TrailBase repo layout and search hints.

## OAuth And SSO Boundary

TrailBase can broker sign-in through configured external OAuth/OIDC providers and
can hand an auth code back to native, desktop, SPA, or different-origin web apps
using PKCE. It should not be described as a full standards-compliant OAuth2/OIDC
identity provider unless the current source has added standard IdP endpoints such
as OIDC discovery, JWKS, `/authorize`, `/userinfo`, and client/scope management.

For SSO-like app integration, start with:

```text
references/oauth-sso.md
```

## Verification Rule

Prefer current TrailBase source over cached knowledge. TrailBase has generated
docs, generated clients, and multiple language SDKs, so nontrivial claims should
be checked against the relevant source file before answering or editing.

Useful source checkout, when present:

```text
~/proj/trailbase
```

Focused validation examples:

```sh
cargo test -p trailbase-client
pnpm --filter trailbase test
trail help
trail run
```
