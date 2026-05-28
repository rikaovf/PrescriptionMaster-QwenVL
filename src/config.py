import os
import torch

# PATHS
BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(BASE_DIR)

IMAGES_DIR = os.path.join(
    ROOT_DIR,
    "images"
)

TEMP_DIR = os.path.join(
    ROOT_DIR,
    "temp"
)

OUTPUT_DIR = os.path.join(
    ROOT_DIR,
    "output"
)

HF_MODELS_DIR = os.path.join(
    BASE_DIR,
    "models"
)

# DATASET
DATASET_DIR = os.path.join(
    ROOT_DIR,
    "dataset"
)

DATASET_IMAGES_DIR = os.path.join(
    DATASET_DIR,
    "images"
)

DATASET_OCR_DIR = os.path.join(
    DATASET_DIR,
    "ocr_raw"
)

DATASET_LABELS_DIR = os.path.join(
    DATASET_DIR,
    "labels"
)

# CREATE DIRS
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

os.makedirs(DATASET_DIR, exist_ok=True)
os.makedirs(DATASET_IMAGES_DIR, exist_ok=True)
os.makedirs(DATASET_OCR_DIR, exist_ok=True)
os.makedirs(DATASET_LABELS_DIR, exist_ok=True)

# GPU
GPU_AVAILABLE = torch.cuda.is_available()