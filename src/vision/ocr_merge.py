def merge_ocr_resultados(resultados):

    textos_unicos = []

    vistos = set()

    for texto in resultados:

        linhas = texto.splitlines()

        for linha in linhas:

            linha = linha.strip()

            if not linha:
                continue

            chave = linha.lower()

            if chave in vistos:
                continue

            vistos.add(chave)

            textos_unicos.append(linha)

    return "\n".join(textos_unicos)