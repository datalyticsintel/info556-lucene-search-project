




import argparse, subprocess, sys, os



def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--input-dir", required=True)
    ap.add_argument("--index", required=True)
    args = ap.parse_args()

    os.makedirs(args.index, exist_ok=True)
    cmd = [
        sys.executable, "-m", "pyserini.index",
        "-collection", "JsonCollection",
        "-generator", "DefaultLuceneDocumentGenerator",
        "-input", args.input_dir,
        "-index", args.index,
        "-storePositions", "-storeDocvectors", "-storeRaw"
    ]
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)





if __name__ == "__main__":
    main()

