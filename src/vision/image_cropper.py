from PIL import Image


def gerar_crops(image_path: str):

    image = Image.open(image_path).convert("RGB")

    largura, altura = image.size

    # =====================================================
    # REGIÕES
    # =====================================================

    topo = image.crop((
        0,
        0,
        largura,
        int(altura * 0.20)
    ))

    centro = image.crop((
        0,
        int(altura * 0.20),
        largura,
        int(altura * 0.80)
    ))

    rodape = image.crop((
        0,
        int(altura * 0.80),
        largura,
        altura
    ))

    return {
        "topo": topo,
        "centro": centro,
        "rodape": rodape
    }