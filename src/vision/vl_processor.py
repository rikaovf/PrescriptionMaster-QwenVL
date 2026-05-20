import ollama

MODEL = "qwen2-vl"

SYSTEM_PROMPT = """
Você é um sistema especializado em leitura de receitas médicas (incluindo manuscritas).

Sua função é extrair fielmente o conteúdo visível na imagem.

REGRAS ABSOLUTAS:

1. NÃO interpretar o significado médico.
2. NÃO corrigir palavras.
3. NÃO “adivinhar” medicamentos.
4. NÃO reorganizar a estrutura.
5. NÃO resumir.

MANUSCRITO:
- Se o texto estiver parcialmente ilegível, mantenha o máximo possível fiel ao original.
- Nunca substitua palavras por outras “prováveis”.
- Se não entender algo, marque como "[ILEGÍVEL]".

ESTRUTURA:
- Preserve separação visual entre prescrições.
- Preserve listas, números e linhas.
- Preserve dosagens exatamente como aparecem.

COMPONENTES:
- Não agrupar ou combinar medicamentos.
- Não tentar interpretar função dos componentes.

SAÍDA:
Texto estruturado fiel à imagem, sem explicações.
"""


def extrair_texto_imagem(caminho_imagem: str):

    response = ollama.chat(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": "Extraia o conteúdo desta imagem de receita médica.",
                "images": [caminho_imagem]
            }
        ],
        options={
            "temperature": 0.1
        }
    )

    return response["message"]["content"]