import pytesseract

def ocr_tesseract(img):

    config = r'--oem 3 --psm 6'

    texto = pytesseract.image_to_string(
        img,
        lang='por',
        config=config
    )

    return texto