import json

import numpy as np
import pandas as pd

zero_shot_file_names = [
    'chinese_scores_50_zero_shot',
    'japanese_scores_50_zero_shot',
    'korean_scores_50_zero_shot',
    'chinese_plausible_scores_50_zero_shot'
]

few_shot_file_names = [
    'chinese_scores_50_few_shot',
    'japanese_scores_50_few_shot',
    'korean_scores_50_few_shot',
    'chinese_plausible_scores_50_few_shot'
]

method_names_with_repetition = [
    'Google',
    'DeepL',
    'Baseline',
    'Diversity Explicit',
    'Diversity Explicit',
    'Diversity Explicit',
    'Diversity Explicit',
    'Diversity Explicit',
    'Diversity Dialog',
    'Diversity Dialog',
    'Diversity Dialog',
    'Diversity Dialog',
    'Diversity Dialog',
    'Zero-Shot Creatively',
    'Context Explicit',
    'Context Explicit',
    'Context Explicit',
    'Context Explicit',
    'Analogy Natural',
    'Analogy Creative',
    'Shuffle Order',
    'Succinct',
    'Two-Step',
    'Discontinuous 1',
    'Discontinuous 2',
    'Few-Shot',
    'Few-Shot Creatively'
]

zero_shot_lines = 250
few_shot_lines = 20

grouping_key_zero = np.repeat(np.arange(zero_shot_lines // 5), 5)[:zero_shot_lines]
grouping_key_few = np.repeat(np.arange(few_shot_lines // 5), 5)[:few_shot_lines]

for zero_shot_file, few_shot_file in zip(zero_shot_file_names, few_shot_file_names):
    zero_raw = pd.read_json(f'../../data/processed/{zero_shot_file}.jsonl', lines=True)
    few_raw = pd.read_json(f'../../data/processed/{few_shot_file}.jsonl', lines=True)

    agg_dict = {col: 'first' for col in zero_raw.columns if col != 'score'}
    agg_dict['score'] = 'mean'

    zero = zero_raw.iloc[:zero_shot_lines].groupby(grouping_key_zero).agg(agg_dict)
    few = few_raw.iloc[:few_shot_lines].groupby(grouping_key_few).agg(agg_dict)

    count = 0

    # print out the zero-shot results
    for index in range(len(zero) // 2):
        method = method_names_with_repetition[count]
        translation = zero.iloc[index * 2].translation
        faithfulness = zero.iloc[index * 2].score
        creativity = zero.iloc[index * 2 + 1].score
        print(f'\\textsc{{{method}}} & \\multicolumn{{1}}{{p{{0.6\linewidth}}}}{{\\raggedright {translation}}} & {faithfulness} & {creativity} \\\\')
        count += 1

    # print out the few-shot results
    for index in range(len(few) // 2):
        method = method_names_with_repetition[count]
        translation = few.iloc[index * 2].translation
        faithfulness = few.iloc[index * 2].score
        creativity = few.iloc[index * 2 + 1].score
        print(f'\\textsc{{{method}}} & \\multicolumn{{1}}{{p{{0.6\linewidth}}}}{{\\raggedright {translation}}} & {faithfulness} & {creativity} \\\\')
        count += 1

    print()

