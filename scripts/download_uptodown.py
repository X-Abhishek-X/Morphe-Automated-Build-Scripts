import sys
import json
import requests
from bs4 import BeautifulSoup

# Mapping from app slug to output filename (package-name based)
APP_FILENAME_MAP = {
    "youtube":       "com.google.android.youtube.apk",
    "google-photos": "com.google.android.apps.photos.apk",
    "reddit":        "com.reddit.frontpage.apk",
}

def get_download_link(version_target: str, uptodown_name: str) -> str:
    """
    Download a specific (or latest) version of an app from Uptodown.
    - uptodown_name: the slug used on uptodown.com (e.g. "youtube", "google-photos", "reddit")
    - version_target: exact version string, "latest", or the app name (treated as latest)
    The downloaded file is saved with the package-name-based filename.
    """
    base_url = f"https://{uptodown_name}.en.uptodown.com/android"
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})

    try:
        response = session.get(f"{base_url}/versions")
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        data_code = soup.find('h1', id='detail-app-name')['data-code']

        page = 1
        
        while page <= 50:
            response = session.get(f"{base_url}/apps/{data_code}/versions/{page}")
            response.raise_for_status()
            version_data = response.json().get('data', [])
            
            if not version_data:
                break
                
            for entry in version_data:
                # If 'latest' is requested (or target equals the app name due to legacy script behavior),
                # grab the very first non-xapk entry we see.
                is_latest_request = version_target in ["latest", uptodown_name]
                version_matches = (
                    is_latest_request
                    or entry["version"] == version_target
                    or entry["version"].startswith(version_target)
                )

                if not version_matches:
                    continue

                version_url_parts = entry["versionURL"]
                version_url = f"{version_url_parts['url']}/{version_url_parts['extraURL']}/{version_url_parts['versionID']}"
                
                is_xapk = entry.get('kindFile') == 'xapk'
                
                # We DO NOT want split bundles (xapk). Skip them and keep looking.
                if is_xapk:
                    print(f"  Skipping xapk entry for version {entry['version']}...", file=sys.stderr)
                    continue

                version_page = session.get(version_url)
                soup2 = BeautifulSoup(version_page.content, "html.parser")
                button = soup2.find('button', id='detail-download-button')
                
                if not button:
                    continue
                    
                onclick = button.get('onclick', '')
                if onclick and "download-link-deeplink" in onclick:
                    version_url += '-x'
                    version_page = session.get(version_url)
                    soup2 = BeautifulSoup(version_page.content, "html.parser")
                    button = soup2.find('button', id='detail-download-button')
                
                if button and 'data-url' in button.attrs:
                    download_url = f"https://dw.uptodown.com/dwn/{button['data-url']}"
                    print(f"URL Found: {download_url}", file=sys.stderr)

                    dl_resp = session.get(download_url, stream=True)
                    dl_resp.raise_for_status()

                    # Determine output filename
                    filename = APP_FILENAME_MAP.get(uptodown_name, f"{uptodown_name}.apk")
                    with open(filename, 'wb') as f:
                        for chunk in dl_resp.iter_content(chunk_size=8192):
                            f.write(chunk)
                    print(f"Saved as: {filename}", file=sys.stderr)
                    return True

            page += 1
            
    except Exception as e:
        sys.stderr.write(f"Error fetching version link: {e}\n")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python download_uptodown.py <uptodown-slug> <version|latest>", file=sys.stderr)
        sys.exit(1)
    
    uptodown_name = sys.argv[1]
    version = sys.argv[2]
    print(f"Downloading {uptodown_name} {version} from Uptodown...", file=sys.stderr)
    success = get_download_link(version, uptodown_name)
    if success:
        print(f"Successfully downloaded APK for {uptodown_name}.")
    else:
        print(f"Failed to download APK for {uptodown_name}.", file=sys.stderr)
        sys.exit(1)
