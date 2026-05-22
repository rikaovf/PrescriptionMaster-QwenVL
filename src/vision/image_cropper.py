from PIL import Image


def gerar_crops(image_path: str):

    image = Image.open(image_path).convert("RGB")

    largura, altura = image.size

    limite_topo = int(altura * 0.25)
    limite_rodape = int(altura * 0.75)

    topo = image.crop((
        0,
        0,
        largura,
        limite_topo
    ))

    centro = image.crop((
        0,
        limite_topo,
        largura,
        limite_rodape
    ))

    rodape = image.crop((
        0,
        limite_rodape,
        largura,
        altura
    ))

    return {
        "topo": topo,
        "centro": centro,
        "rodape": rodape
    }