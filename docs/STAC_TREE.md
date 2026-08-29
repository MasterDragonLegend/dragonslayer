# SFVN radar / STAC tree

On-disk STAC 1.0 catalog. Not a live STAC API (Core landing only).

```
stac/catalog.json
stac/api/landing.json          # conformsTo Core only
stac/sensors/                  # S1/S2, WV02/03, Landsat, Planet, Esri, GIBS, FIRMS
stac/building-plate/           # plate/suite/room/furniture flags
stac/forensic-media/           # photo/video/audio schemas, seated=false
stac/sfvn-backbone/            # owner stack aliases
scripts/verify_raster_analytics.py
strikeforce/folder_raster.py   # per-pin ±0.05° Maxar probe
strikeforce/stac_validate.py
```

Raster flag: Maxar Discovery `cloud-optimized-archive` via `MAXAR_API_KEY`.
`hub-status.vantor.com` is StatusIQ HTML — not used.

Do not commit secrets.env or data/folders pin lists.
