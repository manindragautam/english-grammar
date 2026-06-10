import os
import re
import sys
import time
from collections import defaultdict

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
    print("Error: NLTK library is not installed in the current environment.")
    sys.exit(1)

try:
    import pyphen
except ImportError:
    print("Error: Pyphen library is not installed.")
    sys.exit(1)

try:
    from deep_translator import GoogleTranslator
except ImportError:
    print("Error: deep-translator library is not installed.")
    sys.exit(1)

try:
    import requests
except ImportError:
    print("Error: requests library is not installed.")
    sys.exit(1)


def get_dissection(word, dic):
    """Computes syllable breakdown using pyphen."""
    hyphenated = dic.inserted(word.lower())
    return f"[{hyphenated}]" if hyphenated else f"[{word.lower()}]"


def get_word_details_offline(word):
    """Fetches definition and examples offline via NLTK WordNet with Free Dict API fallback."""
    meaning = ""
    examples = []
    
    try:
        synsets = wn.synsets(word)
        for syn in synsets:
            if not meaning and syn.definition():
                meaning = syn.definition()
            for ex in syn.examples():
                if ex and ex not in examples:
                    # Clean the example text (remove duplicate spaces)
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
        # Capitalize definition first letter
        meaning = meaning[0].upper() + meaning[1:]
    else:
        meaning = f"A vocabulary word: {word.lower()}."
        
    # Format examples
    final_examples = []
    for ex in examples:
        # Capitalize and ensure punctuation
        cleaned = ex.strip()
        if cleaned:
            # Capitalize first letter without changing the rest
            cleaned = cleaned[0].upper() + cleaned[1:]
            if not cleaned.endswith(('.', '!', '?')):
                cleaned += '.'
            # Check to make sure we don't add the exact same example again
            if cleaned not in final_examples:
                final_examples.append(cleaned)
            
    # Limit to 2 examples
    final_examples = final_examples[:2]
    
    # Generate fallbacks if needed
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
            # If the translation is just returning the English word itself, fallback
            if word.lower() not in translated_clean.lower():
                return translated_clean
    except Exception as e:
        print(f"  Hindi translation exception for '{word}': {e}")
        
    return f"{word} का हिंदी अर्थ"


def load_existing_vocab_cache():
    """Loads all existing word details from current markdown files to avoid re-translating or re-fetching."""
    cache = {}
    search_dirs = [
        "public/markdown",
        "public/markdown/beginner",
        "public/markdown/intermediate",
        "public/markdown/advanced"
    ]
    
    for d in search_dirs:
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".md") and len(f) == 4: # e.g., "A.md"
                path = os.path.join(d, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                    
                    # Split content by word entries
                    entries = re.split(r'^##\s+\d+:\s+', content, flags=re.MULTILINE)
                    for entry in entries:
                        lines = entry.strip().split("\n")
                        if not lines or not lines[0].strip():
                            continue
                        word = lines[0].strip().capitalize()
                        
                        # Extract details
                        dissection = ""
                        meaning = ""
                        hindi = ""
                        examples = []
                        
                        for line in lines[1:]:
                            line = line.strip()
                            if line.startswith("- **Dissection:**"):
                                dissection = line.replace("- **Dissection:**", "").strip()
                            elif line.startswith("- **Meaning:**"):
                                meaning = line.replace("- **Meaning:**", "").strip()
                            elif line.startswith("- **Hindi:**"):
                                hindi = line.replace("- **Hindi:**", "").strip()
                            elif line.startswith("1. ") or line.startswith("1."):
                                ex = line.replace("1.", "").replace("1. ", "").strip()
                                if ex: examples.append(ex)
                            elif line.startswith("2. ") or line.startswith("2."):
                                ex = line.replace("2.", "").replace("2. ", "").strip()
                                if ex: examples.append(ex)
                        
                        # Only cache if we got actual data
                        if word and meaning and hindi and len(examples) >= 2:
                            # Verify they are not default fallback placeholders
                            meaning_lower = meaning.lower()
                            ex0_lower = examples[0].lower()
                            if (not any(term in ex0_lower for term in ["is highly useful", "shows how it works", "helps refine your"]) and 
                                "vocabulary word:" not in meaning_lower and
                                "useful word for talking about" not in meaning_lower):
                                cache[word] = {
                                    "dissection": dissection,
                                    "meaning": meaning,
                                    "hindi": hindi,
                                    "examples": examples[:2]
                                }
                except Exception as e:
                    print(f"  Warning: Failed to parse cache from {path}: {e}")
                    
    print(f"Cached details for {len(cache)} existing words from old markdown files.")
    return cache


def generate_vocabulary():
    categories = ["beginner", "intermediate", "advanced"]
    dic = pyphen.Pyphen(lang='en')
    
    # Load existing cache to save time and API rate limits
    vocab_cache = load_existing_vocab_cache()
    
    for cat in categories:
        filename = f"{cat}_words.txt"
        if not os.path.exists(filename):
            print(f"⚠️ Warning: Source word list '{filename}' not found. Skipping...")
            continue
            
        print(f"\n📂 Processing category: '{cat.upper()}' from '{filename}'")
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()
            
        # Parse comma-separated words, filtering out HTML, tags, or non-alphabet strings
        raw_words = re.split(r'[,\n]', content)
        words = []
        for w in raw_words:
            w_clean = w.strip()
            # Must contain only letters and/or hyphens/spaces and length >= 2
            if w_clean and re.match(r'^[A-Za-z\s\-]+$', w_clean) and len(w_clean) >= 2:
                # Skip common HTML/web boilerplate tokens
                if w_clean.lower() not in ['doctype', 'html', 'head', 'body', 'xml', 'div', 'span', 'p', 'meta', 'link', 'script']:
                    words.append(w_clean)
        
        # Sort and remove duplicates
        unique_words = sorted(list(set(words)), key=lambda s: s.lower())
        if not unique_words:
            print(f"  No words found in '{filename}'!")
            continue
            
        print(f"  Found {len(unique_words)} words to process.")
        
        # Group words by first letter
        grouped = defaultdict(list)
        for w in unique_words:
            first_letter = w[0].upper()
            if first_letter.isalpha():
                grouped[first_letter].append(w)
                
        # Define output directory
        target_dir = os.path.join("public", "markdown", cat)
        os.makedirs(target_dir, exist_ok=True)
        
        # Write files grouped by letter
        for letter in sorted(grouped.keys()):
            letter_filepath = os.path.join(target_dir, f"{letter}.md")
            print(f"  ✍️ Writing category file: {target_dir}/{letter}.md ({len(grouped[letter])} words)...")
            
            with open(letter_filepath, "w", encoding="utf-8") as out:
                for idx, word in enumerate(grouped[letter], 1):
                    word_cap = word.capitalize()
                    print(f"    -> {letter} #{idx}: {word_cap}")
                    
                    if word_cap in vocab_cache:
                        print(f"      (Reusing cached details from existing files)")
                        dissection = vocab_cache[word_cap]["dissection"]
                        meaning = vocab_cache[word_cap]["meaning"]
                        hindi = vocab_cache[word_cap]["hindi"]
                        examples = vocab_cache[word_cap]["examples"]
                    else:
                        # Compute details
                        dissection = get_dissection(word_cap, dic)
                        meaning, examples = get_word_details_offline(word_cap)
                        hindi = translate_to_hindi(word_cap)
                        # Simple rate-limit padding for Google Translate request
                        time.sleep(0.5)
                    
                    # Write to markdown file
                    out.write(f"## {idx}: {word_cap}\n")
                    out.write(f"- **Dissection:** {dissection}\n")
                    out.write(f"- **Meaning:** {meaning}\n")
                    out.write(f"- **Hindi:** {hindi}\n")
                    out.write("- **Examples:**\n")
                    out.write(f"  1. {examples[0]}\n")
                    out.write(f"  2. {examples[1]}\n\n")
                    
    print("\n✅ Generation finished! Categorized database files created successfully.")


if __name__ == "__main__":
    generate_vocabulary()
