# dragonslayer

Beta software for DOW

## CMVP / FIPS 140-3

CMVP/FIPS 140-3 integration is built in and can be used once a certified module is wired.  
**Until then, certification is not claimed.**

See also: [CSTL pre-assessment checklist](docs/CSTL_PREASSESSMENT_CHECKLIST.md).

## Raster Analytics validation

```bash
python3 scripts/verify_raster_analytics.py
```

Prints either:

```text
raster_analytics_activated: true
```

or:

```text
raster_analytics_activated: false
```

### GitHub configuration (required)

| Kind | Name | Notes |
|------|------|--------|
| Variable | `RASTER_ANALYTICS_STATUS_URL` | Status endpoint URL |
| Secret | `RASTER_ANALYTICS_TOKEN` | Auth for the status endpoint |
| Secret (optional) | `RASTER_ANALYTICS_GITHUB_PAT` | Fine-grained PAT for this repo only |

Hub activation for `MasterDragonLegend/dragonslayer` must also be granted in the upstream Raster Analytics service. Until then the verifier reports `false`.

### Workflow

`.github/workflows/raster-analytics-validation.yml` runs on push to `main` and on manual **Actions → Raster Analytics validation → Run workflow**.

### Local check

```bash
export RASTER_ANALYTICS_STATUS_URL="https://your-status-endpoint"
export RASTER_ANALYTICS_TOKEN="..."
export RASTER_ANALYTICS_GITHUB_PAT="..."
python3 scripts/verify_raster_analytics.py --require-activated
```

Never commit tokens. Store them only in GitHub **Settings → Secrets and variables → Actions**.
