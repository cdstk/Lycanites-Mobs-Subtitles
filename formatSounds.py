import json
from pathlib import Path

# Re-format output/sounds.json so its layout resembles the source input.json
# (4-space indentation with the "sounds" array kept on a single inline line).
BASE = Path(__file__).resolve().parent
SOUNDS_PATH = BASE / "output" / "sounds.json"

with open(SOUNDS_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)


def format_value(value):
    indent = " " * 8
    close_indent = " " * 4
    keys = list(value.keys())
    parts = []
    for i, (k, v) in enumerate(value.items()):
        comma = "," if i < len(keys) - 1 else ""
        if k == "sounds":
            inner = ", ".join(json.dumps(item) for item in v)
            parts.append(f'{indent}"{k}": [{inner}]{comma}')
        else:
            parts.append(f'{indent}"{k}": {json.dumps(v)}{comma}')
    return "{\n" + "\n".join(parts) + "\n" + close_indent + "}"


lines = ["{"]
items = list(data.items())
for i, (key, value) in enumerate(items):
    comma = "," if i < len(items) - 1 else ""
    lines.append(f'    "{key}": {format_value(value)}{comma}')
lines.append("}")

with open(SOUNDS_PATH, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")

print(f"Formatted {SOUNDS_PATH}")
