# 🤖 Job Hunter LangGraph (LangGraph + Ollama Local)

Pipeline de Inteligência Artificial autônoma construída com **LangGraph** para pesquisar, filtrar, analisar e documentar vagas de emprego de tecnologia alinhadas ao seu perfil profissional. O sistema roda 100% local utilizando modelos executados via **Ollama** (`qwen3-coder:30b`) e ferramentas gratuitas de busca web (**DuckDuckGo**), seguindo uma arquitetura modular baseada em grafos de estados.

---

## 🏗️ Como o Projeto Funciona (Arquitetura)

O projeto utiliza um pipeline sequencial controlado por um Grafo de Estados (*StateGraph*), composto por três nós especializados cujos prompts e templates são desacoplados no arquivo de configuração `config/prompts.yaml`:

1. **Recrutador Especialista e Pesquisador de Vagas (`search_agent`):**
    - Lê o seu currículo oficial.
    - Utiliza um agente ReAct integrado com a ferramenta de busca web (`DuckDuckGo`) para encontrar vagas recentes e aderentes ao seu perfil (Java, Spring Boot, GCP, IA).

2. **Consultor de Carreira Sênior (`advisor_agent`):**
    - Analisa as oportunidades brutas encontradas.
    - Seleciona as 5 melhores vagas com maior fit técnico e cultural, detalhando requisitos, justificativas e links.

3. **Editor Técnico e Especialista em Documentação (`editor_agent`):**
    - Recebe o relatório consolidado, revisa e valida a formatação em Markdown para garantir um documento limpo, profissional e pronto para publicação.

---

## 📂 Estrutura do Projeto

```text
job-hunter-langgraph/
├── config/
│   └── prompts.yaml      # Configuração unificada de papéis, goals, backstories e templates de tarefas
├── data/                 # Diretório opcional para dados complementares
├── output/               # Diretório onde os relatórios em Markdown são salvos com timestamp
├── src/
│   ├── __init__.py
│   ├── state.py          # Contrato de dados compartilhado (TypedDict) que trafega no grafo
│   ├── tools.py          # Ferramenta customizada de busca web (DuckDuckGo)
│   ├── nodes.py          # Funções de cada etapa executando via ChatOllama
│   └── graph.py          # Montagem, interligação das arestas e compilação do StateGraph
├── .env                  # Variáveis de ambiente (URL do Ollama e modelo)
├── README.md             # Documentação do projeto
├── main.py               # Ponto de entrada leve (executa o fluxo e salva o relatório)
└── requirements.txt      # Dependências do projeto
```

---

## ⚙️ Pré-requisitos

- **Python 3.10+** (Ambiente WSL / Ubuntu recomendado)
- **Ollama** rodando localmente (ex: via Docker) com o modelo configurado (`qwen3-coder:30b` na porta `11434`).

---

## 🚀 Instalação e Configuração

Abra o seu terminal no WSL/Ubuntu e siga os passos abaixo:

1. **Navegue até o diretório do projeto**
   ```bash
   cd ~/devtools/repos/job-hunter-langgraph
   ```

2. **Criar e ativar o ambiente virtual Python**
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Instalar as dependências do projeto**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

## ▶️ Como Executar o Projeto

Certifique-se de que o seu container do Ollama está rodando e acessível na porta `11434`.

Com o ambiente virtual ativado (`source venv/bin/activate`), basta executar o script principal:

```bash
python main.py
```

O pipeline será iniciado, os agentes farão as buscas e análises de mercado passo a passo, e o relatório final em Markdown será exibido no console e salvo automaticamente no diretório `output/` com um timestamp exclusivo (ex: `job_report_20261111_183000.md`).