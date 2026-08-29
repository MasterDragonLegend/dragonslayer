"""STAC 1.0 + GeoJSON RFC 7946 checks for SFVN catalogs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DISCLAIMER = "OSINT RESEARCH"
ROOT = Path(__file__).resolve().parent
STAC = ROOT / "stac"


def _load(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def validate_stac_item(doc: dict[str, Any], path: str) -> list[str]:
    err = []
    if doc.get("stac_version") != "1.0.0":
        err.append(f"{path}: stac_version")
    if doc.get("type") != "Feature":
        err.append(f"{path}: type!=Feature")
    if not doc.get("id"):
        err.append(f"{path}: missing id")
    if "properties" not in doc:
        err.append(f"{path}: missing properties")
    elif "datetime" not in doc["properties"]:
        err.append(f"{path}: properties.datetime required (null allowed)")
    if "links" not in doc:
        err.append(f"{path}: missing links")
    geom = doc.get("geometry")
    if geom is not None:
        if geom.get("type") == "Point":
            c = geom.get("coordinates") or []
            if len(c) < 2:
                err.append(f"{path}: bad Point")
            else:
                lon, lat = c[0], c[1]
                if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                    err.append(f"{path}: lon/lat out of range (RFC7946 is lon,lat)")
    return err


def validate_collection(doc: dict[str, Any], path: str) -> list[str]:
    err = []
    if doc.get("type") != "Collection":
        err.append(f"{path}: type!=Collection")
    if doc.get("stac_version") != "1.0.0":
        err.append(f"{path}: stac_version")
    if not doc.get("id"):
        err.append(f"{path}: id")
    if "extent" not in doc:
        err.append(f"{path}: extent")
    if "links" not in doc:
        err.append(f"{path}: links")
    return err


def validate_geojson(doc: dict[str, Any], path: str) -> list[str]:
    err = []
    if doc.get("type") != "FeatureCollection":
        err.append(f"{path}: type!=FeatureCollection")
    if "crs" in doc:
        err.append(f"{path}: RFC7946 forbids crs member")
    feats = doc.get("features")
    if not isinstance(feats, list):
        err.append(f"{path}: features[] required")
        return err
    for i, f in enumerate(feats):
        if f.get("type") != "Feature":
            err.append(f"{path}[{i}]: type!=Feature")
        geom = f.get("geometry")
        if geom is None:
            continue
        if geom.get("type") == "Point":
            c = geom.get("coordinates") or []
            if len(c) < 2:
                err.append(f"{path}[{i}]: bad Point")
            else:
                lon, lat = float(c[0]), float(c[1])
                if not (-180 <= lon <= 180 and -90 <= lat <= 90):
                    err.append(f"{path}[{i}]: lon/lat range")
        props = f.get("properties")
        if props is None:
            err.append(f"{path}[{i}]: properties null not object — use {{}}")
    return err


def run() -> dict[str, Any]:
    errors: list[str] = []
    n_items = n_col = n_gj = 0
    for p in STAC.rglob("*.json"):
        doc = _load(p)
        typ = doc.get("type")
        if typ == "Collection" or (typ == "Catalog"):
            if typ == "Collection":
                errors += validate_collection(doc, str(p))
                n_col += 1
            else:
                if doc.get("stac_version") != "1.0.0":
                    errors.append(f"{p}: catalog stac_version")
        elif typ == "Feature" and "stac_version" in doc:
            errors += validate_stac_item(doc, str(p))
            n_items += 1
    for p in [
        ROOT.parent / "SFVN_BACKBONE.geojson",
        ROOT.parent / "PROXY_SITMAP_IMPORT_20260829.geojson",
    ]:
        if p.is_file():
            errors += validate_geojson(_load(p), str(p))
            n_gj += 1
    return {
        "ok": not errors,
        "collections_or_catalogs": n_col,
        "stac_items": n_items,
        "geojson_files": n_gj,
        "errors": errors[:40],
        "n_errors": len(errors),
        "github_api": "401 on MasterDragonLegend/dragonslayer with stored PAT — token rejected; sensors from local stack + Maxar-Public sample URLs only",
        "disclaimer": DISCLAIMER,
    }
