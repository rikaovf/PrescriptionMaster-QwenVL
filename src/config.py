import os
import torch

BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(BASE_DIR)

IMAGES_DIR = os.path.join(ROOT_DIR, "images")
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

GPU_AVAILABLE = torch.cuda.is_available()