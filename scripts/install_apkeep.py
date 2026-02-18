import os
import requests
import sys
import stat

def install_apkeep():
    print("Fetching latest apkeep release...")
    url = "https://api.github.com/repos/EFForg/apkeep/releases/latest"
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"

    try:
        resp = requests.get(url, headers=headers)
        resp.raise_for_status()
        data = resp.json()
    except Exception as e:
        print(f"Error fetching release info: {e}")
        sys.exit(1)

    tag_name = data.get("tag_name", "unknown")
    print(f"Latest version: {tag_name}")

    assets = data.get("assets", [])
    # Prioritize musl build for static linking (avoids libssl issues)
    target_asset = None
    for asset in assets:
        name = asset["name"]
        if "x86_64-unknown-linux-musl" in name:
            target_asset = asset
            break
    
    # Fallback to gnu if musl not found
    if not target_asset:
        print("Musl build not found, checking for gnu build...")
        for asset in assets:
            name = asset["name"]
            if "x86_64-unknown-linux-gnu" in name:
                target_asset = asset
                break

    if not target_asset:
        print("Error: No suitable binary found for x86_64-linux")
        sys.exit(1)

    download_url = target_asset["browser_download_url"]
    print(f"Downloading {target_asset['name']} from {download_url}...")

    try:
        r = requests.get(download_url, stream=True)
        r.raise_for_status()
        
        # Download to local file 'apkeep'
        with open("apkeep", 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)
                
        print("Download complete.")
        
        # Make executable
        st = os.stat("apkeep")
        os.chmod("apkeep", st.st_mode | stat.S_IEXEC)
        
        # Move to /usr/local/bin
        # Note: This script might need sudo privileges if not root, but in GitHub Actions runner we have sudo.
        # We'll just leave it here or move it via shell command in workflow.
        # Actually, let's just make it available in the current directory or a standard path.
    except Exception as e:
        print(f"Error downloading file: {e}")
        sys.exit(1)

if __name__ == "__main__":
    install_apkeep()
