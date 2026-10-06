La CI est restée verte parce qu’aucun test n’exerçait le format français « 1 250,00 € » qui avait déclenché le défaut.
Le test `test_normalize_numeric_input` appelait la fonction sans assertion : il faisait exécuter du code, mais ne vérifiait aucun résultat.
La CI du dépôt lançait pytest et Ruff, sans mesurer la couverture ni imposer de seuil ; elle ne pouvait donc pas signaler l’absence de ce scénario.

# Couverture des tests : seuil et mesure

Les trois lignes ci-dessus décrivent le dépôt avant ce travail : commit `5668096` pour les tests et la CI, commit `733060e` pour le correctif, livré sans test.

## La preuve par l’historique

Les anciens et les nouveaux tests ont été rejoués contre le code fautif et contre le code corrigé :

| Tests                    | Code fautif (`5668096`) | Code corrigé (`733060e`) |
| ------------------------ | ----------------------- | ------------------------ |
| Anciens (3 tests)        | vert : 3 réussis        | vert : 3 réussis         |
| Nouveaux (14 tests)      | rouge : 5 échecs        | vert : 14 réussis        |

Les anciens tests ne voyaient pas la différence entre le code fautif et le code corrigé. Les nouveaux échouent sur les 5 factures écrites avec une virgule décimale, dont F-0137 « 1 250,00 € ».

## Ce qui a changé

- Un même test est rejoué sur chacune des 8 factures de `tests/fixtures/echantillons.jsonl`. Il compare le montant produit au montant attendu : c’est l’assertion, la vérification du résultat.
- Ces 8 factures laissaient deux chemins du code inexplorés : un montant reçu sous forme de nombre, et un montant absent ou illisible, qui doit être refusé. Des cas les couvrent désormais.
- La CI mesure la couverture de branches : pour chaque « si… sinon », elle vérifie que les deux côtés ont été parcourus. Elle échoue si la couverture totale passe sous le seuil.

## Seuil retenu : 90 %

| État du dépôt                                | Couverture totale |
| -------------------------------------------- | ----------------: |
| Avant ce travail (mesurée les 02 et 06/10)   |              75 % |
| Après ce travail (mesure du 2026-10-06)      |           90,22 % |
| Après ce travail, sans `test_normalize.py`   |           72,83 % |

La dernière ligne simule un retrait des tests de normalisation : la couverture tombe sous le seuil et la CI devient rouge, même si le test restant réussit.

Pourquoi 90 :

- c’est la mesure obtenue, arrondie à l’entier inférieur. La couverture ne peut plus descendre sous 90 % sans que la CI devienne rouge ;
- Martin Fowler juge normal un taux « dans les hauts 80 % ou les 90 % » quand les tests sont réfléchis, et se méfie de 100 % ([Test Coverage](https://martinfowler.com/bliki/TestCoverage.html), consulté le 2026-10-06) ;
- 100 % n’est pas visé. Le code encore non couvert est l’appel réseau réel au fournisseur LLM (`app/llm_client.py`, lignes 33-34 et 37-49), qu’on ne lance pas en CI, et le cas d’une réponse LLM qui n’est pas du JSON (`app/extract.py`, lignes 37-38). Ce dernier cas est testable : il mérite un test, hors du périmètre de ce travail.

Le seuil est une alarme, pas une preuve de qualité : il signale des tests retirés ou oubliés, mais ne dit pas si les tests vérifient les bons résultats.

Le seuil est écrit dans `pyproject.toml` (section `[tool.coverage.report]`), pas dans le workflow. C’est pytest-cov qui lit ce réglage : `ci.yml` ne contient donc aucun seuil, et la CI comme le poste local appliquent la même règle.

## Relancer la mesure en local

Prérequis : [uv](https://docs.astral.sh/uv/) installé. Depuis la racine du dépôt, la même commande que la CI, avec en plus la liste de ce qui n’est pas couvert :

```bash
uv sync
uv run pytest --cov=app --cov-branch --cov-report=term-missing
```

Lire la ligne `Required test coverage of 90.0% reached`. En cas d’échec, pytest affiche `FAIL Required test coverage of 90.0% not reached` et se termine en erreur. La colonne `Missing` liste les lignes et les branches jamais parcourues.
