import argparse
import json
import sys

import pandas as pd

sys.path.append('../')

from utils.api import get_response_gpt

parser = argparse.ArgumentParser()

parser.add_argument('-i', type=str, help='input file')
parser.add_argument('-o', type=str, help='output file')

args = parser.parse_args()

input_path = args.i

data = pd.read_json(input_path, lines=True)

# we want the average of 5 scores
num_of_repeat = 5

outfile = open(args.o, 'a', encoding='utf-8')

for _, row in data.iterrows():
    entry = {}
    entry['idiom'] = row.idiom
    entry['sentence'] = row.sentence
    entry['translation'] = row.translation
    entry['method'] = row.method

    entry['aspect'] = 'faithfulness'

    faithful_prompt = "Please rate the faithfulness of the following idiom translation within a sentence.\n"
    faithful_prompt += f"Idiom to be translated: {row.idiom}\n"
    faithful_prompt += f"Original sentence containing this idiom: {row.sentence}\n"
    faithful_prompt += f"Translation: {row.translation}\n"
    faithful_prompt += "Your faithfulness rating should be a score from 1 to 5, where 1 is not faithful at all and 5 is perfectly faithful. Return a single number as your rating.\n"

    entry['prompt'] = faithful_prompt

    for iteration in range(num_of_repeat):
        entry['iteration'] = iteration
        entry['response'] = get_response_gpt(faithful_prompt, model='gpt-3.5-turbo', seed=iteration)
        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    entry['aspect'] = 'creativity'

    creative_prompt = "Please rate the creativity of the following idiom translation within a sentence.\n"
    creative_prompt += f"Idiom to be translated: {row.idiom}\n"
    creative_prompt += f"Original sentence containing this idiom: {row.sentence}\n"
    creative_prompt += f"Translation: {row.translation}\n"
    creative_prompt += "Your creativity rating should be a score from 1 to 5, where 1 is not creative at all (just plain language) and 5 is perfectly creative. Return a single number as your rating.\n"

    entry['prompt'] = creative_prompt

    for iteration in range(num_of_repeat):
        entry['iteration'] = iteration
        entry['response'] = get_response_gpt(creative_prompt, model='gpt-3.5-turbo', seed=iteration)
        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()