#this is after I created the new enviroment with the correct java and python versions

import argparse
from pyserini.search import SimpleSearcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("query", type=str, help="Search query string")
    parser.add_argument("--index", type=str, default="indexes/tmdb", help="Path to Lucene index")
    args = parser.parse_args()

    searcher = SimpleSearcher(args.index)
    searcher.set_analyzer("english")

    hits = searcher.search(args.query, k=10)

    print(f"\nTop results for query: {args.query}\n")
    for i, hit in enumerate(hits):
        print(f"{i+1}. DocID={hit.docid}, Score={hit.score}")
        print(hit.raw()[:300] + "...")
        print("---")

if __name__ == "__main__":
    main()
