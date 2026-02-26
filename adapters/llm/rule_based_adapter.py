from domain.ports.classificador_port import ClassificadorPort
from domain.entities.documento import TipoDocumento

class RegraSimplesAdapter(ClassificadorPort):
    def classificar(self, texto: str) -> TipoDocumento:
        
        t = texto.lower()
        if "cpf" in t and "rg" in t:
            return TipoDocumento.CONTRATO
        if "danfe" in t or "valor total" in t:
            return TipoDocumento.NOTA_FISCAL
        if "experiência profissional" in t:
            return TipoDocumento.CURRICULO
        
        return TipoDocumento.DESCONHECIDO