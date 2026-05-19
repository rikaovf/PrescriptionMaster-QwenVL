from helpers.file_helper import (
    is_image,
    is_pdf
)

from ocr.easyocr_engine import ocr_easyocr

from pdf.pdf_processor import processar_pdf

def processar_arquivo(caminho):

    if is_image(caminho):

        print("[INFO] Processando imagem")

        return ocr_easyocr(caminho)

    elif is_pdf(caminho):

        print("[INFO] Processando PDF")

        return processar_pdf(caminho)

    return None