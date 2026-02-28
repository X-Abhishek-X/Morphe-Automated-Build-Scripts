import os
import requests
import re
import subprocess
import sys
import json

# Constants
REPO_CLI = "ReVanced/revanced-cli"
REPO_PATCHES = "ReVanced/revanced-patches"
STATE_FILE = ".github/last_built_versions.json"
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
    asset = next((a for a in release["assets"] if a["name"].endswith(".jar")), None)
    if not asset:
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
        # Remove common suffixes like (Beta) or architecture info
        clean_v = v.split(' ')[0]
        for x in clean_v.split('.'):
            # Extract leading digits
            match = re.match(r'(\d+)', x)
            if match:
                parts.append(int(match.group(1)))
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
        
        # Newer CLI uses 'Patch:' while older used 'Name:'
        if stripped.startswith("Name:") or stripped.startswith("Patch:"):
            current_patch_name = re.split(r"Patch:|Name:", stripped, 1)[1].strip()
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
                         # Remove common characters like '-' or ','
                         parts = [v.strip().lstrip('-').strip() for v in content.split(",") if v.strip()]
                         versions.extend(parts)
                continue

            if in_versions:
                # If we hit another header or empty line, we're likely done with versions
                if not stripped or (":" in stripped and not stripped.startswith(" -")):
                    in_versions = False
                    continue 
                
                # Handle list format: " - 1.2.3"
                version_val = stripped.lstrip('-').strip()
                if version_val:
                    versions.append(version_val)
    
    # Fallback: If we found the patch but no specific versions, assumes it's compatible with everything (or latest)
    if found_target_patch and not versions:
        print(f"Patch '{patch_name_filter}' found but no specific compatible versions listed. Assuming 'latest'.")
        return ["latest"]

    return versions

def load_last_built_versions():
    """Load the JSON state file tracking the last successfully built versions."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Warning: Could not read state file: {e}")
    return {}

def save_last_built_versions(versions_dict):
    """Save the current versions to the state file."""
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, 'w') as f:
        json.dump(versions_dict, f, indent=2)
    print(f"State file updated: {STATE_FILE}")

def set_github_output(key, value):
    """Write a key=value pair to GITHUB_OUTPUT."""
    gh_output = os.getenv("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a") as gh_out:
            gh_out.write(f"{key}={value}\n")
    print(f"  → {key}={value}")

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


        # 6. Compare against last built state to detect real changes
        last_built = load_last_built_versions()
        print(f"\nLast built versions: {last_built}")

        current_versions = {
            "patches_tag": patches_tag,
            "cli_tag": cli_tag,
        }
        if latest_yt_version:
            current_versions["youtube"] = latest_yt_version
        if latest_photos_version:
            current_versions["google_photos"] = latest_photos_version

        print(f"Current versions:    {current_versions}")

        # Build is needed if patches changed OR any app version changed
        needs_build = (
            last_built.get("patches_tag") != patches_tag
            or last_built.get("cli_tag") != cli_tag
            or (latest_yt_version and last_built.get("youtube") != latest_yt_version)
            or (latest_photos_version and last_built.get("google_photos") != latest_photos_version)
        )

        if needs_build:
            print("\n✅ Changes detected — build will proceed.")
        else:
            print("\n⏭️  No changes detected — skipping build.")

        # 7. Write all outputs to GITHUB_OUTPUT
        print("\nWriting GitHub outputs...")
        set_github_output("needs_build", "true" if needs_build else "false")
        set_github_output("patches_tag", patches_tag)
        set_github_output("cli_tag", cli_tag)

        if latest_yt_version:
            set_github_output("youtube_version", latest_yt_version)
        if latest_photos_version:
            set_github_output("photos_version", latest_photos_version)

        # 8. Prepare README replacements
        replacements = []
        replacements.append((r"revanced-cli-\d+\.\d+\.\d+(-all)?\.jar", cli_filename))
        replacements.append((r"patches-\d+\.\d+\.\d+\.rvp", patches_filename))

        if latest_yt_version:
            new_yt_apk = f"youtube-revanced-v{latest_yt_version}.apk"
            replacements.append((r"youtube-revanced(-v\d+(\.\d+)+)?\.apk", new_yt_apk))

        if latest_photos_version:
            new_photos_apk = f"google-photos-revanced-v{latest_photos_version}.apk"
            replacements.append((r"google-photos-revanced(-v\d+(\.\d+)+)?\.apk", new_photos_apk))

        # 9. Update files
        any_updated = False
        for filepath in FILES_TO_UPDATE:
            if update_file(filepath, replacements):
                any_updated = True

        # 10. Save current versions as new state (will be committed when build succeeds)
        # We save to a temp file here; the workflow commits it only on successful build
        save_last_built_versions(current_versions)

        # 11. Cleanup
        if not os.getenv("SKIP_CLEANUP"):
            print("Cleaning up downloaded tool files...")
            if os.path.exists(cli_filename):
                os.remove(cli_filename)
            if os.path.exists(patches_filename):
                os.remove(patches_filename)
        else:
            print("Skipping cleanup (SKIP_CLEANUP is set).")

        if any_updated:
            print("README updates applied.")
        else:
            print("README is up to date.")

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
