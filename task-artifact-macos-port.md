# Task Artifact: macOS Clipboard Fixer Port

**Date:** 2026-04-19 21:46 GMT+8  
**Subagent session:** macos-clipboard-fixer-2  
**Task:** Port `clipboard_fixer_gui.py` (Windows) → `clipboard_fixer_macos.py` (macOS)

---

## What Was Done

Created `C:\Users\michael\.qclaw\workspace\clipboard-fixer\clipboard_fixer_macos.py` — a full macOS adaptation of the Windows clipboard fixer tool.

## Key Adaptations Made

| Windows (original) | macOS (ported) |
|---|---|
| `tasklist` / `taskkill` | `pgrep` / `pkill` |
| `clip` command | `pbcopy` (write empty) + `pbpaste` (read) |
| `rdpclip.exe` | `pboard` / `clipboardd` |
| `explorer.exe` restart | `pkill -9 Finder` + `open -a Finder` |
| Windows registry | N/A (removed) |
| `ctypes.windll` admin check | Not needed on macOS |
| Blue theme (`#2196F3`) | Dark crab-theme: bg `#0f0f0f`, accent `#ea580c` |
| `powershell -command "[System.Windows.Forms.Clipboard]::Clear()"` | `subprocess.run(['pbcopy'], input=b'')` |
| `CREATE_NO_WINDOW` flag | Not applicable (Unix subprocess) |
| `restart_explorer()` | `restart_finder()` |
| Windows `cmd` shell | Native `sh` / `launchctl` |

## New macOS-Specific Features

- **`launchctl kickstart` / `launchctl bootstrap`** — proper macOS service restart
- **`pbcopy` / `pbpaste`** — native clipboard primitives
- **`open -a Finder`** — safe Finder restart (vs Windows shell hack)
- **`clipboard_empty()` helper** — checks if pbpaste returns empty

## Functions Ported

1. `check_status()` → `pgrep` for `pboard`, `clipboardd`, `Finder` + pbpaste content check
2. `clear_clipboard()` → `subprocess.run(['pbcopy'], input=b'')`
3. `restart_clipboard()` → `pkill -9 pboard` + `launchctl kickstart` + `launchctl bootstrap`
4. `restart_finder()` → `pkill -9 Finder` + `open -a Finder`
5. `fix_all()` → runs all 5 steps in sequence on a daemon thread

## Theme

- Background: `#0f0f0f`
- Surface/card: `#1a1a1a`
- Accent (crab orange): `#ea580c`
- Text: `#f5f5f5`
- Muted: `#888888`
- Button hover lighten via `_lighten_color()` lut

## Notes for Main Agent

- The tool uses `tkinter` (same as Windows), so the GUI layout is nearly identical.
- All blocking operations run in `threading.Thread` with `daemon=True` to keep UI responsive.
- `launchctl` commands use `shell=True` for `$(id -u)` expansion; `gui/$(id -u)` is the correct per-user launchd domain.
- On macOS 13+ some pasteboard functionality moved to `clipboardd`; both `pboard` and `clipboardd` are checked.
- The file is 12,789 bytes, fully self-contained, no external dependencies beyond stdlib.
