import os
import re
import sys
import time
import requests

# Setup NLTK
try:
    import nltk
    print("Checking NLTK resources...")
    for res in ['wordnet', 'omw-1.4', 'punkt', 'punkt_tab', 'brown', 'reuters', 'gutenberg', 'webtext', 'inaugural', 'state_union']:
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
            elif res == 'webtext':
                from nltk.corpus import webtext
                webtext.sents()
            elif res == 'inaugural':
                from nltk.corpus import inaugural
                inaugural.sents()
            elif res == 'state_union':
                from nltk.corpus import state_union
                state_union.sents()
            elif res == 'punkt':
                nltk.data.find('tokenizers/punkt')
            elif res == 'punkt_tab':
                nltk.data.find('tokenizers/punkt_tab')
        except (LookupError, ValueError):
            print(f"Downloading NLTK '{res}' database...")
            nltk.download(res)
            
    from nltk.corpus import wordnet as wn
    from nltk.tokenize import sent_tokenize
except ImportError:
    print("Error: NLTK library is not installed.")
    sys.exit(1)

def is_placeholder(sentence, word):
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
    return any(p in s for p in patterns)

def build_local_corpora_index():
    from collections import defaultdict
    from nltk.corpus import brown, reuters, gutenberg, webtext, inaugural, state_union
    
    print("Building local corpora index...")
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

    corpora = [
        ('brown', brown.sents()),
        ('reuters', reuters.sents()),
        ('gutenberg', gutenberg.sents()),
        ('webtext', webtext.sents()),
        ('inaugural', inaugural.sents()),
        ('state_union', state_union.sents())
    ]

    for name, sents in corpora:
        try:
            for sent in sents:
                if 6 <= len(sent) <= 22:
                    s_str = reconstruct(sent)
                    for w in set(t.lower() for t in sent if t.isalpha()):
                        if len(index[w]) < 5:
                            index[w].append(s_str)
        except Exception as e:
            print(f"Error indexing {name}: {e}")

    print(f"Indexed {len(index)} unique words from local corpora.")
    return index

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
}

def clean_sentence(s, word):
    s_clean = re.sub(r'\s+', ' ', s.strip())
    if not s_clean:
        return ""
    # Capitalize first letter without changing the rest
    s_clean = s_clean[0].upper() + s_clean[1:]
    if not s_clean.endswith(('.', '!', '?')):
        s_clean += '.'
    return s_clean

def get_wikipedia_sentences(word):
    search_url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "list": "search",
        "srsearch": f'"{word}"',
        "format": "json",
        "srlimit": 5,
        "origin": "*"
    }
    
    sentences_found = []
    try:
        res = requests.get(search_url, params=params, headers=headers, timeout=5)
        if res.status_code == 200:
            data = res.json()
            search_results = data.get("query", {}).get("search", [])
            if search_results:
                page_titles = [r["title"] for r in search_results]
                
                content_url = "https://en.wikipedia.org/w/api.php"
                content_params = {
                    "action": "query",
                    "prop": "extracts",
                    "exintro": False,
                    "explaintext": True,
                    "titles": "|".join(page_titles),
                    "format": "json",
                    "origin": "*"
                }
                
                c_res = requests.get(content_url, params=content_params, headers=headers, timeout=5)
                if c_res.status_code == 200:
                    c_data = c_res.json()
                    pages = c_data.get("query", {}).get("pages", {})
                    for page_id, page_info in pages.items():
                        extract = page_info.get("extract", "")
                        if not extract: continue
                        sents = sent_tokenize(extract)
                        for s in sents:
                            if re.search(r'\b' + re.escape(word.lower()) + r'\b', s.lower()):
                                s_clean = clean_sentence(s, word)
                                if 35 <= len(s_clean) <= 170 and not s_clean.startswith(('==', 'ISBN', 'http', 'File:')):
                                    sentences_found.append(s_clean)
    except Exception as e:
        print(f"    Wikipedia query error for '{word}': {e}")
        
    unique_sents = []
    for s in sentences_found:
        if s not in unique_sents:
            unique_sents.append(s)
    return unique_sents

def get_dictionary_api_sentences(word):
    sentences = []
    try:
        res = requests.get(f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}", headers=headers, timeout=5)
        if res.status_code == 200:
            dict_res = res.json()
            if isinstance(dict_res, list) and dict_res[0].get('meanings'):
                for entry in dict_res:
                    for m in entry.get('meanings', []):
                        for d in m.get('definitions', []):
                            if d.get('example'):
                                s_clean = clean_sentence(d['example'], word)
                                if s_clean and re.search(r'\b' + re.escape(word.lower()) + r'\b', s_clean.lower()):
                                    sentences.append(s_clean)
    except Exception as e:
        print(f"    Free Dictionary API error for '{word}': {e}")
    return sentences

def get_wordnet_sentences(word):
    sentences = []
    try:
        synsets = wn.synsets(word)
        for syn in synsets:
            for ex in syn.examples():
                s_clean = clean_sentence(ex, word)
                if s_clean and re.search(r'\b' + re.escape(word.lower()) + r'\b', s_clean.lower()):
                    sentences.append(s_clean)
    except Exception:
        pass
    return sentences

def fetch_replacements(word, corpora_index, existing_examples):
    word_lower = word.lower()
    
    # Collect candidates
    candidates = []
    
    # 1. Local Corpora
    if word_lower in corpora_index:
        for ex in corpora_index[word_lower]:
            s_clean = clean_sentence(ex, word)
            if s_clean and s_clean not in candidates and not is_placeholder(s_clean, word):
                candidates.append(s_clean)
                
    # 2. WordNet
    if len(candidates) < 3:
        for ex in get_wordnet_sentences(word):
            if ex not in candidates and not is_placeholder(ex, word):
                candidates.append(ex)
                
    # 3. Wikipedia API
    if len(candidates) < 3:
        for ex in get_wikipedia_sentences(word):
            if ex not in candidates and not is_placeholder(ex, word):
                candidates.append(ex)
                
    # 4. Dictionary API
    if len(candidates) < 3:
        for ex in get_dictionary_api_sentences(word):
            if ex not in candidates and not is_placeholder(ex, word):
                candidates.append(ex)
                
    # Filter candidates to make sure they don't match any existing non-placeholder example
    non_placeholder_existing = [ex.lower().strip() for ex in existing_examples if not is_placeholder(ex, word)]
    
    filtered_candidates = []
    for c in candidates:
        if c.lower().strip() not in non_placeholder_existing:
            filtered_candidates.append(c)
            
    return filtered_candidates

def update_entry_examples(filepath, word, replacement_examples):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    parts = re.split(r'(^##\s+\d+:\s+[A-Za-z\t \-]+)', content, flags=re.MULTILINE)
    changed = False
    
    for i in range(1, len(parts), 2):
        header = parts[i]
        body = parts[i+1]
        
        match = re.search(r'##\s+\d+:\s+([A-Za-z\t \-]+)', header)
        if match:
            w = match.group(1).strip()
            if w.lower() == word.lower():
                lines = body.split("\n")
                new_lines = []
                ex_indices = []
                examples = []
                
                for idx, line in enumerate(lines):
                    if line.strip().startswith("1. ") or line.strip().startswith("1."):
                        ex_indices.append(idx)
                        examples.append(line.replace("1.", "").replace("1. ", "").strip())
                    elif line.strip().startswith("2. ") or line.strip().startswith("2."):
                        ex_indices.append(idx)
                        examples.append(line.replace("2.", "").replace("2. ", "").strip())
                
                # Check which ones are placeholders
                replaced_any = False
                rep_idx = 0
                for ex_pos, idx in enumerate(ex_indices):
                    ex_content = examples[ex_pos]
                    if is_placeholder(ex_content, w):
                        if rep_idx < len(replacement_examples):
                            new_ex = replacement_examples[rep_idx]
                            rep_idx += 1
                            # Retain the same indentation as the original line
                            indent = len(lines[idx]) - len(lines[idx].lstrip())
                            num = "1." if ex_pos == 0 else "2."
                            lines[idx] = " " * indent + f"{num} {new_ex}"
                            replaced_any = True
                
                if replaced_any:
                    parts[i+1] = "\n".join(lines)
                    changed = True
                    break
                    
    if changed:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("".join(parts))
        return True
    return False

def main():
    search_dirs = ['public/markdown/beginner', 'public/markdown/intermediate', 'public/markdown/advanced']
    
    # 1. Identify all target words
    print("🔍 Scanning for entries with single placeholders...")
    target_entries = []
    for d in search_dirs:
        if not os.path.exists(d): continue
        for f in os.listdir(d):
            if f.endswith('.md'):
                path = os.path.join(d, f)
                with open(path, 'r', encoding='utf-8') as file:
                    content = file.read()
                entries = re.split(r'^##\s+\d+:\s+', content, flags=re.MULTILINE)
                for entry in entries:
                    lines = entry.strip().split('\n')
                    if not lines or not lines[0].strip(): continue
                    word = lines[0].strip()
                    examples = []
                    for line in lines[1:]:
                        line = line.strip()
                        if line.startswith('1. ') or line.startswith('1.'):
                            ex = line.replace('1.', '').replace('1. ', '').strip()
                            if ex: examples.append(ex)
                        elif line.startswith('2. ') or line.startswith('2.'):
                            ex = line.replace('2.', '').replace('2. ', '').strip()
                            if ex: examples.append(ex)
                    
                    placeholders = [ex for ex in examples if is_placeholder(ex, word)]
                    if placeholders:
                        target_entries.append({
                            "word": word,
                            "filepath": path,
                            "examples": examples,
                            "placeholders_count": len(placeholders)
                        })
                        
    print(f"📊 Found {len(target_entries)} entries to resolve.")
    
    if not target_entries:
        print("🎉 No placeholders found! Exiting.")
        return
        
    corpora_index = build_local_corpora_index()
    
    fixed_count = 0
    skipped = []
    
    log_file_path = "fixed_single_placeholders.log"
    with open(log_file_path, "w", encoding="utf-8") as lf:
        lf.write(f"--- Fix Single Placeholders Log ---\n\n")
        
        for idx, item in enumerate(target_entries, 1):
            word = item["word"]
            filepath = item["filepath"]
            print(f"[{idx}/{len(target_entries)}] Processing: '{word}' in {os.path.basename(filepath)}...")
            
            # Fetch replacement candidates
            candidates = fetch_replacements(word, corpora_index, item["examples"])
            
            if len(candidates) >= item["placeholders_count"]:
                # Success
                success = update_entry_examples(filepath, word, candidates[:item["placeholders_count"]])
                if success:
                    fixed_count += 1
                    lf.write(f"✅ Fixed '{word}' in {filepath}\n")
                    for c in candidates[:item["placeholders_count"]]:
                        lf.write(f"   Replacement: {c}\n")
                else:
                    print(f"  ⚠️ Failed to write updates for '{word}'")
                    skipped.append(word)
                    lf.write(f"❌ Failed to write '{word}' in {filepath}\n")
            else:
                print(f"  ❌ Failed to retrieve enough examples for '{word}' (found {len(candidates)}/{item['placeholders_count']})")
                skipped.append(word)
                lf.write(f"❌ Failed to resolve '{word}' in {filepath} (found {len(candidates)})\n")
                
            # Rate limit politeness
            time.sleep(0.2)
            
    print(f"\n🎉 Finished fixing! Fixed: {fixed_count} words | Skipped/Failed: {len(skipped)} words.")
    if skipped:
        print(f"Skipped words: {skipped}")

if __name__ == "__main__":
    main()
