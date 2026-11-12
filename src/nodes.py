# src/nodes.py
import os
import yaml
from dotenv import load_dotenv
from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.prebuilt import create_react_agent
from src.state import JobHunterState
from src.tools import web_search_tool

# Carrega variáveis de ambiente do arquivo .env (caso existam)
load_dotenv()

OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3-coder:30b")
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")

# Carrega as configurações de prompts e tarefas do YAML
CONFIG_PATH = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config", "prompts.yaml")
)

with open(CONFIG_PATH, "r", encoding="utf-8") as f:
    PROMPTS = yaml.safe_load(f)

# Instancia o modelo local via Ollama
llm = ChatOllama(
    model=OLLAMA_MODEL,
    base_url=OLLAMA_BASE_URL,
    temperature=0.2,
)


def _build_system_prompt(agent_key: str) -> str:
    """Monta a instrução de sistema (SystemMessage) a partir do YAML."""
    cfg = PROMPTS[agent_key]
    return (
        f"Papel: {cfg['role']}\n"
        f"Objetivo: {cfg['goal']}\n"
        f"Contexto e Especialidade: {cfg['backstory']}"
    )


def search_node(state: JobHunterState) -> dict:
    """Nó 1: Pesquisador de Vagas com acesso à ferramenta DuckDuckGo."""
    print("\n--- [1/3] EXECUTANDO: Recrutador Especialista e Pesquisador de Vagas ---")

    system_prompt = _build_system_prompt("job_hunter")
    user_prompt = PROMPTS["job_hunter"]["task_template"].format(
        curriculo_conteudo=state["curriculo_conteudo"]
    )

    # Cria um sub-agente ReAct capaz de invocar ferramentas (DuckDuckGo)
    search_agent = create_react_agent(model=llm, tools=[web_search_tool])

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = search_agent.invoke({"messages": messages})
    raw_jobs_output = response["messages"][-1].content

    return {"raw_jobs": raw_jobs_output}


def advisor_node(state: JobHunterState) -> dict:
    """Nó 2: Consultor de Carreira Sênior (Filtra e seleciona as Top 5 vagas)."""
    print("\n--- [2/3] EXECUTANDO: Consultor de Carreira Sênior ---")

    system_prompt = _build_system_prompt("career_advisor")
    user_prompt = PROMPTS["career_advisor"]["task_template"].format(
        raw_jobs=state["raw_jobs"]
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    return {"selected_jobs": response.content}


def editor_node(state: JobHunterState) -> dict:
    """Nó 3: Editor Técnico (Revisa e formata o relatório final em Markdown)."""
    print("\n--- [3/3] EXECUTANDO: Editor Técnico e Especialista em Documentação ---")

    system_prompt = _build_system_prompt("report_editor")
    user_prompt = PROMPTS["report_editor"]["task_template"].format(
        selected_jobs=state["selected_jobs"]
    )

    messages = [
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_prompt),
    ]

    response = llm.invoke(messages)
    return {"final_report": response.content}