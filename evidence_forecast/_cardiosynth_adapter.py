"""Thin adapter around CardioSynth. Not unit-tested; exercised by the
live integration test in test_trio_smoke.py."""
from __future__ import annotations

from evidence_forecast.pico_spec import PICO


class CardioSynthBackend:
    def pool(self, pico: PICO) -> dict:
        import sys
        sys.path.insert(0, r"C:\cardiosynth")
        from cardiosynth.engine import pool_for_pico  # live import
        result = pool_for_pico(
            population=pico.population,
            intervention=pico.intervention,
            comparator=pico.comparator,
            outcome=pico.outcome,
            outcome_type=pico.outcome_type,
        )
        return dict(
            point=result.pooled_effect,
            ci_low=result.ci[0],
            ci_high=result.ci[1],
            pi_low=result.prediction_interval[0],
            pi_high=result.prediction_interval[1],
            k=result.k,
            tau2=result.tau2,
            i2=result.i2,
            scale=result.scale,
        )
