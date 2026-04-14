import math
import pytest
from evidence_forecast.effect_layer import (
    EffectResult,
    compute_effect,
    EffectBackend,
)
from evidence_forecast.pico_spec import PICO
from evidence_forecast.constants import EFFECT_FIELDS


class _StubBackend(EffectBackend):
    def pool(self, pico: PICO) -> dict:
        return dict(
            point=0.79, ci_low=0.69, ci_high=0.91,
            pi_low=0.55, pi_high=1.13,
            k=5, tau2=0.012, i2=0.18, scale="HR",
        )


@pytest.fixture
def sample_pico() -> PICO:
    return PICO(
        id="t", title="t", population="p", intervention="i",
        comparator="c", outcome="o", outcome_type="binary",
        decision_threshold=1.0,
    )


def test_compute_effect_returns_all_required_fields(sample_pico):
    result = compute_effect(sample_pico, backend=_StubBackend())
    for field in EFFECT_FIELDS:
        assert getattr(result, field) is not None, f"missing {field}"


def test_compute_effect_values_match_backend(sample_pico):
    result = compute_effect(sample_pico, backend=_StubBackend())
    assert math.isclose(result.point, 0.79, abs_tol=1e-9)
    assert math.isclose(result.ci_low, 0.69, abs_tol=1e-9)
    assert math.isclose(result.ci_high, 0.91, abs_tol=1e-9)
    assert result.k == 5
    assert result.scale == "HR"


def test_compute_effect_rejects_malformed_backend(sample_pico):
    class Bad(EffectBackend):
        def pool(self, pico): return {"point": 0.5}  # missing fields
    with pytest.raises(KeyError) as exc:
        compute_effect(sample_pico, backend=Bad())
    assert "missing" in str(exc.value).lower()
