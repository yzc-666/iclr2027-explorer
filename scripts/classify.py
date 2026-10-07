"""Assign fine-grained topic tags to ICLR 2027 submissions.

    python3 scripts/classify.py                  # tag everything, write outputs
    python3 scripts/classify.py --sample opd 20  # print random titles for a tag
"""

import argparse
import json
import os
import random
import re
from collections import Counter
from multiprocessing import Pool
from pathlib import Path

from taxonomy import TAXONOMY

ROOT = Path(__file__).resolve().parent.parent
RAW = ROOT / "data" / "raw" / "papers.json"
OUT_TAGS = ROOT / "data" / "tags.json"
OUT_TAXONOMY = ROOT / "data" / "taxonomy.json"
OUT_REPORT = ROOT / "CATEGORIES.md"


def compile_rule(rule):
    rx = []
    if rule["pat"]:
        rx.append(re.compile(rule["pat"], re.I))
    if rule["acr"]:
        rx.append(re.compile(rule["acr"]))
    ctx = re.compile(rule["ctx"], re.I) if rule["ctx"] else None
    return dict(rule, rx=rx, ctx_rx=ctx)


def hit(regexes, head, body, min_abs):
    if any(r.search(head) for r in regexes):
        return True
    if min_abs > 50:
        return False
    n = 0
    for r in regexes:
        for _ in r.finditer(body):
            n += 1
            if n >= min_abs:
                return True
    return False


def rule_fires(rule, head, body, area, fired=frozenset()):
    if rule["include"]:
        return any(t in fired for t in rule["include"])
    if rule["areas"] is not None and area not in rule["areas"]:
        return False
    if rule["rx"] and not hit(rule["rx"], head, body, rule["min_abs"]):
        return False
    if rule["ctx_rx"] and not hit([rule["ctx_rx"]], head, body, rule["ctx_min"]):
        return False
    return True


def paper_text(p):
    kws = p.get("keywords") or []
    head = p["title"] + " | " + " ; ".join(kws)
    body = (p.get("abstract") or "") + " " + (p.get("TLDR") or "")
    return head, body


def load_tags():
    tags = []
    for group in TAXONOMY:
        for tag_id, zh, en, rules in group["tags"]:
            tags.append(dict(id=tag_id, group=group["id"], zh=zh, en=en, rules=[compile_rule(r) for r in rules]))
    ids = [t["id"] for t in tags]
    dupes = [i for i, c in Counter(ids).items() if c > 1]
    assert not dupes, f"duplicate tag ids: {dupes}"
    umbrella = {t["id"] for t in tags if any(r["include"] for r in t["rules"])}
    for t in tags:
        for r in t["rules"]:
            for inc in r["include"] or []:
                assert inc in ids and inc not in umbrella, f"{t['id']} includes invalid tag {inc}"
    return tags


_TAGS = None


def _init_worker():
    global _TAGS
    _TAGS = load_tags()


def _classify_chunk(chunk):
    out = {}
    for p in chunk:
        head, body = paper_text(p)
        area = p.get("primary_area")
        fired = {t["id"] for t in _TAGS if any(rule_fires(r, head, body, area) for r in t["rules"] if not r["include"])}
        fired |= {t["id"] for t in _TAGS if any(rule_fires(r, head, body, area, fired) for r in t["rules"] if r["include"])}
        out[p["id"]] = [t["id"] for t in _TAGS if t["id"] in fired]
    return out


def classify(papers):
    chunks = [papers[i:i + 500] for i in range(0, len(papers), 500)]
    out = {}
    with Pool(max(1, (os.cpu_count() or 2) - 1), initializer=_init_worker) as pool:
        for part in pool.imap_unordered(_classify_chunk, chunks):
            out.update(part)
    return {p["id"]: out[p["id"]] for p in papers}


def write_outputs(papers, tags, assigned):
    active = [p for p in papers if p["status"] == "active"]
    counts = Counter(t for p in active for t in assigned[p["id"]])
    group_counts = Counter()
    by_group = {}
    for t in tags:
        by_group.setdefault(t["group"], []).append(t)
    for p in active:
        groups = {t["group"] for t in tags if t["id"] in set(assigned[p["id"]])}
        group_counts.update(groups)

    OUT_TAGS.write_text(json.dumps(assigned, ensure_ascii=False, separators=(",", ":")))

    taxonomy = [
        dict(
            id=g["id"], zh=g["zh"], en=g["en"], count=group_counts[g["id"]],
            tags=[
                dict(id=t["id"], zh=t["zh"], en=t["en"], count=counts[t["id"]],
                     includes=[inc for r in t["rules"] for inc in r["include"] or []])
                for t in by_group[g["id"]]
            ],
        )
        for g in TAXONOMY
    ]
    OUT_TAXONOMY.write_text(json.dumps(taxonomy, ensure_ascii=False, indent=1))

    untagged = sum(1 for p in active if not assigned[p["id"]])
    per_paper = [len(assigned[p["id"]]) for p in active]
    lines = [
        "# ICLR 2027 投稿分类统计",
        "",
        f"有效投稿 {len(active):,} 篇（另有撤稿 {sum(p['status'] == 'withdrawn' for p in papers)}、"
        f"desk reject {sum(p['status'] == 'desk_rejected' for p in papers)}，不计入下表）。"
        f"每篇平均 {sum(per_paper) / len(per_paper):.1f} 个标签，未命中任何标签 {untagged:,} 篇"
        f"（{untagged / len(active):.1%}）。标签可重叠，所以各标签数量之和大于论文总数。",
        "",
        "## 一级：OpenReview primary area（作者自选）",
        "",
        "| Primary area | 篇数 |",
        "|---|---:|",
    ]
    for area, n in Counter(p["primary_area"] for p in active).most_common():
        lines.append(f"| {area} | {n:,} |")
    lines += ["", "## 二级：细分标签（规则匹配，见 `scripts/taxonomy.py`）", ""]
    for g in taxonomy:
        lines += [f"### {g['zh']}（{g['en']}）— {g['count']:,} 篇", "", "| 标签 | English | 篇数 |", "|---|---|---:|"]
        for t in sorted(g["tags"], key=lambda t: -t["count"]):
            lines.append(f"| {t['zh']} | {t['en']} | {t['count']:,} |")
        lines.append("")
    OUT_REPORT.write_text("\n".join(lines))
    return counts, untagged


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", nargs=2, metavar=("TAG", "N"))
    ap.add_argument("--seed", type=int, default=0)
    args = ap.parse_args()

    papers = json.loads(RAW.read_text())
    tags = load_tags()

    if args.sample:
        assigned = json.loads(OUT_TAGS.read_text())
        n = int(args.sample[1])
        for tag_id in args.sample[0].split(","):
            tag = next(t for t in tags if t["id"] == tag_id)
            matched = [p for p in papers if p["status"] == "active" and tag_id in assigned[p["id"]]]
            random.Random(args.seed).shuffle(matched)
            print(f"\n== {tag_id}: {len(matched)} papers")
            for p in matched[:n]:
                head, body = paper_text(p)
                why = next((m.group(0) for r in tag["rules"] for rx in r["rx"] for m in [rx.search(head) or rx.search(body)] if m), "area")
                print(f"  - {p['title'][:110]}  <{why}>")
        return

    assigned = classify(papers)
    counts, untagged = write_outputs(papers, tags, assigned)
    print(f"{len(papers)} papers, {len(tags)} tags, untagged active: {untagged}")
    for t in tags:
        print(f"{t['group']:>10} {t['id']:<20} {counts[t['id']]:>6}")


if __name__ == "__main__":
    main()
