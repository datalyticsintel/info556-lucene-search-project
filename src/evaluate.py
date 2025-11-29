#same here as the other two for the enviroment

import json
import argparse

def precision_at_k(retrieved, relevant, k=10):
    if k > len(retrieved):
        k = len(retrieved)
    retrieved_at_k = set(retrieved[:k])
    return len(retrieved_at_k & relevant) / k

def map_score(retrieved, relevant):
    score = 0.0
    hits = 0
    for i, docid in enumerate(retrieved):
        if docid in relevant:
            hits += 1
            score += hits / (i + 1)
    if len(relevant) == 0:
        return 0
    return score / len(relevant)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qrels", required=True)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()

    with open(args.qrels, 'r') as f:
        qrels = json.load(f)

    with open(args.run, 'r') as f:
        run = json.load(f)

    print(f"Evaluating: {args.run}\n")

    for qid, relevant_docs in qrels.items():
        retrieved = [hit["docid"] for hit in run[qid]]
        relevant = set(relevant_docs)

        p10 = precision_at_k(retrieved, relevant, k=10)
        ap = map_score(retrieved, relevant)

        print(f"Query {qid}:")
        print(f"  P@10 = {p10:.4f}")
        print(f"  MAP  = {ap:.4f}\n")

if __name__ == "__main__":
    main()
