import os
import re
import requests
import pyphen
import time
from collections import defaultdict
from deep_translator import GoogleTranslator

# Setup NLTK and download databases offline/free if not present
try:
    import nltk
    print("Checking NLTK resources...")
    try:
        from nltk.corpus import wordnet as wn
        wn.synsets('test')
    except LookupError:
        print("Downloading NLTK WordNet database...")
        nltk.download('wordnet')
        nltk.download('omw-1.4')
        from nltk.corpus import wordnet as wn
except ImportError:
    print("Warning: NLTK library is not installed. Falling back to online lookup only.")
    wn = None

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

def get_word_details_offline(word):
    """Fetches definition and examples offline via NLTK WordNet with Free Dict API fallback."""
    meaning = ""
    examples = []
    
    if wn:
        try:
            synsets = wn.synsets(word)
            for syn in synsets:
                if not meaning and syn.definition():
                    meaning = syn.definition()
                for ex in syn.examples():
                    if ex and ex not in examples:
                        clean_ex = re.sub(r'\s+', ' ', ex.strip())
                        examples.append(clean_ex)
        except Exception as e:
            print(f"  WordNet lookup exception for '{word}': {e}")
        
    # If offline wordnet didn't yield results or has fewer than 2 examples, fall back to online Free Dictionary API
    if not meaning or len(examples) < 2:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", headers=headers, timeout=5)
            # Strictly verify the response is JSON and successful to avoid parsing HTML blocks
            if res.status_code == 200 and 'application/json' in res.headers.get('Content-Type', ''):
                dict_res = res.json()
                if isinstance(dict_res, list) and dict_res[0].get('meanings'):
                    for entry in dict_res:
                        for m in entry.get('meanings', []):
                            for d in m.get('definitions', []):
                                if not meaning and d.get('definition'):
                                    meaning = d['definition']
                                if d.get('example'):
                                    clean_ex = re.sub(r'\s+', ' ', d['example'].strip())
                                    if clean_ex and clean_ex not in examples:
                                        examples.append(clean_ex)
        except Exception as e:
            print(f"  Free Dictionary API fallback failed for '{word}': {e}")
            
    # Clean up results
    if meaning:
        meaning = meaning[0].upper() + meaning[1:]
    else:
        meaning = f"A vocabulary word: {word.lower()}."
        
    # Format examples
    final_examples = []
    for ex in examples:
        cleaned = ex.strip()
        if cleaned:
            cleaned = cleaned[0].upper() + cleaned[1:]
            if not cleaned.endswith(('.', '!', '?')):
                cleaned += '.'
            if cleaned not in final_examples:
                final_examples.append(cleaned)
            
    final_examples = final_examples[:2]
    
    while len(final_examples) < 2:
        word_lower = word.lower()
        if len(final_examples) == 0:
            final_examples.append(f"Learning the word '{word_lower}' can help improve your communication and writing skills.")
        else:
            final_examples.append(f"It is beneficial to understand the meaning and context of '{word_lower}' in daily conversations.")
            
    return meaning, final_examples

def translate_to_hindi(word):
    """Translates a word to Hindi using GoogleTranslator."""
    try:
        translated = GoogleTranslator(source='en', target='hi').translate(word)
        if translated:
            translated_clean = translated.strip()
            if word.lower() not in translated_clean.lower():
                return translated_clean
    except Exception as e:
        print(f"  Hindi translation exception for '{word}': {e}")
        
    return f"{word} का हिंदी अर्थ"

def update_markdown_files():
    if not os.path.exists("daily_words.txt"):
        print("❌ Error: 'daily_words.txt' not found.")
        return

    with open("daily_words.txt", "r", encoding="utf-8") as f:
        content = f.read()

    # Parse comma-separated words, filtering out HTML, tags, or non-alphabet strings
    raw_words = re.split(r'[,\n]', content)
    words = []
    for w in raw_words:
        w_clean = w.strip()
        if w_clean and re.match(r'^[A-Za-z\s\-]+$', w_clean) and len(w_clean) >= 2:
            if w_clean.lower() not in ['doctype', 'html', 'head', 'body', 'xml', 'div', 'span', 'p', 'meta', 'link', 'script']:
                words.append(w_clean.capitalize())

    if not words:
        print("❌ 'daily_words.txt' is empty or has no valid words!")
        return

    processed_words = set()
    dic = pyphen.Pyphen(lang='en')
    
    target_dir = os.path.join("public", "markdown")
    os.makedirs(target_dir, exist_ok=True)
    
    grouped_words = defaultdict(list)
    for word in words:
        if word not in processed_words:
            grouped_words[word[0].upper()].append(word)
            processed_words.add(word)

    for letter in sorted(grouped_words.keys()):
        filename = os.path.join(target_dir, f"{letter}.md")
        current_index = get_next_index(filename)
        
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
                
                meaning, examples = get_word_details_offline(word)
                hindi = translate_to_hindi(word)
                
                f.write(f"## {current_index}: {word}\n")
                f.write(f"- **Dissection:** {dissection}\n")
                f.write(f"- **Meaning:** {meaning}\n")
                f.write(f"- **Hindi:** {hindi}\n")
                f.write("- **Examples:**\n")
                f.write(f"  1. {examples[0]}\n")
                f.write(f"  2. {examples[1]}\n\n")
                
                current_index += 1
                time.sleep(1)

    print(f"\n✅ Update complete! Markdown files have been saved to '{target_dir}'. 'daily_words.txt' remains untouched.")

if __name__ == "__main__":
    update_markdown_files()