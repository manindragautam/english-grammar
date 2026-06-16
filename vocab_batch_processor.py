import os
import re
import json
import subprocess
import time

# --- Configuration ---
TEST_MODE = False                 # Set to False when ready for the full run
BATCH_SIZE = 100                  # 20 words in TEST_MODE per LLM call
TARGET_TEST_FILE = "public/markdown/beginner/B.md"

FOLDERS = [
    "public/markdown/beginner",
    "public/markdown/intermediate",
    "public/markdown/advanced"
]
PROGRESS_FILE = "public/vocab_progress.json"

def load_progress():
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, 'r') as f:
                data = json.load(f)
                if "completed_words" not in data:
                    data["completed_words"] = []
                return data
        except json.JSONDecodeError:
            pass 
    return {"completed_words": []}

def save_progress(progress):
    with open(PROGRESS_FILE, 'w', encoding='utf-8') as f:
        json.dump(progress, f, indent=4, ensure_ascii=False)

def clean_ansi(text):
    """Removes terminal color codes and UI box characters."""
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    return ansi_escape.sub('', text)

def run_hermes_batch(batch):
    """Sends words to Hermes and parses Dissection, Meaning, Hindi, and Examples."""
    
    input_text = ""
    for item in batch:
        input_text += f"Word: {item['word']} | Current Meaning: {item['meaning']}\n"

    prompt = f"""You are an expert English-Hindi vocabulary teacher. I am giving you a list of words.
For EACH word, you must:
1. Provide the Dissection (syllable breakdown, e.g., [ba-sic]).
2. Write a clear, concise meaning.
3. Provide the EXACT Hindi translation that matches YOUR meaning (e.g., if you define "block" as a solid piece of material, use "टुकड़ा", not "अवरोध").
4. Write EXACTLY 2 natural conversational example sentences. 
   -> CRITICAL RULE: You MUST use the exact target word in BOTH example sentences. No synonyms.

INPUT WORDS:
{input_text}

OUTPUT FORMAT (Strictly follow this pattern):
[Word: <insert word>]
Dissection: [<syllables>]
Meaning: <refined meaning>
Hindi: <matching hindi translation>
1. <first example containing the word>
2. <second example containing the word>
"""

    try:
        start_time = time.time()
        result = subprocess.run(
            ["hermes", "chat", "-q", prompt],
            capture_output=True,
            text=True,
            check=True
        )
        output = clean_ansi(result.stdout)
        elapsed = time.time() - start_time
        print(f"✅ Batch generated in {elapsed:.1f}s")
        
        results = {}
        chunks = output.split("[Word:")
        
        for chunk in chunks:
            if not chunk.strip() or "<insert word>" in chunk:
                continue 
                
            word_match = re.search(r'([^\]]+)\]', chunk)
            if not word_match:
                continue
                
            word_key = word_match.group(1).strip().lower()
            
            # Extract all fields safely using re.DOTALL to ignore extra line breaks
            diss_match = re.search(r'Dissection:\s*(?:\*\*?)?\[?(.*?)\]?(?=\n.*Meaning:)', chunk, re.IGNORECASE | re.DOTALL)
            meaning_match = re.search(r'Meaning:\s*(?:\*\*?)?(.*?)(?=\n.*Hindi:)', chunk, re.IGNORECASE | re.DOTALL)
            hindi_match = re.search(r'Hindi:\s*(?:\*\*?)?(.*?)(?=\n.*1\.)', chunk, re.IGNORECASE | re.DOTALL)
            ex1_match = re.search(r'1\.\s*(?:\*\*?)?(.*?)(?=\n.*2\.)', chunk, re.IGNORECASE | re.DOTALL)
            ex2_match = re.search(r'2\.\s*(?:\*\*?)?(.*?)(?=\n|$)', chunk, re.IGNORECASE | re.DOTALL)
            
            if meaning_match and ex1_match and ex2_match and hindi_match and diss_match:
                results[word_key] = {
                    "dissection": diss_match.group(1).replace('**', '').strip(),
                    "meaning": meaning_match.group(1).replace('**', '').strip(),
                    "hindi": hindi_match.group(1).replace('**', '').strip(),
                    "ex1": ex1_match.group(1).replace('**', '').strip(),
                    "ex2": ex2_match.group(1).replace('**', '').strip()
                }
            else:
                print(f"⚠️ Regex failed to extract all fields for: '{word_key}'")

        # 🐛 DEBUGGING: If extraction failed, show us what the LLM actually said!
        if len(results) != len(batch):
            print("\n--- 🐛 RAW LLM OUTPUT ---")
            print(output.strip())
            print("-------------------------\n")

        return results
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Hermes execution failed: {e}")
        return {}

def process_file(filepath, progress):
    if not os.path.exists(filepath):
        return False

    print(f"\n📂 Opening {filepath}")
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    blocks = re.split(r'(?=## \d+: )', content)
    progress_set = set(progress["completed_words"])
    
    batch = []
    modifications_made = False

    for index, block in enumerate(blocks):
        if not block.startswith('## '):
            continue
            
        word_match = re.search(r'##\s+(\d+):\s+(.+)', block)
        if not word_match:
            continue
            
        num = word_match.group(1).strip()
        word = word_match.group(2).strip()
        word_id = f"{filepath}_{num}_{word}" 
        
        if word_id in progress_set:
            continue 
            
        meaning_match = re.search(r'- \*\*Meaning:\*\*(.*?)(?=\n- \*\*Hindi:)', block, re.DOTALL)
        if not meaning_match:
            continue
            
        current_meaning = meaning_match.group(1).strip()
        
        batch.append({
            "index": index,
            "id": word_id,
            "word": word,
            "num": num,
            "meaning": current_meaning
        })
        
        if len(batch) == BATCH_SIZE:
            break 

    if not batch:
        print(f"✨ File complete: {filepath}")
        return False

    print(f"🔄 Processing batch of {len(batch)} words: {', '.join([b['word'] for b in batch])}")
    llm_results = run_hermes_batch(batch)
    
    for item in batch:
        llm_data = llm_results.get(item['word'].lower())
        if not llm_data:
            print(f"⚠️ Missing output for '{item['word']}'. Model skipped it.")
            continue
            
        block = blocks[item['index']]
        
        # 1. Replace Dissection
        block = re.sub(
            r'(- \*\*Dissection:\*\* ).*?(?=\n- \*\*Meaning:)', 
            f"\\1[{llm_data['dissection']}]", 
            block, 
            flags=re.DOTALL
        )

        # 2. Replace Meaning
        block = re.sub(
            r'(- \*\*Meaning:\*\* ).*?(?=\n- \*\*Hindi:)', 
            f"\\1{llm_data['meaning']}", 
            block, 
            flags=re.DOTALL
        )

        # 3. Replace Hindi
        block = re.sub(
            r'(- \*\*Hindi:\*\* ).*?(?=\n- \*\*Examples:)', 
            f"\\1{llm_data['hindi']}", 
            block, 
            flags=re.DOTALL
        )
        
        # 4. Replace Examples
        new_examples = f"- **Examples:**\n  1. {llm_data['ex1']}\n  2. {llm_data['ex2']}\n\n"
        block = re.sub(
            r'- \*\*Examples:\*\*.*', 
            new_examples, 
            block, 
            flags=re.DOTALL
        )
        
        block = re.sub(r'\n{3,}', '\n\n', block)
        
        blocks[item['index']] = block
        progress_set.add(item['id'])
        modifications_made = True

    if modifications_made:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write("".join(blocks))
            
        progress["completed_words"] = list(progress_set)
        save_progress(progress)
        print("💾 File and progress saved.")
        
    return modifications_made

def main():
    progress = load_progress()
    
    if TEST_MODE:
        print("🛠️  RUNNING IN TEST MODE (1 Batch only)")
        process_file(TARGET_TEST_FILE, progress)
    else:
        print("🚀 RUNNING IN PRODUCTION MODE")
        for folder in FOLDERS:
            if not os.path.exists(folder):
                continue
                
            files = sorted([f for f in os.listdir(folder) if f.endswith('.md')])
            
            for file in files:
                while process_file(os.path.join(folder, file), progress):
                    pass

if __name__ == "__main__":
    main()