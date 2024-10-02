import glob
import json
import os
import time


# ChatGPT generated
def read_and_split(directory, suffix, sep='<sep>'):
    # Construct the full path pattern for files with a given suffix
    pattern = os.path.join(directory, f'*{suffix}')

    # List to hold all the results
    all_results = []

    # Iterate over all files with the given suffix in the directory
    for file_path in sorted(glob.glob(pattern)):
        with open(file_path, 'r') as file:
            # Read and split each line in the file
            for line in file:
                split_line = line.strip('\n').split(sep)
                all_results += split_line

    return all_results

directory = '../../data/external/BWB_train'
chinese = read_and_split(directory, '.chs')
english = read_and_split(directory, '.enu')

with open('../../data/external/petci_filtered.json', 'r') as f:
    petci = json.load(f)

idioms = [i['chinese'] for i in petci]

outfile = open('../../data/processed/chinese_parallel_corpus.jsonl', 'a', encoding='utf-8')

start = time.time()

for idiom in idioms:
    results = [{'idiom': idiom, 'chinese': c, 'english': e} for c, e in zip(chinese, english) if idiom in c]

    print(idiom, len(results), f'{time.time() - start:.2f}')

    for entry in results:
        print(json.dumps(entry, ensure_ascii=False), file=outfile, flush=True)

outfile.close()