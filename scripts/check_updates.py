import os, requests, re, subprocess, sys, json

REPO_CLI         = "MorpheApp/morphe-cli"
REPO_MORPHE      = "MorpheApp/morphe-patches"
REPO_DE_REVANCED = "RookieEnough/De-ReVanced"
STATE_FILE       = ".github/last_built_versions.json"

# All supported apps — source tells which .mpp to use
APPS = {
    # ── Morphe native patches ──────────────────────────────────
    "youtube":        {"package": "com.google.android.youtube",               "slug": "youtube",              "source": "morphe"},
    "music":          {"package": "com.google.android.apps.youtube.music",    "slug": "youtube-music",        "source": "morphe"},
    "reddit":         {"package": "com.reddit.frontpage",                     "slug": "reddit",               "source": "morphe"},
    # ── De-ReVanced patches ────────────────────────────────────
    "tiktok":         {"package": "com.zhiliaoapp.musically",                 "slug": "tiktok",               "source": "de_revanced"},
    "tiktok_jp":      {"package": "com.ss.android.ugc.trill",                 "slug": "tiktok-jp",            "source": "de_revanced"},
    "twitch":         {"package": "tv.twitch.android.app",                    "slug": "twitch",               "source": "de_revanced"},
    "facebook":       {"package": "com.facebook.katana",                      "slug": "facebook",             "source": "de_revanced"},
    "messenger":      {"package": "com.facebook.orca",                        "slug": "facebook-messenger",   "source": "de_revanced"},
    "threads":        {"package": "com.instagram.barcelona",                  "slug": "threads",              "source": "de_revanced"},
    "disney_plus":    {"package": "com.disney.disneyplus",                    "slug": "disney-plus",          "source": "de_revanced"},
    "soundcloud":     {"package": "com.soundcloud.android",                   "slug": "soundcloud",           "source": "de_revanced"},
    "strava":         {"package": "com.strava",                               "slug": "strava",               "source": "de_revanced"},
    "tumblr":         {"package": "com.tumblr",                               "slug": "tumblr",               "source": "de_revanced"},
    "amazon_shop":    {"package": "com.amazon.mShop.android.shopping",        "slug": "amazon-shopping",      "source": "de_revanced"},
    "amazon_music":   {"package": "com.amazon.mp3",                           "slug": "amazon-music",         "source": "de_revanced"},
    "google_photos":  {"package": "com.google.android.apps.photos",           "slug": "google-photos",        "source": "de_revanced"},
    "google_news":    {"package": "com.google.android.apps.magazines",        "slug": "google-news",          "source": "de_revanced"},
    "google_rec":     {"package": "com.google.android.apps.recorder",         "slug": "google-recorder",      "source": "de_revanced"},
    "proton_mail":    {"package": "ch.protonmail.android",                    "slug": "protonmail",           "source": "de_revanced"},
    "ms_lens":        {"package": "com.microsoft.office.officelens",          "slug": "microsoft-lens",       "source": "de_revanced"},
    "viber":          {"package": "com.viber.voip",                           "slug": "viber",                "source": "de_revanced"},
    "letterboxd":     {"package": "com.letterboxd.letterboxd",                "slug": "letterboxd",           "source": "de_revanced"},
    "pixiv":          {"package": "jp.pxv.android",                           "slug": "pixiv",                "source": "de_revanced"},
    "cricbuzz":       {"package": "com.cricbuzz.android",                     "slug": "cricbuzz",             "source": "de_revanced"},
    "bandcamp":       {"package": "com.bandcamp.android",                     "slug": "bandcamp",             "source": "de_revanced"},
    "rar":            {"package": "com.rarlab.rar",                           "slug": "rar",                  "source": "de_revanced"},
    "photomath":      {"package": "com.microblink.photomath",                 "slug": "photomath",            "source": "de_revanced"},
    "peacock_tv":     {"package": "com.peacocktv.peacockandroid",             "slug": "peacock-tv",           "source": "de_revanced"},
    "nothing_x":      {"package": "com.nothing.smartcenter",                  "slug": "nothing-smartcenter",  "source": "de_revanced"},
    "inshorts":       {"package": "com.nis.app",                              "slug": "inshorts",             "source": "de_revanced"},
    "icon_studio":    {"package": "ginlemon.iconpackstudio",                  "slug": "icon-pack-studio",     "source": "de_revanced"},
    "hex_editor":     {"package": "com.myprog.hexedit",                       "slug": "hex-editor",           "source": "de_revanced"},
    "gmx_mail":       {"package": "de.gmx.mobile.android.mail",               "slug": "gmx",                  "source": "de_revanced"},
    "angulus":        {"package": "com.drinkplusplus.angulus",                "slug": "angulus",              "source": "de_revanced"},
    "irplus":         {"package": "net.binarymode.android.irplus",            "slug": "irplus",               "source": "de_revanced"},
    "photoshop_mix":  {"package": "com.adobe.photoshopmix",                   "slug": "photoshop-mix",        "source": "de_revanced"},
    "nu_nl":          {"package": "nl.sanomamedia.android.nu",                "slug": "nu-nl",                "source": "de_revanced"},
}

def get_latest_release(repo):
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    return r.json()

def download_file(url, filename):
    # Use browser_download_url (CDN, no API quota) and pass token so authenticated
    # 5000/hr quota applies if a release asset URL ever sneaks through.
    print(f"  Downloading {filename}...")
    headers = {"Accept": "application/octet-stream"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    with requests.get(url, stream=True, headers=headers, allow_redirects=True) as r:
        r.raise_for_status()
        with open(filename, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)

def version_key(v):
    parts = []
    for x in str(v).split("."):
        m = re.match(r"(\d+)", x)
        parts.append(int(m.group(1)) if m else 0)
    return parts

def get_compatible_versions(cli_jar, mpp_files, package_name):
    # Morphe CLI v1.7.0+ : patches go via --patches=<file>; -p is now --with-packages and -v is --with-versions.
    cmd = ["java", "-jar", cli_jar, "list-patches"]
    for f in mpp_files:
        cmd.append(f"--patches={f}")
    cmd += ["-f", package_name, "-p", "-v"]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    except Exception as e:
        print(f"  CLI error for {package_name}: {e}")
        return []
    if result.returncode != 0:
        print(f"  CLI exit {result.returncode} for {package_name}: {result.stderr.strip()[:200]}")
        return []
    all_versions = set()
    cur_pkg = None
    in_versions = False
    for raw in result.stdout.splitlines():
        s = raw.strip()
        if not s:
            in_versions = False
            continue
        if s.startswith("Package name:"):
            cur_pkg = s.split(":", 1)[1].strip()
            in_versions = False
            continue
        if s.startswith("Compatible versions:"):
            in_versions = (cur_pkg == package_name)
            inline = s.split(":", 1)[1].strip()
            if in_versions and inline and inline.lower() not in ("any", "none"):
                for v in inline.split(","):
                    v = v.strip().lstrip("-").strip()
                    if v: all_versions.add(v)
            continue
        if in_versions and re.match(r"^[\d.]", s):
            all_versions.add(s.lstrip("-").strip())
        elif in_versions and ":" in s:
            in_versions = False
    return sorted(all_versions, key=version_key)

def load_state():
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f: return json.load(f)
        except Exception: pass
    return {}

def save_state(state):
    os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)
    with open(STATE_FILE, "w") as f: json.dump(state, f, indent=2)

def set_output(key, value):
    out = os.getenv("GITHUB_OUTPUT")
    if out:
        with open(out, "a") as f: f.write(f"{key}={value}\n")
    print(f"  → {key}={value}")

def main():
    manual_app  = os.environ.get("MANUAL_APP",  "all").strip()
    manual_ver  = os.environ.get("MANUAL_VERSION", "").strip()
    target_arch = os.environ.get("TARGET_ARCH", "arm64-v8a").strip()

    # ── Fetch releases ──────────────────────────────────────────
    cli_rel  = get_latest_release(REPO_CLI)
    mor_rel  = get_latest_release(REPO_MORPHE)
    drvr_rel = get_latest_release(REPO_DE_REVANCED)

    cli_tag  = cli_rel["tag_name"]
    mor_tag  = mor_rel["tag_name"]
    drvr_tag = drvr_rel["tag_name"]

    cli_jar  = next((a for a in cli_rel["assets"]  if a["name"].endswith(".jar")), None)
    mor_mpp  = next((a for a in mor_rel["assets"]  if a["name"].endswith(".mpp")), None)
    drvr_mpp = next((a for a in drvr_rel["assets"] if a["name"].endswith(".mpp")), None)
    if not cli_jar:
        print(f"ERROR: No .jar asset in {REPO_CLI} release {cli_rel['tag_name']}")
        sys.exit(1)
    if not mor_mpp:
        print(f"ERROR: No .mpp asset in {REPO_MORPHE} release {mor_rel['tag_name']}")
        sys.exit(1)
    if not drvr_mpp:
        print(f"ERROR: No .mpp asset in {REPO_DE_REVANCED} release {drvr_rel['tag_name']}")
        sys.exit(1)

    print(f"Morphe CLI:       {cli_tag}  ({cli_jar['name']})")
    print(f"Morphe patches:   {mor_tag}  ({mor_mpp['name']})")
    print(f"De-ReVanced:      {drvr_tag} ({drvr_mpp['name']})")

    if not os.path.exists(cli_jar["name"]):  download_file(cli_jar["browser_download_url"],  cli_jar["name"])
    if not os.path.exists(mor_mpp["name"]):  download_file(mor_mpp["browser_download_url"],  mor_mpp["name"])
    if not os.path.exists(drvr_mpp["name"]): download_file(drvr_mpp["browser_download_url"], drvr_mpp["name"])

    mpp_list = [mor_mpp["name"], drvr_mpp["name"]]

    # ── Manual build for a single app — bypass state check ─────
    if manual_app and manual_app != "all":
        print(f"\nManual build requested: {manual_app} (version_override='{manual_ver}', arch={target_arch})")
        info = APPS.get(manual_app)
        if not info:
            print(f"ERROR: Unknown app '{manual_app}'. Valid keys: {', '.join(APPS)}")
            sys.exit(1)

        if manual_ver:
            version = manual_ver
            print(f"  Using forced version: {version}")
        else:
            versions = get_compatible_versions(cli_jar["name"], mpp_list, info["package"])
            version  = versions[-1] if versions else ""
            print(f"  Latest supported version: {version or 'NONE'}")

        if not version:
            print(f"ERROR: No compatible version found for {manual_app}")
            sys.exit(1)

        apps_to_build = [{
            "key":     manual_app,
            "name":    manual_app.replace("_", "-"),
            "package": info["package"],
            "slug":    info["slug"],
            "version": version,
            "source":  info["source"],
        }]

        set_output("any_needs_build",  "true")
        set_output("apps_to_build",    json.dumps(apps_to_build))
        set_output("morphe_tag",       mor_tag)
        set_output("de_revanced_tag",  drvr_tag)
        set_output("cli_tag",          cli_tag)
        set_output("morphe_mpp",       mor_mpp["name"])
        set_output("de_revanced_mpp",  drvr_mpp["name"])
        set_output("cli_jar",          cli_jar["name"])
        set_output("target_arch",      target_arch)
        return

    # ── Auto mode: check versions for all apps ─────────────────
    last    = load_state()
    current = {"cli_tag": cli_tag, "morphe_tag": mor_tag, "de_revanced_tag": drvr_tag}

    apps_to_build = []
    for key, info in APPS.items():
        versions = get_compatible_versions(cli_jar["name"], mpp_list, info["package"])
        latest   = versions[-1] if versions else ""
        current[key] = latest

        morphe_changed = last.get("morphe_tag")      != mor_tag
        drvr_changed   = last.get("de_revanced_tag") != drvr_tag
        ver_changed    = last.get(key) != latest
        patch_changed  = morphe_changed if info["source"] == "morphe" else drvr_changed

        needs = bool(latest) and (ver_changed or patch_changed)
        if needs:
            apps_to_build.append({
                "key":     key,
                "name":    key.replace("_", "-"),
                "package": info["package"],
                "slug":    info["slug"],
                "version": latest,
                "source":  info["source"],
            })
            print(f"  ✅ {key} → {latest} (rebuild)")
        else:
            print(f"  ⏭️  {key} → {latest or 'no versions'}")

    any_needs = len(apps_to_build) > 0
    save_state(current)

    set_output("any_needs_build",  "true" if any_needs else "false")
    set_output("apps_to_build",    json.dumps(apps_to_build))
    set_output("morphe_tag",       mor_tag)
    set_output("de_revanced_tag",  drvr_tag)
    set_output("cli_tag",          cli_tag)
    set_output("morphe_mpp",       mor_mpp["name"])
    set_output("de_revanced_mpp",  drvr_mpp["name"])
    set_output("cli_jar",          cli_jar["name"])
    set_output("target_arch",      target_arch)

    if not os.getenv("SKIP_CLEANUP"):
        for f in [cli_jar["name"], mor_mpp["name"], drvr_mpp["name"]]:
            if os.path.exists(f): os.remove(f)

if __name__ == "__main__":
    main()
