# Custom WASM APIs

Use this for custom HTTP endpoints inside TrailBase using JavaScript, TypeScript, or Rust WASM components.

## Runtime Loading

On startup, TrailBase automatically loads `*.wasm` components found in:

```text
<traildepot>/wasm
```

These components can register arbitrary HTTP handlers.

## Examples

Docs point to:

- TypeScript template: `examples/wasm-guest-ts`
- JavaScript template: `examples/wasm-guest-js`
- Rust examples: `examples/coffee-vector-search/guests/rust`, `client/testfixture/guests/rust`
- TypeScript richer example: `examples/coffee-vector-search/guests/typescript`

Use examples instead of inventing handler APIs. The docs are intentionally thin.

## TypeScript/JavaScript Pattern

The TS examples demonstrate:

- registering parameterized routes such as `{table}`,
- reading request/query parameters,
- querying the database,
- returning string or JSON responses,
- returning HTTP errors.

Relevant files:

- `examples/wasm-guest-ts/src/index.ts`
- `examples/wasm-guest-js/src/index.js`
- `examples/coffee-vector-search/guests/typescript/src/index.ts`

## Rust Pattern

Rust examples use `trailbase_wasm` APIs such as:

```rust
use trailbase_wasm::db::{Value, query};
use trailbase_wasm::http::{HttpError, HttpRoute, Json, Request, StatusCode, routing};
use trailbase_wasm::{Guest, export};
```

Relevant files:

- `examples/coffee-vector-search/guests/rust/src/lib.rs`
- `client/testfixture/guests/rust/src/lib.rs`

The test fixture also demonstrates DB transactions, file reads, fetch, timers, jobs, and SQLite functions.

## Build And Install

Each example has its own `package.json`, `Cargo.toml`, `Makefile`, or Vite/JCO setup. Use the example-local build flow. Copy or output the built `.wasm` into `<traildepot>/wasm` and restart TrailBase if hot reload is not configured.
