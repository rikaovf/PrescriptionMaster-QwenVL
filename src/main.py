import os

from config import IMAGES_DIR, OUTPUT_DIR

from helpers.json_helper import salvar_json
from helpers.file_helper import is_hidden_file

# 🔥 PIPELINE NOVO (HUGGINGFACE QWEN-VL)
from vision.qwen_vl import extrair_texto_qwen
from llm.extractor import extrair_dados_receita


def salvar_resultado(nome_arquivo, texto):

    nome_saida = os.path.splitext(nome_arquivo)[0]

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{nome_saida}.txt"
    )

    with open(output_path, "w", encoding="utf-8") as f:
        f.write(texto)

    print(f"[INFO] Texto bruto salvo: {output_path}")


def main():

    arquivos = os.listdir(IMAGES_DIR)

    if not arquivos:
        print("[INFO] Nenhum arquivo encontrado")
        return

    print(f"[INFO] Total de arquivos: {len(arquivos)}")

    for arquivo in arquivos:

        # ignora arquivos ocultos do sistema
        if is_hidden_file(arquivo):
            continue

        caminho = os.path.join(IMAGES_DIR, arquivo)

        try:

            print("\n================================================")
            print(f"[PIPELINE] Processando: {arquivo}")
            print("================================================")

            # ============================================
            # ETAPA 1 - VISÃO (Qwen-VL HF)
            # ============================================
            print("[ETAPA 1] Qwen-VL extraindo texto...")

            texto = extrair_texto_qwen(caminho)

            if not texto or not texto.strip():
                print("[WARN] Nenhum texto extraído")
                continue

            print("[ETAPA 1] OK")

            # salva intermediário
            salvar_resultado(arquivo, texto)

            # ============================================
            # ETAPA 2 - EXTRAÇÃO ESTRUTURADA (LLM)
            # ============================================
            print("[ETAPA 2] Estruturando JSON com Qwen2.5...")

            json_resultado = extrair_dados_receita(texto)

            if not json_resultado:
                print("[ERRO] Falha ao estruturar JSON")
                continue

            print("[ETAPA 2] OK")

            # ============================================
            # ETAPA 3 - SALVAR RESULTADO FINAL
            # ============================================
            salvar_json(
                arquivo,
                json_resultado
            )

            print("[PIPELINE] Finalizado com sucesso")

        except Exception as e:

            print("\n[ERRO CRÍTICO]")
            print(f"Arquivo: {arquivo}")
            print(f"Erro: {str(e)}")


if __name__ == "__main__":
    main()