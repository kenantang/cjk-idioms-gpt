import json
import sys

import pandas as pd

sys.path.append('../')

from utils.parse import extract_sentences

file_names = [
    'chinese_translations_50_few_shot',
    'japanese_translations_50_few_shot',
    'korean_translations_50_few_shot',
    'chinese_plausible_translations_50_few_shot'
]

for file_name in file_names:
    raw = pd.read_json(f'../../data/raw/{file_name}_raw.jsonl', lines=True)

    outfile = open(f'../../data/processed/{file_name}.jsonl', 'w', encoding='utf-8')

    for _, row in raw.iterrows():
        idiom = row.idiom
        sentence = row.sentence
        method = row.method

        entry = {
            'idiom': idiom,
            'sentence': sentence,
            'method': method
        }

        # no cleaning is needed
        translation = row.response
        entry['translation'] = translation
        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)


    outfile.close()