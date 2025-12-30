# Roster Update Tool

This tool allows you to quickly swap player names in your raid notes while maintaining (or updating) their class colors.

## Setup

1.  Open `tools/roster_changes.json`.
2.  Add the players you want to replace.

## Usage

### 1. Edit `roster_changes.json`

Format:
```json
{
    "OldPlayerName": {
        "new_name": "NewPlayerName",
        "class": "Class" 
    }
}
```

**Supported Classes:**
- Death Knight
- Demon Hunter
- Druid
- Evoker
- Hunter
- Mage
- Monk
- Paladin
- Priest
- Rogue
- Shaman
- Warlock
- Warrior

*Note: If you omit the "class" field, the script will keep the original color of the old player.*

### 2. Run the Script

Open a terminal in VS Code and run:

```powershell
python tools/update_roster.py
```

This will update **all .txt files** in the main folder (e.g., `dimensius.txt`) with the new names and colors.
