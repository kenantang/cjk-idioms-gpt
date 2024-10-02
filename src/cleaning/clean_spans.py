import json

import matplotlib.pyplot as plt
import nltk
import numpy as np
import pandas as pd
import seaborn as sns
from matplotlib.colors import ListedColormap
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

data = pd.read_json('../../data/raw/chinese_spans_50_optimal_raw.jsonl', lines=True)

total = 0
total_span_in_translation = 0

for _, row in data.iterrows():
    translation = row.translation
    span = row.response

    if span in translation:
        total_span_in_translation += 1
    else:
        print(translation)
        print(span)

    total += 1

print(f'For {total_span_in_translation} out of {total} translations, the extracted span appears in the translation.')

# analysis of unigram saturation
fig, ax = plt.subplots(figsize=(8, 6), dpi=150)

# for recoloring
lines = []
unique_unigram_each_idiom = []

for idiom in data.idiom.unique():
    data_single_idiom = data[data.idiom == idiom]

    unique_unigrams = dict()
    unique_unigram_counts = []

    for _, row in data_single_idiom.iterrows():
        span = row.response

        words = word_tokenize(span)

        stop_words = set(stopwords.words('english'))

        filtered_words = [word.lower() for word in words if word.lower() not in stop_words]

        for word in filtered_words:
            if word in unique_unigrams:
                unique_unigrams[word] += 1
            else:
                unique_unigrams[word] = 1

        unique_unigram_counts.append(len(unique_unigrams))

    print(idiom, unique_unigram_counts[-1])

    unique_unigram_each_idiom.append(unique_unigram_counts[-1])

    num_translations = range(1, len(unique_unigram_counts) + 1)
    line, = ax.plot(num_translations, unique_unigram_counts)
    lines.append(line)

sorted_indices = np.argsort(unique_unigram_each_idiom)
blues_d = sns.color_palette("Blues_d", len(sorted_indices))
blues_d.reverse()
cmap = ListedColormap(blues_d)

for rank, index in enumerate(sorted_indices):
    lines[index].set_color(cmap(rank))

ax.set_xlabel('Number of Translations', fontsize=20)
ax.set_ylabel('Number of Unique Unigrams', fontsize=20)
ax.set_title('Unigram Saturation', fontsize=20)

ax.set_xlim(0, 40)
ax.set_ylim(0, 90)

plt.xticks(fontsize=16)
plt.yticks(fontsize=16)

plt.tight_layout()
plt.savefig('../../figures/unigram_saturation.pdf')
plt.close()