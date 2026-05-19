import json
import os

from config import OUTPUT_DIR

def salvar_json(nome_arquivo, dados):

    nome_saida = os.path.splitext(nome_arquivo)[0]

    output_path = os.path.join(
        OUTPUT_DIR,
        f"{nome_saida}.json"
    )

    with open(
        output_path,
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            dados,
            f,
            ensure_ascii=False,
            indent=4
        )

    print(f"[INFO] JSON salvo: {output_path}")