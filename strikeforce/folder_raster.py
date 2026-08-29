"""Per-pin Maxar raster probe for data/folders.

Tight box ±0.05° around each Point. Seat a collect id only if
cloud-optimized-archive returns a feature in that box.
Does not seat interiors, doors, or command function.
"""
from __future__ import annotations

import json
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

DISCLAIMER = "OSINT RESEARCH"
ROOT = Path(__file__).resolve().parents[1]
FDIR = ROOT / "data" / "folders"
PAD = 0.05


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


def tight_bbox(lon: float, lat: float, pad: float = PAD) -> list[float]:
    return [lon - pad, lat - pad, lon + pad, lat + pad]


def maxar_search(key: str, bbox: list[float]) -> dict[str, Any]:
    url = "https://api.maxar.com/discovery/v1/search?maxar_api_key=" + key
    body = json.dumps(
        {"collections": ["cloud-optimized-archive"], "bbox": bbox, "limit": 1}
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "SFVN-pin-raster"},
    )
    try:
        with urllib.request.urlopen(req, timeout=25) as r:
            payload = json.loads(r.read().decode())
        feats = payload.get("features") or []
        fid = feats[0].get("id") if feats else None
        return {"ok": True, "http": 200, "n": len(feats), "id": fid}
    except urllib.error.HTTPError as e:
        return {"ok": False, "http": e.code, "n": 0, "id": None}
    except Exception as e:
        return {"ok": False, "http": None, "n": 0, "id": None, "error": type(e).__name__}


def run(*, pad: float = PAD, sleep: float = 0.35) -> dict[str, Any]:
    key = _secrets().get("MAXAR_API_KEY") or _secrets().get("VITE_API_KEY") or ""
    if not key:
        return {"ok": False, "error": "MAXAR_API_KEY missing", "disclaimer": DISCLAIMER}
    folders: list[dict[str, Any]] = []
    seated = 0
    scanned = 0
    for path in sorted(FDIR.glob("*.geojson")):
        g = json.loads(path.read_text(encoding="utf-8"))
        feats = g.get("features") or []
        pin_hits = 0
        for f in feats:
            geom = f.get("geometry") or {}
            if geom.get("type") != "Point":
                continue
            lon, lat = float(geom["coordinates"][0]), float(geom["coordinates"][1])
            scanned += 1
            bbox = tight_bbox(lon, lat, pad)
            hit = maxar_search(key, bbox)
            time.sleep(sleep)
            props = f.setdefault("properties", {})
            props["raster_pad_deg"] = pad
            props["raster_bbox"] = bbox
            props["raster_http"] = hit.get("http")
            if hit.get("id"):
                props["raster_id"] = hit["id"]
                props["raster_seated"] = True
                pin_hits += 1
                seated += 1
            else:
                props["raster_id"] = None
                props["raster_seated"] = False
            props["interior"] = False
            props["door"] = False
            props["disclaimer"] = DISCLAIMER
        g["per_pin_raster"] = {"pad_deg": pad, "hits": pin_hits, "n": len(feats)}
        path.write_text(json.dumps(g, indent=2), encoding="utf-8")
        folders.append({"folder": path.stem, "n": len(feats), "raster_seated": pin_hits})
    out = {
        "ok": True,
        "pad_deg": pad,
        "scanned": scanned,
        "seated": seated,
        "folders": folders,
        "rule": "seat raster_id only if tight ±0.05 box returns a collect",
        "disclaimer": DISCLAIMER,
    }
    (FDIR / "PER_PIN_RASTER_SUMMARY.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    return out
