import sys
import time
from pathlib import Path

import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, confusion_matrix

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.preprocessing import preprocess_image
from src.baseline import run_baseline_prediction
from src.improved import run_improved_prediction
from src.guardrails import apply_guardrails


CASES_PATH = ROOT_DIR / "data" / "cases.csv"
IMAGE_DIR = ROOT_DIR / "data" / "sample_images"

BASELINE_OUT = ROOT_DIR / "data" / "results" / "results_baseline.csv"
IMPROVED_OUT = ROOT_DIR / "data" / "results" / "results_improved.csv"
SUMMARY_OUT = ROOT_DIR / "data" / "results" / "comparison_summary.csv"


def evaluate_model(model_name, predict_function, output_path):
    cases = pd.read_csv(CASES_PATH)
    rows = []

    for _, row in cases.iterrows():
        image_name = row["image_name"]
        true_label = row["true_label"]
        image_path = IMAGE_DIR / image_name

        if not image_path.exists():
            print(f"Image introuvable : {image_path}")
            continue

        start = time.time()

        _, quality_info = preprocess_image(image_path)
        raw_output = predict_function(quality_info)
        final_output = apply_guardrails(raw_output, quality_info)

        latency_ms = round((time.time() - start) * 1000, 2)

        rows.append({
            "case_id": row["case_id"],
            "image_name": image_name,
            "true_label": true_label,
            "predicted_class": final_output["predicted_class"],
            "confidence": final_output["confidence"],
            "image_quality": final_output["image_quality"],
            "json_valid": True,
            "latency_ms": latency_ms,
            "model_name": model_name
        })

    df = pd.DataFrame(rows)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(output_path, index=False, encoding="utf-8")

    return df


def compute_summary(df, model_name):
    y_true = df["true_label"]
    y_pred = df["predicted_class"]

    accuracy = accuracy_score(y_true, y_pred)
    macro_f1 = f1_score(y_true, y_pred, average="macro", zero_division=0)

    suspected_true = y_true == "suspected_opacity"
    suspected_pred = y_pred == "suspected_opacity"

    tp = ((suspected_true) & (suspected_pred)).sum()
    fn = ((suspected_true) & (~suspected_pred)).sum()
    fp = ((~suspected_true) & (suspected_pred)).sum()
    tn = ((~suspected_true) & (~suspected_pred)).sum()

    sensitivity = tp / (tp + fn) if (tp + fn) > 0 else 0
    specificity = tn / (tn + fp) if (tn + fp) > 0 else 0

    return {
        "model_name": model_name,
        "accuracy": round(accuracy, 3),
        "macro_f1": round(macro_f1, 3),
        "sensitivity": round(sensitivity, 3),
        "specificity": round(specificity, 3),
        "uncertain_rate": round((y_pred == "uncertain").mean(), 3),
        "json_validity": round(df["json_valid"].mean(), 3),
        "avg_latency_ms": round(df["latency_ms"].mean(), 2),
        "false_positives": int(fp),
        "false_negatives": int(fn),
        "confusion_matrix": confusion_matrix(
            y_true,
            y_pred,
            labels=["normal", "suspected_opacity", "uncertain"]
        ).tolist()
    }


def run_comparison():
    baseline_df = evaluate_model(
        "toy_baseline_v1",
        run_baseline_prediction,
        BASELINE_OUT
    )

    improved_df = evaluate_model(
        "improved_baseline_v1",
        run_improved_prediction,
        IMPROVED_OUT
    )

    summary_df = pd.DataFrame([
        compute_summary(baseline_df, "toy_baseline_v1"),
        compute_summary(improved_df, "improved_baseline_v1")
    ])

    summary_df.to_csv(SUMMARY_OUT, index=False, encoding="utf-8")

    print("=== Comparaison baseline vs improved ===")
    print(summary_df)
    print()
    print(f"Résultats baseline : {BASELINE_OUT}")
    print(f"Résultats improved : {IMPROVED_OUT}")
    print(f"Résumé comparaison : {SUMMARY_OUT}")


if __name__ == "__main__":
    run_comparison()