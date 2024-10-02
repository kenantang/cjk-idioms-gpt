#!/bin/bash

cd ../query
nohup python -u paragraph_translations.py -l c > ../../log/paragraph_translations_chinese.out &
nohup python -u paragraph_translations.py -l j > ../../log/paragraph_translations_japanese.out &
nohup python -u paragraph_translations.py -l k > ../../log/paragraph_translations_korean.out &
nohup python -u paragraph_translations.py -l cp > ../../log/paragraph_translations_chinese_plausible.out &