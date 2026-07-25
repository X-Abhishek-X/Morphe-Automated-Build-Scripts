import json, os, sys

pins_file = ".github/cert_pins.json"
try:
    with open(pins_file) as f:
        pins = json.load(f)
except Exception:
    pins = {}

pkg    = os.environ.get("CERT_PKG", "").strip()
key    = os.environ.get("CERT_KEY", "").strip()
fp     = os.environ.get("CERT_FP",  "").strip()
source = os.environ.get("CERT_SOURCE", "").strip()

if not fp:
    print(f"  WARNING: could not extract cert fingerprint for {key}")
    sys.exit(0)

if pkg not in pins:
    if source.startswith("APKPure"):
        # First-ever pin for this package establishes the trust anchor for
        # every future build — refuse to let the least-vetted source set it.
        # APKMirror/Uptodown both manually review before publishing; APKPure
        # is closer to trust-on-upload. Once a pin exists (from either of
        # the other two), APKPure is fine as an ongoing source since every
        # download is checked against that pin regardless of where it came
        # from — this only gates the FIRST time.
        print(f"::error::{key} has no existing cert pin and APKPure was the only source — refusing to trust it as the baseline. Needs an APKMirror or Uptodown hit first.")
        sys.exit(43)
    pins[pkg] = fp
    os.makedirs(os.path.dirname(pins_file), exist_ok=True)
    with open(pins_file, "w") as f:
        json.dump(pins, f, indent=2)
    print(f"  New cert pinned for {key} (source: {source}): {fp[:16]}...")
elif pins[pkg] == fp:
    print(f"  Cert pin OK")
else:
    print(f"::error::CERT MISMATCH for {key} — pinned cert does not match. Possible re-signed APK!")
    sys.exit(42)
