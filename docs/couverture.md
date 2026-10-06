La CI est restée verte parce qu’aucun test n’exerçait le format français « 1 250,00 € » qui avait déclenché le défaut.
Le test `test_normalize_numeric_input` appelait la fonction sans assertion : il faisait exécuter du code, mais ne vérifiait aucun résultat.
La CI du dépôt lançait pytest et Ruff, sans mesurer la couverture ni imposer de seuil ; elle ne pouvait donc pas signaler l’absence de ce scénario.

# Couverture des tests : seuil et mesure

## Ce qui a changé

- Les 8 factures de `tests/fixtures/echantillons.jsonl` sont rejouées une à une par un test paramétré. Chaque cas compare le montant produit au montant attendu.
- Deux cas oubliés par ces 8 factures sont ajoutés : un montant reçu sous forme de nombre, et un montant absent ou illisible, qui doit être refusé.
- La CI mesure désormais la couverture, branches comprises, et échoue si elle passe sous le seuil.

Contre-épreuve : en remettant le défaut de septembre (virgule supprimée au lieu d’être lue), 4 cas échouent, dont F-0137 « 1 250,00 € ».

## Seuil retenu : 90 %

| Mesure (2026-10-06, Python 3.11)     | Couverture totale |
| ------------------------------------ | ----------------: |
| Avant ce travail                     |              75 % |
| Après ce travail                     |           90,22 % |
| Si l’on supprime `test_normalize.py` |           72,83 % |

Pourquoi 90 :

- c’est la mesure obtenue, arrondie à l’entier inférieur. La couverture ne peut plus baisser sans que la CI devienne rouge ;
- Martin Fowler considère comme normal un taux dans les hauts 80 % ou les 90 % quand les tests sont réfléchis ;
- 100 % n’est pas visé. Le code encore non couvert est surtout l’appel réseau réel au fournisseur LLM, qu’on ne lance pas en CI. Reste aussi le cas d’une réponse LLM qui n’est pas du JSON (`app/extract.py`) : il est testable et mérite un test, hors du périmètre de ce travail.

Le seuil est une alarme, pas une preuve de qualité. Il signale qu’on a retiré ou oublié des tests ; il ne dit pas si les tests vérifient les bons résultats. Seules les assertions le font.

Le seuil est écrit dans `pyproject.toml` (section `[tool.coverage.report]`), pas dans le workflow : la CI et le poste local appliquent ainsi la même règle.

## Relancer la mesure en local

Depuis la racine du dépôt :

```bash
uv sync
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

La dernière ligne indique si le seuil est atteint. La colonne `Missing` liste les lignes et les branches jamais parcourues.
