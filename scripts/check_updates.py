import os, requests, re, subprocess, sys, json

REPO_CLI         = "MorpheApp/morphe-cli"
REPO_MORPHE      = "MorpheApp/morphe-patches"
REPO_DE_REVANCED = "RookieEnough/De-ReVanced"
REPO_PIKO        = "crimera/piko"
REPO_HOODLES     = "hoo-dles/morphe-patches"
STATE_FILE       = ".github/last_built_versions.json"

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
    "threads":        {"package": "com.instagram.barcelona",                  "slug": "threads",              "source": "de_revanced"},
    "soundcloud":     {"package": "com.soundcloud.android",                   "slug": "soundcloud",           "source": "de_revanced"},
    "google_news":    {"package": "com.google.android.apps.magazines",        "slug": "google-news",          "source": "de_revanced"},
    "proton_mail":    {"package": "ch.protonmail.android",                    "slug": "protonmail",           "source": "de_revanced"},
    "viber":          {"package": "com.viber.voip",                           "slug": "viber",                "source": "de_revanced"},
    "pixiv":          {"package": "jp.pxv.android",                           "slug": "pixiv",                "source": "de_revanced"},
    "cricbuzz":       {"package": "com.cricbuzz.android",                     "slug": "cricbuzz",             "source": "de_revanced"},
    "icon_studio":    {"package": "ginlemon.iconpackstudio",                  "slug": "icon-pack-studio",     "source": "de_revanced"},
    # ── Piko patches ───────────────────────────────────────────
    "twitter":        {"package": "com.twitter.android",                      "slug": "twitter-x",            "source": "piko"},
    "instagram":      {"package": "com.instagram.android",                    "slug": "instagram",            "source": "piko"},
    # ── hoo-dles patches ───────────────────────────────────────
    "adguard":        {"package": "com.adguard.android",                      "slug": "adguard",              "source": "hoodles"},
    "prime_video":    {"package": "com.amazon.avod.thirdpartyclient",         "slug": "amazon-prime-video",   "source": "hoodles"},
    "duolingo":       {"package": "com.duolingo",                             "slug": "duolingo",             "source": "hoodles"},
    "myfitnesspal":   {"package": "com.myfitnesspal.android",                 "slug": "myfitnesspal",         "source": "hoodles"},
    "nova_launcher":  {"package": "com.teslacoilsw.launcher",                 "slug": "nova-launcher",        "source": "hoodles"},
    "solid_explorer": {"package": "pl.solidexplorer2",                        "slug": "solid-explorer",       "source": "hoodles"},
    "xodo_pdf":       {"package": "com.xodo.pdf.reader",                      "slug": "xodo-pdf",             "source": "hoodles"},
    "ibis_paint":     {"package": "jp.ne.ibis.ibispaintx.app",                "slug": "ibis-paint-x",         "source": "hoodles"},
    "wps_office":     {"package": "cn.wps.moffice_eng",                       "slug": "wps-office",           "source": "hoodles"},
    "camscanner":     {"package": "com.intsig.camscanner",                    "slug": "camscanner",           "source": "hoodles"},
    "fotmob":         {"package": "com.mobilefootie.wc2010",                  "slug": "fotmob",               "source": "hoodles"},
    "pandora":        {"package": "com.pandora.android",                      "slug": "pandora",              "source": "hoodles"},
    "podcast_addict": {"package": "com.bambuna.podcastaddict",                "slug": "podcast-addict",       "source": "hoodles"},
    "proton_vpn":     {"package": "ch.protonvpn.android",                     "slug": "protonvpn",            "source": "hoodles"},
    "windy":          {"package": "com.windyty.android",                      "slug": "windy",                "source": "hoodles"},
    "sofascore":      {"package": "com.sofascore.results",                    "slug": "sofascore",            "source": "hoodles"},
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
    print(f"  -> {key}={value}")

def main():
    manual_app  = os.environ.get("MANUAL_APP",  "all").strip()
    manual_ver  = os.environ.get("MANUAL_VERSION", "").strip()
    target_arch = os.environ.get("TARGET_ARCH", "arm64-v8a").strip()

    # ── Fetch all releases ─────────────────────────────────────
    cli_rel     = get_latest_release(REPO_CLI)
    mor_rel     = get_latest_release(REPO_MORPHE)
    drvr_rel    = get_latest_release(REPO_DE_REVANCED)
    piko_rel    = get_latest_release(REPO_PIKO)
    hoodles_rel = get_latest_release(REPO_HOODLES)

    cli_tag     = cli_rel["tag_name"]
    mor_tag     = mor_rel["tag_name"]
    drvr_tag    = drvr_rel["tag_name"]
    piko_tag    = piko_rel["tag_name"]
    hoodles_tag = hoodles_rel["tag_name"]

    cli_jar     = next((a for a in cli_rel["assets"]     if a["name"].endswith(".jar")), None)
    mor_mpp     = next((a for a in mor_rel["assets"]     if a["name"].endswith(".mpp")), None)
    drvr_mpp    = next((a for a in drvr_rel["assets"]    if a["name"].endswith(".mpp")), None)
    piko_mpp    = next((a for a in piko_rel["assets"]    if a["name"].endswith(".mpp")), None)
    hoodles_mpp = next((a for a in hoodles_rel["assets"] if a["name"].endswith(".mpp")), None)

    for label, asset in [("CLI jar", cli_jar), ("Morphe mpp", mor_mpp),
                         ("De-ReVanced mpp", drvr_mpp), ("Piko mpp", piko_mpp),
                         ("hoo-dles mpp", hoodles_mpp)]:
        if not asset:
            print(f"ERROR: No asset found for {label}")
            sys.exit(1)

    print(f"Morphe CLI:       {cli_tag}  ({cli_jar['name']})")
    print(f"Morphe patches:   {mor_tag}  ({mor_mpp['name']})")
    print(f"De-ReVanced:      {drvr_tag} ({drvr_mpp['name']})")
    print(f"Piko:             {piko_tag} ({piko_mpp['name']})")
    print(f"hoo-dles:         {hoodles_tag} ({hoodles_mpp['name']})")

    for asset in [cli_jar, mor_mpp, drvr_mpp, piko_mpp, hoodles_mpp]:
        if not os.path.exists(asset["name"]):
            download_file(asset["browser_download_url"], asset["name"])

    mpp_list = [mor_mpp["name"], drvr_mpp["name"], piko_mpp["name"], hoodles_mpp["name"]]

    # ── Manual build ───────────────────────────────────────────
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
        set_output("piko_tag",         piko_tag)
        set_output("hoodles_tag",      hoodles_tag)
        set_output("cli_tag",          cli_tag)
        set_output("morphe_mpp",       mor_mpp["name"])
        set_output("de_revanced_mpp",  drvr_mpp["name"])
        set_output("piko_mpp",         piko_mpp["name"])
        set_output("hoodles_mpp",      hoodles_mpp["name"])
        set_output("cli_jar",          cli_jar["name"])
        set_output("target_arch",      target_arch)
        return

    # ── Auto mode ──────────────────────────────────────────────
    last    = load_state()
    current = {
        "cli_tag": cli_tag, "morphe_tag": mor_tag,
        "de_revanced_tag": drvr_tag, "piko_tag": piko_tag, "hoodles_tag": hoodles_tag,
    }

    apps_to_build = []
    for key, info in APPS.items():
        versions = get_compatible_versions(cli_jar["name"], mpp_list, info["package"])
        latest   = versions[-1] if versions else ""
        current[key] = latest

        patch_changed = {
            "morphe":      last.get("morphe_tag")      != mor_tag,
            "de_revanced": last.get("de_revanced_tag") != drvr_tag,
            "piko":        last.get("piko_tag")         != piko_tag,
            "hoodles":     last.get("hoodles_tag")      != hoodles_tag,
        }[info["source"]]

        needs = bool(latest) and (last.get(key) != latest or patch_changed)
        if needs:
            apps_to_build.append({
                "key":     key,
                "name":    key.replace("_", "-"),
                "package": info["package"],
                "slug":    info["slug"],
                "version": latest,
                "source":  info["source"],
            })
            print(f"  OK {key} -> {latest} (rebuild)")
        else:
            print(f"  -- {key} -> {latest or 'no versions'}")

    any_needs = len(apps_to_build) > 0
    save_state(current)

    set_output("any_needs_build",  "true" if any_needs else "false")
    set_output("apps_to_build",    json.dumps(apps_to_build))
    set_output("morphe_tag",       mor_tag)
    set_output("de_revanced_tag",  drvr_tag)
    set_output("piko_tag",         piko_tag)
    set_output("hoodles_tag",      hoodles_tag)
    set_output("cli_tag",          cli_tag)
    set_output("morphe_mpp",       mor_mpp["name"])
    set_output("de_revanced_mpp",  drvr_mpp["name"])
    set_output("piko_mpp",         piko_mpp["name"])
    set_output("hoodles_mpp",      hoodles_mpp["name"])
    set_output("cli_jar",          cli_jar["name"])
    set_output("target_arch",      target_arch)

    if not os.getenv("SKIP_CLEANUP"):
        for asset in [cli_jar, mor_mpp, drvr_mpp, piko_mpp, hoodles_mpp]:
            if os.path.exists(asset["name"]): os.remove(asset["name"])

if __name__ == "__main__":
    main()