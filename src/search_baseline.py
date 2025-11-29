#this is after I created the new enviroment with the correct java and python versions

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

    with open(args.topics, 'r') as f:
        topics = json.load(f)

    results = {}

    for qid, query in topics.items():
        hits = searcher.search(query, k=20)
        results[qid] = [
            {
                "docid": hit.docid,
                "score": hit.score,
                "raw": searcher.doc(hit.docid).raw()
            }
            for hit in hits
        ]
        print(f"[Baseline] QID={qid} → {len(hits)} hits")

    with open(args.output, "w") as f:
        json.dump(results, f, indent=2)

    print(f"\nSaved baseline BM25 results to {args.output}")

if __name__ == "__main__":
    main()
