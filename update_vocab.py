import os
import re
import requests
import pyphen
import time
from collections import defaultdict
from deep_translator import GoogleTranslator

def get_next_index(filename):
    """Reads the existing markdown file to find the last used number."""
    if not os.path.exists(filename):
        return 1
    
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
        
    matches = re.findall(r"^##\s+(\d+):", content, re.MULTILINE)
    
    if matches:
        return max(int(m) for m in matches) + 1
    return 1

def update_markdown_files():
    if not os.path.exists("daily_words.txt"):
        print("❌ Error: 'daily_words.txt' not found.")
        return

    with open("daily_words.txt", "r", encoding="utf-8") as f:
        content = f.read()

    # Extract words: handle commas, remove quotes, strip spaces
    raw_words = re.findall(r'\b[A-Za-z]+\b', content)
    words = [w.capitalize() for w in raw_words if len(w) > 1]

    if not words:
        print("❌ 'daily_words.txt' is empty or has no valid words!")
        return

    # Track which words have already been processed to avoid duplicates
    processed_words = set()
    
    dic = pyphen.Pyphen(lang='en')
    
    # --- CHANGED: Target directory is now public/markdown ---
    target_dir = os.path.join("public", "markdown")
    os.makedirs(target_dir, exist_ok=True)
    
    grouped_words = defaultdict(list)
    for word in words:
        if word not in processed_words:
            grouped_words[word[0].upper()].append(word)
            processed_words.add(word)

    for letter in sorted(grouped_words.keys()):
        # --- CHANGED: Files are saved in public/markdown ---
        filename = os.path.join(target_dir, f"{letter}.md")
        current_index = get_next_index(filename)
        
        # Open file to read existing words and avoid duplicating them in the markdown
        existing_words = set()
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                existing_matches = re.findall(r"^##\s+\d+:\s+([A-Za-z]+)", f.read(), re.MULTILINE)
                existing_words = set(w.capitalize() for w in existing_matches)
        
        print(f"\n📂 Opening {target_dir}/{letter}.md (Continuing from index {current_index})")
        
        with open(filename, "a", encoding="utf-8") as f:
            for word in grouped_words[letter]:
                if word in existing_words:
                    print(f"  -> Skipping '{word}' (Already in {letter}.md)")
                    continue

                print(f"  -> Processing: {word}...")
                
                hyphenated = dic.inserted(word.lower())
                dissection = f"[{hyphenated}]" if hyphenated else f"[{word.lower()}]"
                
                meaning = f"A useful word for talking about {word}."
                hindi = f"{word} का हिंदी अर्थ"
                ex1 = f"One example sentence with {word} shows how it works."
                ex2 = f"The use of {word} made the meaning very clear."
                
                try:
                    dict_res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}").json()
                    if isinstance(dict_res, list) and dict_res[0].get('meanings'):
                        defs = dict_res[0]['meanings'][0].get('definitions', [])
                        if defs:
                            meaning = defs[0].get('definition', meaning)
                            examples = [d['example'] for m in dict_res[0]['meanings'] for d in m.get('definitions', []) if 'example' in d]
                            if len(examples) > 0: ex1 = examples[0]
                            if len(examples) > 1: ex2 = examples[1]
                except:
                    pass
                    
                try:
                    translated_text = GoogleTranslator(source='en', target='hi').translate(word)
                    if translated_text and not translated_text.isascii():
                        hindi = translated_text
                except:
                    pass
                
                f.write(f"## {current_index}: {word}\n")
                f.write(f"- **Dissection:** {dissection}\n")
                f.write(f"- **Meaning:** {meaning}\n")
                f.write(f"- **Hindi:** {hindi}\n")
                f.write("- **Examples:**\n")
                f.write(f"  1. {ex1.capitalize()}\n")
                f.write(f"  2. {ex2.capitalize()}\n\n")
                
                current_index += 1
                time.sleep(1)

    print(f"\n✅ Update complete! Markdown files have been saved to '{target_dir}'. 'daily_words.txt' remains untouched.")

if __name__ == "__main__":
    update_markdown_files()