# src/tools.py
from langchain_core.tools import tool
from duckduckgo_search import DDGS


@tool("web_search_tool")
def web_search_tool(query: str) -> str:
    """Realiza uma busca na web usando o DuckDuckGo e retorna os principais resultados contendo títulos, links e resumos."""
    print(f"🔎 [DuckDuckGo] Pesquisando por: '{query}'...")
    results = []
    try:
        with DDGS() as ddgs:
            for r in ddgs.text(query, max_results=5):
                results.append(
                    f"Título: {r.get('title')}\n"
                    f"Link: {r.get('href')}\n"
                    f"Resumo: {r.get('body')}\n"
                )
    except Exception as e:
        return f"Erro ao realizar busca na web: {str(e)}"

    return "\n---\n".join(results) if results else "Nenhum resultado encontrado."