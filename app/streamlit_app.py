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


st.set_page_config(page_title="ARVI-RX", layout="wide")

st.title("ARVI-RX — Assistant radiologique virtuel responsable")

st.warning(
    "Position non clinique : ce prototype est uniquement pédagogique. "
    "Il ne constitue pas un dispositif médical et ne doit jamais être utilisé "
    "pour diagnostiquer, trier ou orienter un patient."
)

page = st.sidebar.radio(
    "Navigation",
    ["Analyse", "Logs"]
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