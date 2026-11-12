# src/state.py
from typing import TypedDict


class JobHunterState(TypedDict):
    """Contrato de estado compartilhado entre os nós do pipeline Job Hunter."""

    curriculo_conteudo: str
    raw_jobs: str
    selected_jobs: str
    final_report: str