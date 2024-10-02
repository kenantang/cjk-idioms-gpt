import json
import sys

sys.path.append('../')

from utils.api import get_response_gpt

outfile = open('../../data/raw/paragraph_instructions_raw.jsonl', 'a', encoding='utf-8')

repeat = 1

languages = ['Chinese', 'Japanese', 'Korean']

aspects = ['faithful', 'creative', 'theme']

for language in languages:

    prompts = [
        f'If you are asked to translate a paragraph that contains a {language} idiom, what would you do to ensure that the translation of the idiom is faithful?',
        f'If you are asked to translate a paragraph that contains a {language} idiom, what would you do to ensure that the translation of the idiom is creative?',
        f'If you are asked to translate a paragraph that contains a {language} idiom, what would you do to ensure that the translation of the idiom matches the theme of its context?'
    ]

    for aspect, prompt in zip(aspects, prompts):

        for seed in range(repeat):
            response = get_response_gpt(prompt, 'gpt-4-0125-preview', seed=seed)

            entry = {
                'language': language,
                'aspect': aspect,
                'prompt': prompt,
                'response': response
            }

            print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()