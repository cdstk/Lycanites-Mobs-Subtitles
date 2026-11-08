import json
from pathlib import Path

# Resolve paths relative to this script's location (the repo root) so the
# script can be run from any working directory.
BASE = Path(__file__).resolve().parent
INPUT_PATH = BASE / "lycanitesmobs-source" / "assets" / "lycanitesmobs" / "sounds.json"
OUTPUT_PATH = BASE / "output" / "sounds.json"

with open(INPUT_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

for key, value in data.items():
    subtitle = "MISSING"
    if "mobevent" in key:
        subtitle = key + ".name"
    if "entity" in key:
        subtitle = "subtitles." + key
    if "projectile" in key:
        subtitle = key.replace("projectile", "entity", 1)
    if "block" in key:
        subtitle = key.replace("block", "tile", 1) + ".name"
    if "effect" in key:
        subtitle = key
    if "item" in key:
        subtitle = key
    value["replace"] = True
    value["subtitle"] = subtitle

OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True)
with open(OUTPUT_PATH, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)

print(f"Wrote {OUTPUT_PATH} ({len(data)} events)")
