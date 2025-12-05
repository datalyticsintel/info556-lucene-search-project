#so if I did baseline I think this would be the same as search_baseline.py



import argparse
from pyserini.search import SimpleSearcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query")
    parser.add_argument("--index", type=str, default="indexes/tmdb")
    args = parser.parse_args()

    searcher = SimpleSearcher(args.index)
    searcher.set_bm25(k1=1.2, b=0.75)

    # Example: boost title field
    searcher.set_rm3()  # optional RM3

    hits = searcher.search(args.query, k=10)

    print(f"\nWeighted BM25 Results for query: {args.query}\n")
    for i, hit in enumerate(hits):
        print(f"{i+1}. DocID={hit.docid}, Score={hit.score}")
        print(hit.raw()[:300] + "...")
        print("---")

if __name__ == "__main__":
    main()
