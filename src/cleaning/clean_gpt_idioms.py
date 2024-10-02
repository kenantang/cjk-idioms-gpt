import os
import random
import sys

import pandas as pd

# for import
sys.path.append('../')

from utils.parse import extract_idioms, remove_irrelevant

# read the mining results
mined = pd.read_json(path_or_buf='../../data/raw/gpt_chinese_idioms_raw.jsonl', lines=True)

# get the idioms returned within each response
each_response = mined.output.apply(extract_idioms)

# remove the irrelevant information and construct a full list
full_list = each_response.explode().dropna().apply(remove_irrelevant).to_list()

# further filter out all occurrences of empty strings
full_list = [idiom for idiom in full_list if idiom != '']

# Chinese specific: check if the idiom begin with a Chinese character
full_list = [idiom for idiom in full_list if idiom[0] >= u'\u4e00' and idiom[0] <= u'\u9fff']

# get the unique idioms
full_set = set(full_list)

# write unique idioms to a file
with open('../../data/processed/gpt_chinese_idioms.txt', 'w', encoding='utf-8') as outfile:
    # sort the set so that the output is deterministic
    for idiom in sorted(full_set):
        print(idiom, file=outfile)

# sample 10,000 idioms for budget control
random.seed(0)
with open('../../data/processed/gpt_chinese_idioms_10k.txt', 'w', encoding='utf-8') as outfile:
    # sort the set so that the output is deterministic
    for idiom in random.sample(sorted(full_set), 10000):
        print(idiom, file=outfile)