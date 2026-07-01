from PIL import Image
import numpy as np


def preprocess_image(uploaded_file):
    """
    Prétraitement minimal :
    - ouverture image
    - conversion RGB
    - redimensionnement
    - calcul luminosité/contraste
    - qualité image simple
    """

    image = Image.open(uploaded_file).convert("RGB")
    image = image.resize((512, 512))

    arr = np.array(image) / 255.0

    mean_intensity = float(arr.mean())
    contrast = float(arr.std())

    if mean_intensity < 0.05 or mean_intensity > 0.95 or contrast < 0.05:
        image_quality = "poor"
    elif contrast < 0.12:
        image_quality = "limited"
    else:
        image_quality = "good"

    quality_info = {
        "image_quality": image_quality,
        "mean_intensity": round(mean_intensity, 4),
        "contrast": round(contrast, 4),
        "width": image.size[0],
        "height": image.size[1]
    }

    return image, quality_info