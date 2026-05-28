import os
import json
import shutil

from config import (
    DATASET_IMAGES_DIR,
    DATASET_OCR_DIR,
    DATASET_LABELS_DIR
)

# =========================================================
# COPY IMAGE
# =========================================================

def salvar_dataset_imagem(
    arquivo_original,
    caminho_original
):

    destino = os.path.join(
        DATASET_IMAGES_DIR,
        arquivo_original
    )

    shutil.copy2(
        caminho_original,
        destino
    )

# =========================================================
# SAVE OCR RAW
# =========================================================

def salvar_dataset_ocr(
    nome_arquivo,
    texto
):

    nome_saida = (
        os.path.splitext(nome_arquivo)[0]
        + ".txt"
    )

    destino = os.path.join(
        DATASET_OCR_DIR,
        nome_saida
    )

    with open(
        destino,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(texto)

# =========================================================
# SAVE LABEL JSON
# =========================================================

def salvar_dataset_json(
    nome_arquivo,
    json_resultado
):

    nome_saida = (
        os.path.splitext(nome_arquivo)[0]
        + ".json"
    )

    destino = os.path.join(
        DATASET_LABELS_DIR,
        nome_saida
    )

    with open(
        destino,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            json_resultado,
            f,
            ensure_ascii=False,
            indent=2
        )