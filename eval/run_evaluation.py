import sys
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))


def run_evaluation():
    log_path = Path("outputs/logs.csv")
    cases_path = Path("data/cases.csv")
    out_path = Path("data/results/evaluation_summary.csv")

    if not log_path.exists():
        print("Aucun fichier outputs/logs.csv trouvé. Lance d’abord quelques analyses.")
        return

    if not cases_path.exists():
        print("Aucun fichier data/cases.csv trouvé.")
        return

    logs = pd.read_csv(log_path)
    cases = pd.read_csv(cases_path)

    df = logs.merge(cases, on="image_name", how="inner")

    if df.empty:
        print("Aucune correspondance entre les logs et data/cases.csv.")
        print("Vérifie que les noms d’images sont identiques.")
        return

    y_true = df["true_label"]
    y_pred = df["predicted_class"]

    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)
    labels = ["normal", "suspected_opacity", "uncertain"]

    print("=== Résultats d’évaluation ===")
    print("Accuracy :", round(accuracy, 3))
    print("Macro-F1 :", round(macro_f1, 3))
    print()
    print("Matrice de confusion :")
    print(confusion_matrix(y_true, y_pred, labels=labels))
    print()
    print(classification_report(y_true, y_pred, zero_division=0))

    summary = pd.DataFrame([{
        "accuracy": accuracy,
        "macro_f1": macro_f1,
        "num_cases": len(df),
        "uncertain_rate": (df["predicted_class"] == "uncertain").mean()
    }])

    out_path.parent.mkdir(exist_ok=True)
    summary.to_csv(out_path, index=False)

    print(f"Résumé sauvegardé dans {out_path}")


if __name__ == "__main__":
    run_evaluation()