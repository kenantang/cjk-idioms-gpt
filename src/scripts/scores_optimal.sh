#!/bin/bash

cd ../query
nohup python -u scores.py -i ../../data/processed/chinese_translations_50_optimal.jsonl \
                          -o ../../data/raw/chinese_scores_50_optimal_raw.jsonl \
                          > ../../log/scores_chinese_optimal.out &