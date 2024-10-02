import re

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from adjustText import adjust_text
from matplotlib.lines import Line2D

# set output precision
pd.set_option('display.precision', 2)

file_names = [
    'chinese_scores_50',
    'japanese_scores_50',
    'korean_scores_50',
    'chinese_plausible_scores_50',
]

languages = [
    'Chinese',
    'Japanese',
    'Korean',
    'Plausible Chinese'
]

# for y labels of the heatmap and names on the scatter plot
method_names = [
    'Google',
    'DeepL',
    'Baseline',
    'Diversity Explicit',
    'Diversity Dialog',
    'Zero-Shot Creatively',
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

score_dict = {'score':['size', 'mean', 'std']}

# a data frame that saves the mean scores
mean_scores = pd.DataFrame()

for file_index, file_name in enumerate(file_names):
    scores_zero_shot = pd.read_json(f'../../data/processed/{file_name}_zero_shot.jsonl', lines=True)
    scores_few_shot = pd.read_json(f'../../data/processed/{file_name}_few_shot.jsonl', lines=True)

    scores = pd.concat([scores_zero_shot, scores_few_shot])

    faithful = scores[scores.aspect == 'faithfulness']
    creative = scores[scores.aspect == 'creativity']

    # Get method statistics

    # Create a grouping key that assigns each set of 5 rows the same number
    grouping_key = np.repeat(np.arange(len(faithful) // 5), 5)[:len(faithful)]

    # Dictionary for aggregation
    # Assuming 'score' is to be averaged, and all others use 'first'
    agg_dict = {col: 'first' for col in faithful.columns if col != 'score'}
    agg_dict['score'] = 'mean'

    faithful_mean_iteration = faithful.groupby(grouping_key).agg(agg_dict)
    creative_mean_iteration = creative.groupby(grouping_key).agg(agg_dict)

    print(f'Faithfulness ({file_name}):')
    faithful_mean_std_sentence = faithful_mean_iteration.groupby('method', sort=False, as_index=False).agg(score_dict)
    print(faithful_mean_std_sentence)
    mean_scores[f'{file_name}_faithful'] = faithful_mean_std_sentence.score['mean']

    print(f'Creativity ({file_name}):')
    creative_mean_std_sentence = creative_mean_iteration.groupby('method', sort=False, as_index=False).agg(score_dict)
    print(creative_mean_std_sentence)
    mean_scores[f'{file_name}_creative'] = creative_mean_std_sentence.score['mean']

    # Modified from ChatGPT output

    # Data
    series1 = faithful.groupby('method', sort=False, as_index=False)['score'].mean()
    series2 = creative.groupby('method', sort=False, as_index=False)['score'].mean()

    # Extract names
    names = series1.method

    # Define custom colors
    colors = ['tab:blue'] * 2 + ['tab:orange'] * 3 + ['tab:green'] * 1 + ['tab:red'] * 8 + ['tab:purple'] * 2

    # Extract scores
    scores1 = series1.score.to_list()
    scores2 = series2.score.to_list()

    # Create a DataFrame
    df = pd.DataFrame({
        'faithfulness': scores1,
        'creativity': scores2
    }, index=names)

    # Plotting
    fig, ax = plt.subplots(figsize=(8, 8), dpi=150)

    # Manually selected thresholds
    if file_index == 0:
        ax.set_xlim(3.1, 4.35)
        ax.set_ylim(3.1, 4.35)
        method_font_size = 13
    else:
        ax.set_xlim(2.6, 4.4)
        ax.set_ylim(2.6, 4.4)
        method_font_size = 10

    texts = []

    for i, name in enumerate(df.index):
        ax.scatter(df.loc[name, 'faithfulness'], df.loc[name, 'creativity'], c = colors[i], zorder=2)
        texts.append(ax.text(df.loc[name, 'faithfulness'], df.loc[name, 'creativity'], method_names[i], ha='center', va='center', fontsize=method_font_size, c = colors[i]))

    plt.xlabel('Faithfulness', fontsize=20)
    plt.ylabel('Creativity', fontsize=20)
    plt.title(f'Scores for All Methods ({languages[file_index]})', fontsize=20)
    plt.grid(True)

    plt.xticks(fontsize=16)
    plt.yticks(fontsize=16)

    legend_elements = [
        Line2D([0], [0], marker='o', color='w' , lw=0, label='Commercial Translation Engines', markerfacecolor='tab:blue', markeredgecolor='tab:blue'),
        Line2D([0], [0], marker='o', color='w' , lw=0, label='Naive Creativity', markerfacecolor='tab:orange', markeredgecolor='tab:orange'),
        Line2D([0], [0], marker='o', color='w' , lw=0, label='Zero-Shot Creativity', markerfacecolor='tab:green', markeredgecolor='tab:green'),
        Line2D([0], [0], marker='o', color='w' , lw=0, label='Instructed Creativity', markerfacecolor='tab:red', markeredgecolor='tab:red'),
        Line2D([0], [0], marker='o', color='w' , lw=0, label='Few-Shot Creativity', markerfacecolor='tab:purple', markeredgecolor='tab:purple')
    ]

    ax.legend(handles=legend_elements, loc='best', fontsize=13)

    adjust_text(texts)

    plt.tight_layout()
    plt.savefig(f'../../figures/{file_name}.pdf')
    plt.close()

scores_optimal = pd.read_json(f'../../data/processed/chinese_scores_50_optimal.jsonl', lines=True)

faithful = scores_optimal[scores_optimal.aspect == 'faithfulness']
creative = scores_optimal[scores_optimal.aspect == 'creativity']

print('Faithfulness (optimal methods):')
print(faithful.groupby('method', sort=False, as_index=False).agg(score_dict))

print('Creativity (optimal methods):')
print(creative.groupby('method', sort=False, as_index=False).agg(score_dict))

cometkiwi_optimal = pd.read_json(f'../../data/processed/chinese_cometkiwi_50_optimal.jsonl', lines=True)

print('CometKiwi (optimal methods):')
print(cometkiwi_optimal.groupby('method', sort=False, as_index=False).agg(score_dict))

fig, ax = plt.subplots(figsize=(8, 8), dpi=150)

# for x labels
language_aspects = [
    'Chinese (Faithfulness)',
    'Chinese (Creativity)',
    'Japanese (Faithfulness)',
    'Japanese (Creativity)',
    'Korean (Faithfulness)',
    'Korean (Creativity)',
    'Plausible Chinese (Faithfulness)',
    'Plausible Chinese (Creativity)'
]

sns.heatmap(mean_scores,
            vmin=2.6,
            vmax=4.4,
            cmap=sns.color_palette('Blues_d', as_cmap=True).reversed(),
            annot=True,
            xticklabels=language_aspects,
            yticklabels=method_names,
            fmt='0.2f')

ax.set_ylabel('Method', fontsize=16)
ax.set_xlabel('Language (Aspect)', fontsize=16)
ax.set_title('Heat Map of All Scores', fontsize=16)

plt.tight_layout()
plt.savefig(f'../../figures/all_scores.pdf')
plt.close()