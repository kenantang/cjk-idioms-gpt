import argparse
import json
import sys

import pandas as pd

sys.path.append('../')

from utils.api import get_response_gpt

parser = argparse.ArgumentParser()

parser.add_argument('-l', type=str, help='language')

args = parser.parse_args()

# only support CJK and plausible Chinese
assert args.l in ['c', 'j', 'k', 'cp']

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

input_path = f'../../data/processed/{language_file}_paragraphs.jsonl'

instruction_path = '../../data/processed/paragraph_instructions.jsonl'

outfile = open(f'../../data/raw/{language_file}_paragraph_translations_raw.jsonl', 'a', encoding='utf-8')

data = pd.read_json(input_path, lines=True)

instruction_data = pd.read_json(instruction_path, lines=True)

# get the instructions for a single language
instruction_faithful = instruction_data[
    (instruction_data.language == language_prompt) &
    (instruction_data.aspect == 'faithful')
].iloc[0].instruction
instruction_creative = instruction_data[
    (instruction_data.language == language_prompt) &
    (instruction_data.aspect == 'creative')
].iloc[0].instruction
instruction_theme = instruction_data[
    (instruction_data.language == language_prompt) &
    (instruction_data.aspect == 'theme')
].iloc[0].instruction

model = 'gpt-4-0125-preview'

for _, row in data.iterrows():
    idiom = row.idiom
    sentence = row.sentence
    context = row.context
    paragraph = row.paragraph

    entry = {
        'idiom': idiom,
        'sentence': sentence,
        'context': context,
        'paragraph': paragraph
    }

    # 1. baseline
    baseline = f'Please translate the following paragraph from {language_prompt} to English.\n{paragraph}'

    entry['method'] = 'baseline'
    entry['prompt'] = baseline
    entry['response'] = get_response_gpt(baseline, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 2a. faithful simple
    faithful_simple = f'Please translate the following paragraph from {language_prompt} to English. Please translate the idiom "{idiom}" faithfully. Do not explain.\n{paragraph}'

    entry['method'] = 'faithful_simple'
    entry['prompt'] = faithful_simple
    entry['response'] = get_response_gpt(faithful_simple, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 2b. creative simple
    creative_simple = f'Please translate the following paragraph from {language_prompt} to English. Please translate the idiom "{idiom}" creatively. Do not explain.\n{paragraph}'

    entry['method'] = 'creative_simple'
    entry['prompt'] = creative_simple
    entry['response'] = get_response_gpt(creative_simple, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 2c. theme simple
    theme_simple = f'Please translate the following paragraph from {language_prompt} to English. Please translate the idiom "{idiom}" in a way that matches the theme. Do not explain.\n{paragraph}'

    entry['method'] = 'theme_simple'
    entry['prompt'] = theme_simple
    entry['response'] = get_response_gpt(theme_simple, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 3a. faithful cot
    faithful_cot = f'Please translate the following paragraph from {language_prompt} to English. Please translate the idiom "{idiom}" faithfully. Do not explain.\n{paragraph}\nPlease follow the instructions below:\n{instruction_faithful}'

    entry['method'] = 'faithful_cot'
    entry['prompt'] = faithful_cot
    entry['response'] = get_response_gpt(faithful_cot, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 3b. creative cot
    creative_cot = f'Please translate the following paragraph from {language_prompt} to English. Please translate the idiom "{idiom}" creatively. Do not explain.\n{paragraph}\nPlease follow the instructions below:\n{instruction_creative}'

    entry['method'] = 'creative_cot'
    entry['prompt'] = creative_cot
    entry['response'] = get_response_gpt(creative_cot, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 3c. theme cot
    theme_cot = f'Please translate the following paragraph from {language_prompt} to English. Please translate the idiom "{idiom}" in a way that matches the theme. Do not explain.\n{paragraph}\nPlease follow the instructions below:\n{instruction_theme}'

    entry['method'] = 'theme_cot'
    entry['prompt'] = theme_cot
    entry['response'] = get_response_gpt(theme_cot, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4a. faithful multi-turn
    faithful_turn = f'Please translate the following paragraph from {language_prompt} to English. Please translate the idiom "{idiom}" faithfully. Do not explain.\n{paragraph}'
    faithful_response = get_response_gpt(faithful_turn, model)

    entry['method'] = 'faithful_multi_turn'
    entry['prompt'] = faithful_turn
    entry['response'] = faithful_response
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4b. creative multi-turn
    creative_turn = 'Could you provide an alternative translation of the paragraph, where the idiom is translated more creatively? The translation you provided has been widely used elsewhere.'
    creative_messages = [
        {'role': 'user', 'content': faithful_turn},
        {'role': 'assistant', 'content': faithful_response},
        {'role': 'user', 'content': creative_turn}
    ]
    creative_response = get_response_gpt(creative_messages, model, single_turn=False)

    entry['method'] = 'creative_multi_turn'
    entry['prompt'] = creative_messages
    entry['response'] = creative_response
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4c. theme multi-turn
    theme_turn = 'Could you provide an alternative translation of the paragraph, where the idiom is translated with words that better match the context? The translation you provided can be used verbatim in a different context.'
    theme_messages = [
        {'role': 'user', 'content': faithful_turn},
        {'role': 'assistant', 'content': faithful_response},
        {'role': 'user', 'content': creative_turn},
        {'role': 'assistant', 'content': creative_response},
        {'role': 'user', 'content': theme_turn},
    ]
    theme_response = get_response_gpt(theme_messages, model, single_turn=False)

    entry['method'] = 'theme_multi_turn'
    entry['prompt'] = theme_messages
    entry['response'] = theme_response
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()