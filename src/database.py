import sqlite3
import json
import time
from pathlib import Path

DB_PATH = Path("outputs/predictions.db")


def init_db():
    DB_PATH.parent.mkdir(exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS predictions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            image_name TEXT,
            prompt_version TEXT,
            model_name TEXT,
            predicted_class TEXT,
            confidence REAL,
            image_quality TEXT,
            latency_ms REAL,
            raw_output TEXT,
            final_output TEXT
        )
    """)

    conn.commit()
    conn.close()


def save_prediction_sqlite(
    image_name,
    prompt_version,
    model_name,
    latency_ms,
    raw_output,
    final_output
):
    init_db()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO predictions (
            timestamp,
            image_name,
            prompt_version,
            model_name,
            predicted_class,
            confidence,
            image_quality,
            latency_ms,
            raw_output,
            final_output
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        time.strftime("%Y-%m-%d %H:%M:%S"),
        image_name,
        prompt_version,
        model_name,
        final_output.get("predicted_class"),
        final_output.get("confidence"),
        final_output.get("image_quality"),
        latency_ms,
        json.dumps(raw_output, ensure_ascii=False),
        json.dumps(final_output, ensure_ascii=False)
    ))

    conn.commit()
    conn.close()