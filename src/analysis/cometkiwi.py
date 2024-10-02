import json

import pandas as pd
from comet import load_from_checkpoint
from tqdm import tqdm

data = pd.read_json('../../data/processed/chinese_translations_50_optimal.jsonl', lines=True)

# prepare the data for the model
pairs = []

for _, row in data.iterrows():
    pairs.append({
        'src': row.sentence,
        'mt': row.translation
    })

# load model
model = load_from_checkpoint('/data/kenantang/wmt23-cometkiwi-da-xxl/checkpoints/model.ckpt')

model_output = model.predict(pairs, batch_size=100, gpus=1, devices=[4])

outfile = open(f'../../data/processed/chinese_cometkiwi_50_optimal.jsonl', 'w', encoding='utf-8')

for index, row in data.iterrows():
    entry = {
        'idiom': row.idiom,
        'sentence': row.sentence,
        'translation': row.translation,
        'method': row.method,
        'score': model_output.scores[index]
    }

    print(json.dumps(entry, ensure_ascii=False), file=outfile)

outfile.close()