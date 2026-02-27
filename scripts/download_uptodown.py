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
                        
                        if not is_xapk:
                            return download_url
                        else:
                            if not found_xapk_url:
                                found_xapk_url = download_url
            page += 1
            
        if found_xapk_url:
            return found_xapk_url
            
    except Exception as e:
        sys.stderr.write(f"Error fetching version link: {e}\n")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 3:
        sys.exit(1)
    
    uptodown_name = sys.argv[1]
    version = sys.argv[2]
    link = get_download_link(version, uptodown_name)
    if link:
        print(link)
    else:
        sys.exit(1)
