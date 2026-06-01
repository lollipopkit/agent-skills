# SDK Integration

Use this for first-party clients and language-specific examples. Always inspect the relevant client source for exact API names when editing real code.

## Packages

Top-level README lists first-party packages:

- JavaScript/TypeScript: npm package `trailbase`
- Dart/Flutter: pub package `trailbase`
- Rust: crate `trailbase-client`
- C#/.NET: NuGet package `TrailBase`
- Swift: `client/swift/trailbase`
- Kotlin: Maven artifact `io.trailbase:trailbase-client`
- Go: `client/go/trailbase`
- Python: PyPI package `trailbase`

Check registries for latest versions before giving version pins.

## TypeScript / JavaScript

Source:

- `client/typescript/src/client.ts`
- `client/typescript/src/record_api.ts`
- mirrored under `crates/assets/js/client/src`

Common shape:

```ts
import { initClient } from "trailbase";

const client = initClient("http://localhost:4000");
await client.login("admin@localhost", "secret");

const api = client.records<{ text_not_null: string }>("simple_strict_table");
const id = await api.create({ text_not_null: "test" });
const row = await api.read(id);
await api.update(id, { text_not_null: "updated" });
await api.delete(id);
```

List with filters:

```ts
const list = await client.records("movies").list({
  pagination: { limit: 3 },
  order: ["rank"],
  filters: [
    { column: "watch_time", op: "lessThan", value: "120" },
    { column: "description", op: "like", value: "%love%" },
  ],
});
```

Subscribe:

```ts
const one = await client.records("simple_strict_table").subscribe(id);
const all = await client.records("simple_strict_table").subscribe("*");
```

Useful APIs from `Client`:

- `tokens()`
- `user()`
- `headers()`
- `records(name)`
- `execute([createOp/updateOp/deleteOp], transaction = true)`
- `avatarUrl(userId?)`
- `login(email, password)`
- `loginSecond({ mfaToken, totpCode })`
- `requestOtp(email, { redirectUri })`
- `loginOtp(email, code)`
- `logout()`
- `refreshAuthToken({ force })`

## Other Language Examples

Docs examples live under:

- `docs/examples/record_api_dart`
- `docs/examples/record_api_swift`
- `docs/examples/record_api_dotnet`
- `docs/examples/record_api_rs`
- `docs/examples/record_api_go`
- `docs/examples/record_api_py`
- `docs/examples/record_api_curl`

There is currently no `docs/examples/record_api_kotlin` directory; use the Kotlin client source and tests directly for Kotlin snippets.

Client implementations live under:

- `client/dart/lib/src/client.dart`
- `client/rust/src/lib.rs`
- `client/dotnet/trailbase`
- `client/swift/trailbase/Sources/TrailBase`
- `client/kotlin/lib/src/commonMain/kotlin/Library.kt`
- `client/go/trailbase`
- `client/python/trailbase/__init__.py`

When asked for a language-specific snippet, start from the docs example for that language when one exists, then verify the methods against the corresponding client implementation. For Kotlin, start from the client source or tests.

## Token Persistence

SDKs expose raw tokens for persistence. Persisting tokens means the app must also drop persisted auth tokens on logout. Logout invalidates refresh tokens immediately; the auth JWT can remain valid until expiry.

## Error Handling

TypeScript has `FetchError` with `status`, `url`, `isClient()`, and `isServer()`. Other clients have language-native error types; inspect source before promising exact behavior.
