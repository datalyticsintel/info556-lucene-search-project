#this is after I created the new enviroment with the correct java and python versions

import argparse
from pyserini.search.lucene import LuceneSearcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str)
    parser.add_argument("--index", default="indexes/tmdb")
    args = parser.parse_args()

    searcher = LuceneSearcher(args.index)

    # Standard BM25 base config
    searcher.set_bm25(k1=0.9, b=0.4)

    # Weighted query: boost the title field
    boosted_query = f"title:({args.query})^2.5 contents:({args.query})"

    print(f"\n[WEIGHTED BM25] Query: {args.query}\n")
    hits = searcher.search(boosted_query, k=10)

    for i, hit in enumerate(hits):
        print(f"{i+1}. DocID={hit.docid}, Score={hit.score}")
        raw = searcher.doc(hit.docid).raw()
        print(raw[:300] + "...\n")

if __name__ == "__main__":
    main()
