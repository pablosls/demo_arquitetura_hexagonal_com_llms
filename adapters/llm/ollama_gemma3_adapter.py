import requests
from domain.ports.classificador_port import ClassificadorPort
from domain.entities.documento import TipoDocumento


class OllamaGemma3ClassificadorAdapter(ClassificadorPort):

    def __init__(self):
        self.url = "http://localhost:11434/api/generate"
        self.model = "gemma3:4b"

    def _perguntar_llm(self, prompt: str) -> str:
        response = requests.post(
            self.url,
            json={
                "model": self.model,
                "prompt": prompt,
                "stream": False,
                "options": {
                    "temperature": 0.0,   # IMPORTANTÍSSIMO para classificação
                    "num_predict": 10     # força resposta curta
                }
            },
            timeout=60
        )

        return response.json()["response"].strip().lower()

    def classificar(self, texto: str) -> TipoDocumento:

        prompt = f"""
Você é um classificador de documentos.

Responda APENAS UMA palavra dentre:
contrato
nota_fiscal
curriculo
desconhecido

Documento:
\"\"\"{texto}\"\"\"
"""

        print(f"Prompt enviado ao LLM: {prompt}")

        resposta = self._perguntar_llm(prompt)

        # normalização defensiva
        resposta = resposta.replace(".", "").replace("\n", "").strip()

        if resposta.startswith("contrato"):
            return TipoDocumento.CONTRATO
        if resposta.startswith("nota"):
            return TipoDocumento.NOTA_FISCAL
        if resposta.startswith("curriculo"):
            return TipoDocumento.CURRICULO

        return TipoDocumento.DESCONHECIDO