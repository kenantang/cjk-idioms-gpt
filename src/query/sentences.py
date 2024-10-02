import argparse
import json
import sys
import time

sys.path.append('../')

from utils.api import get_response_gpt

parser = argparse.ArgumentParser()

parser.add_argument('-l', type=str, help='language')
parser.add_argument('-n', type=str, help='number of idioms (50 or more)')

args = parser.parse_args()

# only support CJK and plausible Chinese
assert args.l in ['c', 'j', 'k', 'cp']

# only support files in this project
assert args.n in ['50', 'more']

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
    assert args.n == '50'
    language_prompt = 'Chinese'

input_path = f'../../data/processed/{language_file}_idioms_{args.n}.txt'

idioms = []
with open(input_path, 'r') as f:
    for line in f:
        idioms.append(line.strip('\n'))

outfile =  open(f'../../data/raw/{language_file}_sentences_{args.n}_raw.jsonl', 'a', encoding='utf-8')

for idiom in idioms:
    start_time = time.time()

    prompt = f'Can you make 10 {language_prompt} sentences with the {language_prompt} idiom {idiom}? Only list sentences. Do not explain.'
    response = get_response_gpt(prompt, 'gpt-4-0125-preview')

    entry = {
        'idiom': idiom,
        'prompt': prompt,
        'response': response
    }

    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    print(f'{time.time()-start_time:.2f}')

outfile.close()