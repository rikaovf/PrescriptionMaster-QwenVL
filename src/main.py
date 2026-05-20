import os

from config import (
    IMAGES_DIR,
    OUTPUT_DIR
)

from services.file_processor import processar_arquivo

from helpers.json_helper import salvar_json
from helpers.file_helper import is_hidden_file
from llm.extractor import extrair_dados_receita

def salvar_resultado(nome_arquivo, texto):

    nome_saida = os.path.splitext(nome_arquivo)[0]

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

    print(f"[INFO] OCR salvo: {output_path}")

def main():

    arquivos = os.listdir(IMAGES_DIR)

    if not arquivos:

        print("[INFO] Nenhum arquivo encontrado")
        return

    for arquivo in arquivos:

        # adaptação para o MACOS ignorar arquivos de metadados.
        if is_hidden_file(arquivo):
            continue

        caminho = os.path.join(
            IMAGES_DIR,
            arquivo
        )

        try:

            print("\n================================================")
            print(f"[INFO] Arquivo: {arquivo}")
            print("================================================")

            # =================================================
            # OCR
            # =================================================

            texto_ocr = processar_arquivo(caminho)

            if not texto_ocr:

                print("[INFO] Arquivo ignorado")
                continue

            # =================================================
            # SALVA OCR
            # =================================================

            salvar_resultado(
                arquivo,
                texto_ocr
            )

            # =================================================
            # LLM
            # =================================================

            print("[INFO] Estruturando JSON")

            dados_estruturados = extrair_dados_receita(
                texto_ocr
            )

            if not dados_estruturados:

                print("[ERRO] Falha ao estruturar")
                continue

            # =================================================
            # JSON
            # =================================================

            salvar_json(
                arquivo,
                dados_estruturados
            )

            print("[INFO] Processo concluído")

        except Exception as e:

            print("\n[ERRO CRÍTICO]")
            print(str(e))

if __name__ == "__main__":
    main()