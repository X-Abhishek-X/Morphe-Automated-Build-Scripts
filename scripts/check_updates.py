import os, requests, re, subprocess, sys, json

REPO_CLI         = "MorpheApp/morphe-cli"
REPO_MORPHE      = "MorpheApp/morphe-patches"
REPO_DE_REVANCED = "RookieEnough/De-ReVanced"
REPO_DE_VANCED   = "RookieEnough/De-Vanced"
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
    "messenger":      {"package": "com.facebook.orca",                        "slug": "facebook-messenger",   "source": "de_revanced"},
    "threads":        {"package": "com.instagram.barcelona",                  "slug": "threads",              "source": "de_revanced"},
    "disney_plus":    {"package": "com.disney.disneyplus",                    "slug": "disney-plus",          "source": "de_revanced"},
    "soundcloud":     {"package": "com.soundcloud.android",                   "slug": "soundcloud",           "source": "de_revanced"},
    "strava":         {"package": "com.strava",                               "slug": "strava",               "source": "de_revanced"},
    "tumblr":         {"package": "com.tumblr",                               "slug": "tumblr",               "source": "de_revanced"},
    "amazon_shop":    {"package": "com.amazon.mShop.android.shopping",        "slug": "amazon-shopping",      "source": "de_revanced"},
    "amazon_music":   {"package": "com.amazon.mp3",                           "slug": "amazon-music",         "source": "de_revanced"},
    "google_photos":  {"package": "com.google.android.apps.photos",           "slug": "google-photos",        "source": "de_vanced"},
    "google_news":    {"package": "com.google.android.apps.magazines",        "slug": "google-news",          "source": "de_revanced"},
    "google_rec":     {"package": "com.google.android.apps.recorder",         "slug": "google-recorder",      "source": "de_revanced"},
    "proton_mail":    {"package": "ch.protonmail.android",                    "slug": "protonmail",           "source": "de_revanced"},
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
    "nu_nl":          {"package": "nl.sanomamedia.android.nu",                "slug": "nu-nl",                "source": "de_revanced"},
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

def get_latest_release(repo, include_prerelease=False):
    headers = {"Accept": "application/vnd.github.v3+json"}
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        headers["Authorization"] = f"token {token}"
    if include_prerelease:
        # /releases/latest skips pre-releases; list all and pick newest with a .mpp asset,
        # falling back to the latest stable if no pre-release has the required asset
        url = f"https://api.github.com/repos/{repo}/releases?per_page=20"
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        releases = r.json()
        if not releases:
            raise ValueError(f"No releases found for {repo}")
        pre = next((rel for rel in releases if rel["prerelease"] and any(a["name"].endswith(".mpp") for a in rel["assets"])), None)
        stable = next((rel for rel in releases if not rel["prerelease"] and any(a["name"].endswith(".mpp") for a in rel["assets"])), None)
        chosen = pre if pre else stable
        if not chosen:
            raise ValueError(f"No release with .mpp asset found for {repo}")
        chosen["_used_prerelease"] = chosen["prerelease"]
        return chosen
    url = f"https://api.github.com/repos/{repo}/releases/latest"
    r = requests.get(url, headers=headers)
    r.raise_for_status()
    rel = r.json()
    rel["_used_prerelease"] = False
    return rel

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

def get_apkpure_latest_version(slug, package):
    """Fallback: get latest version when patches have no version constraint.
    Tries Google Play Store first (accessible from CI), then APKPure."""
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36"}

    # 1. Google Play Store — reliably accessible from CI runners
    try:
        url = f"https://play.google.com/store/apps/details?id={package}&hl=en_US&gl=US"
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            # Play Store embeds version history in the page; grab the highest
            versions = re.findall(r'"(\d+\.\d[\d.]{3,})"', r.text)
            if versions:
                best = sorted(versions, key=version_key)[-1]
                print(f"  Play Store version: {best}")
                return best
        print(f"  Play Store returned HTTP {r.status_code}")
    except Exception as e:
        print(f"  Play Store scrape failed: {e}")

    # 2. APKPure main page (works from local, may 403 from CI)
    try:
        url = f"https://apkpure.com/{slug}/{package}"
        r = requests.get(url, headers=headers, timeout=20)
        if r.status_code == 200:
            m = re.search(r'"versionName"\s*:\s*"([\d]+\.[\d][\d.]*)"', r.text)
            if m:
                print(f"  APKPure version: {m.group(1)}")
                return m.group(1)
            m = re.search(r'version one-line">([\d]+\.[\d][\d.]*)<', r.text)
            if m:
                print(f"  APKPure version: {m.group(1)}")
                return m.group(1)
        print(f"  APKPure returned HTTP {r.status_code}")
    except Exception as e:
        print(f"  APKPure scrape failed: {e}")

    return ""

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
    dvcd_rel    = get_latest_release(REPO_DE_VANCED)
    piko_rel    = get_latest_release(REPO_PIKO, include_prerelease=True)
    hoodles_rel = get_latest_release(REPO_HOODLES)

    cli_tag     = cli_rel["tag_name"]
    mor_tag     = mor_rel["tag_name"]
    drvr_tag    = drvr_rel["tag_name"]
    dvcd_tag    = dvcd_rel["tag_name"]
    piko_tag    = piko_rel["tag_name"] + (" (pre-release)" if piko_rel.get("_used_prerelease") else "")
    hoodles_tag = hoodles_rel["tag_name"]

    cli_jar     = next((a for a in cli_rel["assets"]     if a["name"].endswith(".jar")), None)
    mor_mpp     = next((a for a in mor_rel["assets"]     if a["name"].endswith(".mpp")), None)
    drvr_mpp    = next((a for a in drvr_rel["assets"]    if a["name"].endswith(".mpp")), None)
    dvcd_mpp    = next((a for a in dvcd_rel["assets"]    if a["name"].endswith(".mpp")), None)
    piko_mpp    = next((a for a in piko_rel["assets"]    if a["name"].endswith(".mpp")), None)
    hoodles_mpp = next((a for a in hoodles_rel["assets"] if a["name"].endswith(".mpp")), None)

    for label, asset in [("CLI jar", cli_jar), ("Morphe mpp", mor_mpp),
                         ("De-ReVanced mpp", drvr_mpp), ("De-Vanced mpp", dvcd_mpp),
                         ("Piko mpp", piko_mpp), ("hoo-dles mpp", hoodles_mpp)]:
        if not asset:
            print(f"ERROR: No asset found for {label}")
            sys.exit(1)

    print(f"Morphe CLI:       {cli_tag}  ({cli_jar['name']})")
    print(f"Morphe patches:   {mor_tag}  ({mor_mpp['name']})")
    print(f"De-ReVanced:      {drvr_tag} ({drvr_mpp['name']})")
    print(f"De-Vanced:        {dvcd_tag} ({dvcd_mpp['name']})")
    print(f"Piko:             {piko_tag} ({piko_mpp['name']})")
    print(f"hoo-dles:         {hoodles_tag} ({hoodles_mpp['name']})")

    for asset in [cli_jar, mor_mpp, drvr_mpp, dvcd_mpp, piko_mpp, hoodles_mpp]:
        if not os.path.exists(asset["name"]):
            download_file(asset["browser_download_url"], asset["name"])

    source_to_mpp = {
        "morphe":      mor_mpp["name"],
        "de_revanced": drvr_mpp["name"],
        "de_vanced":   dvcd_mpp["name"],
        "piko":        piko_mpp["name"],
        "hoodles":     hoodles_mpp["name"]
    }

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
            mpp_file = source_to_mpp.get(info["source"])
            versions = get_compatible_versions(cli_jar["name"], [mpp_file], info["package"])
            version  = versions[-1] if versions else ""
            if not version:
                print(f"  No pinned versions from CLI (patches work on any version) — falling back to APKPure latest")
                version = get_apkpure_latest_version(info["slug"], info["package"])
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
        set_output("de_vanced_tag",    dvcd_tag)
        set_output("piko_tag",         piko_tag)
        set_output("hoodles_tag",      hoodles_tag)
        set_output("cli_tag",          cli_tag)
        set_output("morphe_mpp",       mor_mpp["name"])
        set_output("de_revanced_mpp",  drvr_mpp["name"])
        set_output("de_vanced_mpp",    dvcd_mpp["name"])
        set_output("piko_mpp",         piko_mpp["name"])
        set_output("hoodles_mpp",      hoodles_mpp["name"])
        set_output("cli_jar",          cli_jar["name"])
        set_output("target_arch",      target_arch)
        return

    # ── Auto mode ──────────────────────────────────────────────
    last    = load_state()
    current = {
        "cli_tag": cli_tag, "morphe_tag": mor_tag,
        "de_revanced_tag": drvr_tag, "de_vanced_tag": dvcd_tag,
        "piko_tag": piko_tag, "hoodles_tag": hoodles_tag,
    }

    apps_to_build = []
    for key, info in APPS.items():
        mpp_file = source_to_mpp.get(info["source"])
        versions = get_compatible_versions(cli_jar["name"], [mpp_file], info["package"])
        latest   = versions[-1] if versions else ""
        if not latest:
            latest = get_apkpure_latest_version(info["slug"], info["package"])
        current[key] = latest

        patch_changed = {
            "morphe":      last.get("morphe_tag")      != mor_tag,
            "de_revanced": last.get("de_revanced_tag") != drvr_tag,
            "de_vanced":   last.get("de_vanced_tag")   != dvcd_tag,
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
    set_output("de_vanced_tag",    dvcd_tag)
    set_output("piko_tag",         piko_tag)
    set_output("hoodles_tag",      hoodles_tag)
    set_output("cli_tag",          cli_tag)
    set_output("morphe_mpp",       mor_mpp["name"])
    set_output("de_revanced_mpp",  drvr_mpp["name"])
    set_output("de_vanced_mpp",    dvcd_mpp["name"])
    set_output("piko_mpp",         piko_mpp["name"])
    set_output("hoodles_mpp",      hoodles_mpp["name"])
    set_output("cli_jar",          cli_jar["name"])
    set_output("target_arch",      target_arch)

    if not os.getenv("SKIP_CLEANUP"):
        for asset in [cli_jar, mor_mpp, drvr_mpp, dvcd_mpp, piko_mpp, hoodles_mpp]:
            if os.path.exists(asset["name"]):
                try:
                    os.remove(asset["name"])
                except Exception as e:
                    print(f"Warning: could not clean up {asset['name']}: {e}")

if __name__ == "__main__":
    main()