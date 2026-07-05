import sys
import time
from pathlib import Path


import pandas as pd
import streamlit as st

ROOT_DIR = Path(__file__).resolve().parents[1]
sys.path.append(str(ROOT_DIR))

from src.preprocessing import preprocess_image
from src.baseline import run_baseline_prediction
from src.guardrails import apply_guardrails
from src.logger import save_log
from src.database import save_prediction_sqlite


st.set_page_config(page_title="ClariRX", layout="wide")

st.title("ClariRX — Assistant radiologique virtuel responsable")

st.warning(
    "Position non clinique : ce prototype est uniquement pédagogique. "
    "Il ne constitue pas un dispositif médical et ne doit jamais être utilisé "
    "pour diagnostiquer, trier ou orienter un patient."
)

page = st.sidebar.radio(
    "Navigation",
    ["Analyse", "Logs", "Dashboard"]
)

if page == "Analyse":
    st.header("Analyse pédagogique d’une radiographie thoracique frontale")

    uploaded_file = st.file_uploader(
        "Dépose une image de radiographie thoracique frontale",
        type=["png", "jpg", "jpeg"]
    )

    if uploaded_file is not None:
        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Image uploadée")
            st.image(uploaded_file, use_container_width=True)

        with col2:
            st.subheader("Informations")
            st.write("Nom du fichier :", uploaded_file.name)

        if st.button("Lancer l’analyse baseline"):
            start_time = time.time()

            image, quality_info = preprocess_image(uploaded_file)
            raw_output = run_baseline_prediction(quality_info)
            final_output = apply_guardrails(raw_output, quality_info)

            latency_ms = round((time.time() - start_time) * 1000, 2)

            save_log(
                image_name=uploaded_file.name,
                prompt_version="baseline_prompt_v1",
                model_name="toy_baseline_v1",
                latency_ms=latency_ms,
                raw_output=raw_output,
                final_output=final_output
            )

            save_prediction_sqlite(
                image_name=uploaded_file.name,
                prompt_version="baseline_prompt_v1",
                model_name="toy_baseline_v1",
                latency_ms=latency_ms,
                raw_output=raw_output,
                final_output=final_output
            )

            st.subheader("Contrôle qualité image")
            st.json(quality_info)

            st.subheader("Sortie JSON structurée")
            st.json(final_output)

            st.info(f"Latence : {latency_ms} ms")

elif page == "Logs":
    st.header("Journalisation des prédictions")

    log_path = Path("outputs/logs.csv")

    if log_path.exists():
        df = pd.read_csv(log_path)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Aucun log disponible pour l’instant. Lance d’abord une analyse.")

elif page == "Dashboard":
    st.header("Dashboard d’évaluation")

    summary_path = Path("data/results/comparison_summary.csv")
    baseline_path = Path("data/results/results_baseline.csv")
    improved_path = Path("data/results/results_improved.csv")

    if summary_path.exists():
        summary_df = pd.read_csv(summary_path)

        st.subheader("Comparaison baseline vs version améliorée")
        st.dataframe(summary_df, use_container_width=True)

        st.subheader("Métriques principales")

        for _, row in summary_df.iterrows():
            st.markdown(f"### {row['model_name']}")

            col1, col2, col3, col4 = st.columns(4)

            col1.metric("Accuracy", row["accuracy"])
            col2.metric("Macro-F1", row["macro_f1"])
            col3.metric("Taux d'incertitude", row["uncertain_rate"])
            col4.metric("Latence moyenne", row["avg_latency_ms"])

            st.write("Faux positifs :", row["false_positives"])
            st.write("Faux négatifs :", row["false_negatives"])
            st.write("Validité JSON :", row["json_validity"])

    else:
        st.info(
            "Aucun résultat de comparaison disponible. "
            "Lance d’abord : python eval\\run_comparison.py"
        )

    if baseline_path.exists():
        st.subheader("Résultats détaillés baseline")
        st.dataframe(pd.read_csv(baseline_path), use_container_width=True)

    if improved_path.exists():
        st.subheader("Résultats détaillés version améliorée")
        st.dataframe(pd.read_csv(improved_path), use_container_width=True)