def run_baseline_prediction(quality_info):
    """
    Baseline jouet reproductible.
    Elle ne fait pas encore de vrai diagnostic visuel.
    Elle sert à tester la chaîne complète :
    image -> prédiction -> JSON -> garde-fous -> logs -> évaluation.
    """

    image_quality = quality_info["image_quality"]

    if image_quality == "poor":
        predicted_class = "uncertain"
        confidence = 0.35
        visual_evidence = ["Image quality is too low for a reliable educational interpretation."]
        justification = "The image quality is insufficient, so the safest output is uncertain."

    elif image_quality == "limited":
        predicted_class = "uncertain"
        confidence = 0.50
        visual_evidence = ["Limited contrast or ambiguous visual information."]
        justification = "The image contains limited information, so the system avoids a confident classification."

    else:
        predicted_class = "normal"
        confidence = 0.65
        visual_evidence = ["No obvious opacity pattern detected by the baseline heuristic."]
        justification = "The baseline does not detect obvious suspicious visual evidence."

    return {
        "image_quality": image_quality,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "visual_evidence": visual_evidence,
        "justification": justification,
        "limitations": [
            "Baseline pédagogique simple.",
            "Ne remplace pas une analyse médicale.",
            "Ne détecte pas réellement toutes les anomalies."
        ],
        "warning": "Prototype pédagogique uniquement. Cette sortie ne constitue pas un diagnostic médical."
    }