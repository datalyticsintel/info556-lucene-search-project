Improving Search Quality with Domain-Specific Weighting in Lucene
INFO 556 — Information Retrieval
Fall 2025
Author: Antonio Escalante Jr.

Overview
This project explores how domain-specific weighting of text fields can improve search quality within Lucene-based retrieval systems. Standard BM25 implementations often rely on a single combined text field, which can unintentionally overweight long descriptions while underweighting concise but informative fields such as titles or keywords.

To address this, the project compares:

Baseline BM25 using a single unified contents field
A multi-field, boosted approach where title, keywords, cast, and overview receive different weights during retrieval

The goal is to determine whether carefully tuning field weights leads to better top-rank relevance, improved precision, and more intuitive search results—particularly for movie and TV metadata.


Dataset
    The dataset used in this project is a TMDb-style metadata collection obtained from Kaggle.
    It includes fields such as: title, overview, keywords, genres, and cast
    Due to size restrictions, the dataset is not included in this repository.

To reproduce the experiments:

Download:
TMDB Movie Dataset v11 (2023)
https://www.kaggle.com/datasets/asaniczka/tmdb-movies-dataset-2023-930k-movies
Place it in the following folder (create it if necessary):
    data/raw/
Ensure the file is named:
    TMDB_movie_dataset_v11.csv
Project Structure
Project/
│
├── src/
│   ├── prepare_tmdb.py        # Preprocess CSV → JSONL for Lucene
│   ├── index_tmdb.py          # Build Lucene index via Pyserini
│   └── search_tmdb.py         # Run baseline vs boosted ranking experiments
│
├── experiments/
│   ├── queries.json           # Search queries for evaluation
│   └── qrels.json             # Relevance judgments (to be populated)
│
├── data/
│   ├── raw/                   # Kaggle dataset goes here (not tracked in Git)
│   └── processed/             # Generated JSONL documents (not tracked in Git)
│
├── indexes/                   # Lucene index (not tracked in Git)
├── results/                   # Evaluation output, charts, tables
├── .gitignore
└── README.md




Installation & Setup
1. Create a virtual environment
python3 -m venv .venv (this is what I used, you can use conda if you prefer, I was on a M4 Macbook Pro)
source .venv/bin/activate

2. Install dependencies
pip install --upgrade pip
pip install pyserini pandas numpy

Usage

1. Preprocess the dataset
Converts the CSV dataset into JSONL documents suitable for multi-field Lucene indexing.
python src/prepare_tmdb.py \
  --csv data/raw/TMDB_movie_dataset_v11.csv \
  --out data/processed/tmdb_docs.jsonl

2. Build the Lucene index
python src/index_tmdb.py \
  --input-dir data/processed \
  --index indexes/tmdb

3. Run search experiments
Runs baseline BM25 and boosted multi-field queries:
python src/search_tmdb.py \
  --index indexes/tmdb \
  --queries experiments/queries.json \
  --qrels experiments/qrels.json \
  --k 10





Evaluation
Evaluation uses:
    Precision@k
    Mean Average Precision (MAP)
    Side-by-side comparison of top-ranked results for baseline vs boosted retrieval
    Manual relevance judgments (stored in qrels.json once you populate them)

Users may expand the evaluation by:
    Adjusting BM25 parameters (so thats k1, b)
    Changing field weights
    Adding new queries
    Incorporating additional movie metadata fields