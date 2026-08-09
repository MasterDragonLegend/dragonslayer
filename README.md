# dragonslayer

Beta software for DOW

## Raster Analytics validation

This repository validates Raster Analytics activation through:

```bash
python3 scripts/verify_raster_analytics.py
```

The command always prints a line in this format:

```text
raster_analytics_activated: true
```

or:

```text
raster_analytics_activated: false
```

### Required GitHub configuration

Set the following before running the GitHub Actions validation workflow:

- Repository variable: `RASTER_ANALYTICS_STATUS_URL`
- Repository or environment secret: `RASTER_ANALYTICS_TOKEN`
- Optional repository or environment secret: `RASTER_ANALYTICS_GITHUB_PAT`

The workflow sends an authenticated `GET` request to `RASTER_ANALYTICS_STATUS_URL` and adds the current `owner/repo` as the `repository` query parameter. The remote endpoint must return JSON containing `raster_analytics_activated` (or a compatible `active`/`enabled` field) for the repository.

If the integration expects a GitHub personal access token, store it in `RASTER_ANALYTICS_GITHUB_PAT` and grant that PAT access to this repository. Use a **fine-grained personal access token** scoped to `MasterDragonLegend/dragonslayer` with the smallest permissions the upstream Raster Analytics service accepts. Start with read-only repository access (for example `Contents: Read`) and add more only if the service explicitly requires it.

For safety, the verifier only forwards `RASTER_ANALYTICS_GITHUB_PAT` to `github.com` or `api.github.com`. If your Raster Analytics status endpoint is hosted anywhere else, configure `RASTER_ANALYTICS_TOKEN` for that endpoint and keep the PAT limited to GitHub access only.

Hub activation must also be granted in the upstream Raster Analytics service for `MasterDragonLegend/dragonslayer`. Until that external hub-side activation is complete, this repository’s validation path will continue to report `raster_analytics_activated: false`.

### Workflow validation path

The workflow lives at `.github/workflows/raster-analytics-validation.yml`. It runs automatically on pushes to the default branch (`main`) and can also be run manually through **Actions → Raster Analytics validation → Run workflow**.

### Re-run until activation is true

1. Configure `RASTER_ANALYTICS_STATUS_URL`.
2. Configure `RASTER_ANALYTICS_TOKEN`.
3. If required by your GitHub-side integration, configure `RASTER_ANALYTICS_GITHUB_PAT` with repository access.
4. Grant hub-side Raster Analytics activation for `MasterDragonLegend/dragonslayer` in the upstream service.
5. Run the workflow manually, or push to `main`.
6. Open the `Verify Raster Analytics activation` step and check the printed line:
   - `raster_analytics_activated: true` means activation is complete.
   - `raster_analytics_activated: false` means activation is still pending or the endpoint/configuration is not ready.
7. Re-run the workflow after fixing the integration or waiting for the upstream service to finish provisioning.

For local verification, export the same values and run:

```bash
export RASTER_ANALYTICS_STATUS_URL="https://example.invalid/raster/status"
export RASTER_ANALYTICS_TOKEN="..."
export RASTER_ANALYTICS_GITHUB_PAT="..."
python3 scripts/verify_raster_analytics.py --require-activated
```
