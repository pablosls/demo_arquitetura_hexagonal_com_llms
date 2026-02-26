from openai import OpenAI

from domain.ports.classificador_port import ClassificadorPort
from domain.entities.documento import TipoDocumento

client = OpenAI()

class OpenAIClassificadorAdapter(ClassificadorPort):
    def classificar(self, texto: str) -> TipoDocumento:
        resposta = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": "Classifique o documento como: contrato, nota_fiscal, curriculo"
                },
                {
                    "role": "user",
                    "content": texto
                }
            ]
        )
        
        conteudo = resposta.choices[0].message.content.strip().lower()
        if conteudo in TipoDocumento._value2member_map_:
            return TipoDocumento(conteudo)
        return TipoDocumento.DESCONHECIDO