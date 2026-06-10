import os
import re
import sys
import time
import requests

# Setup NLTK and download databases offline/free if not present
try:
    import nltk
    print("Checking NLTK resources...")
    # Check and download tokenizers first, then corpora that rely on them
    for res in ['wordnet', 'omw-1.4', 'punkt', 'punkt_tab', 'brown', 'reuters', 'gutenberg']:
        try:
            if res == 'wordnet':
                from nltk.corpus import wordnet
                wordnet.synsets('test')
            elif res == 'brown':
                from nltk.corpus import brown
                brown.sents()
            elif res == 'reuters':
                from nltk.corpus import reuters
                reuters.sents()
            elif res == 'gutenberg':
                from nltk.corpus import gutenberg
                gutenberg.sents()
            elif res == 'punkt':
                nltk.data.find('tokenizers/punkt')
            elif res == 'punkt_tab':
                nltk.data.find('tokenizers/punkt_tab')
        except (LookupError, ValueError):
            print(f"Downloading NLTK '{res}' database...")
            nltk.download(res)
            
    from nltk.corpus import wordnet as wn
except ImportError:
    print("Error: NLTK library is not installed in the current environment.")
    sys.exit(1)


def is_placeholder(sentence, word):
    """Checks if a sentence is one of the fallback placeholder templates."""
    s = sentence.lower().strip()
    w = word.lower().strip()
    patterns = [
        f"learning the word '{w}' can help improve",
        f"learning the word '{w}' helps refine",
        f"learning the word '{w}' is highly useful",
        f"it is beneficial to understand the meaning and context of '{w}'",
        f"understanding the term '{w}' helps refine",
        f"the word '{w}' is highly useful in descriptive",
        f"one example sentence with {w} shows how it works",
        f"one example sentence with '{w}' shows how it works",
        f"the use of {w} made the meaning very clear",
        f"the use of '{w}' made the meaning very clear",
    ]
    for p in patterns:
        if p in s:
            return True
    return False


def build_local_corpora_index():
    """Indexes sentences from Brown, Reuters, and Gutenberg corpora by word."""
    from collections import defaultdict
    from nltk.corpus import brown, reuters, gutenberg
    
    print("Building local corpora index for word examples...")
    index = defaultdict(list)
    
    def reconstruct(tokens):
        sent_str = ""
        for token in tokens:
            if token in ['.', ',', '!', '?', ';', ':', "'s", "n't", '"', "'", '`', '-']:
                sent_str += token
            else:
                if sent_str:
                    sent_str += " " + token
                else:
                    sent_str += token
        sent_str = re.sub(r'\s+([.,!?;:])', r'\1', sent_str)
        sent_str = sent_str.strip()
        if sent_str and not sent_str[-1] in ['.', '!', '?']:
            sent_str += '.'
        return sent_str

    # Index sentences of length between 6 and 20 words
    # 1. Brown Corpus
    try:
        for sent in brown.sents():
            if 6 <= len(sent) <= 20:
                s_str = reconstruct(sent)
                for w in set(t.lower() for t in sent if t.isalpha()):
                    if len(index[w]) < 3:
                        index[w].append(s_str)
    except Exception as e:
        print(f"  Error indexing Brown corpus: {e}")
        
    # 2. Reuters Corpus
    try:
        for sent in reuters.sents():
            if 6 <= len(sent) <= 20:
                s_str = reconstruct(sent)
                for w in set(t.lower() for t in sent if t.isalpha()):
                    if len(index[w]) < 3:
                        index[w].append(s_str)
    except Exception as e:
        print(f"  Error indexing Reuters corpus: {e}")

    # 3. Gutenberg Corpus
    try:
        for sent in gutenberg.sents():
            if 6 <= len(sent) <= 20:
                s_str = reconstruct(sent)
                for w in set(t.lower() for t in sent if t.isalpha()):
                    if len(index[w]) < 3:
                        index[w].append(s_str)
    except Exception as e:
        print(f"  Error indexing Gutenberg corpus: {e}")

    print(f"Indexed {len(index)} unique words from NLTK local corpora.")
    return index


def get_real_examples(word, corpora_index):
    """Fetches high-quality non-placeholder examples via NLTK corpora, WordNet, and Free Dictionary API."""
    examples = []
    word_lower = word.lower()
    
    # 1. Try NLTK Corpora Index
    if word_lower in corpora_index:
        for ex in corpora_index[word_lower]:
            if ex and ex not in examples:
                if not is_placeholder(ex, word):
                    examples.append(ex)
                    
    # 2. Try WordNet
    if len(examples) < 2:
        try:
            synsets = wn.synsets(word)
            for syn in synsets:
                for ex in syn.examples():
                    if ex and ex not in examples:
                        clean_ex = re.sub(r'\s+', ' ', ex.strip())
                        if not is_placeholder(clean_ex, word):
                            examples.append(clean_ex)
        except Exception as e:
            print(f"  WordNet lookup exception for '{word}': {e}")
        
    # 3. Try Free Dictionary API if we still don't have enough
    if len(examples) < 2:
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", headers=headers, timeout=5)
            if res.status_code == 200 and 'application/json' in res.headers.get('Content-Type', ''):
                dict_res = res.json()
                if isinstance(dict_res, list) and dict_res[0].get('meanings'):
                    for entry in dict_res:
                        for m in entry.get('meanings', []):
                            for d in m.get('definitions', []):
                                if d.get('example'):
                                    clean_ex = re.sub(r'\s+', ' ', d['example'].strip())
                                    if clean_ex and clean_ex not in examples:
                                        if not is_placeholder(clean_ex, word):
                                            examples.append(clean_ex)
        except Exception as e:
            print(f"  Free Dictionary API lookup failed for '{word}': {e}")
            
    # Format examples
    final_examples = []
    for ex in examples:
        cleaned = ex.strip()
        if cleaned:
            # Capitalize first letter without modifying the rest
            cleaned = cleaned[0].upper() + cleaned[1:]
            if not cleaned.endswith(('.', '!', '?')):
                cleaned += '.'
            if cleaned not in final_examples:
                final_examples.append(cleaned)
                
    return final_examples[:2]


def update_word_in_file(filepath, target_word, new_examples):
    """Replaces the examples for a target word in the markdown file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = re.split(r'(^##\s+\d+:\s+[A-Za-z\t \-]+)', content, flags=re.MULTILINE)
    changed = False
    
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i+1]
        
        match = re.search(r'##\s+\d+:\s+([A-Za-z\t \-]+)', header)
        if match:
            word = match.group(1).strip()
            if word.lower() == target_word.lower():
                lines = body.split("\n")
                new_lines = []
                in_examples = False
                
                for line in lines:
                    if "- **Examples:**" in line:
                        in_examples = True
                        new_lines.append(line)
                    elif in_examples:
                        if line.strip().startswith("1. ") or line.strip().startswith("1."):
                            new_lines.append(f"  1. {new_examples[0]}")
                        elif line.strip().startswith("2. ") or line.strip().startswith("2."):
                            new_lines.append(f"  2. {new_examples[1]}")
                            in_examples = False
                        else:
                            new_lines.append(line)
                    else:
                        new_lines.append(line)
                        
                parts[i+1] = "\n".join(new_lines)
                changed = True
                break
                
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("".join(parts))
        return True
    return False


def run_fix_workflow():
    search_dirs = [
        "public/markdown",
        "public/markdown/beginner",
        "public/markdown/intermediate",
        "public/markdown/advanced"
    ]
    
    placeholder_words = []
    
    print("🔍 Scanning markdown files for placeholders...")
    for d in search_dirs:
        if not os.path.exists(d):
            continue
        for f in os.listdir(d):
            if f.endswith(".md") and len(f) == 4: # e.g. "A.md"
                path = os.path.join(d, f)
                try:
                    with open(path, "r", encoding="utf-8") as file:
                        content = file.read()
                        
                    entries = re.split(r'^##\s+\d+:\s+', content, flags=re.MULTILINE)
                    for entry in entries:
                        lines = entry.strip().split("\n")
                        if not lines or not lines[0].strip():
                            continue
                        word = lines[0].strip().capitalize()
                        
                        examples = []
                        for line in lines[1:]:
                            line = line.strip()
                            if line.startswith("1. ") or line.startswith("1."):
                                ex = line.replace("1.", "").replace("1. ", "").strip()
                                if ex: examples.append(ex)
                            elif line.startswith("2. ") or line.startswith("2."):
                                ex = line.replace("2.", "").replace("2. ", "").strip()
                                if ex: examples.append(ex)
                                
                        # Check if any examples are placeholders
                        has_placeholder = False
                        for ex in examples:
                            if is_placeholder(ex, word):
                                has_placeholder = True
                                break
                                
                        if has_placeholder or len(examples) < 2:
                            placeholder_words.append({
                                "word": word,
                                "file": path,
                                "current_examples": examples
                            })
                except Exception as e:
                    print(f"  Warning: Failed to parse {path}: {e}")
                    
    print(f"📊 Found {len(placeholder_words)} entries with placeholders.")
    
    # 2. Log to file
    log_filename = "placeholder_words.log"
    print(f"📝 Logging identified placeholder words to {log_filename}...")
    with open(log_filename, "w", encoding="utf-8") as log_file:
        log_file.write(f"--- Placeholder Words Scan Log ({len(placeholder_words)} found) ---\n\n")
        for idx, item in enumerate(placeholder_words, 1):
            log_file.write(f"{idx}. Word: {item['word']} | File: {item['file']}\n")
            for i, ex in enumerate(item['current_examples'], 1):
                log_file.write(f"   Ex {i}: {ex}\n")
            log_file.write("\n")
            
    # 3. Update .gitignore
    gitignore_path = ".gitignore"
    if os.path.exists(gitignore_path):
        print(f"🛡️ Updating {gitignore_path}...")
        with open(gitignore_path, "r", encoding="utf-8") as gi:
            gi_content = gi.read()
        if log_filename not in gi_content:
            with open(gitignore_path, "a", encoding="utf-8") as gi:
                gi.write(f"\n# Log of words with placeholder examples\n{log_filename}\n")
            print(f"  Added '{log_filename}' to .gitignore.")
        else:
            print(f"  '{log_filename}' is already in .gitignore.")
            
    # Build corpora index for local example lookup
    corpora_index = build_local_corpora_index()
            
    # 4. Try fixing
    fixed_count = 0
    skipped_count = 0
    
    print("\n🛠️ Starting fixing phase...")
    for idx, item in enumerate(placeholder_words, 1):
        word = item['word']
        filepath = item['file']
        print(f"  [{idx}/{len(placeholder_words)}] Processing word: '{word}' in {filepath}...")
        
        # Get real examples
        new_examples = get_real_examples(word, corpora_index)
        
        if len(new_examples) > 0:
            examples_to_write = []
            if len(new_examples) >= 2:
                examples_to_write = new_examples[:2]
            else:
                # We have exactly 1 new example. Merge with current examples to keep a fallback.
                current_ex = item['current_examples']
                second_ex = current_ex[1] if len(current_ex) > 1 else f"It is beneficial to understand the meaning and context of '{word.lower()}' in daily conversations."
                examples_to_write = [new_examples[0], second_ex]
                
            success = update_word_in_file(filepath, word, examples_to_write)
            if success:
                print(f"    ✅ Fixed! Replaced {len(new_examples)} placeholder(s).")
                fixed_count += 1
            else:
                print(f"    ⚠️ Warning: Found new examples but failed to write to markdown.")
                skipped_count += 1
        else:
            print(f"    ❌ Skipped: Could not find any real examples. Keep fallback.")
            skipped_count += 1
            
        # Very short rate limit delay (corpora is local/instant, only dictionary API lookup gets rate limited)
        # If the word was in local corpora, we don't query API, so we can run faster!
        # If we didn't query online, we don't need a long sleep.
        time.sleep(0.1)
        
    print(f"\n🎉 Finished! Fixed: {fixed_count} words | Skipped/Unchanged: {skipped_count} words.")


if __name__ == "__main__":
    run_fix_workflow()
