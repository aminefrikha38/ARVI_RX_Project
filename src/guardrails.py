from pydantic import ValidationError
from src.schemas import PredictionOutput


FORBIDDEN_MEDICAL_TERMS = [
    "pneumonie",
    "cancer",
    "tumeur",
    "tuberculose",
    "infection grave",
    "vous avez",
    "le patient a",
    "il faut prendre",
    "traitement recommandé"
]


def force_uncertain(reason):
    return {
        "image_quality": "poor",
        "predicted_class": "uncertain",
        "confidence": 0.0,
        "visual_evidence": [],
        "justification": reason,
        "limitations": [reason],
        "warning": "Prototype pédagogique uniquement. Cette sortie ne constitue pas un diagnostic médical."
    }


def contains_forbidden_terms(result):
    text = str(result).lower()
    return any(term in text for term in FORBIDDEN_MEDICAL_TERMS)


def apply_guardrails(result, quality_info):
    """
    Garde-fous :
    - JSON conforme au schéma
    - classes autorisées
    - confiance minimale
    - incertitude si image pauvre
    - warning obligatoire
    - blocage des termes médicaux trop affirmatifs
    """

    try:
        PredictionOutput(**result)
    except ValidationError:
        return force_uncertain("Sortie JSON invalide ou non conforme au schéma attendu.")

    if contains_forbidden_terms(result):
        return force_uncertain("Sortie rejetée : formulation trop clinique ou hors périmètre pédagogique.")

    if quality_info["image_quality"] == "poor":
        result["predicted_class"] = "uncertain"
        result["confidence"] = min(result["confidence"], 0.5)
        result["limitations"].append("Qualité d’image insuffisante.")

    if result["confidence"] < 0.60:
        result["predicted_class"] = "uncertain"
        result["limitations"].append("Confiance trop faible pour conclure.")

    result["warning"] = "Prototype pédagogique uniquement. Cette sortie ne constitue pas un diagnostic médical."

    return result