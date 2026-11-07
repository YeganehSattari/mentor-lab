import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mentor_lab.evaluate import evaluate  # noqa: E402
from mentor_lab.policies import LinUCB, RandomPolicy, RoundRobin  # noqa: E402

for name, mk in [("random", lambda s: RandomPolicy(s)), ("round-robin", lambda s: RoundRobin()), ("linucb", lambda s: LinUCB(d=6))]:
    r = evaluate(mk, list(range(10)))
    print(name, repr(r["returns"]), repr(r["iqm"]), repr(r["ci"]), repr(r["mean_cost"]))