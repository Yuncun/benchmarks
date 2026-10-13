#!/usr/bin/env python3
"""Tables from the board snapshot plus a run's scores.json.

usage: python3 rank.py full|small|areas <run>/scores.json [run name]
"""
import csv, json, os, sys

here = os.path.dirname(os.path.abspath(__file__))
mode, scores_path = sys.argv[1], sys.argv[2]
name = sys.argv[3] if len(sys.argv) > 3 else "Microsoft-Decision-1"
scores = json.load(open(scores_path))
mine = scores["scores"]["balanced_skill"]

board = list(csv.DictReader(open(os.path.join(here, "board-snapshot", "board.csv"))))
for r in board:
    r["public"] = float(r["public"]); r["full"] = float(r["full"]) if r["full"] else None
    r["params"] = float(r["params"]) if r["params"] else None
rows = board + [{"name": name, "public": mine, "full": None, "params": 9e9, "mine": True}]
rows.sort(key=lambda r: -r["public"])

def line(i, r, params=False):
    n = f"**{r['name']}**" if r.get("mine") else r["name"]
    full = "" if r["full"] is None else f"{r['full']:.1f}"
    p = f" {r['params']/1e9:.1f}B |" if params else ""
    return f"| {i} | {n} |{p} {r['public']:.1f} | {full} | {r.get('notes', '')} |"

if mode == "full":
    print("| Rank | Model | Public index | Full score (board) | Notes |\n|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        print(line(i, r))
elif mode == "small":
    print("| Rank overall | Model | Params | Public index | Full score (board) | Notes |\n|---|---|---|---|---|---|")
    for i, r in enumerate(rows, 1):
        if r["params"] and r["params"] <= 10.5e9:
            print(line(i, r, params=True))
elif mode == "areas":
    areas = {a["id"]: 100 * a["skill"] for a in scores["areas"]}
    ref = {r["name"]: r for r in board}
    cols = [name] + [n for n in ("Jev", "vLLM-SR d3 (27B)", "Cloudflare clef-flash") if n in ref]
    print("| Area | " + " | ".join(cols) + " |\n|---|" + "---|" * len(cols))
    labels = {"knowledge": "Knowledge & Reasoning", "language": "Language Understanding", "retrieval": "Retrieval & Classification", "tools": "Tools & Automation", "arts": "Arts & Human Taste"}
    for k, lab in labels.items():
        print(f"| {lab} | " + " | ".join([f"{areas[k]:.1f}"] + [ref[n].get(f"area_{k}", "") for n in cols[1:]]) + " |")
