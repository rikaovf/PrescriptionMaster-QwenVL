from vision.qwen_vl import extrair_texto_qwen
from vision.fallback_ocr import extrair_texto_fallback
from llm.extractor import extrair_dados_receita


def processar_receita(image_path: str):

    texto = ""

    # =========================
    # TENTA QWEN-VL PRIMEIRO
    # =========================
    try:
        print("[INFO] Usando Qwen-VL")
        texto = extrair_texto_qwen(image_path)

    except Exception as e:
        print("[WARN] Qwen-VL falhou, usando OCR fallback")
        print(str(e))

        # =========================
        # FALLBACK OCR
        # =========================
        texto = extrair_texto_fallback(image_path)

    # =========================
    # EXTRACTOR JSON (SEU MODELO ATUAL)
    # =========================
    json_final = extrair_dados_receita(texto)

    return json_final