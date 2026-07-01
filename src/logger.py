import csv
import json
import time
from pathlib import Path


LOG_PATH = Path("outputs/logs.csv")


def save_log(image_name, prompt_version, model_name, latency_ms, raw_output, final_output):
    LOG_PATH.parent.mkdir(exist_ok=True)
    file_exists = LOG_PATH.exists()

    with open(LOG_PATH, mode="a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(
            file,
            fieldnames=[
                "timestamp",
                "image_name",
                "prompt_version",
                "model_name",
                "predicted_class",
                "confidence",
                "latency_ms",
                "raw_output",
                "final_output"
            ]
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "image_name": image_name,
            "prompt_version": prompt_version,
            "model_name": model_name,
            "predicted_class": final_output.get("predicted_class"),
            "confidence": final_output.get("confidence"),
            "latency_ms": latency_ms,
            "raw_output": json.dumps(raw_output, ensure_ascii=False),
            "final_output": json.dumps(final_output, ensure_ascii=False)
        })