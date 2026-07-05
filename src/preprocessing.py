from PIL import Image
import numpy as np


def preprocess_image(uploaded_file):
    """
    Prétraitement minimal :
    - ouverture image
    - conversion RGB
    - redimensionnement
    - calcul qualité image
    - calcul d'un score visuel simple d'opacité
    """

    image = Image.open(uploaded_file).convert("RGB")
    image = image.resize((512, 512))

    arr = np.array(image) / 255.0
    gray = np.array(image.convert("L")) / 255.0

    mean_intensity = float(arr.mean())
    contrast = float(arr.std())

    if mean_intensity < 0.05 or mean_intensity > 0.95 or contrast < 0.05:
        image_quality = "poor"
    elif contrast < 0.12:
        image_quality = "limited"
    else:
        image_quality = "good"

    # Zone centrale approximative du thorax
    h, w = gray.shape
    y1, y2 = int(0.18 * h), int(0.88 * h)
    x1, x2 = int(0.12 * w), int(0.88 * w)
    thorax_zone = gray[y1:y2, x1:x2]

    mid = thorax_zone.shape[1] // 2
    left_zone = thorax_zone[:, :mid]
    right_zone = thorax_zone[:, mid:]

    bright_ratio = float((thorax_zone > 0.62).mean())
    asymmetry = float(abs(left_zone.mean() - right_zone.mean()))

    # Score simple : plus il y a de zones claires/asymétriques, plus le score augmente
    opacity_score = float((0.7 * bright_ratio) + (2.0 * asymmetry))

    quality_info = {
        "image_quality": image_quality,
        "mean_intensity": round(mean_intensity, 4),
        "contrast": round(contrast, 4),
        "bright_ratio": round(bright_ratio, 4),
        "asymmetry": round(asymmetry, 4),
        "opacity_score": round(opacity_score, 4),
        "width": image.size[0],
        "height": image.size[1]
    }

    return image, quality_info