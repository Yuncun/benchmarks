#!/usr/bin/env python3
"""Rank runs against every board entry on a subset of public benchmarks.

usage: python3 rank_slice.py --slice 25,28,43,45,30,1,9,64 name=path/to/scores.json [name=... ]

The slice index uses the board's formula (area weights, gold 1.2) restricted to
the chosen benchmarks, with area weights renormalized over the areas present.
"""
import argparse, csv, json, os, statistics

here = os.path.dirname(os.path.abspath(__file__))
ap = argparse.ArgumentParser()
ap.add_argument("--slice", required=True)
ap.add_argument("runs", nargs="*")
args = ap.parse_args()
slice_ids = set(args.slice.split(","))
panel = json.load(open(os.path.join(here, "board-snapshot", "panel.json")))
areas, bmeta = panel["areas"], panel["benchmarks"]

def slice_index(skills):
    tot = wsum = 0.0
    for a in areas.values():
        ids = [b for b in a["benchmarks"] if b in slice_ids]
        if not ids:
            continue
        if any(b not in skills for b in ids):
            return None
        num = sum(bmeta[b]["gold"] * skills[b] for b in ids)
        den = sum(bmeta[b]["gold"] for b in ids)
        tot += a["weight"] * num / den; wsum += a["weight"]
    return 100 * tot / wsum

board, names = {}, {}
for r in csv.DictReader(open(os.path.join(here, "board-snapshot", "board-benchmarks.csv"))):
    board.setdefault(r["engine"], {})[r["benchmark"]] = float(r["skill"]); names[r["engine"]] = r["name"]
full = {r["engine"]: float(r["public"]) for r in csv.DictReader(open(os.path.join(here, "board-snapshot", "board.csv")))}

entries = []
for engine, skills in board.items():
    si = slice_index(skills)
    if si is not None:
        entries.append(dict(name=names[engine], slice=si, public=full.get(engine), mine=False))
for spec in args.runs:
    name, path = spec.split("=", 1)
    s = json.load(open(path))
    skills = {b: v["index_skill"] for b, v in s["benchmarks"].items() if v.get("index_skill") is not None}
    si = slice_index(skills)
    entries.append(dict(name=name, slice=si, public=s["scores"]["balanced_skill"] if s.get("complete") else None, mine=True))
entries.sort(key=lambda e: -e["slice"])

print("Slice: " + ", ".join(bmeta[b]["short"] for b in sorted(slice_ids, key=int)) + f" ({len(slice_ids)} of 37 public benchmarks).\n")
print("| Rank on slice | Model | Slice index | Public index |\n|---|---|---|---|")
mine_pos = [i for i, e in enumerate(entries, 1) if e["mine"]]
for i, e in enumerate(entries, 1):
    if i <= 10 or e["name"] == "Jev" or any(abs(i - p) <= 3 for p in mine_pos):
        n = f"**{e['name']}**" if e["mine"] else e["name"]
        pub = "" if e["public"] is None else f"{e['public']:.1f}"
        print(f"| {i} | {n} | {e['slice']:.1f} | {pub} |")
print(f"\n{len(entries)} entries ranked on the slice.")
# how well the slice reproduces the public ranking, over board entries only
b = [e for e in entries if not e["mine"] and e["public"] is not None]
rs = {e["name"]: i for i, e in enumerate(sorted(b, key=lambda e: -e["slice"]), 1)}
rp = {e["name"]: i for i, e in enumerate(sorted(b, key=lambda e: -e["public"]), 1)}
n = len(b); d = sum((rs[k] - rp[k]) ** 2 for k in rs)
print(f"Across the {n} board entries, slice rank vs public rank: Spearman {1 - 6*d/(n*(n*n-1)):.3f}, median shift {statistics.median(abs(rs[k]-rp[k]) for k in rs):.0f} places.")
