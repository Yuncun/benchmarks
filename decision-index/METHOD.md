# Method

## Microsoft-Decision-1

- Model: `microsoft/microsoft-decision-1` through OpenRouter (Azure endpoint, model tag `microsoft-decision-1-20261009`, 32,768-token context).
- Suite: Decision Index 0.3 public suite, all 140,620 requests, rebuilt from the pinned sources with the maintainer's kit, [apolinario/decision-index](https://github.com/apolinario/decision-index) at commit `f8552a13`, and verified against the published hashes.
- Engine: [`or_engine.py`](or_engine.py), the kit's `http` engine plus the translations listed in `environment.json`. Requests over the model's context limit are recorded as unsupported and count as wrong: 241 requests were rejected, one of them inside a scored subset.
- Scoring: the kit's `score` command, unmodified. Public index 55.39, `complete: true`.
- Cost: about $4 of input tokens. Output tokens are free for this model.
- Latency in the result rows is OpenRouter round-trip time, not comparable to the board's single-GPU latency column.
- Reproducibility: a fresh 300-row sample re-run the same day (`microsoft-decision-1/recheck-300.jsonl`) gave the identical choice on 1,594 of 1,633 questions (97.6%), with probabilities differing by up to 0.19. A re-run will score near 55.4, not exactly on it.

The public index is 20% of the board's Full score. The other 80% is private tests run only by the maintainer, who cannot run an API-only model, so Decision-1 has no Full score and no board entry.

## Checking

1. Re-score: clone the kit at the commit above and run `python -m decision_index score --results microsoft-decision-1/results.jsonl.gz`. It prints `balanced_skill: 55.39`.
2. Confirm the rows are the suite's: every result row carries the request's `run_id` and `payload_sha256`; `suite rebuild` and `suite verify` in the kit produce the same ids and hashes.
3. Re-run rows: `python -m decision_index suite sample --n 300`, then `run --engine or_engine:OpenRouterSystemOne` with an OpenRouter key. `recheck.py` compares the answers with the published file.
4. Each result row carries the OpenRouter generation id for its request.

## Files

| Path | What |
|---|---|
| `microsoft-decision-1/results.jsonl.gz` | all 140,620 result rows: answers, probabilities, token usage, generation id |
| `microsoft-decision-1/scores.json` | the kit's score file: index, areas, every benchmark |
| `microsoft-decision-1/recheck-300.jsonl` | the 300-row re-run |
| `microsoft-decision-1/benchmark-summary.json`, `environment.json` | per-benchmark counts and the engine settings |
| `board-snapshot/board.csv`, `v03.json` | the board's published scores for all 149 entries, 2026-10-12 |
| `rank.py` | builds the README list, `small-models.md` and `areas.md` |
| `recheck.py` | compares a re-run with the published results |
