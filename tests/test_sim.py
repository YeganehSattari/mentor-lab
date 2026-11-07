import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
from mentor_lab.env import InternSim  # noqa: E402
from mentor_lab.evaluate import evaluate, iqm  # noqa: E402
from mentor_lab.policies import LinUCB, RoundRobin  # noqa: E402
from mentor_lab.seeds import derive_seed  # noqa: E402


def test_deterministic():
    a = evaluate(lambda s: LinUCB(d=6), [1, 2, 3]); b = evaluate(lambda s: LinUCB(d=6), [1, 2, 3])
    assert a["returns"] == b["returns"]


def test_bounds_and_horizon():
    env = InternSim(); ctx = env.reset(7); steps = 0; done = False
    while not done:
        ctx, r, c, done = env.step([0, 1, 2]); steps += 1
        assert 0 <= r <= env.n and 0 <= c <= env.n and len(ctx) == env.n
    assert steps == env.horizon


def test_round_robin_is_fair():
    assert evaluate(lambda s: RoundRobin(), [0, 1])["mean_cost"] == 0.0


def test_iqm():
    assert iqm([0, 1, 2, 3, 100, 4, 5, 6]) == 3.5


def test_seed_independent_of_hashseed():
    code = "import sys;sys.path.insert(0,'src');from mentor_lab.seeds import derive_seed;print(derive_seed(3,'x'))"
    out = {subprocess.run([sys.executable, "-c", code], capture_output=True, text=True, cwd=Path(__file__).resolve().parents[1],
                          env={**os.environ, "PYTHONHASHSEED": h}).stdout for h in ("1", "2")}
    assert len(out) == 1 and str(derive_seed(3, "x")) in out.pop()


def test_full_eval_bitwise_identical_across_hashseeds():
    script = Path(__file__).resolve().parents[1] / "scripts" / "repro_check.py"
    outs = [subprocess.run([sys.executable, str(script)], capture_output=True, text=True, check=True,
                           env={**os.environ, "PYTHONHASHSEED": h}).stdout for h in ("1", "12345")]
    assert outs[0] == outs[1] and "linucb" in outs[0]


def test_llm_format_failure_rate_is_about_10_percent(caplog):
    import logging
    from mentor_lab.schemas import format_failure_rate
    with caplog.at_level(logging.INFO, logger="mentor_lab.llm"):
        rate = format_failure_rate(1000)
    assert 0.07 <= rate <= 0.13
    assert "format failure rate" in caplog.text


def test_strict_model_rejects_bad_outputs():
    import pytest
    from pydantic import ValidationError
    from mentor_lab.schemas import parse_draft
    bad = '{"intern": "H-01", "strengths": [], "issues": [], "evidence": [], "next_step": "x", "confidence": "high"}'
    with pytest.raises(ValidationError):
        parse_draft(bad)
    with pytest.raises(ValidationError):
        parse_draft("Sure! Here is the feedback: {}")