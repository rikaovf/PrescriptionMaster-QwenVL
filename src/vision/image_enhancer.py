from PIL import (
    Image,
    ImageEnhance,
    ImageFilter
)


def melhorar_imagem(image: Image.Image) -> Image.Image:

    # ==================================================
    # 1. ESCALA 2X
    # ==================================================

    largura, altura = image.size

    image = image.resize(
        (
            largura * 2,
            altura * 2
        ),
        Image.Resampling.LANCZOS
    )

    # ==================================================
    # 2. ESCALA DE CINZA
    # ==================================================

    image = image.convert("L")

    # ==================================================
    # 3. CONTRASTE
    # ==================================================

    contraste = ImageEnhance.Contrast(image)

    image = contraste.enhance(2.0)

    # ==================================================
    # 4. NITIDEZ
    # ==================================================

    nitidez = ImageEnhance.Sharpness(image)

    image = nitidez.enhance(2.5)

    # ==================================================
    # 5. SHARPEN EXTRA
    # ==================================================

    image = image.filter(
        ImageFilter.SHARPEN
    )

    # ==================================================
    # 6. VOLTA PARA RGB
    # ==================================================

    image = image.convert("RGB")

    return image