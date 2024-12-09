# Creative and Context-Aware Translation of East Asian Idioms with GPT-4

This repository contains the code and data for our paper on creative idiom translation. The paper has been accepted by both [EMNLP 2024 Findings](https://aclanthology.org/2024.findings-emnlp.544/) and [the Eleventh Workshop on Asian Translation (WAT 2024)](https://aclanthology.org/2024.wat-1.1/).


## Paper

You can find the preprint version of the paper in [this repository](paper.pdf), on [arXiv](https://arxiv.org/abs/2410.00988), or in [ACL Anthology](https://aclanthology.org/2024.findings-emnlp.544/).

## Source Code

You can find the source code in the [src](src) folder. The workflow to reproduce our results is summarized in [workflow.pdf](workflow.pdf).

## Data

All the data that we generated can be found in [data/data.tgz](data/data.tgz). To reproduce our results, you would also need to download external data from the sources mentioned in our paper.

[12/09/24] We used Llama-3.3-70B-Instruct to [annotate](src/query/spans_llama.py) the [spans](data/chinese_spans_500_optimal_raw.jsonl) for 20000 translations of 500 Chinese idioms. Qualitatively, the annotation result is comparable to gpt-4-0125-preview and much better than gpt-3.5-turbo.

## Examples

Translation examples can be found in our [paper](https://arxiv.org/abs/2410.00988) or our interative [demo](https://kenantang.github.io/cjk-idioms-gpt).

## Citation

If you find our work useful, please consider citing [our paper](https://aclanthology.org/2024.findings-emnlp.544/):

```BibTeX
@inproceedings{tang-etal-2024-creative,
    title = "Creative and Context-Aware Translation of {E}ast {A}sian Idioms with {GPT}-4",
    author = "Tang, Kenan  and
      Song, Peiyang  and
      Qin, Yao  and
      Yan, Xifeng",
    editor = "Al-Onaizan, Yaser  and
      Bansal, Mohit  and
      Chen, Yun-Nung",
    booktitle = "Findings of the Association for Computational Linguistics: EMNLP 2024",
    month = nov,
    year = "2024",
    address = "Miami, Florida, USA",
    publisher = "Association for Computational Linguistics",
    url = "https://aclanthology.org/2024.findings-emnlp.544",
    doi = "10.18653/v1/2024.findings-emnlp.544",
    pages = "9285--9305"
}
```