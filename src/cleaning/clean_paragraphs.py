import json

import pandas as pd

languages = [
    'chinese',
    'japanese',
    'korean',
    'chinese_plausible'
]

for language in languages:
    raw = pd.read_json(f'../../data/raw/{language}_paragraphs_raw.jsonl', lines=True)

    outfile = open(f'../../data/processed/{language}_paragraphs.jsonl', 'w', encoding='utf-8')

    total_with_sentence = 0
    total_with_idiom = 0
    total = 0

    for _, row in raw.iterrows():
        idiom = row.idiom
        sentence = row.sentence
        context = row.context
        paragraph = row.response

        total += 1

        if sentence in paragraph:
            total_with_sentence += 1

        if idiom in paragraph:
            total_with_idiom += 1

        entry = {
            'idiom': idiom,
            'sentence': sentence,
            'context': context,
            'paragraph': paragraph
        }

        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    print(f'Language: {language}')
    print(f'Number of paragraphs: {total}')
    print(f'Number of paragraphs with idiom: {total_with_idiom}')
    print(f'Number of paragraphs with sentence: {total_with_sentence}')

    outfile.close()