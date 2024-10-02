import json
import sys

import pandas as pd

sys.path.append('../')

from utils.api import get_response_gpt

languages = ['chinese', 'japanese', 'korean', 'chinese_plausible']
languages_prompt = ['Chinese', 'Japanese', 'Korean', 'Chinese']
contexts = [
    'a news report',
    'a romance novel',
    'an everyday conversation',
    'a history book'
]

for language, language_prompt in zip(languages, languages_prompt):

    data = pd.read_json(f'../../data/processed/{language}_sentences_50.jsonl', lines=True)

    # the first sentence of each of the 20 first idioms
    sample = data.iloc[0::10].iloc[:20]

    outfile = open(f'../../data/raw/{language}_paragraphs_raw.jsonl', 'a', encoding='utf-8')

    for _, row in sample.iterrows():
        idiom = row.idiom
        sentence = row.sentence

        for context in contexts:
            prompt = f'In the style of {context}, please imagine a paragraph in {language_prompt} that contains the following sentence:\n{sentence}'

            response = get_response_gpt(prompt, 'gpt-4-0125-preview')

            entry = {
                'idiom': idiom,
                'sentence': sentence,
                'context': context,
                'prompt': prompt,
                'response': response
            }

            print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    outfile.close()