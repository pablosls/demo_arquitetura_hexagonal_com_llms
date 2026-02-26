from fastapi import FastAPI
from application.classificar_documento_use_case import ClassificarDocumentoUseCase
from adapters.llm.rule_based_adapter import RegraSimplesAdapter
from adapters.llm.ollama_gemma3_adapter import OllamaGemma3ClassificadorAdapter
from adapters.agents.langgraph_agent import LangGraphClassificadorAdapter


app = FastAPI()

classificador = ClassificarDocumentoUseCase(RegraSimplesAdapter())
classificador_langgraph = ClassificarDocumentoUseCase(LangGraphClassificadorAdapter())
classificador_gemma3 = ClassificarDocumentoUseCase(OllamaGemma3ClassificadorAdapter())

@app.post("/classificar")
def classificar(texto: str):
    resultado = classificador.executar(texto)
    return {"tipo": resultado.value}

@app.post("/classificar/gemma3")
def classificar_gemma3(texto: str):
    resultado = classificador_gemma3.executar(texto)
    return {"tipo": resultado.value}

@app.post("/classificar/langgraph")
def classificar_langgraph(texto: str):
    resultado = classificador_langgraph.executar(texto)
    return {"tipo": resultado.value}


