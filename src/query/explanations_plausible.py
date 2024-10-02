import json
import re
import sys

from tqdm import tqdm

sys.path.append('../')

from utils.api import get_response_gpt

plausible_list = []

with open('../../data/processed/chinese_plausible_idioms_50.txt', 'r') as f:
    for line in f:
        plausible_list.append(line.strip('\n'))

outfile = open('../../data/raw/chinese_plausible_explanations_50.jsonl', 'a', encoding='utf-8')

for idiom in tqdm(plausible_list):
    prompt = f'Is {idiom} a Chinese idiom? Please explain.'
    response = get_response_gpt(prompt, 'gpt-4-0125-preview')

    entry = {
        'idiom': idiom,
        'prompt': prompt,
        'response': response
    }

    print(json.dumps(entry, ensure_ascii=False), file=outfile)

outfile.close()