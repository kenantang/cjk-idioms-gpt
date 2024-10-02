import json

import pandas as pd

raw = pd.read_json('../../data/raw/chinese_translations_500_optimal_raw.jsonl', lines=True)

outfile = open(f'../../data/processed/chinese_translations_500_optimal.jsonl', 'w', encoding='utf-8')
outfile_partial = open(f'../../data/processed/chinese_translations_50_optimal.jsonl', 'w', encoding='utf-8')

for index, row in raw.iterrows():
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
    if index < 50 * 10 * 4:
        print(json.dumps(entry, ensure_ascii=False), file=outfile_partial, flush=True)

outfile.close()
outfile_partial.close()