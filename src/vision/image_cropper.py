from PIL import Image

from vision.image_enhancer import (
    melhorar_imagem
)


def gerar_crops(image_path: str):

    image = Image.open(
        image_path
    ).convert("RGB")

    image = melhorar_imagem(image)

    largura, altura = image.size

    limite_topo = int(altura * 0.25)

    limite_rodape = int(altura * 0.75)

    topo = image.crop(
        (
            0,
            0,
            largura,
            limite_topo
        )
    )

    centro = image.crop(
        (
            0,
            limite_topo,
            largura,
            limite_rodape
        )
    )

    rodape = image.crop(
        (
            0,
            limite_rodape,
            largura,
            altura
        )
    )

    return {

        # NOVO
        "pagina_completa": image,

        "topo": topo,

        "centro": centro,

        "rodape": rodape
    }