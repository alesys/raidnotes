import os
import webbrowser
import sys

def generate_preview(note_path):
    if not os.path.exists(note_path):
        print(f"Error: File {note_path} not found.")
        return

    with open(note_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Escape backslashes and quotes for JS string
    js_content = content.replace('\\', '\\\\').replace('`', '\\`').replace('$', '\\$')

    base_dir = os.path.dirname(os.path.abspath(__file__))
    template_path = os.path.join(base_dir, "preview_template.html")
    output_path = os.path.join(base_dir, "preview.html")

    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # Inject content
    # We append a script call to loadNote
    injection = f"""
    <script>
        const noteContent = `{js_content}`;
        loadNote(noteContent);
    </script>
    """
    
    final_html = html.replace("</body>", f"{injection}</body>")

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Preview generated at {output_path}")
    webbrowser.open('file://' + output_path)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target_file = sys.argv[1]
    else:
        # Default to dimensius.txt in parent folder
        target_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "dimensius.txt")
    
    generate_preview(target_file)
