import json

import pandas as pd

languages = [
    'chinese',
    'japanese',
    'korean',
    'chinese_plausible'
]

for language in languages:
    raw = pd.read_json(f'../../data/raw/{language}_paragraph_translations_raw.jsonl', lines=True)

    outfile = open(f'../../data/processed/{language}_paragraph_translations.jsonl', 'w', encoding='utf-8')

    for _, row in raw.iterrows():

        # noise not observed
        # also, currently we do not use these files for other downstream analysis

        entry = {
            'idiom': row.idiom,
            'sentence': row.sentence,
            'context': row.context,
            'paragraph': row.paragraph,
            'method': row.method,
            'translation': row.response
        }

        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    outfile.close()