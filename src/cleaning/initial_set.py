import json
import random

import pandas as pd

random.seed(0)

num = 50

# chinese

with open('../../data/external/petci_filtered.json', 'r') as f:
    petci = json.load(f)

random.shuffle(petci)

chinese_idioms_num = [idiom['chinese'] for idiom in petci[:num]]
chinese_idioms_more = [idiom['chinese'] for idiom in petci[num:]]

with open(f'../../data/processed/chinese_idioms_{num}.txt', 'w', encoding='utf-8') as outfile:
    for idiom in chinese_idioms_num:
        print(idiom, file=outfile, flush=True)

with open('../../data/processed/chinese_idioms_more.txt', 'w', encoding='utf-8') as outfile:
    for idiom in chinese_idioms_more:
        print(idiom, file=outfile, flush=True)

# japanese

goo = pd.read_json('../../data/external/japanese_idioms_goo.jsonl', lines=True)

japanese_idioms_list = list(goo.idiom.apply(lambda x: x.split('【')[1].split('】')[0]).unique())

random.shuffle(japanese_idioms_list)

japanese_idioms_num = japanese_idioms_list[:num]
japanese_idioms_more = japanese_idioms_list[num:]

with open(f'../../data/processed/japanese_idioms_{num}.txt', 'w', encoding='utf-8') as outfile:
    for idiom in japanese_idioms_num:
        print(idiom, file=outfile, flush=True)

with open('../../data/processed/japanese_idioms_more.txt', 'w', encoding='utf-8') as outfile:
    for idiom in japanese_idioms_more:
        print(idiom, file=outfile, flush=True)

# korean

with open('../../data/external/korean_idioms.json', 'r') as f:
    korean_idioms_raw = json.load(f)

korean_idioms_list = [idiom['Q'].split('(')[1].split(')')[0] for idiom in korean_idioms_raw['idioms']]

# deduplicate, size 2318 -> 2316
korean_idioms_list = list(dict.fromkeys(korean_idioms_list))

random.shuffle(korean_idioms_list)

korean_idioms_num = korean_idioms_list[:num]
korean_idioms_more = korean_idioms_list[num:]

with open(f'../../data/processed/korean_idioms_{num}.txt', 'w', encoding='utf-8') as outfile:
    for idiom in korean_idioms_num:
        print(idiom, file=outfile, flush=True)

with open('../../data/processed/korean_idioms_more.txt', 'w', encoding='utf-8') as outfile:
    for idiom in korean_idioms_more:
        print(idiom, file=outfile, flush=True)

