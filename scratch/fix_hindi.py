import os
import re
import time
from deep_translator import GoogleTranslator

def fix_hindi_translations():
    markdown_dir = os.path.join("public", "markdown")
    if not os.path.exists(markdown_dir):
        print(f"Directory {markdown_dir} not found!")
        return

    files = [f for f in os.listdir(markdown_dir) if f.endswith(".md")]
    translator = GoogleTranslator(source='en', target='hi')
    
    for filename in files:
        filepath = os.path.join(markdown_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        modified = False
        sections = content.split("## ")
        new_sections = [sections[0]]
        
        for sec in sections[1:]:
            lines = sec.split("\n")
            header = lines[0]
            word_match = re.search(r"^[0-9]+:\s*([A-Za-z\-]+)", header)
            if not word_match:
                word_match = re.search(r"^Word:\s*([A-Za-z\-]+)", header)
                
            if word_match:
                word = word_match.group(1)
                
                # Check current Hindi line
                hindi_line_idx = -1
                current_hindi = ""
                for i, line in enumerate(lines):
                    if line.startswith("- **Hindi:**"):
                        hindi_line_idx = i
                        current_hindi = line.replace("- **Hindi:**", "").strip()
                        break
                
                # Check if it needs translation
                # We always check translation to ensure accuracy
                if hindi_line_idx != -1:
                    try:
                        # Translate the word
                        translated = translator.translate(word)
                        if translated:
                            translated_clean = translated.strip()
                            # If translated text still contains the english word (meaning it failed or copied), skip
                            if word.lower() not in translated_clean.lower():
                                if translated_clean != current_hindi:
                                    lines[hindi_line_idx] = f"- **Hindi:** {translated_clean}"
                                    print(f"🔄 '{word}': '{current_hindi}' -> '{translated_clean}'")
                                    modified = True
                        time.sleep(0.3) # Avoid rate limits
                    except Exception as e:
                        print(f"❌ Error translating '{word}': {e}")
            
            new_sections.append("\n".join(lines))
            
        if modified:
            new_content = "## ".join(new_sections)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(new_content)
            print(f"✅ Saved fixes in {filename}\n")

if __name__ == "__main__":
    fix_hindi_translations()
