#!/bin/bash

cd ../query
nohup python -u scores.py -i ../../data/processed/chinese_translations_50_zero_shot.jsonl \
                          -o ../../data/raw/chinese_scores_50_zero_shot_raw.jsonl \
                          > ../../log/scores_chinese_zero_shot.out &
nohup python -u scores.py -i ../../data/processed/japanese_translations_50_zero_shot.jsonl \
                          -o ../../data/raw/japanese_scores_50_zero_shot_raw.jsonl \
                          > ../../log/scores_japanese_zero_shot.out &
nohup python -u scores.py -i ../../data/processed/korean_translations_50_zero_shot.jsonl \
                          -o ../../data/raw/korean_scores_50_zero_shot_raw.jsonl \
                          > ../../log/scores_korean_zero_shot.out &
nohup python -u scores.py -i ../../data/processed/chinese_plausible_translations_50_zero_shot.jsonl \
                          -o ../../data/raw/chinese_plausible_scores_50_zero_shot_raw.jsonl \
                          > ../../log/scores_chinese_plausible_zero_shot.out &