#same here as the other two for the enviroment

import json
import argparse

def precision_at_k(retrieved, relevant, k=10):
    retrieved_k = retrieved[:k]
    return sum(1 for d in retrieved_k if d in relevant) / k

def average_precision(retrieved, relevant):
    score = 0.0
    hits = 0
    for i, docid in enumerate(retrieved, start=1):
        if docid in relevant:
            hits += 1
            score += hits / i
    if len(relevant) == 0:
        return 0.0
    return score / len(relevant)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--qrels", required=True)
    ap.add_argument("--run", required=True)
    args = ap.parse_args()

    with open(args.qrels) as f:
        qrels = json.load(f)

    with open(args.run) as f:
        run = json.load(f)

    print(f"\nEvaluating: {args.run}\n")

    for qid in qrels:
        true_rels = set(int(x) for x in qrels[qid]["relevant"])

        # FIX: convert run docIDs to int
        retrieved = []
        for hit in run[qid]:
            try:
                docid = int(hit["docid"])
                retrieved.append(docid)
            except:
                continue

        p10 = precision_at_k(retrieved, true_rels, k=10)
        map_ = average_precision(retrieved, true_rels)

        print(f"Query {qid}:")
        print(f"  P@10 = {p10:.4f}")
        print(f"  MAP  = {map_:.4f}\n")


if __name__ == "__main__":
    main()
