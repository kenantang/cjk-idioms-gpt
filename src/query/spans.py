import json
import sys

import pandas as pd

sys.path.append('../')

from utils.api import get_response_gpt

data = pd.read_json('../../data/processed/chinese_translations_50_optimal.jsonl', lines=True)

model = 'gpt-4-0125-preview'

outfile = open(f'../../data/raw/chinese_spans_50_optimal_raw.jsonl', 'a', encoding='utf-8')

for _, row in data.iterrows():
    idiom = row.idiom
    sentence = row.sentence
    method = row.method
    translation = row.translation

    entry = {
        'idiom': idiom,
        'sentence': sentence,
        'method': method,
        'translation': translation
    }

    extract_prompt = 'Given the English translation of the Chinese sentence, please only output the span that corresponds to the Chinese idiom.\n\n'
    extract_prompt += f'Chinese sentence: {sentence}\n'
    extract_prompt += f'English translation: {translation}\n'
    extract_prompt += f'Chinese idiom: {idiom}\n'
    extract_prompt += 'Span:\n'

    entry['prompt'] = extract_prompt
    entry['response'] = get_response_gpt(extract_prompt, model)

    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()