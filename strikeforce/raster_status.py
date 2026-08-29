"""SFVN raster status — two different doors.

hub-status.vantor.com = public StatusIQ HTML dashboard. Not a JSON activation API.
api.maxar.com/discovery = Raster Analytics catalog if MAXAR_API_KEY is entitled.
The dragonslayer verifier flag raster_analytics_activated stays false until Vantor
issues a JSON activation endpoint for this repo.
"""
from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DISCLAIMER = "OSINT RESEARCH"
ROOT = Path(__file__).resolve().parents[1]


def _secrets() -> dict[str, str]:
    out: dict[str, str] = {}
    for p in (ROOT / "secrets.env", ROOT / "satellite_radar_stack" / "config" / "secrets.env"):
        if not p.exists():
            continue
        for line in p.read_text(encoding="utf-8", errors="replace").splitlines():
            if not line or line.startswith("#") or "=" not in line:
                continue
            k, v = line.split("=", 1)
            out[k.strip()] = v.strip()
    return out


def status() -> dict[str, Any]:
    s = _secrets()
    hub = s.get("RASTER_ANALYTICS_STATUS_URL", "")
    key = s.get("MAXAR_API_KEY") or s.get("VITE_API_KEY") or ""
    maxar_ok = False
    maxar_id = None
    maxar_err = None
    if key:
        url = "https://api.maxar.com/discovery/v1/search?maxar_api_key=" + key
        body = json.dumps(
            {"collections": ["cloud-optimized-archive"], "bbox": [-105.0, 40.0, -104.0, 41.0], "limit": 1}
        ).encode()
        req = urllib.request.Request(
            url, data=body, method="POST",
            headers={"Content-Type": "application/json", "User-Agent": "SFVN-raster"},
        )
        try:
            with urllib.request.urlopen(req, timeout=20) as r:
                payload = json.loads(r.read().decode())
            feats = payload.get("features") or []
            maxar_ok = r.status == 200 and bool(feats)
            if feats:
                maxar_id = feats[0].get("id")
        except Exception as e:
            maxar_err = type(e).__name__
    return {
        "ok": True,
        "hub_status_url_host": "hub-status.vantor.com",
        "hub_status_url_kind": "StatusIQ public HTML dashboard — not a JSON activation API",
        "dragonslayer_verifier_activated": False,
        "reason": "Verifier GET on hub-status.vantor.com returns HTML 400. That page is not the Raster Analytics entitlement API.",
        "maxar_discovery_cloud_optimized_archive": maxar_ok,
        "maxar_sample_id": maxar_id,
        "maxar_error": maxar_err,
        "need_for_true_flag": "A Vantor JSON status URL that returns raster_analytics_activated, plus repo grant on MasterDragonLegend/dragonslayer",
        "disclaimer": DISCLAIMER,
    }
