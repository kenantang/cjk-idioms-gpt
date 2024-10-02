import json
import re

import pandas as pd

cjk_data = pd.read_json('../../data/raw/paragraph_instructions_raw.jsonl', lines=True)

outfile = open(f'../../data/processed/paragraph_instructions.jsonl', 'w', encoding='utf-8')

for _, row in cjk_data.iterrows():
    entry = {
        'language': row.language,
        'aspect': row.aspect,
        'instruction': row.response
    }

    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()

c_repeat_data = pd.read_json('../../data/raw/paragraph_instructions_raw_repeated.jsonl', lines=True)

def count_steps(text):
    pattern = r'\b\d+.*?\.'
    matches = re.findall(pattern, text)
    return len(matches)

for _, row in c_repeat_data.iterrows():
    print(f'{row.aspect}: {count_steps(row.response)} steps')