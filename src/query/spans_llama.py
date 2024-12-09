# WARNING: The code is inefficient and will be replaced by a vllm implementation.

import os
os.environ['HF_HOME'] = '/data/kenantang/llama'
os.environ["CUDA_VISIBLE_DEVICES"] = "0,1"

import transformers
import torch
import pandas as pd
import json
from tqdm import tqdm

model_id = "meta-llama/Llama-3.3-70B-Instruct"

pipeline = transformers.pipeline(
    "text-generation",
    model=model_id,
    model_kwargs={"torch_dtype": torch.bfloat16},
    device_map="auto"
)

def get_response_llama(prompt):

    seed = 0
    torch.cuda.manual_seed_all(seed)

    messages = [
        {"role": "system", "content": "You are an AI chatbot."},
        {"role": "user", "content": prompt},
    ]

    outputs = pipeline(
        messages,
        max_new_tokens=256,
    )

    return outputs[0]["generated_text"][-1]["content"]

data = pd.read_json('chinese_translations_500_optimal.jsonl', lines=True)

outfile = open(f'chinese_spans_500_optimal_raw.jsonl', 'a', encoding='utf-8')

for _, row in tqdm(data.iterrows()):
    idiom = row.idiom
    sentence = row.sentence
    method = row.method
    translation = row.translation

    entry = {
        'idiom': idiom,
        'sentence': sentence,
        'method': method,
        'translation': translation
    }

    extract_prompt = 'Given the English translation of the Chinese sentence, please only output the span that corresponds to the Chinese idiom.\n\n'
    extract_prompt += f'Chinese sentence: {sentence}\n'
    extract_prompt += f'English translation: {translation}\n'
    extract_prompt += f'Chinese idiom: {idiom}\n'
    extract_prompt += 'Span:\n'

    entry['prompt'] = extract_prompt
    entry['response'] = get_response_llama(extract_prompt)

    print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()