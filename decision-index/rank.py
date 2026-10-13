#!/usr/bin/env python3
"""Print where a run's public index lands against the board snapshot.

usage: python3 rank.py <run>/scores.json [board-snapshot/board.csv]
"""
import csv, json, sys

scores = json.load(open(sys.argv[1]))
board_path = sys.argv[2] if len(sys.argv) > 2 else "board-snapshot/board.csv"
mine = scores["scores"]["balanced_skill"]
name = "Microsoft-Decision-1 (9B, API)"

board = list(csv.DictReader(open(board_path)))
for r in board:
    r["public"] = float(r["public"]); r["full"] = float(r["full"]) if r["full"] else None
    r["params"] = float(r["params"]) if r["params"] else None
rows = board + [{"name": name, "public": mine, "full": None, "params": 9e9, "mine": True}]
rows.sort(key=lambda r: -r["public"])
pos = next(i for i, r in enumerate(rows, 1) if r.get("mine"))

def fmt(r, i):
    full = "" if r["full"] is None else f"{r['full']:.1f}"
    n = f"**{r['name']}**" if r.get("mine") else r["name"]
    return f"| {i} | {n} | {r['public']:.1f} | {full} |"

print(f"Public index {mine:.2f}: rank {pos} of {len(rows)} by public score.\n")
print("| Rank | Model | Public | Full (board) |\n|---|---|---|---|")
shown = set()
for i, r in enumerate(rows, 1):
    if i <= 10 or abs(i - pos) <= 3 or r["name"] == "Jev":
        print(fmt(r, i)); shown.add(i)
print(f"\n{len(rows) - len(shown)} other entries omitted.\n")

small = [(i, r) for i, r in enumerate(rows, 1) if r["params"] and r["params"] <= 10.5e9]
print("Models of 10B parameters or fewer:\n\n| Rank overall | Model | Params | Public | Full (board) |\n|---|---|---|---|---|")
for i, r in small[:12]:
    full = "" if r["full"] is None else f"{r['full']:.1f}"
    n = f"**{r['name']}**" if r.get("mine") else r["name"]
    print(f"| {i} | {n} | {r['params']/1e9:.1f}B | {r['public']:.1f} | {full} |")
print(f"\n{len(small) - 12} smaller models omitted.")

areas = {a["id"]: 100 * a["skill"] for a in scores["areas"]}
ref = {r["name"]: r for r in board}
cols = [name] + [n for n in ("Jev", "vLLM-SR d3 (27B)", "Cloudflare clef-flash") if n in ref]
print("\nPer area, chance-corrected 0 to 100:\n\n| Area | " + " | ".join(cols) + " |\n|---|" + "---|" * len(cols))
labels = {"knowledge": "Knowledge & Reasoning", "language": "Language Understanding", "retrieval": "Retrieval & Classification", "tools": "Tools & Automation", "arts": "Arts & Human Taste"}
for k, lab in labels.items():
    vals = [f"{areas[k]:.1f}"] + [ref[n].get(f"area_{k}", "") for n in cols[1:]]
    print(f"| {lab} | " + " | ".join(vals) + " |")
