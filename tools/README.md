## Tools

### 1. Roster Updater (Manual)
Quickly swap player names globally.
1. Edit `tools/roster_changes.json`.
2. Run `python tools/update_roster.py`.

### 2. AI Note Editor
Update notes using natural language instructions.
Requires `OPENAI_API_KEY` environment variable.

**Usage:**
```powershell
$env:OPENAI_API_KEY="your-key-here"
python tools/ai_update.py "Change Sombyra to Ulgarscita (Rogue) in the liquidMass section"
```

### 3. Note Preview
View the rendered note with class colors in your browser.

**Usage:**
```powershell
python tools/show_preview.py
```

