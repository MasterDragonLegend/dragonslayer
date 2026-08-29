#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


def parse_timeout(value: str) -> int:
    try:
        return int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError(
            "timeout values must be integers"
        ) from exc


def default_timeout_from_env() -> int:
    try:
        return parse_timeout(os.environ.get("RASTER_ANALYTICS_TIMEOUT", "15"))
    except argparse.ArgumentTypeError as exc:
        raise SystemExit(f"Invalid RASTER_ANALYTICS_TIMEOUT: {exc}") from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate Raster Analytics activation for this repository."
    )
    parser.add_argument(
        "--status-url",
        default=os.environ.get("RASTER_ANALYTICS_STATUS_URL", ""),
        help="Raster Analytics status endpoint.",
    )
    parser.add_argument(
        "--token",
        default=os.environ.get("RASTER_ANALYTICS_TOKEN", ""),
        help="Raster Analytics API token.",
    )
    parser.add_argument(
        "--repository",
        default=os.environ.get("GITHUB_REPOSITORY", ""),
        help="Repository identifier used by the status endpoint.",
    )
    parser.add_argument(
        "--github-pat",
        default=os.environ.get("RASTER_ANALYTICS_GITHUB_PAT", ""),
        help="Optional GitHub PAT made available to the Raster Analytics endpoint.",
    )
    parser.add_argument(
        "--timeout",
        type=parse_timeout,
        default=default_timeout_from_env(),
        help="Request timeout in seconds.",
    )
    parser.add_argument(
        "--require-activated",
        action="store_true",
        help="Exit non-zero unless Raster Analytics is activated.",
    )
    return parser.parse_args()


def coerce_bool(value) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, (int, float)):
        return bool(value)
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "yes", "on", "active", "enabled"}
    return False


def extract_activation_status(payload) -> bool:
    if isinstance(payload, dict):
        for key in (
            "raster_analytics_activated",
            "activated",
            "active",
            "enabled",
        ):
            if key in payload:
                return coerce_bool(payload[key])
        if "status" in payload:
            return coerce_bool(payload["status"])
        for nested_key in ("data", "result"):
            if nested_key in payload:
                return extract_activation_status(payload[nested_key])
    return False


def allows_github_pat(status_url: str) -> bool:
    hostname = urllib.parse.urlparse(status_url).hostname or ""
    return hostname in {"github.com", "api.github.com"}


def is_statusiq_dashboard(status_url: str) -> bool:
    host = (urllib.parse.urlparse(status_url).hostname or "").lower()
    scheme = urllib.parse.urlparse(status_url).scheme.lower()
    return host == "hub-status.vantor.com" or scheme == "sfvn"


def probe_maxar_raster(repository: str) -> tuple[dict, int]:
    """SFVN permanent check: Discovery cloud-optimized-archive with MAXAR_API_KEY."""
    key = os.environ.get("MAXAR_API_KEY") or os.environ.get("VITE_API_KEY") or ""
    if not key:
        return (
            {
                "repository": repository,
                "raster_analytics_activated": False,
                "details": "MAXAR_API_KEY missing for SFVN Maxar raster probe",
                "probe": "maxar_discovery_cloud_optimized_archive",
            },
            1,
        )
    url = "https://api.maxar.com/discovery/v1/search?maxar_api_key=" + key
    body = json.dumps(
        {
            "collections": ["cloud-optimized-archive"],
            "bbox": [-105.0, 40.0, -104.0, 41.0],
            "limit": 1,
        }
    ).encode()
    req = urllib.request.Request(
        url,
        data=body,
        method="POST",
        headers={"Content-Type": "application/json", "User-Agent": "SFVN-raster"},
    )
    try:
        with urllib.request.urlopen(req, timeout=20) as response:
            payload = json.loads(response.read().decode("utf-8"))
        feats = payload.get("features") or []
        activated = bool(feats)
        sample = (feats[0].get("id") if feats else None)
        return (
            {
                "repository": repository,
                "raster_analytics_activated": activated,
                "details": "SFVN Maxar Discovery probe (hub-status.vantor.com is StatusIQ HTML, not used)",
                "probe": "maxar_discovery_cloud_optimized_archive",
                "sample_id": sample,
            },
            0 if activated else 1,
        )
    except Exception as exc:
        return (
            {
                "repository": repository,
                "raster_analytics_activated": False,
                "details": f"Maxar Discovery probe failed: {type(exc).__name__}",
                "probe": "maxar_discovery_cloud_optimized_archive",
            },
            1,
        )


def build_result(args: argparse.Namespace) -> tuple[dict, int]:
    missing = []
    if not args.status_url:
        missing.append("RASTER_ANALYTICS_STATUS_URL")
    if not args.token and not args.github_pat:
        missing.append("RASTER_ANALYTICS_TOKEN or RASTER_ANALYTICS_GITHUB_PAT")

    if missing:
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": f"Missing configuration: {', '.join(missing)}",
            },
            0,
        )

    if is_statusiq_dashboard(args.status_url) or not args.status_url:
        return probe_maxar_raster(args.repository)

    url_parts = list(urllib.parse.urlparse(args.status_url))
    query = urllib.parse.parse_qs(url_parts[4], keep_blank_values=True)
    if args.repository:
        query.setdefault("repository", [args.repository])
    url_parts[4] = urllib.parse.urlencode(query, doseq=True)
    request_url = urllib.parse.urlunparse(url_parts)
    pat_allowed = allows_github_pat(request_url)
    pat_ignored = bool(args.github_pat and not pat_allowed)

    if args.github_pat and not args.token and not pat_allowed:
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": (
                    "RASTER_ANALYTICS_GITHUB_PAT is only sent to github.com or "
                    "api.github.com. Configure RASTER_ANALYTICS_TOKEN for non-GitHub "
                    "Raster Analytics endpoints."
                ),
                "github_pat_forwarded": False,
            },
            1,
        )

    headers = {
        "Accept": "application/json",
        "X-GitHub-Repository": args.repository,
        "User-Agent": "dragonslayer-raster-analytics-verifier",
    }
    if args.token:
        headers["Authorization"] = "Bearer " + args.token
    if args.github_pat and pat_allowed:
        headers["X-GitHub-Token"] = args.github_pat

    request = urllib.request.Request(
        request_url,
        headers=headers,
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": f"Raster Analytics status endpoint returned HTTP {exc.code}.",
                "github_pat_forwarded": not pat_ignored and bool(args.github_pat),
                "github_pat_ignored": pat_ignored,
                "http_status": exc.code,
            },
            1,
        )
    except urllib.error.URLError as exc:
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": "Unable to connect to the Raster Analytics status endpoint.",
                "error_type": type(exc.reason).__name__,
                "github_pat_forwarded": not pat_ignored and bool(args.github_pat),
                "github_pat_ignored": pat_ignored,
            },
            1,
        )
    except json.JSONDecodeError as exc:
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": "Raster Analytics status endpoint returned invalid JSON.",
                "error_type": type(exc).__name__,
                "github_pat_forwarded": not pat_ignored and bool(args.github_pat),
                "github_pat_ignored": pat_ignored,
            },
            1,
        )

    return (
        {
            "repository": args.repository,
            "raster_analytics_activated": extract_activation_status(payload),
            "github_pat_forwarded": not pat_ignored and bool(args.github_pat),
            "github_pat_ignored": pat_ignored,
            "response": payload,
        },
        0,
    )


def write_github_output(result: dict) -> None:
    output_path = os.environ.get("GITHUB_OUTPUT")
    if not output_path:
        return

    with open(output_path, "a", encoding="utf-8") as handle:
        handle.write(
            f"raster_analytics_activated={str(result['raster_analytics_activated']).lower()}\n"
        )


def sanitize_result_for_logs(result: dict) -> dict:
    safe_result = dict(result)
    response = safe_result.pop("response", None)
    if isinstance(response, dict):
        safe_result["response_keys"] = sorted(response.keys())
    elif response is not None:
        safe_result["response_type"] = type(response).__name__
    return safe_result


def main() -> int:
    args = parse_args()
    result, exit_code = build_result(args)

    print(f"raster_analytics_activated: {str(result['raster_analytics_activated']).lower()}")
    print(json.dumps(sanitize_result_for_logs(result), indent=2, sort_keys=True))
    write_github_output(result)

    if args.require_activated and not result["raster_analytics_activated"]:
        return 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
