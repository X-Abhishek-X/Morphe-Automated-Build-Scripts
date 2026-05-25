import json, os, sys

pins_file = ".github/cert_pins.json"
try:
    with open(pins_file) as f:
        pins = json.load(f)
except Exception:
    pins = {}

pkg = os.environ.get("CERT_PKG", "").strip()
key = os.environ.get("CERT_KEY", "").strip()
fp  = os.environ.get("CERT_FP",  "").strip()

if not fp:
    print(f"  WARNING: could not extract cert fingerprint for {key}")
    sys.exit(0)

if pkg not in pins:
    pins[pkg] = fp
    os.makedirs(os.path.dirname(pins_file), exist_ok=True)
    with open(pins_file, "w") as f:
        json.dump(pins, f, indent=2)
    print(f"  New cert pinned for {key}: {fp[:16]}...")
elif pins[pkg] == fp:
    print(f"  Cert pin OK")
else:
    print(f"::error::CERT MISMATCH for {key} — pinned cert does not match. Possible re-signed APK!")
    sys.exit(42)
