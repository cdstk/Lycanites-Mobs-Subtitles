import json

with open("input.json", "r", encoding="utf-8") as f:
    data = json.load(f)

for key, value in data.items():
    subtitle = "MISSING"
    if("mobevent" in key):
        subtitle = key + ".name"
    if("entity" in key):
        subtitle = "subtitles." + key;
    if("projectile" in key):
        subtitle = key.replace("projectile", "entity", 1)
    if("block" in key):
        subtitle = key.replace("block", "tile", 1) + ".name"
    if("effect" in key):
        subtitle = key
    if("item" in key):
        subtitle = key
    value["replace"] = True
    value["subtitle"] = subtitle

with open("sounds.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2, ensure_ascii=False)