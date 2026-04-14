import math
import pytest
from evidence_forecast.representativeness import (
    compute_representativeness,
    RepresentativenessResult,
)


def test_perfect_overlap_score_is_one():
    trial_countries = {"USA": 0.5, "DEU": 0.5}
    burden = {"USA": 0.5, "DEU": 0.5}
    r = compute_representativeness(trial_countries, burden)
    assert math.isclose(r.overlap_score, 1.0, abs_tol=1e-9)
    assert r.trial_country_count == 2


def test_zero_overlap_score_is_zero():
    trial_countries = {"USA": 1.0}
    burden = {"IND": 1.0}
    r = compute_representativeness(trial_countries, burden)
    assert math.isclose(r.overlap_score, 0.0, abs_tol=1e-9)


def test_partial_overlap_uses_min_weights():
    # Bhattacharyya-style min-weight overlap
    trial_countries = {"USA": 0.8, "IND": 0.2}
    burden = {"USA": 0.3, "IND": 0.7}
    r = compute_representativeness(trial_countries, burden)
    # min(0.8,0.3) + min(0.2,0.7) = 0.3 + 0.2 = 0.5
    assert math.isclose(r.overlap_score, 0.5, abs_tol=1e-9)


def test_empty_trial_countries_returns_zero_and_flags():
    r = compute_representativeness({}, {"USA": 1.0})
    assert r.overlap_score == 0.0
    assert r.trial_country_count == 0
    assert r.source == "none"


def test_weights_not_normalised_raises():
    with pytest.raises(ValueError):
        compute_representativeness({"USA": 0.5, "DEU": 0.9}, {"USA": 1.0})
