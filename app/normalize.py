"""Normalisation des montants extraits des factures."""

from __future__ import annotations

from decimal import Decimal, InvalidOperation

CENT = Decimal("0.01")

_CURRENCY_MARKS = ("€", "EUR", "eur")
_SPACES = (" ", " ", " ")


def normalize_amount(raw: str | int | float | None) -> Decimal:
    """Convertit un montant brut (« 1 250,00 € », « 1250.00 »…) en Decimal arrondi au centime."""
    if raw is None:
        raise ValueError("montant absent")
    if isinstance(raw, (int, float)):
        return Decimal(str(raw)).quantize(CENT)

    text = raw.strip()
    for mark in _CURRENCY_MARKS:
        text = text.replace(mark, "")
    for space in _SPACES:
        text = text.replace(space, "")

    negative = text.startswith("-")
    text = text.lstrip("+-")

    if "," in text and "." in text:
        if text.rfind(",") > text.rfind("."):
            # 1.250,00 : point = milliers, virgule = décimale
            text = text.replace(".", "").replace(",", ".")
        else:
            # 1,250.00 : virgule = milliers, point = décimale
            text = text.replace(",", "")
    elif "," in text:
        # 1250,00 : virgule décimale
        text = text.replace(",", ".")

    try:
        value = Decimal(text)
    except InvalidOperation as exc:
        raise ValueError(f"montant illisible : {raw!r}") from exc

    if negative:
        value = -value
    return value.quantize(CENT)
