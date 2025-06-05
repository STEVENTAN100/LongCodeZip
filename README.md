# LongCodeZip

This repository is the official implementation of LongCodeZip, a novel two-stage long code compression method.


## Method Overview

![Overview](assets/overview.png)

LongCodeZip introduces a two-stage code compression framework specifically designed for code LLMs:

1. **Coarse-grained Compression**: Function-based chunking and ranking using conditional perplexity with respect to the query to select the most relevant functions.

2. **Fine-grained Compression**: Entropy-based block detection combined with 0/1 knapsack optimization to maximize relevance within adaptive token budgets.

The method is plug-and-play and can be integrated with existing code LLMs to achieve significant compression ratios while maintaining or improving task performance.

## Repository Structure

This repository contains implementations and experiments for three code-related tasks:

```
LongCodeZip/
├── repo-qa/                   # Code Retrieval Task
│   ├── main.py               # Main evaluation script
│   ├── run.sh                # Experiment runner
│   ├── code_compressor.py    # Core compression implementation
│   ├── compute_score.py      # Evaluation metrics
│   └── ...
├── long-code-completion/      # Code Completion Task
│   ├── main.py               # Main evaluation script
│   ├── run.sh                # Experiment runner
│   ├── code_compressor.py    # Core compression implementation
│   ├── utils.py              # Utility functions
│   └── ...
├── module-summarization/      # Code Summarization Task
│   ├── main.py               # Main evaluation script
│   ├── run.sh                # Experiment runner
│   ├── code_compressor.py    # Core compression implementation
│   ├── utils.py              # Utility functions
│   └── ...
└── README.md
```

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Quick Start

Each task directory contains a `run.sh` script for easy experimentation. Simply navigate to the desired task directory and run:

```bash
cd <task_directory>
bash run.sh
```

### Code Retrieval (RepoQA)

Navigate to the `repo-qa` directory and run experiments with different compression ratios:

```bash
cd repo-qa
bash run.sh
```

The script will evaluate LongCodeZip on the RepoQA dataset with compression ratios, running experiments in parallel on multiple GPUs.

**Key Parameters:**
- `--compression-ratio`: Controls the compression level
- `--model`: Specifies the base LLM model
- `--backend`: Backend for model inference (vllm)

### Code Completion

Navigate to the `long-code-completion` directory:

```bash
cd long-code-completion
bash run.sh
```

This evaluates LongCodeZip on long-context code completion tasks with various configurations including different target token limits, fine-grained compression ratios, and importance beta values.

**Key Parameters:**
- `--code_compressor_target_token`: Target token budget
- `--code_compressor_fine_ratio`: Fine-grained compression ratio
- `--importance_beta`: Importance weighting parameter

### Code Summarization

Navigate to the `module-summarization` directory:

```bash
cd module-summarization
bash run.sh
```

This runs code summarization experiments with fine-grained compression and various beta values for importance weighting.

**Key Parameters:**
- `--code_compressor_target_token`: Target token budget
- `--code_compressor_fine_ratio`: Fine-grained compression ratio
- `--importance_beta`: Importance weighting parameter

## Configuration

Each task can be customized by modifying the respective `run.sh` file or by directly calling the main scripts with custom parameters. Key configuration options include:

- **Model Selection**: Compatible with various code LLMs (default: Qwen2.5-Coder-7B-Instruct)
- **Compression Ratios**: Adjustable compression levels for different use cases
- **Token Budgets**: Configurable target token limits
- **GPU Configuration**: Multi-GPU support for parallel experiments

## Performance

LongCodeZip achieves up to **5.6× compression ratio** without sacrificing task performance across code completion, summarization, and retrieval tasks. And even when using a 0.5B Qwen model as the compressor, it can also achieve competitive performance.

## Contact

Please feel free to contact us if you have any questions.