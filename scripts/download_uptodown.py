import sys
import json
import requests
from bs4 import BeautifulSoup

def get_download_link(version_target: str, uptodown_name: str) -> str:
    base_url = f"https://{uptodown_name}.en.uptodown.com/android"
    session = requests.Session()
    session.headers.update({"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
    try:
        response = session.get(f"{base_url}/versions")
        response.raise_for_status()
        soup = BeautifulSoup(response.content, "html.parser")
        data_code = soup.find('h1', id='detail-app-name')['data-code']

        page = 1
        found_xapk_url = None
        
        while page <= 50:
            response = session.get(f"{base_url}/apps/{data_code}/versions/{page}")
            response.raise_for_status()
            version_data = response.json().get('data', [])
            
            if not version_data:
                break
                
            for entry in version_data:
                # We want a version that starts with the main target components (e.g., "20.14.43" or "6.94")
                if entry["version"] == version_target or entry["version"].startswith(version_target):
                    version_url_parts = entry["versionURL"]
                    version_url = f"{version_url_parts['url']}/{version_url_parts['extraURL']}/{version_url_parts['versionID']}"
                    
                    is_xapk = entry.get('kindFile') == 'xapk'
                    
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
                        
                        if is_xapk:
                            return download_url
                        else:
                            if not found_xapk_url:
                                found_xapk_url = download_url
            page += 1
            
        if found_xapk_url:
            print(f"URL Found: {found_xapk_url}", file=sys.stderr)
            # Perform the actual download maintaining the session
            dl_resp = session.get(found_xapk_url, stream=True)
            dl_resp.raise_for_status()
            with open(f"com.google.android.apps.{uptodown_name}.apk".replace(".apps.youtube", ".youtube"), 'wb') as f:
                for chunk in dl_resp.iter_content(chunk_size=8192):
                    f.write(chunk)
            return True
            
    except Exception as e:
        sys.stderr.write(f"Error fetching version link: {e}\n")
    return False

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    
    uptodown_name = sys.argv[1]
    version = sys.argv[2]
    print(f"Downloading {uptodown_name} {version} from Uptodown...", file=sys.stderr)
    success = get_download_link(version, uptodown_name)
    if success:
        print(f"Successfully downloaded independent APK.")
    else:
        sys.exit(1)
