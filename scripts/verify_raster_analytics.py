#!/usr/bin/env python3
import argparse
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request


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
        "--timeout",
        type=int,
        default=int(os.environ.get("RASTER_ANALYTICS_TIMEOUT", "15")),
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


def build_result(args: argparse.Namespace) -> tuple[dict, int]:
    missing = []
    if not args.status_url:
        missing.append("RASTER_ANALYTICS_STATUS_URL")
    if not args.token:
        missing.append("RASTER_ANALYTICS_TOKEN")

    if missing:
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": f"Missing configuration: {', '.join(missing)}",
            },
            0,
        )

    url_parts = list(urllib.parse.urlparse(args.status_url))
    query = urllib.parse.parse_qs(url_parts[4], keep_blank_values=True)
    if args.repository:
        query.setdefault("repository", [args.repository])
    url_parts[4] = urllib.parse.urlencode(query, doseq=True)
    request_url = urllib.parse.urlunparse(url_parts)

    request = urllib.request.Request(
        request_url,
        headers={
            "Accept": "application/json",
            "Authorization": f"******",
            "X-GitHub-Repository": args.repository,
            "User-Agent": "dragonslayer-raster-analytics-verifier",
        },
        method="GET",
    )

    try:
        with urllib.request.urlopen(request, timeout=args.timeout) as response:
            payload = json.load(response)
    except urllib.error.HTTPError as exc:
        message = exc.read().decode("utf-8", errors="replace").strip()
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": f"HTTP {exc.code}: {message or exc.reason}",
            },
            1,
        )
    except urllib.error.URLError as exc:
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": f"Connection error: {exc.reason}",
            },
            1,
        )
    except json.JSONDecodeError as exc:
        return (
            {
                "repository": args.repository,
                "raster_analytics_activated": False,
                "details": f"Invalid JSON response: {exc}",
            },
            1,
        )

    return (
        {
            "repository": args.repository,
            "raster_analytics_activated": extract_activation_status(payload),
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


def main() -> int:
    args = parse_args()
    result, exit_code = build_result(args)

    print(f"raster_analytics_activated: {str(result['raster_analytics_activated']).lower()}")
    print(json.dumps(result, indent=2, sort_keys=True))
    write_github_output(result)

    if args.require_activated and not result["raster_analytics_activated"]:
        return 1
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
