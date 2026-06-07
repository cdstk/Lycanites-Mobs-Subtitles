import json

with open("sounds.json", "r", encoding="utf-8") as f:
    data = json.load(f)

with open("en_us.lang", "w") as f:
    for key, value in data.items():
        langKey = value["subtitle"]
        if "entity" in langKey and "subtitles" in langKey:
            # Not fully current entry result, but that's for another time
            langEntry = langKey.replace("subtitles.entity.", "", 1)
            langEntry = langEntry.replace(".", " ", 1).title()
            f.write(f"{langKey}={langEntry}\n")