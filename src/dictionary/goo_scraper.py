import json
import time

import requests
from bs4 import BeautifulSoup
from tqdm import tqdm

# first, we get all categories and keywords

url = 'https://dictionary.goo.ne.jp/idiom/'

response = requests.get(url)

soup = BeautifulSoup(response.text, 'html.parser')

elements = soup.find_all('a')

# then, we loop over categories and keywords

with open('../../data/external/japanese_idioms_goo.jsonl', 'w', encoding='utf-8') as outfile:

    for element in tqdm(elements):
        url_suffix = element.get('href')

        if url_suffix.startswith('/idiom/category/') or url_suffix.startswith('/idiom/keyword/'):
            url = f'https://dictionary.goo.ne.jp{url_suffix}'

            # limit the scraping frequency
            time.sleep(5)
            response = requests.get(url)

            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')

                idiom_list = soup.find(class_ = 'content_list')

                # to prevent calling find_all on an empty list
                if idiom_list is not None:

                    # the idiom and kana
                    idiom_titles = [i.text.strip() for i in idiom_list.find_all(class_ = 'title')]

                    # the explanation
                    idiom_texts = [i.text.strip() for i in idiom_list.find_all(class_ = 'text')]

                    for title, text in zip(idiom_titles, idiom_texts):
                        entry = {'idiom': title, 'explanation': text}
                        print(json.dumps(entry, ensure_ascii=False), file=outfile)