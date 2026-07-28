"""Contratos de dados entre agentes e orquestrador.

O "protocolo" do sistema: todo agente consome/produz estes schemas.
É aqui que o pipeline deixa de ser conceitual e vira operacional —
entradas, saídas e regras explícitas, validadas pelo pydantic.
"""

from __future__ import annotations

import uuid
from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


class TaskKind(str, Enum):
    EXTRACT = "extract"        # PDF -> dados estruturados
    FORECAST = "forecast"      # série temporal -> previsão
    PRICE = "price"            # instrumento -> valor
    PLAN = "plan"              # linguagem natural -> subtarefas (LLM)


class Task(BaseModel):
    """Unidade de trabalho roteável pelo orquestrador."""

    id: str = Field(default_factory=lambda: uuid.uuid4().hex[:8])
    kind: TaskKind
    payload: dict[str, Any]
    # custo estimado de execução por agente (entra na função objetivo do GAP)
    cost_hint: float = 1.0
    depends_on: list[str] = Field(default_factory=list)


class AgentSpec(BaseModel):
    """Capacidades e capacidade (no sentido de recurso) de um agente."""

    name: str
    handles: list[TaskKind]
    capacity: float = 10.0     # restrição de capacidade do GAP


class Message(BaseModel):
    """Envelope de comunicação agente <-> orquestrador."""

    task_id: str
    sender: str
    ok: bool
    result: dict[str, Any] | None = None
    error: str | None = None


class Assignment(BaseModel):
    """Solução de alocação: task_id -> agent_name (saída dos solvers)."""

    mapping: dict[str, str]
    objective_value: float
    feasible: bool
