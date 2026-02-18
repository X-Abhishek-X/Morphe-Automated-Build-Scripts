import os
import requests
import re
import subprocess
import sys

# Constants
REPO_CLI = "ReVanced/revanced-cli"
REPO_PATCHES = "ReVanced/revanced-patches"
FILES_TO_UPDATE = [
    "README.md"
]

def get_latest_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    print(f"Fetching latest release for {repo}...")
    headers = {
        "Accept": "application/vnd.github.v3+json"
    }
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    
    resp = requests.get(url, headers=headers)
    try:
        resp.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error retrieving {repo}: {e}")
        print(f"Response: {resp.text}")
        raise
    return resp.json()

def download_file(url, filename):
    print(f"Downloading {filename}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, 'wb') as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def get_cli_artifact(release):
    tag = release["tag_name"]
    # Look for the jar file
    asset = next((a for a in release["assets"] if a["name"].endswith("-all.jar")), None)
    if not asset:
        # Fallback: sometimes release assets might be named differently or it's a prerelease
        # But REPO_CLI/releases/latest gets the latest stable.
        raise Exception(f"No CLI jar found in release {tag}")
    return tag, asset["name"], asset["browser_download_url"]

def get_patches_artifact(release):
    tag = release["tag_name"]
    # Look for the rvp file
    asset = next((a for a in release["assets"] if a["name"].endswith(".rvp")), None)
    if not asset:
        raise Exception(f"No patches RVP found in release {tag}")
    return tag, asset["name"], asset["browser_download_url"]

def version_key(v):
    parts = []
    try:
        for x in v.split('.'):
            if x.isdigit():
                parts.append(int(x))
            else:
                parts.append(0)
    except:
        return [0]
    return parts

def get_compatible_versions(cli_jar, patches_rvp, package_name, patch_name_filter):
    print(f"Checking compatible versions for {package_name}...")
    cmd = [
        "java", "-jar", cli_jar,
        "list-patches",
        "-p", patches_rvp,
        "-f", package_name,
        "-v"
    ]

    # Run command and capture output
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except FileNotFoundError:
        print("Error: Java executable not found. Please ensure Java is installed and in your PATH.")
        return []
    except subprocess.CalledProcessError as e:
        print(f"Error running CLI: {e.stderr}")
        return []

    output = result.stdout
    print(f"--- CLI Output for {package_name} ---")
    print(output)
    print("---------------------------------------")

    # Parse output to find compatible versions for the specific patch
    lines = output.splitlines()
    versions = []
    in_patch = False
    in_versions = False
    found_target_patch = False

    for line in lines:
        stripped = line.strip()
        if stripped.startswith("Name:"):
            current_patch_name = stripped.split("Name:", 1)[1].strip()
            if patch_name_filter.lower() in current_patch_name.lower():
                in_patch = True
                found_target_patch = True
            else:
                in_patch = False
            in_versions = False

        if in_patch:
            if stripped.startswith("Compatible versions:"):
                in_versions = True
                # Handle inline versions if any (e.g. "Compatible versions: 1.2.3")
                content = stripped.split(":", 1)[1].strip()
                if content:
                    if content.lower() != "any" and content.lower() != "none":
                         parts = [v.strip() for v in content.split(",") if v.strip()]
                         versions.extend(parts)
                continue

            if in_versions:
                if not stripped or ":" in stripped:
                    in_versions = False
                    continue 

                versions.append(stripped)
    
    # Fallback: If we found the patch but no specific versions, assumes it's compatible with everything (or latest)
    if found_target_patch and not versions:
        print(f"Patch '{patch_name_filter}' found but no specific compatible versions listed. Assuming 'latest'.")
        return ["latest"]

    return versions

def update_file(filepath, replacements):
    print(f"Updating {filepath}...")
    if not os.path.exists(filepath):
        print(f"File {filepath} not found.")
        return False

    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    new_content = content
    updated = False

    for pattern, replacement in replacements:
        if re.search(pattern, new_content):
            new_content_subs = re.sub(pattern, replacement, new_content)
            if new_content_subs != new_content:
                updated = True
                new_content = new_content_subs

    if updated:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath}")
        return True
    else:
        print(f"No changes needed for {filepath}")
        return False

def main():
    try:
        # 1. Get latest info
        cli_release = get_latest_release(REPO_CLI)
        patches_release = get_latest_release(REPO_PATCHES)

        cli_tag, cli_filename, cli_url = get_cli_artifact(cli_release)
        patches_tag, patches_filename, patches_url = get_patches_artifact(patches_release)

        print(f"Latest CLI: {cli_tag} ({cli_filename})")
        print(f"Latest Patches: {patches_tag} ({patches_filename})")

        # 2. Download files
        if not os.path.exists(cli_filename):
            download_file(cli_url, cli_filename)
        if not os.path.exists(patches_filename):
            download_file(patches_url, patches_filename)

        # 3. Get YouTube compatible version
        yt_versions = get_compatible_versions(cli_filename, patches_filename, "com.google.android.youtube", "Video ads")

        latest_yt_version = None
        if not yt_versions:
            print("Could not find compatible versions for YouTube Video ads patch. Skipping YouTube version update.")
        else:

            yt_versions.sort(key=version_key)
            latest_yt_version = yt_versions[-1]
            print(f"Latest supported YouTube version: {latest_yt_version}")
            if os.getenv("GITHUB_OUTPUT"):
                with open(os.getenv("GITHUB_OUTPUT"), "a") as gh_out:
                    gh_out.write(f"youtube_version={latest_yt_version}\n")

        # 4. Get Google Photos compatible version
        photos_versions = get_compatible_versions(cli_filename, patches_filename, "com.google.android.apps.photos", "Spoof features")
        latest_photos_version = None

        if not photos_versions:
            print("Could not find compatible versions for Google Photos Spoof features patch.")
        else:
            if "latest" in photos_versions:
                latest_photos_version = "latest"
            else:
                photos_versions.sort(key=version_key)
                latest_photos_version = photos_versions[-1]
            
            print(f"Latest supported Google Photos version: {latest_photos_version}")
            if os.getenv("GITHUB_OUTPUT"):
                with open(os.getenv("GITHUB_OUTPUT"), "a") as gh_out:
                    gh_out.write(f"photos_version={latest_photos_version}\n")

        # 5. Prepare replacements
        replacements = []

        # Use regex that matches the versioning scheme (X.X.X, possibly with extra suffix if needed, but standard is numbers)
        replacements.append((r"revanced-cli-\d+\.\d+\.\d+-all\.jar", cli_filename))
        replacements.append((r"patches-\d+\.\d+\.\d+\.rvp", patches_filename))

        if latest_yt_version:
            new_yt_apk = f"youtube-{latest_yt_version}.apk"
            replacements.append((r"youtube-\d+\.\d+\.\d+\.apk", new_yt_apk))

        if latest_photos_version:
            new_photos_apk = f"google-photos-{latest_photos_version}.apk"
            replacements.append((r"google-photos-\d+\.\d+\.\d+\.apk", new_photos_apk))

        # 6. Update files
        any_updated = False
        for filepath in FILES_TO_UPDATE:
            if update_file(filepath, replacements):
                any_updated = True

        # 7. Cleanup
        if not os.getenv("SKIP_CLEANUP"):
            print("Cleaning up...")
            if os.path.exists(cli_filename):
                os.remove(cli_filename)
            if os.path.exists(patches_filename):
                os.remove(patches_filename)
        else:
            print("Skipping cleanup (SKIP_CLEANUP is set).")

        if any_updated:
            print("Updates applied.")
        else:
            print("Everything is up to date.")

    except Exception as e:
        print(f"An error occurred: {e}")
        # Clean up in case of error
        try:
            if 'cli_filename' in locals() and os.path.exists(cli_filename):
                os.remove(cli_filename)
            if 'patches_filename' in locals() and os.path.exists(patches_filename):
                os.remove(patches_filename)
        except:
            pass
        sys.exit(1)

if __name__ == "__main__":
    main()
