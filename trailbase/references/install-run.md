# Install And Run

Use this for installation, local startup, Docker, admin UI, auth UI, and build-from-source questions.

## Binary Install

TrailBase ships as a single executable, `trail`. Users can download a GitHub Release for macOS, Linux, or Windows. The repo README and docs also provide one-line installers:

```sh
# Linux and macOS
curl -sSL https://trailbase.io/install.sh | bash

# Windows PowerShell
iwr https://trailbase.io/install.ps1 | iex
```

Verify installation:

```sh
trail help
```

## Docker

The README shows this local alias pattern:

```sh
alias trail='
  mkdir -p traildepot && \
  docker run \
      -p 4000:4000 \
      -e ADDRESS=0.0.0.0:4000 \
      --mount type=bind,source="$PWD"/traildepot,target=/app/traildepot \
      trailbase/trailbase /app/trail'
```

Check current image tags if the user asks for production or latest Docker usage.

## Start Local Server

```sh
trail run
```

On first start, TrailBase creates `./traildepot`, initializes config/data/secrets, creates an admin user, and prints credentials. Admin UI:

```text
http://localhost:4000/_/admin/
```

Auth UI is optional:

```sh
trail components add trailbase/auth_ui
```

Then open:

```text
http://localhost:4000/_/auth/login
```

## Build From Source

The README lists dependencies: Rust, Node.js, geos, protobuf, pnpm. Build flow:

```sh
git submodule update --init --recursive
pnpm install
cargo build --bin trail
```

Use `--release` only when optimized binary output is needed.

## Production Notes

- Use TLS/HTTPS for auth.
- Built-in TLS starts when `<traildepot>/secrets/certs/key.pem` and `cert.pem` exist.
- Reverse proxies such as nginx/caddy should set `X-Forwarded-For`.
- For SSE/realtime subscriptions behind nginx, disable buffering/cache and avoid connection upgrade assumptions.
- Consider `--admin-address=<IP>:<PORT>` to bind admin APIs/UI to a private address.
- Keep production config read-only where possible, but keep data directories writable.
- Healthcheck endpoint: `/api/healthcheck`.
- Backups are periodically written to `traildepot/backups/backup.db` by default; consider Litestream for continuous replication.
