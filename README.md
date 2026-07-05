# ARVI-RX — Assistant radiologique virtuel responsable

## Contexte

ARVI-RX est un prototype pédagogique d’IA médicale multimodale.  
Il sert à construire une chaîne simple, prudente, traçable et évaluée autour d’une radiographie thoracique frontale.

## Position non clinique

Ce dépôt n’est pas un dispositif médical.  
Il ne doit jamais être utilisé pour diagnostiquer, trier ou orienter un patient.  
Toute sortie produite par le système doit rester un résultat expérimental et pédagogique.

## Objectif du prototype

Le système accepte une radiographie thoracique frontale et retourne une sortie JSON structurée contenant :

- `image_quality`
- `predicted_class`
- `confidence`
- `visual_evidence`
- `justification`
- `limitations`
- `warning`

Les classes autorisées sont :

- `normal`
- `suspected_opacity`
- `uncertain`

## Fonctionnalités Must Have

- Dépôt Git propre et documenté
- Interface Streamlit
- Upload d’une image
- Affichage de l’image
- Prétraitement minimal
- Baseline reproductible
- Sortie JSON structurée
- Garde-fous
- Warning non clinique obligatoire
- Journalisation des prédictions
- Évaluation simple
- Registre d’erreurs

## Should Have : comparaison baseline vs improved

La baseline initiale utilise une heuristique simple basée sur la qualité d’image et un score visuel d’opacité.

La version améliorée ajoute une règle plus prudente :
- seuil plus strict pour suspected_opacity ;
- utilisation de uncertain en cas de signal faible ;
- réduction des faux positifs.

Pour lancer la comparaison :

```bash
python eval/run_comparison.py
python -m venv .venv