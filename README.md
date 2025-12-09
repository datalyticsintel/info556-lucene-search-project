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

Place it in the following folder:
    data/raw/
Ensure the file is named:
    TMDB_movie_dataset_v11.csv

Project Structure
Project/
src/
 ├── prepare_tmdb.py      #Cleans & converts raw CSV to JSONL for indexing
 ├── index_tmdb.py     #Builds Lucene index using Pyserini
 ├── search_baseline.py    #BM25 (default) search
 ├── search_tmdb.py      #Alternative variant (if used, used for experiments)
 ├── search_weighted.py    #Weighted BM25 search 
 └── evaluate.py         #Computes Precision@10, MAP, nDCG
  

data/
 ├── raw/   #Original dataset
 └── processed/  #JSONL input to indexer

experiments/
 ├── queries.json   #Search queries
 ├── qrels.json      #Relevance judgments
 └── README_experiments.md

runs/
 ├── bm25_baseline.json    
 ├── bm25_weighted.json    

indexes/  #Lucene index (optional to include, can be regenerated)

requirements.txt
README.md




Installation & Setup
  This project requires:
  Python 3.11
  Java 21 (via Homebrew on macOS)
  Pyserini + Pyjnius

1. Clone the repository
https://github.com/datalyticsintel/info556-lucene-search-project.git


2. Create a virtual environment
python3.11 -m venv .venv311 (this is what I used, you can use conda if you prefer, I was on a M4 Macbook Pro)
source .venv311/bin/activate


3. Install dependencies - Look at requirements below 
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


4. Running the Full Retrieval Pipeline 
Required Java Setup for Pyserini
(Necessary on macOS, especially with M-series chips)
Add these environment variables before indexing or searching:
export JAVA_HOME="/opt/homebrew/opt/openjdk/libexec/openjdk.jdk/Contents/Home"
export JVM_PATH="$JAVA_HOME/lib/server/libjvm.dylib"


5. Running Baseline and Weighted Search
Baseline BM25 Search:
python src/search_baseline.py "space adventure" (space adventure is an example query)

Weights BM25 Search:
python src/search_weighted.py "space adventure" (space adventure is an example query)

Both scripts print:
  docID
  BM25 score
  raw JSONL metadata
  differences in ranking


Evaluation
Evaluation uses:
    Precision@10
    Mean Average Precision (MAP)
    Normalized Discounted Cumulative Gain (NDCG)@10
    Custom queries and relevance judgments (qrels) in experiments/
      experiments/queries.json  
      experiments/qrels.json


Run evaluation foir Baseline:
python src/evaluate.py \
  --qrels experiments/qrels.json \
  --run runs/bm25_baseline.json


Run evaluation for Weighted:
python src/evaluate.py \
  --qrels experiments/qrels.json \
  --run runs/bm25_weighted.json


Preliminary Results
| Query                | Baseline P@10 | Weighted P@10 | Notes                                          |
| -------------------- | ------------- | ------------- | ---------------------------------------------- |
| Q1: Las Vegas movies | 0.60          | 0.40          | Baseline better at broad topical match         |
| Q2: Female leads     | 0.40          | 0.30          | Weighted search over-focuses on title/keywords |
| Q3: Holocaust        | 0.50          | 0.30          | Baseline benefits from long overview fields    |
| Q4: Babies           | 0.50          | **0.00**      | Weighted search fails: sparse keywords         |
| Q5: Brittany Murphy  | 0.50          | 0.40          | Both effective; baseline more consistent       |

| Query                | Baseline P@10 | Weighted P@10 | Notes                                          |
| -------------------- | ------------- | ------------- | ---------------------------------------------- |
| Q1: Las Vegas movies | 0.60          | 0.40          | Baseline better at broad topical match         |
| Q2: Female leads     | 0.40          | 0.30          | Weighted search over-focuses on title/keywords |
| Q3: Holocaust        | 0.50          | 0.30          | Baseline benefits from long overview fields    |
| Q4: Babies           | 0.50          | **0.00**      | Weighted search fails: sparse keywords         |
| Q5: Brittany Murphy  | 0.50          | 0.40          | Both effective; baseline more consistent       |

Interpretation:
  The baseline BM25 model consistently outperforms the weighted variant across all metrics.
  
  Weighted BM25 improves model sensitivity to fields like title and keywords, but:
  It underperforms when metadata is sparse
  It over-amplifies short fields
  It fails dramatically when keywords do not include the semantic concept (e.g., “babies”)

Key takeaway:
Domain weighting can help retrieval only when fields contain rich, reliable signals.
In this dataset, long overview fields contribute more to relevance than boosted short fields.

Users may expand the evaluation by:
    Adjusting BM25 parameters (so thats k1, b)
    Changing field weights
    Adding new queries
    Incorporating additional movie metadata fields

Requeirements
    Python 3.7+
    Pyserini
    Pandas
    NumPy
    argparse
    pyjnius
    java (for Lucene backend)

Recommeded .gitignore
  data/raw/
  data/processed/
  indexes/
  runs/
  .DS_Store
  *.pyc
  __pycache__/

Acknowledgments and References
    TMDb Movie Dataset v11 (2023) - Kaggle
    Pyserini Documentation and example indexing scripts - https://pyserini.io/
    The Anserini/Lucene Indexing and Retrieval Framework 
    Troubleshooting Java environment on macOS with M-series chips
    INFO 556 Course Materials from the University of Arizona