import cv2

def preprocess_image(img_path):

    img = cv2.imread(img_path)

    gray = cv2.cvtColor(
        img,
        cv2.COLOR_BGR2GRAY
    )

    denoise = cv2.fastNlMeansDenoising(gray)

    blur = cv2.GaussianBlur(
        denoise,
        (3,3),
        0
    )

    _, thresh = cv2.threshold(
        blur,
        0,
        255,
        cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    return thresh