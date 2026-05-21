import cv2
import pytesseract
from PIL import Image


def preprocess(image_path: str):

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    return thresh


def extrair_texto_fallback(image_path: str):

    img = preprocess(image_path)

    pil_img = Image.fromarray(img)

    config = "--oem 3 --psm 6"

    return pytesseract.image_to_string(
        pil_img,
        lang="por",
        config=config
    )