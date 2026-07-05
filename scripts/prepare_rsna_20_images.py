from pathlib import Path
import shutil
import pandas as pd
from PIL import Image, ImageEnhance, ImageFilter


# =========================
# À ADAPTER SI BESOIN
# =========================

DATASET_DIR = Path(r"C:\Users\amine\Downloads\archive (1)")
PROJECT_DIR = Path(r"C:\Users\amine\PycharmProjects\ARVI_RX_Project")

TRAIN_METADATA = DATASET_DIR / "stage2_train_metadata.csv"
TRAINING_DIR = DATASET_DIR / "Training"

OUTPUT_IMG_DIR = PROJECT_DIR / "data" / "sample_images"
OUTPUT_CSV = PROJECT_DIR / "data" / "cases.csv"

OUTPUT_IMG_DIR.mkdir(parents=True, exist_ok=True)


# =========================
# LECTURE DU CSV
# =========================

df = pd.read_csv(TRAIN_METADATA)

print("Colonnes trouvées :")
print(df.columns)
print(df.head())

# On cherche automatiquement les colonnes importantes
possible_id_cols = ["patientId", "patient_id", "id", "filename", "image_name", "image"]
possible_label_cols = ["Target", "target", "label", "class"]

id_col = None
label_col = None

for col in possible_id_cols:
    if col in df.columns:
        id_col = col
        break

for col in possible_label_cols:
    if col in df.columns:
        label_col = col
        break

if id_col is None:
    raise ValueError("Impossible de trouver la colonne d'identifiant image.")

if label_col is None:
    raise ValueError("Impossible de trouver la colonne de label / Target.")

print("Colonne image utilisée :", id_col)
print("Colonne label utilisée :", label_col)

# On enlève les doublons éventuels
df = df.drop_duplicates(subset=[id_col])


# =========================
# SÉLECTION DES CAS
# =========================

normal_df = df[df[label_col] == 0].head(8)
opacity_df = df[df[label_col] == 1].head(8)

# Pour uncertain, on prend 4 images normales ou opacité et on les dégrade
uncertain_df = df.head(4)

selected_cases = []


def find_image(image_id):
    image_id = str(image_id)

    possible_names = [
        image_id,
        image_id + ".png",
        image_id + ".jpg",
        image_id + ".jpeg"
    ]

    for name in possible_names:
        matches = list(TRAINING_DIR.rglob(name))
        if matches:
            return matches[0]

    matches = list(TRAINING_DIR.rglob(f"*{image_id}*"))
    if matches:
        return matches[0]

    return None


def copy_case(row, counter, true_label, comment):
    image_id = row[id_col]
    image_path = find_image(image_id)

    if image_path is None:
        print(f"Image introuvable pour : {image_id}")
        return None

    new_name = f"case_{counter:03d}.png"
    output_path = OUTPUT_IMG_DIR / new_name

    img = Image.open(image_path).convert("RGB")
    img.save(output_path)

    return {
        "case_id": f"case_{counter:03d}",
        "image_name": new_name,
        "true_label": true_label,
        "comment": comment
    }


def create_uncertain_case(row, counter):
    image_id = row[id_col]
    image_path = find_image(image_id)

    if image_path is None:
        print(f"Image introuvable pour uncertain : {image_id}")
        return None

    new_name = f"case_{counter:03d}.png"
    output_path = OUTPUT_IMG_DIR / new_name

    img = Image.open(image_path).convert("RGB")
    img = img.resize((512, 512))

    # Dégradation volontaire : faible contraste + sombre + flou
    img = ImageEnhance.Contrast(img).enhance(0.35)
    img = ImageEnhance.Brightness(img).enhance(0.45)
    img = img.filter(ImageFilter.GaussianBlur(radius=2))

    img.save(output_path)

    return {
        "case_id": f"case_{counter:03d}",
        "image_name": new_name,
        "true_label": "uncertain",
        "comment": "Image volontairement dégradée pour tester la classe uncertain"
    }


counter = 1

for _, row in normal_df.iterrows():
    case = copy_case(
        row,
        counter,
        "normal",
        "Cas normal issu du dataset RSNA Training"
    )
    if case:
        selected_cases.append(case)
        counter += 1

for _, row in opacity_df.iterrows():
    case = copy_case(
        row,
        counter,
        "suspected_opacity",
        "Cas avec opacité annotée dans le dataset RSNA Training"
    )
    if case:
        selected_cases.append(case)
        counter += 1

for _, row in uncertain_df.iterrows():
    case = create_uncertain_case(row, counter)
    if case:
        selected_cases.append(case)
        counter += 1


# =========================
# SAUVEGARDE cases.csv
# =========================

cases_df = pd.DataFrame(selected_cases)
cases_df.to_csv(OUTPUT_CSV, index=False, encoding="utf-8")

print()
print("Terminé.")
print(f"{len(cases_df)} images copiées dans : {OUTPUT_IMG_DIR}")
print(f"Fichier cases.csv créé : {OUTPUT_CSV}")
print()
print(cases_df)