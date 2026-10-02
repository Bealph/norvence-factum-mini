from decimal import Decimal

from app.extract import Invoice, extract_invoice
from app.llm_client import MockLLMClient


def test_extract_invoice_happy_path():
    client = MockLLMClient(
        {
            "artisan": "Plomberie Garnier",
            "numero": "PG-2024-0412",
            "date": "2024-09-12",
            "montant_ttc": "980.50",
        }
    )

    invoice = extract_invoice("Facture PG-2024-0412 ... Total TTC 980.50", client)

    assert invoice == Invoice(
        artisan="Plomberie Garnier",
        numero="PG-2024-0412",
        date="2024-09-12",
        montant_ttc=Decimal("980.50"),
    )
    assert "PG-2024-0412" in client.prompts[0]
