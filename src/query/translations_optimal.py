import json
import sys

import numpy as np
import pandas as pd

sys.path.append('../')

from utils.api import get_response_gpt

parallel = pd.read_json('../../data/processed/chinese_parallel_corpus.jsonl', lines=True)

sentences = pd.read_json('../../data/processed/chinese_sentences_more.jsonl', lines=True)

examples = pd.read_json(f'../../data/processed/chinese_translations_50_most_creative.jsonl', lines=True)

np.random.seed(0)

# deduplicate idioms manually
sentences.drop(list(range(31440, 31450)) + list(range(20990, 21000)), inplace=True)

# unique idioms in petci (excluding 50 sampled)
unique_idioms = sentences.idiom.unique()

frequencies = parallel.idiom.value_counts().reset_index().rename(columns={"index": "idiom", "count": "frequency"})

# select k most frequent idioms
k = 500

# for few-shot
number_of_examples = 5

selected_idioms = []

for _, row in frequencies.iterrows():
    if row.idiom in unique_idioms:
        selected_idioms.append(row.idiom)
        print(row.idiom, row.frequency, 'selected')
    else:
        print(row.idiom, row.frequency, 'skipped')

    if len(selected_idioms) == k:
        break

selected_sentences = sentences[sentences.idiom.isin(selected_idioms)].reset_index()

print(selected_sentences.idiom.value_counts().head())
print(selected_sentences.idiom.value_counts().tail())
print(len(selected_sentences))

model = 'gpt-4-0125-preview'

outfile = open(f'../../data/raw/chinese_translations_{k}_optimal_raw.jsonl', 'a', encoding='utf-8')

for index, row in selected_sentences.iterrows():

    idiom = row.idiom
    sentence = row.sentence

    entry = {
        'idiom': idiom,
        'sentence': sentence,
    }

    # 3a. zero-shot creatively
    zero_shot_creatively = f'Please creatively translate the following sentence from Chinese to English:\n{sentence}'
    entry['method'] = 'zero_shot_creatively'
    entry['prompt'] = zero_shot_creatively
    entry['response'] = get_response_gpt(zero_shot_creatively, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4c. analogy creative
    analogy_creative = f'Please translate the following sentence from Chinese to English:\n{sentence}\nIn the translation, please create a new analogy that has not been commonly used in English.'
    entry['method'] = 'analogy_creative'
    entry['prompt'] = analogy_creative
    entry['response'] = get_response_gpt(analogy_creative, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    prompt_idx = np.random.choice(len(examples), number_of_examples, replace=False)
    prompt_examples = [examples.iloc[i] for i in prompt_idx]


    # 5a. few-shot
    few_shot = f'Please translate the following sentences from Chinese to English:\n'
    for prompt_example in prompt_examples:
        few_shot += f'Chinese: {prompt_example.sentence}\nEnglish: {prompt_example.translation}\n'

    few_shot += f'Chinese: {sentence}\nEnglish: '

    entry['method'] = 'few_shot'
    entry['prompt'] = few_shot
    entry['response'] = get_response_gpt(few_shot, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 5b. few-shot creatively
    few_shot_creatively = f'Please creatively translate the following sentences from Chinese to English:\n'
    for prompt_example in prompt_examples:
        few_shot_creatively += f'Chinese: {prompt_example.sentence}\nEnglish: {prompt_example.translation}\n'

    few_shot_creatively += f'Chinese: {sentence}\nEnglish: '

    entry['method'] = 'few_shot_creatively'
    entry['prompt'] = few_shot_creatively
    entry['response'] = get_response_gpt(few_shot_creatively, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()