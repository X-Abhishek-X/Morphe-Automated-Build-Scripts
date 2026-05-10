#!/usr/bin/env python3
"""Standalone Uptodown version-specific APK downloader.

Used as a deeper fallback when apkeep cannot find the exact version on
its hardcoded sources (aptoide / apk-pure / apk-mirror). Morphe patches
require version-specific APKs, so generic "latest" downloads cause
patch failures — this scrapes Uptodown's per-version pages.

Logic adapted from scripts/downloader_src/uptodown.py.
"""
import sys, argparse, time
from pathlib import Path

try:
    from curl_cffi import requests as _http
    from curl_cffi.requests.impersonate import DEFAULT_CHROME
    sess = _http.Session(impersonate=DEFAULT_CHROME)
except ImportError:
    import requests as _http
    sess = _http.Session()
    sess.headers.update({
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 8) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Mobile Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })

from bs4 import BeautifulSoup


def generate_slugs(name: str, package: str):
    """Generate plausible Uptodown subdomain slugs from app name + package."""
    slugs = set()
    package_dash = package.replace('.', '-')
    parts = package.split('.')

    slugs.update([
        name,
        name.replace('-', ''),
        name.replace('-', '_'),
        name.replace('_', '-'),
        package_dash,
    ])

    if len(parts) >= 2:
        slugs.update([parts[1], parts[-1], f"{parts[1]}-{parts[-1]}"])
        if len(parts) >= 3:
            slugs.add(f"com-{parts[1]}{parts[2]}")
            slugs.add(f"com-{'-'.join(parts[1:])}")
            slugs.add(f"{parts[1]}-{parts[2]}")

    for suffix in ('', '-android', '-mobile', '-plus', '-pro', '-lite', '-mea'):
        slugs.add(name + suffix)
        slugs.add(package_dash + suffix)

    return sorted({s.lower() for s in slugs if s and len(s) > 1})


def find_download_url(slug: str, version: str, timeout=15):
    base = f"https://{slug}.en.uptodown.com/android"
    try:
        r = sess.get(f"{base}/versions", timeout=timeout)
        if r.status_code != 200:
            return None
    except Exception:
        return None

    soup = BeautifulSoup(r.content, "html.parser")
    name_el = soup.find('h1', id='detail-app-name')
    if not name_el or not name_el.get('data-code'):
        return None
    data_code = name_el['data-code']

    for page in range(1, 30):
        try:
            r = sess.get(f"{base}/apps/{data_code}/versions/{page}", timeout=timeout)
            r.raise_for_status()
            entries = r.json().get('data', [])
        except Exception:
            return None
        if not entries:
            return None

        for e in entries:
            if e.get("version") != version:
                continue
            vp = e.get("versionURL", {})
            if not vp:
                continue
            version_url = f"{vp['url']}/{vp['extraURL']}/{vp['versionID']}"
            try:
                detail = sess.get(version_url, timeout=timeout)
                detail.raise_for_status()
            except Exception:
                continue
            soup = BeautifulSoup(detail.content, "html.parser")
            btn = soup.find('button', id='detail-download-button')
            if not btn:
                continue
            if 'download-link-deeplink' in (btn.get('onclick') or ''):
                try:
                    detail = sess.get(version_url + '-x', timeout=timeout)
                    soup = BeautifulSoup(detail.content, "html.parser")
                    btn = soup.find('button', id='detail-download-button')
                except Exception:
                    continue
            if btn and btn.get('data-url'):
                return f"https://dw.uptodown.com/dwn/{btn['data-url']}"

        if all(e.get("version", "") < version for e in entries):
            return None

    return None


def download_to(url: str, path: Path, timeout=120):
    r = sess.get(url, stream=True, timeout=timeout)
    r.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open('wb') as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return path


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--name', required=True, help='App slug hint (e.g. "youtube")')
    p.add_argument('--package', required=True, help='Package name')
    p.add_argument('--version', required=True, help='Exact version string')
    p.add_argument('--output', required=True, help='Output APK file path')
    args = p.parse_args()

    slugs = generate_slugs(args.name, args.package)
    print(f"[uptodown_dl] {args.package}@{args.version} — trying {len(slugs)} slugs", file=sys.stderr)

    for slug in slugs:
        url = find_download_url(slug, args.version)
        if not url:
            continue
        print(f"[uptodown_dl] HIT: {slug}  ->  {url}", file=sys.stderr)
        try:
            out = download_to(url, Path(args.output))
            size = out.stat().st_size
            if size < 1024:
                print(f"[uptodown_dl] WARN: tiny file ({size} bytes), discarding", file=sys.stderr)
                out.unlink(missing_ok=True)
                continue
            print(f"[uptodown_dl] OK: wrote {size:,} bytes", file=sys.stderr)
            return 0
        except Exception as ex:
            print(f"[uptodown_dl] download err: {ex}", file=sys.stderr)
            continue
        time.sleep(0.3)

    print(f"[uptodown_dl] FAILED: no Uptodown source had {args.package}@{args.version}", file=sys.stderr)
    return 1


if __name__ == '__main__':
    sys.exit(main())
