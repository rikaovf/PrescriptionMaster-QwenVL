import json
import ollama
from prompts.llm_prompt import PROMPT

MODEL_NAME = "qwen2.5"

def montar_prompt(texto_ocr: str) -> str:
    return f"""
TEXTO OCR DA RECEITA MÉDICA:

{texto_ocr}

INSTRUÇÕES:
- Extraia todas as prescrições da imagem.
- Cada fórmula deve ser separada corretamente.
- Não invente dados.
- Retorne apenas JSON válido.
"""


def validar_json(texto: str):
    try:
        return json.loads(texto)
    except json.JSONDecodeError:
        return None


# 🔥 FUNÇÃO QUE O SEU MAIN JÁ USA (NÃO PODE MUDAR O NOME)
def extrair_dados_receita(texto_ocr: str):
    """
    Função principal usada pelo sistema.
    NÃO ALTERAR NOME (compatibilidade com main.py)
    """

    response = ollama.chat(
        model=MODEL_NAME,

        messages=[
            {
                "role": "system",
                "content": PROMPT
            },
            {
                "role": "user",
                "content": montar_prompt(texto_ocr)
            }
        ],

        options={
            "temperature": 0.1
        },

        format="json"
    )

    output = response["message"]["content"]

    dados = validar_json(output)

    if not dados:
        print("[ERRO] JSON inválido retornado pelo LLM")
        print(output)
        return None

    return dados