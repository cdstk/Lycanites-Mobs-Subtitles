import json
import re
import sys
from pathlib import Path

# Suppress "[Client thread/WARN]: Missing sound for event:" warnings from a
# latest.log by emitting empty sound entries for events that have no associated
# sound file in lycanitesmobs-source. An entry such as
# "entity.spriggan.step": {"sounds": []} suppresses the warning.
BASE = Path(__file__).resolve().parent
LOG_PATH = BASE / "info" / "latest.log"
SOURCE_SOUNDS_DIR = BASE / "lycanitesmobs-source" / "assets" / "lycanitesmobs" / "sounds"
OUTPUT_DIR = BASE / "output"
MISSING_PATH = OUTPUT_DIR / "missing_sounds.json"
SOUNDS_PATH = OUTPUT_DIR / "sounds.json"

PATTERN = re.compile(r"Missing sound for event: lycanitesmobs:([\w.]+)")


def collect_missing_events(log_text):
    events = []
    seen = set()
    for match in PATTERN.finditer(log_text):
        event = match.group(1)
        if event not in seen:
            seen.add(event)
            events.append(event)
    return events


def event_to_file(event):
    # entity.spriggan.step -> sounds/entity/spriggan/step.ogg
    return SOURCE_SOUNDS_DIR / (event.replace(".", "/") + ".ogg")


def main(merge=False):
    log_text = LOG_PATH.read_text(encoding="utf-8", errors="replace")
    events = collect_missing_events(log_text)

    missing = {}
    have_file = 0
    for event in events:
        if event_to_file(event).exists():
            have_file += 1
        else:
            missing[event] = {"sounds": []}

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    lines = ["{"]
    items = list(missing.items())
    for i, (event, entry) in enumerate(items):
        comma = "," if i < len(items) - 1 else ""
        lines.append(f'    "{event}": {json.dumps(entry, ensure_ascii=False)}{comma}')
    lines.append("}")
    with open(MISSING_PATH, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")

    print(f"Missing-sound warnings in log: {len(events)} unique events")
    print(f"  have a sound file (not suppressible): {have_file}")
    print(f"  no file (suppressed with empty entry): {len(missing)}")
    print(f"  wrote {MISSING_PATH}")

    if merge and missing:
        if SOUNDS_PATH.exists():
            with open(SOUNDS_PATH, "r", encoding="utf-8") as f:
                data = json.load(f)
        else:
            data = {}
        added = 0
        for event, entry in missing.items():
            if event not in data:
                data[event] = entry
                added += 1
        with open(SOUNDS_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"  merged {added} new empty entries into {SOUNDS_PATH}")


if __name__ == "__main__":
    main(merge="--merge" in sys.argv)
