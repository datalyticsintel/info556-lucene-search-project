#same here as the other two for the enviroment

import json
import argparse
import math

# -----------------------------
# Utility functions
# -----------------------------

def precision_at_k(relevant, retrieved, k=10):
    retrieved_k = retrieved[:k]
    num_rel = sum(1 for d in retrieved_k if d in relevant)
    return num_rel / k

def average_precision(relevant, retrieved):
    hits = 0
    sum_prec = 0
    for i, docid in enumerate(retrieved, start=1):
        if docid in relevant:
            hits += 1
            sum_prec += hits / i
    return sum_prec / len(relevant) if relevant else 0

def dcg(scores):
    return sum(rel / math.log2(i + 2) for i, rel in enumerate(scores))

def ndcg_at_k(relevant, retrieved, k=10):
    retrieved_k = retrieved[:k]
    rel_scores = [1 if d in relevant else 0 for d in retrieved_k]

    dcg_val = dcg(rel_scores)

    ideal = sorted(rel_scores, reverse=True)
    idcg_val = dcg(ideal)

    return dcg_val / idcg_val if idcg_val > 0 else 0

# -----------------------------
# Main evaluation
# -----------------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--qrels", required=True)
    parser.add_argument("--run", required=True)
    args = parser.parse_args()

    # Load qrels
    with open(args.qrels, "r") as f:
        qrels = json.load(f)

    # Load run results
    with open(args.run, "r") as f:
        run = json.load(f)

    print("\n=== Evaluation Results ===\n")
    map_total = 0
    ndcg_total = 0
    p10_total = 0
    num_queries = len(qrels)

    for qid, rel_docs in qrels.items():
        rel_set = set(rel_docs["relevant"])  # list of docids
        retrieved = [hit["docid"] for hit in run[qid]]

        p10 = precision_at_k(rel_set, retrieved, k=10)
        ap = average_precision(rel_set, retrieved)
        ndcg = ndcg_at_k(rel_set, retrieved, k=10)

        p10_total += p10
        map_total += ap
        ndcg_total += ndcg

        print(f"QID {qid}:")
        print(f"  Precision@10 = {p10:.4f}")
        print(f"  MAP          = {ap:.4f}")
        print(f"  nDCG@10      = {ndcg:.4f}\n")

    print("=== Averages ===")
    print(f"Mean Precision@10 = {p10_total / num_queries:.4f}")
    print(f"MAP               = {map_total / num_queries:.4f}")
    print(f"Mean nDCG@10      = {ndcg_total / num_queries:.4f}")

if __name__ == "__main__":
    main()
