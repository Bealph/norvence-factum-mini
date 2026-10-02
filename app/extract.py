"""Extraction des champs d'une facture via le LLM, puis normalisation."""

from __future__ import annotations

import json
from dataclasses import dataclass
from decimal import Decimal

from app.llm_client import LLMClient
from app.normalize import normalize_amount

PROMPT = """Tu extrais les champs d'une facture d'artisan.
Réponds uniquement en JSON avec les clés : artisan, numero, date, montant_ttc.
Recopie le montant tel qu'il apparaît sur la facture.

Facture :
{text}
"""


class ExtractionError(Exception):
    pass


@dataclass(frozen=True)
class Invoice:
    artisan: str
    numero: str
    date: str
    montant_ttc: Decimal


def extract_invoice(text: str, client: LLMClient) -> Invoice:
    raw = client.complete(PROMPT.format(text=text))
    try:
        fields = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise ExtractionError(f"réponse LLM non JSON : {raw[:80]!r}") from exc

    return Invoice(
        artisan=fields["artisan"],
        numero=fields["numero"],
        date=fields["date"],
        montant_ttc=normalize_amount(fields["montant_ttc"]),
    )
