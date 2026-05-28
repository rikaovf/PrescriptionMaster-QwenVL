import json
import os
import re

from rapidfuzz import fuzz
from unidecode import unidecode

# =========================================================
# ERP PATHS
# =========================================================

BASE_DIR = os.path.dirname(__file__)

PRODUTOS_PATH = os.path.join(
    BASE_DIR,
    "produtos.json"
)

# =========================================================
# STOPWORDS FARMACÊUTICAS
# =========================================================

STOPWORDS = {

    "caps",
    "cps",
    "cap",
    "uso",
    "interno",
    "externo",
    "formula",
    "fórmula",
    "composto",
    "composta",
    "solucao",
    "solução",
    "gel",
    "creme",
    "locao",
    "loção",
    "shampoo",
    "xarope",
    "ml",
    "mg",
    "g",
    "mcg",
    "ui"

}

# =========================================================
# LOAD JSON SAFE
# =========================================================

def carregar_json_seguro(path):

    encodings = [
        "utf-8",
        "utf-8-sig",
        "cp1252",
        "latin1"
    ]

    for encoding in encodings:

        try:

            with open(
                path,
                "r",
                encoding=encoding
            ) as f:

                return json.load(f)

        except Exception:
            pass

    raise Exception(
        f"Não foi possível ler o JSON: {path}"
    )

# =========================================================
# LOAD ERP PRODUCTS
# =========================================================

ERP_PRODUTOS = carregar_json_seguro(
    PRODUTOS_PATH
)

print(
    f"[ERP] Produtos carregados: {len(ERP_PRODUTOS)}"
)

# =========================================================
# NORMALIZAR TEXTO
# =========================================================

def normalizar_texto(texto):

    if not texto:
        return ""

    texto = texto.lower()

    texto = unidecode(texto)

    texto = re.sub(
        r"[^a-z0-9\s]",
        " ",
        texto
    )

    texto = re.sub(
        r"\s+",
        " ",
        texto
    )

    return texto.strip()

# =========================================================
# TOKENIZAR
# =========================================================

def tokenizar(texto):

    texto = normalizar_texto(
        texto
    )

    tokens = texto.split()

    tokens_limpos = []

    for token in tokens:

        if token in STOPWORDS:
            continue

        if len(token) <= 1:
            continue

        tokens_limpos.append(token)

    return tokens_limpos

# =========================================================
# SCORE CONTEXTUAL
# =========================================================

def calcular_score(
    texto1,
    texto2
):

    score_1 = fuzz.partial_ratio(
        texto1,
        texto2
    )

    score_2 = fuzz.token_set_ratio(
        texto1,
        texto2
    )

    score_3 = fuzz.token_sort_ratio(
        texto1,
        texto2
    )

    return max(
        score_1,
        score_2,
        score_3
    )

# =========================================================
# MATCH ERP PRODUTO
# =========================================================

def buscar_produto_erp(
    nome_produto,
    score_minimo=70
):

    tokens_ocr = tokenizar(
        nome_produto
    )

    texto_ocr = " ".join(
        tokens_ocr
    )

    melhor_match = None
    melhor_score = 0

    for produto in ERP_PRODUTOS:

        descricao = produto.get(
            "descricao",
            ""
        )

        tokens_erp = tokenizar(
            descricao
        )

        texto_erp = " ".join(
            tokens_erp
        )

        # =============================================
        # SCORE CONTEXTUAL
        # =============================================

        score = calcular_score(
            texto_ocr,
            texto_erp
        )

        # =============================================
        # BONUS:
        # TOKEN CONTIDO
        # =============================================

        for token in tokens_ocr:

            if token in tokens_erp:

                score += 10

        score = min(score, 100)

        # =============================================
        # BEST MATCH
        # =============================================

        if score > melhor_score:

            melhor_score = score
            melhor_match = produto

    # =================================================
    # SCORE FINAL
    # =================================================

    if (
        melhor_match
        and melhor_score >= score_minimo
    ):

        return {

            "codigo": melhor_match.get(
                "codigo"
            ),

            "descricao": melhor_match.get(
                "descricao"
            ),

            "score": round(
                melhor_score,
                2
            )
        }

    return None

# =========================================================
# NORMALIZAR RECEITA
# =========================================================

def normalizar_receita(
    receita_json
):

    formulas = receita_json.get(
        "formulas",
        []
    )

    for formula in formulas:

        componentes = formula.get(
            "componentes",
            []
        )

        for componente in componentes:

            nome = componente.get(
                "nome"
            )

            if not nome:
                continue

            match = buscar_produto_erp(
                nome
            )

            componente["erp_match"] = match

    return receita_json