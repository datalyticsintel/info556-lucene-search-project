
import argparse, json
from pyserini.search.lucene import LuceneSearcher

def baseline_query(text):
    return f'contents:({text})'

def boosted_query(text, wt_title=3.0, wt_kw=2.0, wt_cast=1.5, wt_overview=1.0):
    return f'(title:({text})^{wt_title} OR keywords:({text})^{wt_kw} OR cast:({text})^{wt_cast} OR overview:({text})^{wt_overview})'

def run(searcher, queries, make_query, k=10):
    runs = {}
    for qid, text in queries.items():
        q = make_query(text)
        hits = searcher.search(q, k=k)
        runs[qid] = [(searcher.doc(h.docid).get("id"), h.score) for h in hits]
    return runs

def p_at_k(run, qrels, k=10):
    vals = []
    for qid, hits in run.items():
        rel = set(qrels.get(qid, {}).keys())
        topk = [docid for docid,_ in hits[:k]]
        vals.append(sum(1 for d in topk if d in rel)/len(topk) if topk else 0.0)
    return sum(vals)/len(vals) if vals else 0.0

def map_score(run, qrels):
    aps = []
    for qid, hits in run.items():
        rel = set(qrels.get(qid, {}).keys())
        if not rel: 
            continue
        num_rel = 0
        precs = []
        for i, (docid, _) in enumerate(hits, 1):
            if docid in rel:
                num_rel += 1
                precs.append(num_rel / i)
        aps.append(sum(precs)/len(rel))
    return sum(aps)/len(aps) if aps else 0.0

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--index", required=True)
    ap.add_argument("--queries", required=True)
    ap.add_argument("--qrels", required=True)
    ap.add_argument("--k", type=int, default=10)
    ap.add_argument("--k1", type=float, default=None)
    ap.add_argument("--b", type=float, default=None)
    ap.add_argument("--wt-title", type=float, default=3.0)
    ap.add_argument("--wt-kw", type=float, default=2.0)
    ap.add_argument("--wt-cast", type=float, default=1.5)
    ap.add_argument("--wt-overview", type=float, default=1.0)
    args = ap.parse_args()

    searcher = LuceneSearcher(args.index)
    if args.k1 is not None and args.b is not None:
        searcher.set_bm25(k1=args.k1, b=args.b)

    queries = json.load(open(args.queries, "r", encoding="utf-8"))
    qrels   = json.load(open(args.qrels, "r", encoding="utf-8"))

    base = run(searcher, queries, baseline_query, k=args.k)
    boost = run(searcher, queries, lambda t: boosted_query(
        t, args.wt_title, args.wt_kw, args.wt_cast, args.wt_overview
    ), k=args.k)

    print("\n=== Metrics (k = {}) ===".format(args.k))
    print("Baseline  P@{}: {:.4f}".format(args.k, p_at_k(base, qrels, args.k)))
    print("Boosted   P@{}: {:.4f}".format(args.k, p_at_k(boost, qrels, args.k)))
    print("Baseline   MAP: {:.4f}".format(map_score(base, qrels)))
    print("Boosted    MAP: {:.4f}".format(map_score(boost, qrels)))

    for qid in list(queries.keys())[:3]:
        print(f"\n--- {qid}: {queries[qid]}")
        print("Baseline top:")
        for i,(docid,score) in enumerate(base[qid][:5],1):
            print(f"  {i:>2}. {docid}  {score:.2f}")
        print("Boosted top:")
        for i,(docid,score) in enumerate(boost[qid][:5],1):
            print(f"  {i:>2}. {docid}  {score:.2f}")

if __name__ == "__main__":
    main()

