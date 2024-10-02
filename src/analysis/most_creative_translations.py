import json

import pandas as pd

input_names = [
    'chinese_scores_50_zero_shot',
    'japanese_scores_50_zero_shot',
    'korean_scores_50_zero_shot',
    'chinese_plausible_scores_50_zero_shot',
]

output_names = [
    'chinese_translations_50_most_creative',
    'japanese_translations_50_most_creative',
    'korean_translations_50_most_creative',
    'chinese_plausible_translations_50_most_creative',
]

for input_name, output_name in zip(input_names, output_names):
    scores = pd.read_json(f'../../data/processed/{input_name}.jsonl', lines=True)

    creative = scores[scores.aspect == 'creativity']

    most_creative = creative[creative.score == 5].drop(['iteration'], axis=1).drop_duplicates()

    outfile = open(f'../../data/processed/{output_name}.jsonl', 'w', encoding='utf-8')

    for _, row in most_creative.iterrows():
        entry = {
            'idiom': row.idiom,
            'sentence': row.sentence,
            'translation': row.translation,
            'method': row.method,
        }

        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

    print(f'Input: {input_name}')
    print(most_creative['method'].value_counts())

    outfile.close()