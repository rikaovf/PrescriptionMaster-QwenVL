import os
import pdfplumber

from pdf2image import convert_from_path

from config import TEMP_DIR

from helpers.image_helper import preprocess_image
from ocr.tesseract_engine import ocr_tesseract

def extract_text_from_pdf(pdf_path):

    texto_completo = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            texto = page.extract_text()

            if texto:
                texto_completo += texto + "\n"

    return texto_completo.strip()

def processar_pdf_ocr(pdf_path):

    imagens = convert_from_path(
        pdf_path,
        dpi=300
    )

    textos = []

    for i, page in enumerate(imagens):

        img_temp = os.path.join(
            TEMP_DIR,
            f"temp_page_{i}.png"
        )

        page.save(img_temp, "PNG")

        img_processada = preprocess_image(img_temp)

        texto = ocr_tesseract(img_processada)

        textos.append(texto)

        os.remove(img_temp)

    return "\n".join(textos)

def processar_pdf(pdf_path):

    texto_pdf = extract_text_from_pdf(pdf_path)

    if texto_pdf.strip():
        print("[INFO] PDF textual encontrado")
        return texto_pdf

    print("[INFO] PDF escaneado detectado")

    return processar_pdf_ocr(pdf_path)