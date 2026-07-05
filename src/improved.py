def run_improved_prediction(quality_info):
    """
    Version améliorée de la baseline.

    Objectif :
    - être plus prudente
    - réduire les faux positifs
    - utiliser davantage la classe uncertain si le signal est ambigu
    """

    image_quality = quality_info["image_quality"]
    opacity_score = quality_info.get("opacity_score", 0)
    bright_ratio = quality_info.get("bright_ratio", 0)
    asymmetry = quality_info.get("asymmetry", 0)

    if image_quality == "poor":
        predicted_class = "uncertain"
        confidence = 0.35
        visual_evidence = [
            "Image quality is too low for a reliable educational interpretation."
        ]
        justification = "The image quality is insufficient, so the safest output is uncertain."

    elif image_quality == "limited":
        predicted_class = "uncertain"
        confidence = 0.50
        visual_evidence = [
            "Limited contrast or ambiguous visual information."
        ]
        justification = "The image contains limited information, so the system avoids a confident classification."

    elif opacity_score >= 0.12 and (bright_ratio >= 0.10 or asymmetry >= 0.04):
        predicted_class = "suspected_opacity"
        confidence = 0.72
        visual_evidence = [
            f"Opacity heuristic score: {round(opacity_score, 4)}",
            f"Bright area ratio: {round(bright_ratio, 4)}",
            f"Left/right asymmetry: {round(asymmetry, 4)}"
        ]
        justification = (
            "The improved baseline detects a stronger visual pattern compatible "
            "with a suspected opacity. This remains an educational heuristic."
        )

    elif opacity_score >= 0.07:
        predicted_class = "uncertain"
        confidence = 0.55
        visual_evidence = [
            f"Borderline opacity heuristic score: {round(opacity_score, 4)}"
        ]
        justification = (
            "The visual signal is borderline. The improved version chooses uncertainty "
            "instead of producing an overconfident prediction."
        )

    else:
        predicted_class = "normal"
        confidence = 0.68
        visual_evidence = [
            "No strong opacity pattern detected by the improved heuristic."
        ]
        justification = (
            "The improved baseline does not detect sufficient visual evidence "
            "for suspected opacity."
        )

    return {
        "image_quality": image_quality,
        "predicted_class": predicted_class,
        "confidence": confidence,
        "visual_evidence": visual_evidence,
        "justification": justification,
        "limitations": [
            "Improved baseline pédagogique.",
            "Ne remplace pas une analyse médicale.",
            "Utilise une heuristique expérimentale.",
            "Privilégie l'incertitude en cas de signal faible."
        ],
        "warning": "Prototype pédagogique uniquement. Cette sortie ne constitue pas un diagnostic médical."
    }