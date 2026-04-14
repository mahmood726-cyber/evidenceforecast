import os
from pathlib import Path
import pytest


@pytest.fixture
def seed_env(monkeypatch: pytest.MonkeyPatch):
    monkeypatch.setenv("TRUTHCERT_HMAC_KEY", "test-key-not-for-production")
    monkeypatch.setenv("PYTHONHASHSEED", "0")


@pytest.fixture
def project_root() -> Path:
    return Path(__file__).resolve().parent.parent
