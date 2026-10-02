"""Replay two synthetic Jev responses without a network request or API key."""
import json
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from jev_core import decide

POLICY = json.loads((Path(__file__).resolve().parents[1] / "policy.json").read_text())

class FakeResponse:
    def __init__(self, result): self.result = result
    def __enter__(self): return self
    def __exit__(self, *args): return False
    def read(self, *args): return json.dumps(self.result).encode()


def replay(probability):
    def open_fixture(request, timeout):
        payload = json.loads(request.data)
        assert payload["state"]["text"] == TEXT
        assert request.full_url == "https://api.typesafe.ai/v1/systemone"
        return FakeResponse({"model": POLICY["model"], "answers": {POLICY["question"]: {"choice": CHOICE, "probabilities": {CHOICE: probability}}}})
    return decide(TEXT, POLICY, "offline-fixture", opener=open_fixture)


TEXT = 'A prospect asks for a product demonstration and pricing.'
CHOICE = 'sales'

if __name__ == "__main__":
    high = replay(0.96)
    low = replay(0.52)
    assert high["outcome"] == CHOICE
    assert low["outcome"] == "review"
    assert high["inputSha256"] == low["inputSha256"]
    print(json.dumps({"accepted": high, "lowConfidence": low}, indent=2))
