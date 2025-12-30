import os
import sys
import openai

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

SYSTEM_PROMPT = """
You are an expert World of Warcraft raid note editor.
Your task is to modify a Method Raid Tools (MRT) note based on a user's natural language instruction.

MRT Notes use color codes like |cffRRGGBBName|r.
Example: |cffC79C6EWarriorName|r

Rules:
1. Output ONLY the updated note content. No markdown blocks, no explanations.
2. Maintain the structure of the note exactly (newlines, spacing).
3. If the user asks to swap players, replace the name and update the color code if the class changes.
4. If the user specifies a class (e.g. "Bob is a Mage"), use the correct hex color:
   - Mage: 69CCF0
   - Warrior: C79C6E
   - Paladin: F58CBA
   - Hunter: ABD473
   - Rogue: FFF569
   - Priest: FFFFFF
   - Death Knight: C41F3B
   - Shaman: 0070DE
   - Warlock: 9482C9
   - Monk: 00FF96
   - Druid: FF7D0A
   - Demon Hunter: A330C9
   - Evoker: 33937F
5. If the user mentions a specific section (e.g. "in liquidMass"), try to only affect that area if possible, but usually roster swaps are global unless specified otherwise. If the instruction is "replace X with Y in section Z", only do it there.
"""

def update_note_with_ai(note_path, instruction, api_key):
    if not os.path.exists(note_path):
        print(f"Error: File {note_path} not found.")
        return

    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    client = openai.OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Current Note:\n\n{content}\n\nInstruction: {instruction}"}
            ],
            temperature=0.1
        )
        
        new_content = response.choices[0].message.content
        
        # Basic validation to ensure we didn't get a chatty response
        if "Here is the updated" in new_content or "```" in new_content:
            # Try to strip markdown code blocks if present
            new_content = new_content.replace("```plaintext", "").replace("```", "").strip()

        with open(note_path, 'w', encoding='utf-8') as f:
            f.write(new_content)
            
        print(f"Successfully updated {note_path}")
        
    except Exception as e:
        print(f"Error calling OpenAI: {e}")

if __name__ == "__main__":
    # Usage: python ai_update.py "instruction" [optional_file_path]
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set.")
        sys.exit(1)

    if len(sys.argv) < 2:
        print("Usage: python ai_update.py \"instruction\" [file_path]")
        sys.exit(1)

    instruction = sys.argv[1]
    
    if len(sys.argv) > 2:
        target_file = sys.argv[2]
    else:
        target_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dimensius.txt")

    print(f"Processing instruction: '{instruction}' on file: {target_file}")
    update_note_with_ai(target_file, instruction, api_key)
