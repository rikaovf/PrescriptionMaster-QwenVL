import os

from config import (
    IMAGES_DIR,
    OUTPUT_DIR,
    TEMP_DIR
)

from helpers.json_helper import salvar_json

from helpers.file_helper import (
    is_hidden_file,
    is_pdf,
    is_image,
    pdf_to_images
)

from vision.qwen_vl import extrair_texto_qwen
from llm.extractor import extrair_dados_receita


# =========================================================
# SALVAR TEXTO BRUTO
# =========================================================

def salvar_resultado(nome_arquivo, texto):

    nome_saida = os.path.splitext(nome_arquivo)[0]

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{nome_saida}.txt"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"[INFO] Texto bruto salvo: {output_path}")


# =========================================================
# MAIN
# =========================================================

def main():

    arquivos = os.listdir(IMAGES_DIR)

    if not arquivos:
        print("[INFO] Nenhum arquivo encontrado")
        return

    print(f"[INFO] Total de arquivos: {len(arquivos)}")

    for arquivo in arquivos:

        # ignora arquivos ocultos
        if is_hidden_file(arquivo):
            continue

        caminho = os.path.join(
            IMAGES_DIR,
            arquivo
        )

        try:

            print("\n================================================")
            print(f"[PIPELINE] Processando: {arquivo}")
            print("================================================")

            texto_final = ""

            # =================================================
            # PDF
            # =================================================

            if is_pdf(caminho):

                print("[INFO] PDF detectado")

                imagens = pdf_to_images(
                    caminho,
                    TEMP_DIR
                )

                for imagem in imagens:

                    texto_pagina = extrair_texto_qwen(
                        imagem
                    )

                    texto_final += (
                        texto_pagina + "\n\n"
                    )

                    # remove imagem temporária
                    os.remove(imagem)

            # =================================================
            # IMAGEM
            # =================================================

            elif is_image(caminho):

                print("[INFO] Imagem detectada")

                texto_final = extrair_texto_qwen(
                    caminho
                )

            # =================================================
            # FORMATO INVÁLIDO
            # =================================================

            else:

                print(
                    f"[WARNING] Formato não suportado: {arquivo}"
                )

                continue

            # =================================================
            # TEXTO VAZIO
            # =================================================

            if not texto_final.strip():

                print("[WARN] Nenhum texto extraído")

                continue

            print("[ETAPA 1] OK")

            # =================================================
            # SALVA OCR BRUTO
            # =================================================

            salvar_resultado(
                arquivo,
                texto_final
            )

            # =================================================
            # ETAPA 2 - LLM
            # =================================================

            # json_resultado = extrair_dados_receita(
            #     texto_final
            # )

            # salvar_json(
            #     arquivo,
            #     json_resultado
            # )

            print("[PIPELINE] Finalizado com sucesso")

        except Exception as e:

            print("\n[ERRO CRÍTICO]")
            print(f"Arquivo: {arquivo}")
            print(f"Erro: {str(e)}")


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()