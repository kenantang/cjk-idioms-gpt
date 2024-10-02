import argparse
import json
import sys
import time

import numpy as np
import pandas as pd

sys.path.append('../')

from utils.api import get_response_gpt

parser = argparse.ArgumentParser()

parser.add_argument('-l', type=str, help='language')

args = parser.parse_args()

if args.l == 'c':
    language_file = 'chinese'
    language_prompt = 'Chinese'
elif args.l == 'j':
    language_file = 'japanese'
    language_prompt = 'Japanese'
elif args.l == 'k':
    language_file = 'korean'
    language_prompt = 'Korean'
elif args.l == 'cp':
    language_file = 'chinese_plausible'
    language_prompt = 'Chinese'

sentence_path = f'../../data/processed/{language_file}_sentences_50.jsonl'
example_path = f'../../data/processed/{language_file}_translations_50_most_creative.jsonl'

sentences = pd.read_json(sentence_path, lines=True)
examples = pd.read_json(example_path, lines=True)

np.random.seed(0)

model = 'gpt-4-0125-preview'

outfile = open(f'../../data/raw/{language_file}_translations_50_few_shot_raw.jsonl', 'a', encoding='utf-8')

number_of_examples = 5

for _, row in sentences.iterrows():
    idiom = row.idiom
    sentence = row.sentence

    entry = {
        'idiom': idiom,
        'sentence': sentence,
    }

    prompt_idx = np.random.choice(len(examples), number_of_examples, replace=False)
    prompt_examples = [examples.iloc[i] for i in prompt_idx]


    # 5a. few-shot
    few_shot = f'Please translate the following sentences from {language_prompt} to English:\n'
    for prompt_example in prompt_examples:
        few_shot += f'{language_prompt}: {prompt_example.sentence}\nEnglish: {prompt_example.translation}\n'

    few_shot += f'{language_prompt}: {sentence}\nEnglish: '

    entry['method'] = 'few_shot'
    entry['prompt'] = few_shot
    entry['response'] = get_response_gpt(few_shot, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 5b. few-shot creatively
    few_shot_creatively = f'Please creatively translate the following sentences from {language_prompt} to English:\n'
    for prompt_example in prompt_examples:
        few_shot_creatively += f'{language_prompt}: {prompt_example.sentence}\nEnglish: {prompt_example.translation}\n'

    few_shot_creatively += f'{language_prompt}: {sentence}\nEnglish: '

    entry['method'] = 'few_shot_creatively'
    entry['prompt'] = few_shot_creatively
    entry['response'] = get_response_gpt(few_shot_creatively, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()