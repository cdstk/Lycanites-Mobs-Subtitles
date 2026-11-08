# Lycanites Mobs Subtitles

Generates Subtitles and Lang Keys for Lycanites Mobs from the
`lycanitesmobs-source` project directory, and suppresses missing-sound
warnings from a client log.

## Required local files/folders

| Path | Purpose |
|------|---------|
| `lycanitesmobs-source/assets/lycanitesmobs/sounds.json` | Input sound definitions (`appendSubtitle.py`) |
| `lycanitesmobs-source/assets/lycanitesmobs/sounds/**` | Actual `.ogg` sound files (`fixMissingSounds.py`) |
| `info/latest.log` | Client log containing missing-sound warnings (`fixMissingSounds.py`) |

Outputs are written to the `output/` directory (created automatically).

## Scripts

- **`appendSubtitle.py`** — Reads the source `sounds.json`, adds `replace: true` and a `subtitle` key to every event, writes `output/sounds.json`.
- **`formatSounds.py`** — Re-formats `output/sounds.json` so its layout matches the source `input.json` (4-space indent, inline `sounds` arrays).
- **`createLang.py`** — Reads `output/sounds.json`, checks each `subtitle` field against
  `lycanitesmobs-source/assets/lycanitesmobs/lang/en_US.lang`, and writes only subtitle
  lang keys that are not already assigned to `output/en_us.lang`.
- **`fixMissingSounds.py`** — Scans `info/latest.log` for `Missing sound for event:` warnings, checks whether each event has a corresponding sound file in `lycanitesmobs-source`, and writes empty entries (`"sounds": []`) for missing ones to `output/missing_sounds.json` to suppress the warnings. Pass `--merge` to also inject those empty entries into `output/sounds.json`.

## Execution order

```sh
python3 appendSubtitle.py
python3 formatSounds.py
python3 createLang.py
python3 fixMissingSounds.py        # -> output/missing_sounds.json
# optional: fold missing entries into output/sounds.json:
# python3 fixMissingSounds.py --merge
```

Run from the repository root (paths resolve relative to each script, so it works from any working directory).
