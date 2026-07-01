# Architecture du projet ARVI-RX

ARVI-RX est organisé selon une architecture simple :

- `app/` : interface web Streamlit.
- `src/` : logique principale du prototype : prétraitement, baseline, garde-fous, logs.
- `prompts/` : prompts utilisés pour la baseline et les futures versions améliorées.
- `data/` : images de test et fichier `cases.csv`.
- `eval/` : scripts d’évaluation.
- `api/` : API FastAPI minimale ou future.
- `tests/` : tests de contrôle minimal.
- `notebooks/` : notebooks d’expérimentation.
- `finetuning/` : dossier réservé aux expérimentations futures, non obligatoire pour le Must Have.

Le prototype est non clinique et uniquement pédagogique.