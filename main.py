# main.py
import os
from datetime import datetime
from src.graph import create_workflow

CURRICULO_PATH = "/home/guiassys/devtools/repos/interview-guiassys/docs/resume/cv-guilherme-main.md"
OUTPUT_DIR = "/home/guiassys/devtools/repos/job-hunter-langgraph/output"


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    if os.path.exists(CURRICULO_PATH):
        with open(CURRICULO_PATH, "r", encoding="utf-8") as f:
            curriculo_conteudo = f.read()
    else:
        raise FileNotFoundError(
            f"Não foi possível encontrar o currículo em: {CURRICULO_PATH}"
        )

    print("## Iniciando Pipeline Job Hunter Modularizado (LangGraph + Ollama) ##")

    # Estado inicial injetado no grafo
    initial_state = {
        "curriculo_conteudo": curriculo_conteudo,
        "raw_jobs": "",
        "selected_jobs": "",
        "final_report": "",
    }

    # Compila e executa o pipeline
    app = create_workflow()
    resultado_final = app.invoke(initial_state)

    final_content = resultado_final.get(
        "final_report", "Nenhum relatório foi gerado pela pipeline."
    )

    # Salva o relatório em Markdown com timestamp exclusivo
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"job_report_{timestamp}.md"
    filepath = os.path.join(OUTPUT_DIR, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(str(final_content))

    print("\n\n##################################################")
    print(f"## RELATÓRIO SALVO COM SUCESSO: {filepath} ##")
    print("##################################################\n")
    print(final_content)


if __name__ == "__main__":
    main()