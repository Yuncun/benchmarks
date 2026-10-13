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

## SnapJudge v0.2.0

- Model: [scgopi/SnapJudge](https://github.com/scgopi/SnapJudge) v0.2.0, run through its own MLX code on an Apple M5 Max behind a small `/v1/systemone` wrapper. It accepts at most 12 options per question; requests over that are refused and count as wrong, the board's rule.
- Slice run, 2026-10-13: 8 of the 37 public benchmarks (BFCL, Home appliances, GPQA Diamond, WinoGrande, GSM8K, CRUXEval, HLE, New Yorker), 7,496 requests. Files in `snapjudge-slice8/`; `rank_slice.py` re-ranks every board entry on the same 8 benchmarks, output in `ranking-slice8.md`.
- The row on the live page is an estimate until the full run lands. Across the 149 board entries, a linear fit of the public index on the 8-benchmark slice index gives public = 4.98 + 0.887 × slice, residual SD 3.3 points, 90% of entries within 5.4 points. SnapJudge's slice index of 27.3 gives an estimated public index of 29.2. Its area columns on the page are slice-only values for the three areas the slice covers; the other two show a dash. Calibration and answered share are not computed for the slice.
- Full public suite run: scheduled for 2026-10-13; the estimate row is replaced by the measured score when it completes.

## JevBench page

`docs/jevbench.html` shows a snapshot of the live JevBench boards (benchmarkheaven.com/jev-models and /api), parsed from the board pages on the date in `docs/data/jevbench-boards.json`, because the published v1.6.1 feed lags the live board. Microsoft-Decision-1 is measured there by Benchmark Heaven as a hosted API: official rank 6 on the API board by Composite (69.1), Intelligence 57.2, calibration 84.4; a preliminary A2 re-run shows Intelligence 59.2 and is not ranked. Before that measurement was found, an extrapolation from the Decision Index public score through 21 models on both boards gave an estimated Intelligence of 58.9 (range 51 to 66).
