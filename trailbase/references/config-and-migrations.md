# Configuration And Migrations

Use this for `traildepot/config.textproto`, Record API exposure, ACLs/access rules, schema migration, and production rollout planning.

## Record API Requirements

To expose a table or view through Record APIs:

- Use a `STRICT` SQLite `TABLE` or `VIEW` so TrailBase can provide type-safe JSON schemas and client bindings.
- Provide an `INTEGER`, UUIDv4, or UUIDv7 primary key.
- Prefer UUIDv4 for hard-to-guess random IDs; prefer `INTEGER` or UUIDv7 for stable sorting and efficient cursor pagination.
- Views can expose subsets, joins, computed columns, and read-only projections. Computed columns need a top-level `CAST(... AS TYPE)` so TrailBase can infer the type.

## Config Example

Record APIs can be configured in admin UI or directly in `<traildepot>/config.textproto`.

```textproto
record_apis: [
  {
    name: "profiles"
    table_name: "profiles"
    conflict_resolution: REPLACE
    acl_authenticated: [READ, CREATE]
    create_access_rule: "_REQ_.user = _USER_.id"
  },
]
```

Key fields:

- `name`: public API name under `/api/records/v1/<name>`.
- `table_name`: source `TABLE` or `VIEW`.
- `conflict_resolution`: insert conflict behavior.
- `autofill_missing_user_id_columns`: fills missing FK-to-`_user(id)` fields with the authenticated user; use only when useful, e.g. static forms. This is plural in the protobuf schema and example configs.
- `acl_world` / `acl_authenticated`: coarse operation matrix.
- `*_access_rule`: SQL boolean rule to narrow access.

The same table/view can be exposed multiple times with different API names and permissions.

## Access Rules

ACL checks run first; SQL access rules narrow access after that. Available pseudo tables:

- `_REQ_`: request fields for `CREATE` and `UPDATE`; absent or explicit `null` fields become `NULL`.
- `_REQ_FIELDS_`: field-presence set for `CREATE` and `UPDATE`; use `'field' IN _REQ_FIELDS_`.
- `_ROW_`: target record for `READ`, `UPDATE`, and `DELETE`.
- `_USER_.id`: authenticated user ID, or `NULL` for unauthenticated requests.

Common owner checks:

```sql
_REQ_.user = _USER_.id
_ROW_.user = _USER_.id
```

Group/capability example:

```sql
(_REQ_.secret = 'foo' AND EXISTS(
  SELECT 1 FROM groups
  WHERE groups.member = _USER_.id
    AND groups.name = 'mygroup'
))
```

Be careful when exposing authorization tables themselves; use tight permissions to avoid privilege escalation.

## Write-Only Columns

Columns whose names start with `_` can be written on insert/update but are hidden from read/list responses. Use views if hidden columns need to be exposed under different names in a read-only API.

## Migrations

Migration files live under `traildepot/migrations/` and use:

```text
U<timestamp>__<name>.sql
```

Create an empty migration:

```sh
trail migration
```

Apply by restarting TrailBase or sending `SIGHUP` to a running instance. Admin UI table changes also generate migrations and apply them.

Migrations are append-only. Do not remove applied migration files. Local reset for experiments: stop TrailBase and remove `traildepot/data/main.db`; schema history is tracked in `main._schema_history`.

## API Rollout Risk

Schema changes to exposed tables/views change API contracts. High-risk changes:

- Adding a `NOT NULL` column without a `DEFAULT`: new creates must provide it.
- Removing a non-null/read-critical column: old clients may break.

For required-field changes, prefer creating a versioned API or compatibility view, migrating clients, then retiring the old API.
