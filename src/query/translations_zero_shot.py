import argparse
import json
import sys
import time

import pandas as pd

sys.path.append('../')

from utils.api import get_response_gpt, get_translation_deepl, get_translation_google

parser = argparse.ArgumentParser()

parser.add_argument('-l', type=str, help='language')

args = parser.parse_args()

# DeepL: https://developers.deepl.com/docs/resources/supported-languages
# Google: https://cloud.google.com/translate/docs/languages

if args.l == 'c':
    language_file = 'chinese'
    language_prompt = 'Chinese'
    language_google = 'zh'
    language_deepl = 'ZH'
elif args.l == 'j':
    language_file = 'japanese'
    language_prompt = 'Japanese'
    language_google = 'ja'
    language_deepl = 'JA'
elif args.l == 'k':
    language_file = 'korean'
    language_prompt = 'Korean'
    language_google = 'ko'
    language_deepl = 'KO'
elif args.l == 'cp':
    language_file = 'chinese_plausible'
    language_prompt = 'Chinese'
    language_google = 'zh'
    language_deepl = 'ZH'

input_path = f'../../data/processed/{language_file}_sentences_50.jsonl'

data = pd.read_json(input_path, lines=True)

model = 'gpt-4-0125-preview'

# different contexts
contexts = [
    'a news report',
    'a romance novel',
    'an everyday conversation',
    'a history book'
]

outfile = open(f'../../data/raw/{language_file}_translations_50_zero_shot_raw.jsonl', 'a', encoding='utf-8')

for _, row in data.iterrows():
    idiom = row.idiom
    sentence = row.sentence

    entry = {
        'idiom': idiom,
        'sentence': sentence,
    }

    # 1a. Google
    entry['method'] = 'google'
    entry['prompt'] = 'N/A'
    entry['response'] = get_translation_google(text = sentence, source_language_code = language_google)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 1b. DeepL
    entry['method'] = 'deepl'
    entry['prompt'] = 'N/A'
    entry['response'] = get_translation_deepl(text = sentence, source_lang = language_deepl)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 2a. baseline
    baseline = f'Please translate the following sentence from {language_prompt} to English:\n{sentence}'
    entry['method'] = 'baseline'
    entry['prompt'] = baseline
    entry['response'] = get_response_gpt(baseline, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 2b. diversity explicit
    diversity_explicit = f'Please generate 5 different translations of the following sentence from {language_prompt} to English:\n{sentence}'
    diversity_explicit_response = get_response_gpt(diversity_explicit, model)

    entry['method'] = 'diversity_explicit'
    entry['prompt'] = diversity_explicit
    entry['response'] = diversity_explicit_response
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 2c. diversity dialog
    diversity_dialog = 'Please generate another 5 different translations.'
    diversity_dialog_messages = [
        {'role': 'user', 'content': diversity_explicit},
        {'role': 'assistant', 'content': diversity_explicit_response},
        {'role': 'user', 'content': diversity_dialog}
    ]

    entry['method'] = 'diversity_dialog'
    entry['prompt'] = diversity_dialog_messages
    entry['response'] = get_response_gpt(diversity_dialog_messages, model, single_turn=False)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 3a. zero-shot creatively
    zero_shot_creatively = f'Please creatively translate the following sentence from {language_prompt} to English:\n{sentence}'
    entry['method'] = 'zero_shot_creatively'
    entry['prompt'] = zero_shot_creatively
    entry['response'] = get_response_gpt(zero_shot_creatively, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4a. context explicit
    for context in contexts:
        context_explicit = f'The sentence below comes from {context}. Please translate it from {language_prompt} to English:\n{sentence}'
        entry['method'] = 'context_explicit'
        entry['prompt'] = context_explicit
        entry['response'] = get_response_gpt(context_explicit, model)
        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4b. analogy natural
    analogy_natural = f'Please translate the following sentence from {language_prompt} to English:\n{sentence}\nIn the translation, please use an analogy commonly used in English.'
    entry['method'] = 'analogy_natural'
    entry['prompt'] = analogy_natural
    entry['response'] = get_response_gpt(analogy_natural, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4c. analogy creative
    analogy_creative = f'Please translate the following sentence from {language_prompt} to English:\n{sentence}\nIn the translation, please create a new analogy that has not been commonly used in English.'
    entry['method'] = 'analogy_creative'
    entry['prompt'] = analogy_creative
    entry['response'] = get_response_gpt(analogy_creative, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4d. shuffle order
    shuffle_order = f'Please translate the following sentence from {language_prompt} to English:\n{sentence}\nPlease try to change the order of clauses to make the translation more natural.'
    entry['method'] = 'shuffle_order'
    entry['prompt'] = shuffle_order
    entry['response'] = get_response_gpt(shuffle_order, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4e. succinct
    succinct = f'Please translate the following sentence from {language_prompt} to English:\n{sentence}\nPlease translate the {language_prompt} idiom appeared in the sentence as succinctly as possible.'
    entry['method'] = 'succinct'
    entry['prompt'] = succinct
    entry['response'] = get_response_gpt(succinct, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4f. two_step
    step_1 = f'Please rewrite the following sentence in {language_prompt} without using a {language_prompt} idiom:\n{sentence}'
    rewritten_sentence = get_response_gpt(step_1, model)
    step_2 = 'Please translate the rewritten sentence to English.'
    two_step_messages = [
        {'role': 'user', 'content': step_1},
        {'role': 'assistant', 'content': rewritten_sentence},
        {'role': 'user', 'content': step_2}
    ]

    entry['method'] = 'two_step'
    entry['prompt'] = two_step_messages
    entry['response'] = get_response_gpt(two_step_messages, model, single_turn=False)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4g. discontinuous 1
    discontinous_1 = f'Please translate the following sentence from {language_prompt} to English:\n{sentence}\nPlease do not use a continuous span to translate the {language_prompt} idiom appeared in the sentence.'
    entry['method'] = 'discontinuous_1'
    entry['prompt'] = discontinous_1
    entry['response'] = get_response_gpt(discontinous_1, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    # 4h. discontinuous 2
    discontinous_2 = f'Please translate the following sentence from {language_prompt} to English:\n{sentence}\nPlease do not use a multi-word expression to translate the {language_prompt} idiom appeared in the sentence.'
    entry['method'] = 'discontinuous_2'
    entry['prompt'] = discontinous_2
    entry['response'] = get_response_gpt(discontinous_2, model)
    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()