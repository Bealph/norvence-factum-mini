import json
from decimal import Decimal
from pathlib import Path

import pytest

from app.normalize import normalize_amount

FIXTURES = Path(__file__).parent / "fixtures" / "echantillons.jsonl"
ECHANTILLONS = [
    json.loads(ligne)
    for ligne in FIXTURES.read_text(encoding="utf-8").splitlines()
    if ligne.strip()
]


@pytest.mark.parametrize("cas", ECHANTILLONS, ids=[cas["id"] for cas in ECHANTILLONS])
def test_normalize_echantillons(cas):
    assert normalize_amount(cas["montant_brut"]) == Decimal(cas["montant_attendu"])


@pytest.mark.parametrize(
    ("brut", "attendu"),
    [(1250, "1250.00"), (980.5, "980.50")],
)
def test_normalize_numeric_input(brut, attendu):
    assert normalize_amount(brut) == Decimal(attendu)


@pytest.mark.parametrize("brut", [None, "", "mille euros"])
def test_normalize_rejects_unreadable_amount(brut):
    with pytest.raises(ValueError):
        normalize_amount(brut)
