import os
import requests
import re
import subprocess
import sys
import json

REPO_CLI     = "MorpheApp/morphe-cli"
REPO_PATCHES = "MorpheApp/morphe-patches"
STATE_FILE   = ".github/last_built_versions.json"

APPS = {
    "youtube": {
        "package":       "com.google.android.youtube",
        "uptodown_slug": "youtube",
    },
    "music": {
        "package":       "com.google.android.apps.youtube.music",
        "uptodown_slug": "youtube-music",
    },
    "reddit": {
        "package":       "com.reddit.frontpage",
        "uptodown_slug": "reddit",
    },
}

def get_latest_release(repo):
    url     = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github.v3+json"}
    token   = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    resp = requests.get(url, headers=headers)
    resp.raise_for_status()
    return resp.json()

def download_file(url, filename):
    print(f"Downloading {filename}...")
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                f.write(chunk)

def get_cli_artifact(release):
    tag   = release["tag_name"]
    asset = next((a for a in release["assets"] if a["name"].endswith(".jar")), None)
    if not asset:
        raise Exception(f"No CLI jar in release {tag}")
    return tag, asset["name"], asset["browser_download_url"]

def get_patches_artifact(release):
    tag   = release["tag_name"]
    asset = next((a for a in release["assets"] if a["name"].endswith(".mpp")), None)
    if not asset:
        raise Exception(f"No patches .mpp in release {tag}")
    return tag, asset["name"], asset["browser_download_url"]

def version_key(v):
    parts = []
    try:
        for x in v.split("."):
            m = re.match(r"(\d+)", x)
            parts.append(int(m.group(1)) if m else 0)
    except Exception:
        return [0]
    return parts

def get_compatible_versions(cli_jar, patches_mpp, package_name):
    """Return sorted list of all compatible versions for a package across all patches."""
    cmd = ["java", "-jar", cli_jar, "list-patches", "-p", patches_mpp, "-f", package_name, "-v"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
    except (FileNotFoundError, subprocess.CalledProcessError) as e:
        print(f"CLI error for {package_name}: {e}")
        return []

    output       = result.stdout
    all_versions = set()
    in_versions  = False

    for line in output.splitlines():
        s = line.strip()
        if s.startswith("Compatible versions:"):
            in_versions = True
            inline = s.split(":", 1)[1].strip()
            if inline and inline.lower() not in ("any", "none"):
                for v in inline.split(","):
                    v = v.strip().lstrip("-").strip()
                    if v:
                        all_versions.add(v)
        elif in_versions:
            if ":" in s and not s.startswith("-") and not s.startswith(" "):
                in_versions = False
            elif s:
                v = s.lstrip("-").strip()
                if v:
                    all_versions.add(v)

    return sorted(all_versions, key=version_key)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2)

def set_output(key, value):
    gh_output = os.getenv("GITHUB_OUTPUT")
    if gh_output:
        with open(gh_output, "a") as f:
            f.write(f"{key}={value}\n")
    print(f"  → {key}={value}")

def main():
    cli_release     = get_latest_release(REPO_CLI)
    patches_release = get_latest_release(REPO_PATCHES)

    cli_tag,     cli_filename,     cli_url     = get_cli_artifact(cli_release)
    patches_tag, patches_filename, patches_url = get_patches_artifact(patches_release)

    print(f"Morphe CLI:     {cli_tag} ({cli_filename})")
    print(f"Morphe Patches: {patches_tag} ({patches_filename})")

    if not os.path.exists(cli_filename):
        download_file(cli_url, cli_filename)
    if not os.path.exists(patches_filename):
        download_file(patches_url, patches_filename)

    # Get latest supported version per app
    app_versions = {}
    for app_key, info in APPS.items():
        versions = get_compatible_versions(cli_filename, patches_filename, info["package"])
        if versions:
            latest = versions[-1]
            app_versions[app_key] = latest
            print(f"Latest supported {app_key}: {latest}")
        else:
            print(f"No compatible versions found for {app_key}")

    last = load_state()
    print(f"\nLast built: {last}")

    current = {"patches_tag": patches_tag, "cli_tag": cli_tag, **app_versions}
    print(f"Current:    {current}")

    any_needs_build = False
    for app_key in APPS:
        ver = app_versions.get(app_key, "")
        changed = (
            last.get("patches_tag") != patches_tag
            or last.get(app_key) != ver
        )
        needs = changed and bool(ver)
        set_output(f"{app_key}_needs_build", "true" if needs else "false")
        set_output(f"{app_key}_version", ver)
        if needs:
            any_needs_build = True
            print(f"✅ {app_key} needs rebuild (version: {ver})")
        else:
            print(f"⏭️  {app_key} up to date")

    set_output("any_needs_build", "true" if any_needs_build else "false")
    set_output("patches_tag", patches_tag)
    set_output("cli_tag", cli_tag)

    save_state(current)

    if not os.getenv("SKIP_CLEANUP"):
        for f in [cli_filename, patches_filename]:
            if os.path.exists(f):
                os.remove(f)
    else:
        print("Skipping cleanup (SKIP_CLEANUP set).")

if __name__ == "__main__":
    main()
