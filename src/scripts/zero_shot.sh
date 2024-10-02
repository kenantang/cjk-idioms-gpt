#!/bin/bash

cd ../query
nohup python -u translations_zero_shot.py -l c > ../../log/translations_chinese_zero_shot.out &
nohup python -u translations_zero_shot.py -l j > ../../log/translations_japanese_zero_shot.out &
nohup python -u translations_zero_shot.py -l k > ../../log/translations_korean_zero_shot.out &
nohup python -u translations_zero_shot.py -l cp > ../../log/translations_chinese_plausible_zero_shot.out &