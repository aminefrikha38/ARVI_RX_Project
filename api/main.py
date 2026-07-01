from fastapi import FastAPI

app = FastAPI(
    title="ARVI-RX API",
    description="API de démonstration pour le prototype pédagogique ARVI-RX.",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "project": "ARVI-RX",
        "status": "prototype pédagogique",
        "warning": "Ce projet ne constitue pas un dispositif médical."
    }