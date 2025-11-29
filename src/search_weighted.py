#so if I did baseline I think this would be the same as search_baseline.py




import json
import argparse
from pyserini.search.lucene import LuceneSearcher

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--index', required=True)
    parser.add_argument('--topics', required=True)
    parser.add_argument('--output', required=True)
    args = parser.parse_args()

    searcher = LuceneSearcher(args.index)
    searcher.set_bm25(k1=0.9, b=0.4)

    # FIELD WEIGHTS – these are tunable
    weights = {
        "title": 3.0,
        "keywords": 2.0,
        "overview": 1.0
    }

    with open(args.topics, 'r') as f:
        topics = json.load(f)

    results = {}

    for qid, query in topics.items():
        # Build weighted multi-field query
        weighted_query = " ".join([
            f"{field}:{query}^{w}" for field, w in weights.items()
        ])

        hits = searcher.search(weighted_query, k=20)
        results[qid] = [
            {
                "docid": hit.docid,
                "score": hit.score,
                "raw": searcher.doc(hit.docid).raw()
            }
            for hit in hits
        ]
        print(f"[Weighted] QID={qid} → {len(hits)} hits")

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved WEIGHTED BM25 results to {args.output}")

if __name__ == "__main__":
    main()
