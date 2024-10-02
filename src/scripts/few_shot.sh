#!/bin/bash

cd ../query
nohup python -u translations_few_shot.py -l c > ../../log/translations_chinese_few_shot.out &
nohup python -u translations_few_shot.py -l j > ../../log/translations_japanese_few_shot.out &
nohup python -u translations_few_shot.py -l k > ../../log/translations_korean_few_shot.out &
nohup python -u translations_few_shot.py -l cp > ../../log/translations_chinese_plausible_few_shot.out &