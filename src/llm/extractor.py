import json
import ollama

from llm.validator import validar_json

def extrair_dados_receita(texto_ocr):

    prompt = f"""
Você é especialista em prescrições médicas manipuladas.

Extraia:

- nome do médico
- CRM do médico
- nome do paciente
- telefone do paciente
- posologia
- tipo da receita

COMPONENTES:
- insumo
- quantidade
- unidade
- qsp

REGRAS:
- Retorne APENAS JSON
- Não invente dados
- Se não encontrar, deixe vazio
- qsp deve ser true ou false

Formato:

{{
  "medico": {{
    "nome": "",
    "crm": ""
  }},
  "paciente": {{
    "nome": "",
    "telefone": ""
  }},
  "receita": {{
    "tipo": "",
    "posologia": ""
  }},
  "componentes": [
    {{
      "insumo": "",
      "quantidade": "",
      "unidade": "",
      "qsp": false
    }}
  ]
}}

TEXTO OCR:
\"\"\"
{texto_ocr}
\"\"\"
"""

    try:

        response = ollama.chat(
            model='qwen2.5',
            messages=[
                {
                    'role': 'user',
                    'content': prompt
                }
            ]
        )

        conteudo = response['message']['content']

        # remove markdown se vier
        conteudo = conteudo.replace("```json", "")
        conteudo = conteudo.replace("```", "")

        dados = json.loads(conteudo)

        return validar_json(dados)

    except Exception as e:

        print("[ERRO] Falha no LLM")
        print(str(e))

        return None