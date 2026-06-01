# OAuth, OIDC, And SSO

Use this when the user asks whether TrailBase can be used for OAuth SSO, OIDC, social login, PKCE, or cross-origin/native app login.

## Current Boundary

TrailBase supports:

- Password, OTP, and OAuth-backed login into TrailBase's own auth system.
- Configured external OAuth providers under `auth.oauth_providers`.
- A generic `OIDC0` external provider with `auth_url`, `token_url`, and `user_api_url`.
- Browser/WebView login with an auth-code + PKCE handoff back to native apps, desktop apps, SPAs, or different-origin web apps.
- TrailBase-issued `auth_token`, `refresh_token`, and `csrf_token` after `/api/auth/v1/token`.

Do not describe current TrailBase as a full standards-compliant OAuth2/OIDC identity provider for arbitrary third-party clients unless source verification shows that has changed. In the checked source, the implemented shape is an application auth service and OAuth/OIDC client/broker. It does not expose the usual OIDC provider surface such as:

- `/.well-known/openid-configuration`
- JWKS endpoint
- standard `/authorize`
- standard `/userinfo`
- standard client registration or per-client `client_id` / `scope` management for relying-party apps

TrailBase can still be used as practical SSO for apps you control if those apps delegate login to TrailBase UI or OAuth login routes and then consume TrailBase tokens.

## Configuring External OAuth/OIDC Login

Configure providers in `traildepot/config.textproto` under `auth.oauth_providers`. Built-in provider ids include `APPLE`, `DISCORD`, `GITLAB`, `GOOGLE`, `FACEBOOK`, `MICROSOFT`, `TWITCH`, `YANDEX`, and `GITHUB`. Generic OIDC uses `OIDC0`.

Generic OIDC example:

```textproto
auth {
  oauth_providers: [{
    key: "oidc0"
    value {
      client_id: "<client-id>"
      client_secret: "<client-secret>"
      provider_id: OIDC0
      display_name: "Corporate Login"
      auth_url: "https://idp.example.com/authorize"
      token_url: "https://idp.example.com/token"
      user_api_url: "https://idp.example.com/userinfo"
    }
  }]
  redirect_uri_allowlist: ["https://app.example.com/auth/callback"]
}
```

For native/mobile/desktop callbacks, use `custom_uri_schemes` or explicit `redirect_uri_allowlist` as appropriate.

## Login Flow For App SSO

For a web app or native app that wants TrailBase-mediated SSO:

1. Generate a PKCE verifier and challenge in the app.
2. Send the user to TrailBase login or provider login:

```text
GET /api/auth/v1/oauth/<provider>/login?response_type=code&pkce_code_challenge=<challenge>&redirect_uri=<app-callback>
```

You can also use the built-in auth UI:

```text
GET /_/auth/login?response_type=code&pkce_code_challenge=<challenge>&redirect_uri=<app-callback>
```

3. After successful login, TrailBase redirects to the app callback with an authorization code.
4. Exchange the code for TrailBase tokens:

```sh
curl \
  --header "Content-Type: application/json" \
  --request POST \
  --data '{"authorization_code":"<code>","pkce_code_verifier":"<verifier>"}' \
  http://localhost:4000/api/auth/v1/token
```

5. Use the returned TrailBase `auth_token` as:

```text
Authorization: Bearer <auth_token>
```

This is suitable when downstream apps call TrailBase APIs or trust TrailBase JWTs directly. If an app requires standard OIDC discovery, ID tokens, JWKS validation, or a conventional OAuth client configuration screen, verify current source first; older checked source does not provide that full IdP contract.

## Source Checks

Useful source locations:

- `docs/src/content/docs/documentation/auth.mdx`: auth-code + PKCE documentation.
- `crates/core/proto/config.proto`: `OAuthProviderId`, `OAuthProviderConfig`, `oauth_providers`, `custom_uri_schemes`, `redirect_uri_allowlist`.
- `crates/core/src/auth/oauth/login.rs`: external provider login and TrailBase-to-provider PKCE.
- `crates/core/src/auth/oauth/callback.rs`: provider callback and TrailBase authorization-code handoff.
- `crates/core/src/auth/api/token.rs`: app exchanges TrailBase authorization code and PKCE verifier for tokens.
- `crates/core/src/auth/oauth/providers/oidc.rs`: generic OIDC external provider implementation.
- `crates/core/src/auth/oauth/list_providers.rs`: `GET /api/auth/v1/oauth/providers`.
- `crates/auth-ui/src/lib.rs`: built-in auth UI forwarding of `redirect_uri`, `response_type`, and `pkce_code_challenge`.

Search hints:

```sh
rg -n "response_type|pkce_code_challenge|redirect_uri|oauth_providers|OIDC0" crates docs client examples
rg -n "well-known|openid-configuration|jwks|userinfo|authorize" crates docs
```
