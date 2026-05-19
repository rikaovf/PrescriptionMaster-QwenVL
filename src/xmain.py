import os
import cv2
import torch
import easyocr
import pdfplumber
import pytesseract

from pdf2image import convert_from_path

# =========================================================
# PATHS
# =========================================================

BASE_DIR = os.path.dirname(__file__)
ROOT_DIR = os.path.dirname(BASE_DIR)

IMAGES_DIR = os.path.join(ROOT_DIR, "images")
TEMP_DIR = os.path.join(ROOT_DIR, "temp")
OUTPUT_DIR = os.path.join(ROOT_DIR, "output")

# cria pastas automaticamente
os.makedirs(TEMP_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# =========================================================
# GPU
# =========================================================

GPU_AVAILABLE = torch.cuda.is_available()

print(f"[INFO] GPU disponível: {GPU_AVAILABLE}")

# =========================================================
# OCR
# =========================================================

reader = easyocr.Reader(
    ['pt'],
    gpu=GPU_AVAILABLE
)

# =========================================================
# HELPERS
# =========================================================

def is_image(file_path):
    extensoes = (
        '.png',
        '.jpg',
        '.jpeg',
        '.bmp',
        '.tiff'
    )

    return file_path.lower().endswith(extensoes)

def is_pdf(file_path):
    return file_path.lower().endswith('.pdf')

# =========================================================
# PREPROCESSAMENTO
# =========================================================

def preprocess_image(img_path):

    img = cv2.imread(img_path)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    # remove ruído
    denoise = cv2.fastNlMeansDenoising(gray)

    # blur leve
    blur = cv2.GaussianBlur(
        denoise,
        (3,3),
        0
    )

    # binarização
    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh

# =========================================================
# OCR TESSERACT
# =========================================================

def ocr_tesseract(img):

    config = r'--oem 3 --psm 6'

    texto = pytesseract.image_to_string(
        img,
        lang='por',
        config=config
    )

    return texto

# =========================================================
# OCR EASYOCR
# =========================================================

def ocr_easyocr(img_path):

    result = reader.readtext(img_path)

    texto = "\n".join(
        [r[1] for r in result]
    )

    return texto

# =========================================================
# PDF TEXTUAL
# =========================================================

def extract_text_from_pdf(pdf_path):

    texto_completo = ""

    with pdfplumber.open(pdf_path) as pdf:

        for page in pdf.pages:

            texto = page.extract_text()

            if texto:
                texto_completo += texto + "\n"

    return texto_completo.strip()

# =========================================================
# PDF OCR
# =========================================================

def processar_pdf_ocr(pdf_path):

    print(f"[INFO] Convertendo PDF em imagem: {pdf_path}")

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

        print(f"[INFO] OCR página {i}")

        texto = ocr_tesseract(img_processada)

        textos.append(texto)

        os.remove(img_temp)

    return "\n".join(textos)

# =========================================================
# PROCESSAMENTO PDF
# =========================================================

def processar_pdf(pdf_path):

    print(f"[INFO] Verificando PDF textual")

    texto_pdf = extract_text_from_pdf(pdf_path)

    # PDF já possui texto interno
    if texto_pdf.strip():

        print("[INFO] PDF textual encontrado")

        return texto_pdf

    # PDF escaneado
    print("[INFO] PDF escaneado detectado")

    return processar_pdf_ocr(pdf_path)

# =========================================================
# PROCESSAMENTO IMAGEM
# =========================================================

def processar_imagem(img_path):

    print(f"[INFO] Usando EasyOCR")

    return ocr_easyocr(img_path)

# =========================================================
# SALVAR RESULTADO
# =========================================================

def salvar_resultado(nome_arquivo, texto):

    nome_saida = os.path.splitext(nome_arquivo)[0]

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{nome_saida}.txt"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(texto)

    print(f"[INFO] Resultado salvo: {output_path}")

# =========================================================
# MAIN
# =========================================================

def main():

    arquivos = os.listdir(IMAGES_DIR)

    if not arquivos:
        print("[INFO] Nenhum arquivo encontrado")
        return

    for arquivo in arquivos:

        caminho = os.path.join(
            IMAGES_DIR,
            arquivo
        )

        try:

            # =================================================
            # IMAGEM
            # =================================================

            if is_image(caminho):

                print(f"\n📷 Processando imagem: {arquivo}")

                texto = processar_imagem(caminho)

            # =================================================
            # PDF
            # =================================================

            elif is_pdf(caminho):

                print(f"\n📄 Processando PDF: {arquivo}")

                texto = processar_pdf(caminho)

            # =================================================
            # IGNORADO
            # =================================================

            else:

                print(f"\n⚠️ Arquivo ignorado: {arquivo}")

                continue

            # =================================================
            # RESULTADO
            # =================================================

            print("\n--- TEXTO EXTRAÍDO ---")
            print(texto)
            print("----------------------\n")

            salvar_resultado(
                arquivo,
                texto
            )

        except Exception as e:

            print(f"\n[ERRO] {arquivo}")
            print(str(e))

# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()