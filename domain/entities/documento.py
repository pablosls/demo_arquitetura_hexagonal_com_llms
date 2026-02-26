from enum import Enum


class TipoDocumento(Enum):
    CONTRATO = "contrato"
    NOTA_FISCAL = "nota_fiscal"
    CURRICULO = "curriculo"
    DESCONHECIDO = "desconhecido"
    
class Documento:
    def __init__(self, texto: str):
        if len(texto) > 100:
            raise ValueError("O texto do documento deve conter no máximo 10 caracteres.")
        self.texto = texto
