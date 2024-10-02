import json
import sys
import time

sys.path.append('../')

from utils.api import get_response_gpt

# read in the list of pinyins
pinyins = []
with open('../../data/external/pinyin.txt', 'r') as f:
    for line in f:
        pinyins.append(line.strip('\n'))

# number of repeats for a single pinyin
repeat = 5

with open('../../data/raw/gpt_chinese_idioms_raw.jsonl', 'w', encoding='utf-8') as outfile:

    # loop over all pinyins as initials and save results
    for pinyin in pinyins:

        prompt = f'Give 200 Chinese idioms that begin with {pinyin}. Only list idioms. Do not explain them. No duplicates.'

        # repeat multiple times to observe the different behaviors
        for seed in range(repeat):

            # for timing each response
            start_time = time.time()

            entry = {'prompt': prompt, 'output': get_response_gpt(prompt, 'gpt-4-0125-preview', seed=seed)}

            # set the ensure_ascii flag so that Chinese characters are saved
            print(json.dumps(entry, ensure_ascii=False), file=outfile)

            # for logging
            print(f'{pinyin} {time.time()-start_time:.2f}s')