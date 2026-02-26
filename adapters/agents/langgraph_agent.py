from langgraph.graph import StateGraph, END
from typing import TypedDict
from openai import OpenAI

from domain.ports.classificador_port import ClassificadorPort
from domain.entities.documento import TipoDocumento

client = OpenAI()

class AgentState(TypedDict):
    texto: str
    resposta: str
    

def classificar_node(state: AgentState):
    prompt = f"""
    Classifique o texto do documento em apenas uma das seguintes categorias:
    "contrato", "nota_fiscal" ou "curriculo".
    
    Responda apenas com a categoria, sem explicações ou formatações adicionais.
    
    Documento:
    {state['texto']}
    """
    
    print(f"Prompt enviado ao LLM: {prompt}")
    
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{
            "role": "user",
            "content": prompt
        }]  
    )
    
    conteudo = resp.choices[0].message.content.strip().lower()
    print(f"Resposta do LLM: {conteudo}")
    return {"resposta": conteudo}

def criar_grafo():
    graph = StateGraph(AgentState)
    
    graph.add_node("classificar", classificar_node)
    graph.set_entry_point("classificar")
    graph.add_edge("classificar", END)
    
    return graph.compile()

class LangGraphClassificadorAdapter(ClassificadorPort):
    def __init__(self):
        self.graph = criar_grafo()
    
    def classificar(self, texto: str) -> TipoDocumento:
        resultado = self.graph.invoke({
            "texto": texto, 
            "resposta": ""
            })
        
        r = resultado["resposta"]
        
        if r in TipoDocumento._value2member_map_:
            return TipoDocumento(r)
        return TipoDocumento.DESCONHECIDO
        
        


