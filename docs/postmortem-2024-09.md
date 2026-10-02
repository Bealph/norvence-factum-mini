# Post-mortem — montants multipliés par 100 (septembre 2024)

**Statut** : clos · **Gravité** : élevée · **Rédaction** : équipe outils internes

## Résumé

Entre le 9 et le 12 septembre, 37 factures d'artisans affichant un montant de la forme « 1 250,00 € » ont été exportées en comptabilité à 125 000 €. Le module de normalisation des montants supprimait la virgule au lieu de la lire comme séparateur décimal.

## Chronologie

- **09/09** — mise en production d'une nouvelle version du prompt d'extraction : le LLM recopie désormais le montant tel qu'il apparaît sur la facture (format français) au lieu de le reformater.
- **09/09 → 12/09** — 37 factures exportées avec un montant multiplié par 100. Deux règlements partent avant blocage.
- **12/09** — alerte du service comptable sur un appel de fonds incohérent pour la résidence Les Tilleuls.
- **12/09** — correctif poussé sur `main` (commit « fix: lire la virgule décimale dans les montants »). Pas de test ajouté, faute de temps.
- **13/09 → 20/09** — rapprochement manuel, annulation des écritures, récupération des deux virements.

## Impact

- 37 écritures erronées, 2 virements à récupérer auprès des artisans.
- Environ 3 jours-personne côté comptabilité.

## Ce qui a fonctionné

- Le service comptable a détecté l'anomalie en moins de 4 jours.
- Le correctif a été déployé dans l'heure.

## Question ouverte

La CI est restée verte avant, pendant et après l'incident.

**Pourquoi la CI était-elle verte ?**
