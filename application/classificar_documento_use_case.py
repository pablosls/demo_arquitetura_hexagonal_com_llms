from domain.entities.documento import Documento
from domain.ports.classificador_port import ClassificadorPort

class ClassificarDocumentoUseCase:
    def __init__(self, classificador: ClassificadorPort):
        self.classificador = classificador

    def executar(self, texto: str):
        documento = Documento(texto)
        return self.classificador.classificar(documento.texto)

