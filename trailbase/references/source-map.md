# Source Map

Use this to quickly find TrailBase implementation and docs in a local checkout.

https://github.com/trailbaseio/trailbase

## Docs

- Top-level overview/install: `README.md`
- Website docs: `docs/src/content/docs`
- Install guide: `docs/src/content/docs/getting-started/install.mdx`
- Record APIs: `docs/src/content/docs/documentation/apis_record.mdx`
- Custom WASM APIs: `docs/src/content/docs/documentation/apis_js.mdx`
- API overview: `docs/src/content/docs/documentation/apis_overview.mdx`
- Auth: `docs/src/content/docs/documentation/auth.mdx`
- Migrations: `docs/src/content/docs/documentation/migrations.mdx`
- Production: `docs/src/content/docs/documentation/production.mdx`
- Type safety: `docs/src/content/docs/documentation/type_safety.mdx`
- Models and relations: `docs/src/content/docs/documentation/models_and_relations.mdx`
- Benchmarks/FAQ/roadmap: `docs/src/content/docs/reference`

## Server And CLI

- CLI entry: `crates/cli/src/bin/trail.rs`
- CLI args: `crates/cli/src/args.rs`
- CLI library: `crates/cli/src/lib.rs`
- Core server/application: `crates/core/src`
- Config schema: `crates/core/proto/config.proto`
- Auth UI component: `crates/auth-ui`
- Assets/templates/admin/client: `crates/assets`
- WASM runtime host: `crates/wasm-runtime-host`
- WASM guest SDK: `crates/wasm-runtime-guest`

## Clients

- Rust client crate: `client/rust` and `crates/client`
- TypeScript client package: `client/typescript`, mirrored in `crates/assets/js/client`
- Dart client: `client/dart`
- .NET client: `client/dotnet`
- Swift client: `client/swift/trailbase`
- Kotlin client: `client/kotlin`
- Go client: `client/go/trailbase`
- Python client: `client/python`

## Test Fixtures And Examples

- General client integration fixture: `client/testfixture`
- Client integration tests: `client/typescript/tests/integration`, `client/dart/test`, `client/go/trailbase/*_test.go`, etc.
- Docs Record API examples: `docs/examples/record_api_*`
- Blog example: `examples/blog`
- Data CLI tutorial: `examples/data-cli-tutorial`
- WASM guest examples: `examples/wasm-guest-ts`, `examples/wasm-guest-js`
- Vector search example: `examples/coffee-vector-search`

## Search Hints

Use `rg` first:

```sh
rg -n "record_apis|acl_authenticated|access_rule|api/records/v1|api/auth/v1" crates docs client examples
rg -n "subscribe|Refresh-Token|CSRF-Token|auth_token|refresh_token" client crates/assets/js/client
rg -n "config.proto|RecordApi|LoginRequest|RefreshRequest" crates client
rg -n "oauth/providers|response_type|pkce_code_challenge|redirect_uri_allowlist|well-known|jwks|userinfo|OIDC0|oauth_providers" crates docs client examples
```
