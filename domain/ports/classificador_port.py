from abc import ABC, abstractmethod
from domain.entities.documento import TipoDocumento

class ClassificadorPort(ABC):
    @abstractmethod
    def classificar(self, texto: str) -> TipoDocumento:
        pass