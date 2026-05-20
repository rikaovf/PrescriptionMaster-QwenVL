import json
import ollama

MODEL_NAME = "qwen2.5"


SYSTEM_PROMPT = """
Você é um especialista farmacêutico em interpretação de receitas médicas manipuladas.

Sua função é analisar textos OCR de receitas médicas e retornar APENAS um JSON válido estruturado.

────────────────────────────────────────
REGRAS GERAIS
────────────────────────────────────────

- Nunca invente informações.
- Se não encontrar algo, use null.
- OCR pode conter erros de escrita.
- Retorne APENAS JSON válido.
- Não use markdown.
- Não use explicações.
- Não use ```json.

────────────────────────────────────────
REGRA CRÍTICA: IDENTIFICAÇÃO DE FÓRMULAS
────────────────────────────────────────

Uma receita pode conter múltiplas fórmulas.

CASO 1 — FÓRMULAS ENUMERADAS:
Se o texto contiver:
- "1 - Prescrição"
- "2 -"
- "3."
- "Rx 1", "Rx 2"

ENTÃO:
Cada número representa UMA fórmula independente.
Cada bloco numerado deve ser separado corretamente no array "formulas".
Se na mesma linha houver o símbolo de "+", ou ",", não significa que é outra formula, e sim mais um componente da mesma fórmula, então neste caso considere as regras de componentes.

CASO 2 — SEM NUMERAÇÃO:
Se NÃO houver numeração clara:
- Identifique mudanças de contexto farmacêutico.
- Mudança de tipo (creme, cápsula, solução, shampoo)
- Mudança de posologia
- Separação visual no OCR

Cada mudança indica uma NOVA fórmula.

────────────────────────────────────────
REGRA DE COMPONENTES (MUITO IMPORTANTE)
────────────────────────────────────────

Para cada fórmula:

- Identifique apenas INSUMOS / matérias-primas farmacêuticas como "componentes".
- Exemplos de componentes:
  - princípios ativos
  - substâncias manipuláveis
  - drogas farmacêuticas
  - excipientes quando claramente parte da fórmula

- NÃO considere como componente:
  - instruções de uso
  - posologia
  - observações clínicas
  - modo de aplicar
  - recomendações ao paciente

────────────────────────────────────────
REGRA DE OBSERVAÇÕES
────────────────────────────────────────

Se existir qualquer informação que NÃO seja componente ou posologia, mas esteja ligada à fórmula, coloque em:

"observacao": ""

Exemplos de observações:
- "uso tópico apenas"
- "agitar antes de usar"
- "manter refrigerado"
- "uso contínuo por 30 dias"
- instruções adicionais do médico

────────────────────────────────────────
REGRA DE ESTRUTURA
────────────────────────────────────────

Cada fórmula deve conter:

- tipo_formula
- posologia
- qsp
- componentes
- observacao (se existir)

────────────────────────────────────────
ESTRUTURA FINAL OBRIGATÓRIA
────────────────────────────────────────

{
  "info_prescritor": {
    "nome": "",
    "crm": "",
    "info_contato": {
      "fone": ""
    }
  },

  "paciente": {
    "nome": "",
    "fone": ""
  },

  "formulas": [
    {
      "tipo_formula": "",
      "posologia": "",
      "qsp": "",
      "observacao": "",

      "componentes": [
        {
          "nome": "",
          "dosagem": ""
        }
      ]
    }
  ]
}
"""


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
                "content": SYSTEM_PROMPT
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