#This is where I preapred the tmdb data for indexing


import argparse, json, pandas as pd, ast, re

def as_list(val):
    """Convert TMDB-like string/list/dict fields to a clean Python list of strings."""
    if val is None:
        return []
    s = str(val).strip()
    if not s or s.lower() in {"nan", "none"}:
        return []

    # Try to parse as Python literal (e.g., TMDB's '[{"name": "Action"}]')
    try:
        obj = ast.literal_eval(s)
        if isinstance(obj, list):
            out = []
            for item in obj:
                if isinstance(item, dict) and "name" in item:
                    out.append(str(item["name"]))
                else:
                    out.append(str(item))
            return out
    except Exception:
        pass

    # Fallback: treat it as a pipe/comma separated list
    parts = re.split(r"[|,;/]", s)
    return [p.strip() for p in parts if p.strip()]


def choose_col(df, candidates, default=None):
    """Pick the first matching column from a list of possible names."""
    for c in candidates:
        if c in df.columns:
            return c
        for col in df.columns:
            if col.lower() == c.lower():
                return col
    return default


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--csv", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--max-cast", type=int, default=8)
    args = ap.parse_args()

    df = pd.read_csv(args.csv, low_memory=False)

    # Column mapping
    id_col       = choose_col(df, ["id", "tmdb_id", "movie_id", "movieId"])
    title_col    = choose_col(df, ["title", "original_title", "movie_title"])
    overview_col = choose_col(df, ["overview", "description", "plot", "synopsis"])
    keywords_col = choose_col(df, ["keywords", "tags", "tagline"])
    cast_col     = choose_col(df, ["cast", "actors", "top_cast", "cast_names"])
    genres_col   = choose_col(df, ["genres", "genre", "genre_names"])

    if id_col is None or title_col is None:
        raise SystemExit(
            f"Could not find id/title columns. Found: {list(df.columns)[:30]} ..."
        )

    with open(args.out, "w", encoding="utf-8") as fout:
        for _, row in df.iterrows():
            # --- FIX: cast ID to integer ---
            mid_raw = row.get(id_col)
            try:
                mid = int(mid_raw)
            except Exception:
                continue  # skip rows with bad IDs

            title = str(row.get(title_col, "") or "").strip()
            overview = str(row.get(overview_col, "") or "").strip() if overview_col else ""

            kws = []
            if keywords_col:
                kws += as_list(row.get(keywords_col))
            if genres_col:
                kws += as_list(row.get(genres_col))

            cast_list = as_list(row.get(cast_col))[:args.max_cast] if cast_col else []

            # Build combined searchable content
            doc = {
                "id": mid,                         # ← INTEGER NOW (IMPORTANT)
                "title": title,
                "overview": overview,
                "keywords": " ".join(kws),
                "cast": " ".join(cast_list),
                "contents": " ".join(
                    x for x in [title, " ".join(kws), overview, " ".join(cast_list)]
                    if x
                )
            }

            fout.write(json.dumps(doc, ensure_ascii=False) + "\n")

    print(f"Wrote {args.out}")


if __name__ == "__main__":
    main()

