import json
import sys
import time

import pandas as pd

sys.path.append('../')

from utils.api import get_response_gpt

# only take the first 100 sentences
num = 100
data = pd.read_json('../../data/processed/chinese_sentences_50.jsonl', lines=True).iloc[:num]

# manually insert to avoid floating point error
temperatures = [0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8]

# we only use 10 idioms (10 * 10 = 100 sentences)
outfile = open('../../data/raw/chinese_translations_10_zero_shot_temperature_raw.jsonl', 'a', encoding='utf-8')

for _, row in data.iterrows():

    idiom = row.idiom
    sentence = row.sentence

    prompt = f'Please translate the following sentence from Chinese to English:\n{sentence}'

    for temperature in temperatures:
        entry = {
            'idiom': idiom,
            'sentence': sentence,
            'temperature': temperature,
            'prompt': prompt,
            'response': get_response_gpt(prompt, 'gpt-4-0125-preview', temperature=temperature)
        }

        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()
