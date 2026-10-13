# benchmarks

Notes and run files for benchmarking decision models (fixed-option questions in, calibrated probabilities out).

## Microsoft-Decision-1 on the Jev Decision Index public suite

Run date: 2026-10-13. Suite: Decision Index 0.3 public suite, all 140,620 requests, scored with the maintainer's kit. Board snapshot: Decision Index 0.3.2, generated 2026-10-12.

Public index 55.39: rank 34 of 150 by public score.

| Rank | Model | Public | Full (board) |
|---|---|---|---|
| 1 | RSI-Jev v6.1 VL 27B (effort auto) | 65.6 | 58.7 |
| 2 | vLLM-SR d3 (27B) | 65.5 | 66.3 |
| 3 | Torchcast Decision 27B | 65.1 | 59.9 |
| 4 | Decider 31B (NVFP4) | 64.3 | 64.6 |
| 5 | Matilda Jev v1.5 | 63.5 | 59.2 |
| 6 | Darwin-27B-ZTC | 62.6 | 62.5 |
| 7 | Perplexity Decider v1.1 (27B) | 62.2 | 62.8 |
| 8 | Cloudflare clef | 61.7 | 53.1 |
| 9 | Quyet-1.0-Large | 60.8 | 58.7 |
| 10 | Sieve 27B | 60.0 | 60.2 |
| 20 | Jev | 58.0 | 60.1 |
| 31 | Cloudflare clef-omni (30B-A3B) | 56.5 | 48.3 |
| 32 | Cloudflare clef-flash | 56.1 | 47.6 |
| 33 | simple-jev · Qwen3.8-27B (featherless) | 56.0 | 51.8 |
| 34 | **Microsoft-Decision-1 (9B, API)** | 55.4 |  |
| 35 | frontier-infra Jebadiah 27B | 55.1 | 55.6 |
| 36 | vLLM-SR d3-mini (4B) | 54.9 | 52.6 |
| 37 | JEV-27B | 53.6 | 55.6 |

132 other entries omitted.

Models of 10B parameters or fewer:

| Rank overall | Model | Params | Public | Full (board) |
|---|---|---|---|---|
| 18 | Nace.AI Drex v1.5 | 8.9B | 58.1 | 49.7 |
| 22 | vLLM-SR d3-flash (9B) | 8.4B | 57.8 | 55.8 |
| 27 | Bespoke Nimble 9B v3 | 9.7B | 57.2 | 54.7 |
| 32 | Cloudflare clef-flash | 9.7B | 56.1 | 47.6 |
| 34 | **Microsoft-Decision-1 (9B, API)** | 9.0B | 55.4 |  |
| 36 | vLLM-SR d3-mini (4B) | 4.5B | 54.9 | 52.6 |
| 39 | Sieve 9B Plus | 9.7B | 53.4 | 50.9 |
| 43 | CoCo-Decision-4B 2.0.0 | 4.2B | 51.9 | 45.2 |
| 46 | RSI-Jev v6.1 VL 4B | 4.7B | 51.0 | 46.3 |
| 47 | ezjev 4B s2 | 4.7B | 50.8 | 47.0 |
| 50 | Sieve 4B | 4.7B | 50.1 | 46.1 |
| 53 | LiquidAI d1-3B | 3.1B | 49.0 | 38.9 |

88 smaller models omitted.

Per area, chance-corrected 0 to 100:

| Area | Microsoft-Decision-1 (9B, API) | Jev | vLLM-SR d3 (27B) | Cloudflare clef-flash |
|---|---|---|---|---|
| Knowledge & Reasoning | 39.6 | 53.9 | 55.3 | 53.0 |
| Language Understanding | 62.4 | 59.2 | 68.0 | 47.2 |
| Retrieval & Classification | 56.8 | 55.4 | 66.9 | 52.2 |
| Tools & Automation | 75.1 | 75.1 | 82.6 | 81.9 |
| Arts & Human Taste | 39.3 | 39.1 | 51.0 | 48.4 |

The public index is 20% of the board's headline Full score. The other 80% is private tests only the maintainer runs, and the maintainer cannot run an API-only model, so Decision-1 has no Full score and is not on the board. Ranks above are by the public column, which the board publishes for every entry.

## How the run was made

- Model: `microsoft/microsoft-decision-1` through OpenRouter (Azure endpoint, model tag `microsoft-decision-1-20261009`, 32,768-token context).
- Kit: [apolinario/decision-index](https://github.com/apolinario/decision-index) at commit `f8552a13`, suite rebuilt from the pinned sources and verified against the published hashes.
- Engine: [`decision-index/or_engine.py`](decision-index/or_engine.py), the kit's `http` engine plus the translations listed in `environment.json`. Requests over the model's context limit are recorded as unsupported and count as wrong; 241 requests were rejected, one of them inside a scored subset.
- Cost: about $4 of input tokens. Output tokens are free for this model.
- Latency in the results is OpenRouter round-trip time and is not comparable to the board's single-GPU latency column.
- Decision-1's answers are reproducible: a fresh 300-row sample re-run the same day (`recheck-300.jsonl`) gave the identical choice on 1,594 of 1,633 questions (97.6%), with probabilities differing by up to 0.19. The model is not fully deterministic, so a re-score of a re-run will land near 55.4, not exactly on it.

## Checking the result

1. Re-score: clone the kit at the commit above, then `python -m decision_index score --results decision-index/microsoft-decision-1/results.jsonl.gz`. It should print `balanced_skill: 55.39`.
2. Confirm the rows are the suite's: every result row carries the request's `run_id` and `payload_sha256`; rebuilding the suite with the kit (`suite rebuild`, `suite verify`) gives the same ids and hashes.
3. Re-run any rows yourself: the model is public. `python -m decision_index suite sample --n 300` then `run --engine or_engine:OpenRouterSystemOne` with an OpenRouter key costs a few cents; `decision-index/recheck.py` compares the answers with the published file.
4. Each result row also carries the OpenRouter generation id for that request.

## Layout

| Path | What |
|---|---|
| `decision-index/microsoft-decision-1/results.jsonl.gz` | all 140,620 result rows: answers, probabilities, token usage, generation id |
| `decision-index/microsoft-decision-1/scores.json` | the kit's score file: index, areas, every benchmark |
| `decision-index/microsoft-decision-1/recheck-300.jsonl` | the 300-row re-run used for the reproducibility check |
| `decision-index/microsoft-decision-1/benchmark-summary.json`, `environment.json` | per-benchmark counts and the engine settings |
| `decision-index/board-snapshot/board.csv`, `v03.json` | the board's published scores for all 149 entries, as of 2026-10-12 |
| `decision-index/rank.py` | prints the tables above from `scores.json` and the snapshot |
| `decision-index/recheck.py` | compares a re-run with the published results |
| `ranking.md` | output of `rank.py` |
