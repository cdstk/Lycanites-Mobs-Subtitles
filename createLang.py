import json
from pathlib import Path

BASE = Path(__file__).resolve().parent
SOUNDS_PATH = BASE / "output" / "sounds.json"
OUTPUT_PATH = BASE / "output" / "en_us.lang"
# Source lang file to check for already-assigned subtitle usages.
SOURCE_LANG_PATH = BASE / "lycanitesmobs-source" / "assets" / "lycanitesmobs" / "lang" / "en_US.lang"


def load_assigned_keys(path):
    """Return the set of lang keys already assigned a value in the source lang file."""
    keys = set()
    if not path.exists():
        return keys
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "=" in line:
                keys.add(line.split("=", 1)[0])
    return keys


with open(SOUNDS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

assigned_keys = load_assigned_keys(SOURCE_LANG_PATH)

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
written = 0
skipped = 0
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    for key, value in data.items():
        langKey = value["subtitle"]
        if langKey in assigned_keys:
            skipped += 1
            continue
        if "entity" in langKey and "subtitles" in langKey:
            # Not fully current entry result, but that's for another time
            langEntry = langKey.replace("subtitles.entity.", "", 1)
            langEntry = langEntry.replace(".", " ").title()
            f.write(f"{langKey}={langEntry}\n")
            written += 1

print(f"Wrote {OUTPUT_PATH} ({written} new entries, {skipped} already assigned)")
