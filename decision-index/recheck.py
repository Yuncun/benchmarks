#!/usr/bin/env python3
"""Compare a re-run's answers with the published run, row by row.

usage: python3 recheck.py <published results.jsonl[.gz]> <rerun results.jsonl>
"""
import gzip, json, sys

def load(path):
    opener = gzip.open if path.endswith(".gz") else open
    out = {}
    with opener(path, "rt") as f:
        for line in f:
            r = json.loads(line)
            if r.get("status") == "ok":
                out[r["run_id"]] = r["response"]["answers"]
    return out

def pick(a):
    return a.get("choice") if "choice" in a else json.dumps(a.get("value", a), sort_keys=True)

pub, new = load(sys.argv[1]), load(sys.argv[2])
same = total = 0; maxdiff = 0.0
for rid, answers in new.items():
    if rid not in pub:
        continue
    for q, a in answers.items():
        total += 1
        b = pub[rid].get(q, {})
        same += pick(a) == pick(b)
        for k, v in (a.get("probabilities") or {}).items():
            maxdiff = max(maxdiff, abs(v - (b.get("probabilities") or {}).get(k, v)))
print(f"{len(new)} rows re-run, {total} questions compared, {same} identical choices ({100*same/max(total,1):.1f}%), largest probability difference {maxdiff:.4f}")
