import pytest
from pathlib import Path
import yaml

from evidence_forecast.pico_spec import load_pico, PICOValidationError
from evidence_forecast.constants import PICO_REQUIRED_FIELDS


def _write(tmp_path: Path, data: dict) -> Path:
    p = tmp_path / "pico.yaml"
    p.write_text(yaml.safe_dump(data))
    return p


def test_valid_pico_loads(tmp_path: Path):
    data = {
        "id": "sglt2i_hfpef",
        "title": "SGLT2i in HFpEF",
        "population": "Adults with HFpEF (LVEF >=50%)",
        "intervention": "SGLT2 inhibitor",
        "comparator": "Placebo",
        "outcome": "Composite HF hospitalisation or CV death",
        "outcome_type": "binary",
        "decision_threshold": 1.0,
    }
    pico = load_pico(_write(tmp_path, data))
    assert pico.id == "sglt2i_hfpef"
    assert pico.outcome_type == "binary"


@pytest.mark.parametrize("missing", PICO_REQUIRED_FIELDS)
def test_missing_required_field_raises(tmp_path: Path, missing: str):
    data = {
        "id": "x", "title": "t", "population": "p", "intervention": "i",
        "comparator": "c", "outcome": "o", "outcome_type": "binary",
        "decision_threshold": 1.0,
    }
    data.pop(missing)
    with pytest.raises(PICOValidationError) as exc:
        load_pico(_write(tmp_path, data))
    assert missing in str(exc.value)


def test_unknown_outcome_type_raises(tmp_path: Path):
    data = {
        "id": "x", "title": "t", "population": "p", "intervention": "i",
        "comparator": "c", "outcome": "o", "outcome_type": "quantum",
        "decision_threshold": 1.0,
    }
    with pytest.raises(PICOValidationError):
        load_pico(_write(tmp_path, data))
