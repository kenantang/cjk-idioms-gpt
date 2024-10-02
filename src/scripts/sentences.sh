#!/bin/bash

cd ../query
nohup python -u sentences.py -l c -n 50 > ../../log/sentences_chinese_50.out &
nohup python -u sentences.py -l c -n more > ../../log/sentences_chinese_more.out &
nohup python -u sentences.py -l j -n 50 > ../../log/sentences_japanese_50.out &
nohup python -u sentences.py -l j -n more > ../../log/sentences_japanese_more.out &
nohup python -u sentences.py -l k -n 50 > ../../log/sentences_korean_50.out &
nohup python -u sentences.py -l k -n more > ../../log/sentences_korean_more.out &
nohup python -u sentences.py -l cp -n 50 > ../../log/sentences_chinese_plausible_50.out &