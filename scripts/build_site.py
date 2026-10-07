"""Build the static site data under docs/data/ from the classified papers.

    python3 scripts/build_site.py

Re-run after editing docs/app.js or docs/style.css too: it stamps their
content hashes into docs/index.html.

Outputs
  docs/data/meta.json      taxonomy, areas, statuses, counts
  docs/data/papers.json    one row per paper:
                           [id, number, title, keywords, area_idx, status_idx, [tag_idx...]]
  docs/data/abs/<k>.json   abstracts for rows k*SHARD .. (k+1)*SHARD-1, loaded lazily
"""

import hashlib
import json
import re
import shutil
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "docs" / "data"
SHARD = 500
STATUSES = ["active", "withdrawn", "desk_rejected"]


def dump(path, obj):
    path.write_text(json.dumps(obj, ensure_ascii=False, separators=(",", ":")))


def stamp_assets():
    """Append a content hash to app.js / style.css references so browsers drop stale copies."""
    index = ROOT / "docs" / "index.html"
    html = index.read_text()
    for name in ("app.js", "style.css"):
        digest = hashlib.sha1((ROOT / "docs" / name).read_bytes()).hexdigest()[:10]
        html = re.sub(rf'"{re.escape(name)}(\?v=[0-9a-f]*)?"', f'"{name}?v={digest}"', html)
    index.write_text(html)


def main():
    papers = json.loads((ROOT / "data" / "raw" / "papers.json").read_text())
    assigned = json.loads((ROOT / "data" / "tags.json").read_text())
    taxonomy = json.loads((ROOT / "data" / "taxonomy.json").read_text())

    papers.sort(key=lambda p: (STATUSES.index(p["status"]), p["number"]))

    tags, groups = [], []
    for gi, g in enumerate(taxonomy):
        idx = []
        for t in g["tags"]:
            idx.append(len(tags))
            tags.append(dict(id=t["id"], zh=t["zh"], en=t["en"], g=gi, count=t["count"], includes=t.get("includes", [])))
        groups.append(dict(id=g["id"], zh=g["zh"], en=g["en"], tags=idx))
    tag_index = {t["id"]: i for i, t in enumerate(tags)}
    for t in tags:
        children = [tag_index[c] for c in t.pop("includes")]
        if children:
            t["children"] = children

    area_counts = Counter(p["primary_area"] for p in papers if p["status"] == "active")
    areas = [a for a, _ in area_counts.most_common()]
    areas += sorted({p["primary_area"] for p in papers} - set(areas))
    area_index = {a: i for i, a in enumerate(areas)}

    rows, abstracts = [], []
    for p in papers:
        kws = "; ".join(k.strip() for k in p.get("keywords") or [] if k.strip())
        rows.append([
            p["id"], p["number"], p["title"].strip(), kws,
            area_index[p["primary_area"]], STATUSES.index(p["status"]),
            [tag_index[t] for t in assigned[p["id"]]],
        ])
        abstract = (p.get("abstract") or "").strip()
        if p.get("TLDR"):
            abstract += "\n\nTL;DR: " + p["TLDR"].strip()
        abstracts.append(abstract)

    if OUT.exists():
        shutil.rmtree(OUT)
    (OUT / "abs").mkdir(parents=True)
    dump(OUT / "papers.json", rows)
    for k in range(0, len(abstracts), SHARD):
        dump(OUT / "abs" / f"{k // SHARD}.json", abstracts[k:k + SHARD])

    version = hashlib.sha1((OUT / "papers.json").read_bytes()).hexdigest()[:10]
    status_counts = Counter(p["status"] for p in papers)
    dump(OUT / "meta.json", dict(
        version=version,
        built=date.today().isoformat(),
        total=len(papers),
        statuses=STATUSES,
        statusCounts={s: status_counts[s] for s in STATUSES},
        areas=areas,
        areaCounts=[area_counts[a] for a in areas],
        groups=groups,
        tags=tags,
        shardSize=SHARD,
    ))
    stamp_assets()
    size = sum(f.stat().st_size for f in OUT.rglob("*.json")) / 1e6
    print(f"{len(rows)} papers, {len(tags)} tags, {len(abstracts) // SHARD + 1} abstract shards, {size:.1f} MB total")


if __name__ == "__main__":
    main()
