import os

from config import (
    IMAGES_DIR,
    OUTPUT_DIR,
    TEMP_DIR
)

from helpers.json_helper import salvar_json

from helpers.dataset_helper import (
    salvar_dataset_imagem,
    salvar_dataset_ocr,
    salvar_dataset_json
)

from helpers.file_helper import (
    is_hidden_file,
    is_pdf,
    is_image,
    pdf_to_images
)

from vision.qwen_vl import extrair_texto_qwen
from llm.extractor import extrair_dados_receita

from erp.normalizer import (
    normalizar_receita
)

# =========================================================
# SAVE OCR OUTPUT
# =========================================================

def salvar_resultado(
    nome_arquivo,
    texto
):

    nome_saida = os.path.splitext(
        nome_arquivo
    )[0]

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{nome_saida}.txt"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        f.write(texto)

    print(
        f"[INFO] Texto bruto salvo: {output_path}"
    )


# =========================================================
# MAIN
# =========================================================

def main():

    arquivos = os.listdir(
        IMAGES_DIR
    )

    if not arquivos:

        print(
            "[INFO] Nenhum arquivo encontrado"
        )

        return

    print(
        f"[INFO] Total de arquivos: {len(arquivos)}"
    )

    for arquivo in arquivos:

        # ignora ocultos
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

                print(
                    "[INFO] PDF detectado"
                )

                imagens = pdf_to_images(
                    caminho,
                    TEMP_DIR
                )

                for imagem in imagens:

                    texto_pagina = (
                        extrair_texto_qwen(
                            imagem
                        )
                    )

                    texto_final += (
                        texto_pagina + "\n\n"
                    )

                    # remove temp
                    os.remove(imagem)

            # =================================================
            # IMAGE
            # =================================================

            elif is_image(caminho):

                print(
                    "[INFO] Imagem detectada"
                )

                texto_final = (
                    extrair_texto_qwen(
                        caminho
                    )
                )

            # =================================================
            # INVALID
            # =================================================

            else:

                print(
                    f"[WARNING] Formato não suportado: {arquivo}"
                )

                continue

            # =================================================
            # EMPTY OCR
            # =================================================

            if not texto_final.strip():

                print(
                    "[WARN] Nenhum texto extraído"
                )

                continue

            print(
                "[ETAPA 1] OCR OK"
            )

            # =================================================
            # SAVE OCR OUTPUT
            # =================================================

            salvar_resultado(
                arquivo,
                texto_final
            )

            # =================================================
            # SAVE DATASET RAW
            # =================================================

            salvar_dataset_imagem(
                arquivo,
                caminho
            )

            salvar_dataset_ocr(
                arquivo,
                texto_final
            )

            # =================================================
            # LLM STRUCTURE
            # =================================================

            print(
                "[ETAPA 2] Estruturando JSON..."
            )

            json_resultado = (
                extrair_dados_receita(
                    texto_final
                )
            )

            # =================================================
            # ERP NORMALIZER
            # =================================================

            print(
                "[ETAPA 3] Normalizando ERP..."
            )

            json_resultado = normalizar_receita(
                json_resultado
            )

            print(
                "[ETAPA 3] ERP OK"
            )

            if not json_resultado:

                print(
                    "[ERRO] Falha ao estruturar JSON"
                )

                continue

            print(
                "[ETAPA 2] JSON OK"
            )

            # =================================================
            # SAVE JSON
            # =================================================

            salvar_json(
                arquivo,
                json_resultado
            )

            salvar_dataset_json(
                arquivo,
                json_resultado
            )

            print(
                "[PIPELINE] Finalizado com sucesso"
            )

        except Exception as e:

            print("\n[ERRO CRÍTICO]")
            print(f"Arquivo: {arquivo}")
            print(f"Erro: {str(e)}")


# =========================================================
# START
# =========================================================

if __name__ == "__main__":
    main()