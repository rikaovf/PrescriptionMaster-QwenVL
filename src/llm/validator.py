from models.prescription_model import Prescription

def validar_json(dados):

    try:

        validado = Prescription(**dados)

        return validado.model_dump()

    except Exception as e:

        print("[ERRO] JSON inválido")
        print(str(e))

        return None