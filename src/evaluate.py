#same here as the other two for the enviroment

import json
import argparse
import math

def precision_at_k(retrieved, relevant, k=10):
    retrieved_k = retrieved[:k]
    hits = sum(1 for docid in retrieved_k if docid in relevant)
    return hits / k

def average_precision(retrieved, relevant):
    score = 0.0
    hits = 0
    for i, docid in enumerate(retrieved):
        if docid in relevant:
            hits += 1
            score += hits / (i + 1)
    return score / len(relevant) if relevant else 0.0

def ndcg_at_k(retrieved, relevant, k=10):
    dcg = 0.0
    for i, docid in enumerate(retrieved[:k]):
        if docid in relevant:
            dcg += 1 / math.log2(i + 2)

    ideal_hits = min(len(relevant), k)
    idcg = sum(1 / math.log2(i + 2) for i in range(ideal_hits))

    return dcg / idcg if idcg > 0 else 0.0

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qrels", required=True)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()

    with open(args.qrels, "r") as f:
        qrels = json.load(f)
    with open(args.run, "r") as f:
        run = json.load(f)

    print("\n=== Evaluation Results ===\n")

    p10_list, map_list, ndcg10_list = [], [], []

    for qid, query_info in qrels.items():
        relevant = set(query_info["relevant"])

        retrieved = []
        for hit in run.get(qid, []):
            docraw = json.loads(hit["raw"])
            retrieved.append(docraw["id"])  # <-- use TMDB ID from raw JSON

        p10 = precision_at_k(retrieved, relevant, k=10)
        ap = average_precision(retrieved, relevant)
        ndcg10 = ndcg_at_k(retrieved, relevant, k=10)

        p10_list.append(p10)
        map_list.append(ap)
        ndcg10_list.append(ndcg10)

        print(f"QID {qid}:")
        print(f"  Precision@10 = {p10:.4f}")
        print(f"  MAP          = {ap:.4f}")
        print(f"  nDCG@10      = {ndcg10:.4f}\n")

    print("=== Averages ===")
    print(f"Mean Precision@10 = {sum(p10_list)/len(p10_list):.4f}")
    print(f"MAP               = {sum(map_list)/len(map_list):.4f}")
    print(f"Mean nDCG@10      = {sum(ndcg10_list)/len(ndcg10_list):.4f}")

if __name__ == "__main__":
    main()
