"""Decision Index engine for OpenRouter's /v1/systemone.
Identical to the kit's http engine except for mechanical schema translations OpenRouter's request
validator requires, plus two transport details, all recorded in provenance:
  - a yes/no (noul) question whose `criteria` is an empty object is sent without the key;
  - a `state` that is neither a string nor an object (a JSON array) is sent as its JSON text;
  - a 4xx whose body names the model's context limit is a declared capacity limit (Unsupported),
    matching how the kit treats its own capacity markers;
  - HTTP 429 (rate limit) is retried with backoff instead of being recorded as an error.
Instructions, option keys, descriptions and ordering are never changed."""
import json, time
from decision_index.engines import Unsupported
from decision_index.engines.http import HttpSystemOne, CAPACITY_MARKERS

EXTRA_MARKERS = ("context limit", "exceeds the", "token limit")

class OpenRouterSystemOne(HttpSystemOne):
    name = "openrouter-systemone"
    def __init__(self, **options):
        super().__init__(**options)
        self.provenance = dict(self.provenance, kind="openrouter-systemone",
            translation="noul questions with empty criteria sent without the criteria key; array state sent as JSON text; 4xx naming the context limit recorded as unsupported; 429 retried with backoff; nothing else changed")
    def __call__(self, state, questions):
        if not isinstance(state, (str, dict)):
            state = json.dumps(state, ensure_ascii=False)
        qs = {}
        for k, q in questions.items():
            if q.get("type") == "noul" and isinstance(q.get("criteria"), dict) and not q["criteria"]:
                q = {kk: vv for kk, vv in q.items() if kk != "criteria"}
            qs[k] = q
        body = {"model": self.model, "state": state, "questions": qs, **self.extra}
        for attempt in range(6):
            r = self.client.post("/v1/systemone", json=body)
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(min(2 ** attempt, 30)); continue
            break
        if r.status_code in (400, 413, 422):
            message = r.text
            if any(s in message for s in CAPACITY_MARKERS + EXTRA_MARKERS):
                raise Unsupported(message[:500])
        r.raise_for_status()
        raw = r.json()
        return {k: v for k, v in raw.items() if k != "evaluation_trace"}, raw
