from pathlib import Path
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix, classification_report

ROOT_DIR = Path(__file__).resolve().parents[1]

LOG_PATH = ROOT_DIR / "outputs" / "logs.csv"
CASES_PATH = ROOT_DIR / "data" / "cases.csv"
OUT_PATH = ROOT_DIR / "data" / "results" / "evaluation_summary.csv"


def run_evaluation():
    if not LOG_PATH.exists():
        print(f"Aucun fichier logs.csv trouvé ici : {LOG_PATH}")
        print("Lance d’abord quelques analyses dans l’application Streamlit.")
        return

    if not CASES_PATH.exists():
        print(f"Aucun fichier cases.csv trouvé ici : {CASES_PATH}")
        return

    logs = pd.read_csv(LOG_PATH)
    cases = pd.read_csv(CASES_PATH)

    df = logs.merge(cases, on="image_name", how="inner")

    if df.empty:
        print("Aucune correspondance entre les logs et data/cases.csv.")
        print("Vérifie que les noms d’images sont identiques.")
        print()
        print("Images dans logs.csv :")
        print(logs["image_name"].unique())
        print()
        print("Images dans cases.csv :")
        print(cases["image_name"].unique())
        return

    y_true = df["true_label"]
    y_pred = df["predicted_class"]

    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)

    labels = ["normal", "suspected_opacity", "uncertain"]

    print("=== Résultats d’évaluation ===")
    print("Nombre de cas évalués :", len(df))
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

    OUT_PATH.parent.mkdir(exist_ok=True)
    summary.to_csv(OUT_PATH, index=False)

    print()
    print(f"Résumé sauvegardé dans {OUT_PATH}")


if __name__ == "__main__":
    run_evaluation()