# src/graph.py
from langgraph.graph import StateGraph, START, END
from src.state import JobHunterState
from src.nodes import search_node, advisor_node, editor_node


def create_workflow():
    """Constrói e compila o grafo de estados do pipeline Job Hunter."""
    # Inicializa o grafo tipado com o contrato de estado compartilhado
    workflow = StateGraph(JobHunterState)

    # Registra os nós (etapas do pipeline)
    workflow.add_node("search_agent", search_node)
    workflow.add_node("advisor_agent", advisor_node)
    workflow.add_node("editor_agent", editor_node)

    # Define o fluxo sequencial (arestas)
    workflow.add_edge(START, "search_agent")
    workflow.add_edge("search_agent", "advisor_agent")
    workflow.add_edge("advisor_agent", "editor_agent")
    workflow.add_edge("editor_agent", END)

    # Compila o grafo para execução
    return workflow.compile()