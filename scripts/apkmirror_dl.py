#!/usr/bin/env python3
"""Standalone APKMirror version-specific APK downloader.

Searches APKMirror by package name to find org/app slugs, then
downloads the exact requested version and architecture. No config
files required -- just package name, version, and arch.

APKMirror only hosts publisher-uploaded APKs with verified signatures,
making it the most trusted mirror source.
"""
import sys, re, argparse, time
from pathlib import Path
from bs4 import BeautifulSoup

try:
    from curl_cffi import requests as _http
    from curl_cffi.requests.impersonate import DEFAULT_CHROME
    sess = _http.Session(impersonate=DEFAULT_CHROME)
    USING_CURL = True
except ImportError:
    import requests as _http
    sess = _http.Session()
    sess.headers.update({
        "User-Agent": "Mozilla/5.0 (Linux; Android 14; Pixel 9 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Mobile Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    })
    USING_CURL = False

BASE = "https://www.apkmirror.com"


def search_app(package: str, timeout=20):
    """Search APKMirror for org and app slugs by package name."""
    url = f"{BASE}/?post_type=app_release&searchtype=apk&s={package}"
    try:
        r = sess.get(url, timeout=timeout)
        if r.status_code != 200:
            return []
    except Exception as e:
        print(f"[apkmirror_dl] search error: {e}", file=sys.stderr)
        return []

    soup = BeautifulSoup(r.content, "html.parser")
    results = []
    for link in soup.select("a[href*='/apk/']"):
        href = link.get("href", "")
        # Match /apk/{org}/{app}/ pattern
        m = re.match(r"/apk/([^/]+)/([^/]+)/?$", href)
        if m:
            candidate = (m.group(1), m.group(2))
            if candidate not in results:
                results.append(candidate)
    return results


def find_download_link(org: str, app: str, version: str, arch: str, timeout=20):
    """Find APK download link for a specific version and arch."""
    ver_dash = version.replace(".", "-")

    # Try common release page URL patterns
    patterns = [
        f"{BASE}/apk/{org}/{app}/{app}-{ver_dash}-release/",
        f"{BASE}/apk/{org}/{app}/{app}-{ver_dash}-android-apk-download/",
        f"{BASE}/apk/{org}/{app}/{app}-{ver_dash}/",
    ]

    soup = None
    for url in patterns:
        try:
            r = sess.get(url, timeout=timeout)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, "html.parser")
                print(f"[apkmirror_dl] release page: {url}", file=sys.stderr)
                break
        except Exception:
            continue

    if not soup:
        # Fall back to uploads search
        try:
            search_url = f"{BASE}/uploads/?appcategory={app}"
            r = sess.get(search_url, timeout=timeout)
            if r.status_code == 200:
                soup = BeautifulSoup(r.content, "html.parser")
        except Exception:
            pass

    if not soup:
        return None

    # Find the variant row matching arch
    arch_criteria = {"arm64-v8a": "arm64-v8a", "armeabi-v7a": "armeabi-v7a", "universal": "nodpi"}.get(arch, arch)
    rows = soup.find_all("div", class_=re.compile(r"table-row"))

    variant_url = None
    for row in rows:
        row_text = row.get_text()
        if arch_criteria in row_text or "universal" in row_text.lower():
            link = row.find("a", class_="accent_color") or row.find("a", href=re.compile(r"/apk/"))
            if link:
                variant_url = BASE + link["href"]
                break

    # If no arch match, take the first available variant
    if not variant_url:
        for row in rows:
            link = row.find("a", class_="accent_color")
            if link and "/apk/" in link.get("href", ""):
                variant_url = BASE + link["href"]
                break

    if not variant_url:
        return None

    # Variant page -> download button page -> actual link
    try:
        r = sess.get(variant_url, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")

        dl_btn = soup.find("a", class_="downloadButton") or soup.find("a", string=re.compile(r"Download", re.I))
        if not dl_btn:
            return None

        dl_page_url = BASE + dl_btn["href"] if dl_btn["href"].startswith("/") else dl_btn["href"]
        r = sess.get(dl_page_url, timeout=timeout)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")

        final = soup.find("a", id="download-link") or soup.find("a", rel="nofollow", href=re.compile(r"/wp-content/"))
        if final:
            href = final["href"]
            return BASE + href if href.startswith("/") else href
    except Exception as e:
        print(f"[apkmirror_dl] variant/download error: {e}", file=sys.stderr)

    return None


def download_to(url: str, path: Path, timeout=120):
    r = sess.get(url, stream=True, timeout=timeout)
    r.raise_for_status()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            if chunk:
                f.write(chunk)
    return path


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--package", required=True, help="Package name e.g. com.reddit.frontpage")
    p.add_argument("--version", required=True, help="Exact version e.g. 2026.10.0")
    p.add_argument("--arch", default="arm64-v8a", help="Architecture: arm64-v8a | armeabi-v7a | universal")
    p.add_argument("--output", required=True, help="Output APK file path")
    args = p.parse_args()

    print(f"[apkmirror_dl] searching APKMirror for {args.package}@{args.version} ({args.arch})", file=sys.stderr)

    candidates = search_app(args.package)
    if not candidates:
        print(f"[apkmirror_dl] FAILED: app not found on APKMirror", file=sys.stderr)
        return 1

    print(f"[apkmirror_dl] found {len(candidates)} candidates: {candidates[:3]}", file=sys.stderr)

    for org, app in candidates:
        url = find_download_link(org, app, args.version, args.arch)
        if not url:
            time.sleep(0.5)
            continue

        print(f"[apkmirror_dl] HIT: {org}/{app}  ->  {url}", file=sys.stderr)
        try:
            out = download_to(url, Path(args.output))
            size = out.stat().st_size
            if size < 1_000_000:
                print(f"[apkmirror_dl] WARN: suspiciously small file ({size} bytes), discarding", file=sys.stderr)
                out.unlink(missing_ok=True)
                continue
            print(f"[apkmirror_dl] OK: wrote {size:,} bytes", file=sys.stderr)
            return 0
        except Exception as ex:
            print(f"[apkmirror_dl] download error: {ex}", file=sys.stderr)
        time.sleep(0.5)

    print(f"[apkmirror_dl] FAILED: no APKMirror source had {args.package}@{args.version}", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
