import json
import sys

import pandas as pd

sys.path.append('../')

from utils.parse import extract_sentences

file_names = [
    'chinese_sentences_50',
    'chinese_sentences_more',
    'japanese_sentences_50',
    'japanese_sentences_more',
    'korean_sentences_50',
    'korean_sentences_more',
    'chinese_plausible_sentences_50'
]

for file_name in file_names:
    raw = pd.read_json(f'../../data/raw/{file_name}_raw.jsonl', lines=True)

    outfile = open(f'../../data/processed/{file_name}.jsonl', 'w', encoding='utf-8')

    total = 0
    total_with_idiom = 0
    total_wrong_format = 0

    for _, row in raw.iterrows():
        sentences = extract_sentences(row.response)

        # check if for each response, we get 10 sentences
        if len(sentences) > 10:
            # take the first 10, as the last line is an explanation
            sentences = sentences[:10]
            total_wrong_format += 1
        elif len(sentences) < 10:
            # no sentences are made
            sentences = ['' for _ in range(10)]
            total_wrong_format += 1

        for sentence in sentences:
            entry = {
                'idiom': row.idiom,
                'sentence': sentence
            }

            total += 1
            if row.idiom in sentence:
                total_with_idiom += 1

            print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    print(f'File: {file_name}')
    print(f'Number of sentences: {total}')
    print(f'Number of sentence with idiom: {total_with_idiom}')
    print(f'Number of idioms with a wrong format: {total_wrong_format}')