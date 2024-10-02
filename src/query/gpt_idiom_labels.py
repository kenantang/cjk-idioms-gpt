import json
import sys
import time

sys.path.append('../')

from utils.api import get_response_gpt

# read in the list of sampled Chinese idioms
idioms = []
with open('../../data/processed/gpt_chinese_idioms_10k.txt', 'r') as f:
    for line in f:
        idioms.append(line.strip('\n'))

# use append mode because API calls can be interrupted by the rate limit
with open('../../data/raw/gpt_chinese_idiom_labels_10k_raw.jsonl', 'a', encoding='utf-8') as outfile:

    # loop over all idioms and save results
    for idiom in idioms:

        # control the rate so that we send fewer than 600 requests per minute
        time.sleep(0.1)

        prompt = f'Is {idiom} a Chinese idiom? Output yes or no.'

        entry = {'prompt': prompt, 'output': get_response_gpt(prompt, 'gpt-4-0125-preview')}

        # set the ensure_ascii flag so that Chinese characters are saved
        print(json.dumps(entry, ensure_ascii=False), file=outfile)