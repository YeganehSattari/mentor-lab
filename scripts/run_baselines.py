"""python scripts/run_baselines.py  →  Random vs RoundRobin vs LinUCB on 10 seeds (IQM, 95% CI, fairness cost)."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mentor_lab.evaluate import evaluate          # noqa: E402
from mentor_lab.policies import LinUCB, RandomPolicy, RoundRobin  # noqa: E402

SEEDS = list(range(10))
for name, mk in [("random", lambda s: RandomPolicy(s)), ("round-robin", lambda s: RoundRobin()), ("linucb", lambda s: LinUCB(d=6))]:
    r = evaluate(mk, SEEDS)
    print(f"{name:12s} IQM={r['iqm']:.2f}  95%CI=[{r['ci'][0]:.2f}, {r['ci'][1]:.2f}]  fairness-cost/ep={r['mean_cost']:.1f}")
