"""Fill this repo from your local project folder, then upload the result to GitHub.

Usage (from inside this repo folder):
    python prepare_repo.py /path/to/your/project

It expects, inside that project folder:
    undervalued_stocks_v7.ipynb
    outputs_value_v7/            (tables, camera figures, screen/watchlist)

What it does:
    - copies the notebook to notebook/, replacing any email address with
      "your.email@example.com" and clearing cell outputs that contain one
    - copies CSV/Markdown tables to tables/, camera PNGs to figures/,
      and anything with "screen" or "watchlist" in its name to screen/
    - skips raw data (prices, caches, company facts, parquet/pickle files)
    - warns about any file over 25 MB (GitHub's browser-upload limit)
"""
import json
import re
import shutil
import sys
from pathlib import Path

EMAIL = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")
PLACEHOLDER = "your.email@example.com"
RAW_HINTS = ("price", "yahoo", "yf_", "cache", "companyfacts", "company_facts",
             "raw", "submissions", "xbrl")
RAW_EXT = {".parquet", ".pkl", ".pickle", ".feather", ".h5", ".zip", ".gz", ".json"}
MAX_MB = 25

repo = Path(__file__).resolve().parent
if len(sys.argv) != 2:
    sys.exit(__doc__)
src = Path(sys.argv[1]).expanduser().resolve()
nb_src = src / "undervalued_stocks_v7.ipynb"
out_src = src / "outputs_value_v7"
for p in (nb_src, out_src):
    if not p.exists():
        sys.exit(f"Not found: {p}")


def scrub(text):
    return EMAIL.sub(PLACEHOLDER, text)


# 1. Notebook: scrub emails everywhere, drop outputs that leak one
nb = json.loads(nb_src.read_text(encoding="utf-8"))
for cell in nb.get("cells", []):
    cell["source"] = [scrub(s) for s in cell.get("source", [])] if isinstance(cell.get("source"), list) else scrub(cell.get("source", ""))
    if cell.get("cell_type") == "code":
        outs = json.dumps(cell.get("outputs", []))
        if EMAIL.search(outs):
            cell["outputs"] = json.loads(scrub(outs))
nb_out = repo / "notebook" / nb_src.name
nb_out.write_text(json.dumps(nb, indent=1, ensure_ascii=False), encoding="utf-8")
left = EMAIL.findall(nb_out.read_text(encoding="utf-8"))
left = [e for e in left if e != PLACEHOLDER]
print(f"notebook -> {nb_out.relative_to(repo)}  ({'CLEAN' if not left else 'EMAILS LEFT: ' + ', '.join(set(left))})")

# 2. Outputs
copied, skipped = [], []
for f in sorted(out_src.rglob("*")):
    if not f.is_file():
        continue
    name = f.name.lower()
    rel = f.relative_to(out_src)
    if f.suffix.lower() in RAW_EXT or any(h in str(rel).lower() for h in RAW_HINTS):
        skipped.append(rel)
        continue
    if "screen" in name or "watchlist" in name:
        dest = repo / "screen"
    elif f.suffix.lower() in {".csv", ".md", ".txt"}:
        dest = repo / "tables"
    elif f.suffix.lower() == ".png" and "camera" in str(rel).lower():
        dest = repo / "figures"
    else:
        skipped.append(rel)
        continue
    target = dest / f.name
    if f.suffix.lower() in {".csv", ".md", ".txt"}:
        target.write_text(scrub(f.read_text(encoding="utf-8", errors="replace")), encoding="utf-8")
    else:
        shutil.copy2(f, target)
    copied.append(target.relative_to(repo))

print(f"\ncopied {len(copied)} files:")
for c in copied:
    print("  ", c)
print(f"\nskipped {len(skipped)} files (raw data or not needed):")
for s in skipped:
    print("  ", s)

big = [p for p in repo.rglob("*") if p.is_file() and p.stat().st_size > MAX_MB * 1e6]
total = sum(1 for p in repo.rglob("*") if p.is_file() and ".git" not in p.parts)
print(f"\n{total} files in repo.")
if big:
    print(f"Over {MAX_MB} MB (use GitHub Desktop or git, not the browser):")
    for b in big:
        print("  ", b.relative_to(repo))
if total > 100:
    print("More than 100 files: the browser uploader takes 100 at a time, so upload in batches or use GitHub Desktop.")
print("\nDone. Check figures/ and screen/, then delete prepare_repo.py if you like and upload.")
