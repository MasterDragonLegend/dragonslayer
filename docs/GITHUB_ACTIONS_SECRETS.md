# GitHub Actions secrets (secure setup)

Do **not** put live tokens in the repo, README, or PR comments.

## Where to configure

Repo → **Settings** → **Secrets and variables** → **Actions**

### Variables (non-secret)

- `RASTER_ANALYTICS_STATUS_URL` — HTTPS status endpoint

### Secrets

- `RASTER_ANALYTICS_TOKEN` — bearer/token for the status URL
- `RASTER_ANALYTICS_GITHUB_PAT` — optional fine-grained PAT scoped to this repo

## Rotation

1. Create the new secret value upstream.
2. Update the GitHub Actions secret.
3. Revoke the old token.
4. Re-run **Raster Analytics validation**.

Never push `.secrets/` or `secrets.env`.
