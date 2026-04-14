"""Shared constants — single source of truth for field names and schema.

Per lessons.md: multi-component builds define shared constants FIRST to
prevent placeholder mismatches between modules.
"""
from __future__ import annotations

SCHEMA_VERSION = "1.0.0"
FORECAST_HORIZON_MONTHS = 24
HMAC_ENV_VAR = "TRUTHCERT_HMAC_KEY"

PICO_REQUIRED_FIELDS = (
    "id",
    "title",
    "population",
    "intervention",
    "comparator",
    "outcome",
    "outcome_type",
    "decision_threshold",
)

CARD_TOP_LEVEL_FIELDS = (
    "schema_version",
    "pico_id",
    "generated_utc",
    "effect",
    "flip",
    "representativeness",
    "truthcert",
)

EFFECT_FIELDS = ("point", "ci_low", "ci_high", "pi_low", "pi_high",
                 "k", "tau2", "i2", "scale")

FLIP_FIELDS = ("probability", "ci_low", "ci_high", "horizon_months",
               "model_version", "pipeline_empty")

REPRESENTATIVENESS_FIELDS = ("overlap_score", "trial_country_count",
                             "burden_weighted", "source")

TRUTHCERT_FIELDS = ("sha256", "hmac_sha256", "signed_utc", "key_source")
