# Norvence Factum Mini

Extraction des champs de factures d'artisans par un LLM, normalisation des montants, puis préparation de l'export vers la comptabilité.

## Features

- Extraction structurée (artisan, numéro, date, montant TTC) d'une facture texte via un client LLM
- Client LLM simulé pour les tests, client HTTP pour l'environnement réel
- Normalisation des montants au format français et anglo-saxon (séparateurs de milliers, virgule ou point décimal, symbole €)
- Jeu d'échantillons de factures réelles anonymisées dans `tests/fixtures/`
- Intégration continue GitHub Actions (lint + tests) sur chaque push et pull request

## Stack

- Python 3.11
- uv (gestion des dépendances)
- pytest 8
- ruff
- GitHub Actions

## Setup

```bash
make install              # uv sync — install dependencies
cp .env.example .env      # only needed for the real LLM client
make test                 # run the test suite
```

## Layout

```
app/
  extract.py        # appel LLM + parsing JSON → Invoice
  llm_client.py     # MockLLMClient (tests) et HttpLLMClient (réel)
  normalize.py      # normalisation des montants
tests/
  fixtures/echantillons.jsonl   # montants bruts et valeurs attendues
  test_normalize.py
  test_pipeline.py
docs/
  postmortem-2024-09.md
.github/workflows/ci.yml
```

## Useful commands

```bash
make fmt        # ruff format + autofix
make lint       # ruff check
```

## Contact

Équipe outils internes — Norvence Gestion.
