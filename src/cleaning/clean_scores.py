import json
import sys

import pandas as pd

sys.path.append('../')

from utils.parse import extract_score

# not all these files can be cleaned parallelly
# when actually running the code, comment out the lines that are not needed
file_names = [
    'chinese_scores_50_zero_shot',
    'japanese_scores_50_zero_shot',
    'korean_scores_50_zero_shot',
    'chinese_plausible_scores_50_zero_shot',
    'chinese_scores_50_few_shot',
    'japanese_scores_50_few_shot',
    'korean_scores_50_few_shot',
    'chinese_plausible_scores_50_few_shot',
    'chinese_scores_50_optimal'
]

for file_name in file_names:
    raw = pd.read_json(f'../../data/raw/{file_name}_raw.jsonl', lines=True)

    outfile = open(f'../../data/processed/{file_name}.jsonl', 'w', encoding='utf-8')

    for _, row in raw.iterrows():
        score = extract_score(row.response)

        # check if score is in 1-5
        assert score in [1, 2, 3, 4, 5], f'Cannot parse {row.response}'

        entry = {
            'idiom': row.idiom,
            'sentence': row.sentence,
            'translation': row.translation,
            'method': row.method,
            'aspect': row.aspect,
            'iteration': row.iteration,
            'score': extract_score(row.response)
        }

        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    print(f'Done: {file_name}')

    outfile.close()