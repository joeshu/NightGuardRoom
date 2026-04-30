#!/usr/bin/env python3
"""Download a GitHub Actions artifact zip safely.

Why this exists:
GitHub's Actions artifact API endpoint requires a GitHub token, but it usually
responds with a 302 redirect to a temporary release-assets/blob-storage URL.
That redirected URL is authenticated by its signed query string, not by the
GitHub API bearer token. Reusing the GitHub Authorization header on the
redirect target can cause HTTP 401 from the storage service.

This script deliberately disables urllib's automatic redirect handling for the
GitHub API request, extracts the Location header, then downloads the temporary
URL without the GitHub Authorization header.

Inputs:
  --owner OWNER --repo REPO --artifact-id ID --out artifact.zip
  Optional --token-env GITHUB_TOKEN (default: GITHUB_TOKEN, falls back GH_TOKEN)
"""
from __future__ import annotations

import argparse
import os
import urllib.error
import urllib.request
from pathlib import Path


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def api_request(url: str, token: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Authorization": f"Bearer {token}",
            "User-Agent": "hermes-software-commander-artifact-downloader",
        },
    )


def get_redirect_location(url: str, token: str, timeout: int) -> str:
    opener = urllib.request.build_opener(NoRedirect)
    req = api_request(url, token)
    try:
        with opener.open(req, timeout=timeout) as resp:
            # Rare, but if GitHub ever returns bytes directly without redirect.
            raise RuntimeError(f"expected redirect, got HTTP {resp.status}")
    except urllib.error.HTTPError as exc:
        if exc.code not in (301, 302, 303, 307, 308):
            body = exc.read(400).decode("utf-8", "replace")
            raise RuntimeError(f"GitHub artifact API failed: HTTP {exc.code}: {body}") from exc
        location = exc.headers.get("Location")
        if not location:
            raise RuntimeError("GitHub artifact API redirect missing Location header") from exc
        return location


def download_signed_url(url: str, out: Path, timeout: int) -> int:
    # IMPORTANT: no GitHub Authorization header here.
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "hermes-software-commander-artifact-downloader"},
    )
    out.parent.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        data = resp.read()
    out.write_bytes(data)
    return len(data)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--owner", required=True)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--artifact-id", required=True)
    parser.add_argument("--out", required=True)
    parser.add_argument("--token-env", default="GITHUB_TOKEN")
    parser.add_argument("--timeout", type=int, default=60)
    args = parser.parse_args()

    token = os.environ.get(args.token_env) or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit(f"missing token env: {args.token_env} / GH_TOKEN / GITHUB_TOKEN")

    api_url = f"https://api.github.com/repos/{args.owner}/{args.repo}/actions/artifacts/{args.artifact_id}/zip"
    location = get_redirect_location(api_url, token, args.timeout)
    size = download_signed_url(location, Path(args.out), args.timeout)
    print(f"ARTIFACT_DOWNLOAD_OK path={args.out} bytes={size}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
