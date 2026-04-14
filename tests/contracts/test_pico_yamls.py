from pathlib import Path
import pytest
from evidence_forecast.pico_spec import load_pico

PICO_DIR = Path(__file__).resolve().parents[2] / "configs" / "picos"

EXPECTED_IDS = {"sglt2i_hfpef", "tirzepatide_hfpef_acm", "empareg_t2dm"}


def test_all_three_picos_load():
    yamls = sorted(PICO_DIR.glob("*.yaml"))
    loaded = [load_pico(p) for p in yamls]
    assert {p.id for p in loaded} == EXPECTED_IDS


@pytest.mark.parametrize("filename,expected_id", [
    ("sglt2i_hfpef.yaml", "sglt2i_hfpef"),
    ("tirzepatide_hfpef_acm.yaml", "tirzepatide_hfpef_acm"),
    ("empareg_t2dm.yaml", "empareg_t2dm"),
])
def test_pico_id_matches_filename(filename: str, expected_id: str):
    pico = load_pico(PICO_DIR / filename)
    assert pico.id == expected_id
