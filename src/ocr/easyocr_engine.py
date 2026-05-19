import easyocr

from config import GPU_AVAILABLE

reader = easyocr.Reader(
    ['pt'],
    gpu=GPU_AVAILABLE
)

def ocr_easyocr(img_path):

    result = reader.readtext(img_path)

    texto = "\n".join(
        [r[1] for r in result]
    )

    return texto