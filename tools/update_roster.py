import json
import re
import os

# WoW Class Colors (RRGGBB)
CLASS_COLORS = {
    "Death Knight": "C41F3B",
    "Demon Hunter": "A330C9",
    "Druid": "FF7D0A",
    "Evoker": "33937F",
    "Hunter": "ABD473",
    "Mage": "69CCF0",
    "Monk": "00FF96",
    "Paladin": "F58CBA",
    "Priest": "FFFFFF",
    "Rogue": "FFF569",
    "Shaman": "0070DE",
    "Warlock": "9482C9",
    "Warrior": "C79C6E"
}

def get_color_code(class_name):
    """Returns the MRT color code string |cffRRGGBB."""
    if class_name in CLASS_COLORS:
        return f"|cff{CLASS_COLORS[class_name]}"
    return None

def update_note(note_path, changes):
    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    for old_name, data in changes.items():
        new_name = data.get("new_name")
        new_class = data.get("class")
        
        if not new_name:
            continue

        # Regex to find the old name wrapped in MRT color tags
        # Matches: |c(8 hex chars)OldName|r
        pattern = re.compile(r"(\|c[0-9a-fA-F]{8})" + re.escape(old_name) + r"(\|r)")
        
        def replacement(match):
            color_part = match.group(1)
            end_part = match.group(2)
            
            if new_class:
                new_color = get_color_code(new_class)
                if new_color:
                    color_part = new_color.lower() # MRT often uses lowercase
            
            return f"{color_part}{new_name}{end_part}"

        content = pattern.sub(replacement, content)

    with open(note_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Updated {note_path}")

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    json_path = os.path.join(base_dir, "tools", "roster_changes.json")
    
    # Load changes
    try:
        with open(json_path, 'r') as f:
            changes = json.load(f)
    except FileNotFoundError:
        print("roster_changes.json not found.")
        return

    # Update all .txt files in the root directory
    for filename in os.listdir(base_dir):
        if filename.endswith(".txt"):
            update_note(os.path.join(base_dir, filename), changes)

if __name__ == "__main__":
    main()
