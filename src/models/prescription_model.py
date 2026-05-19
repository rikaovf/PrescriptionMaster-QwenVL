from pydantic import BaseModel
from typing import List

class Componente(BaseModel):

    insumo: str
    quantidade: str
    unidade: str
    qsp: bool

class Medico(BaseModel):

    nome: str
    crm: str

class Paciente(BaseModel):

    nome: str
    telefone: str

class Receita(BaseModel):

    tipo: str
    posologia: str

class Prescription(BaseModel):

    medico: Medico
    paciente: Paciente
    receita: Receita
    componentes: List[Componente]