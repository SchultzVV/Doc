"""Agente planejador via LLM (Claude API).

Papel: decompor um pedido em linguagem natural em Tasks tipadas.
O LLM é só o motor de linguagem — a saída é forçada a um JSON Schema
(structured outputs), e quem executa/roteia é o orquestrador.
"""

from __future__ import annotations

from typing import Any

import anthropic

from qmas.agents.base import Agent
from qmas.core.contracts import TaskKind

MODEL = "claude-opus-5"

PLAN_SCHEMA = {
    "type": "object",
    "properties": {
        "tasks": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "kind": {"type": "string", "enum": [k.value for k in TaskKind if k != TaskKind.PLAN]},
                    "payload": {"type": "object", "additionalProperties": False, "properties": {
                        "description": {"type": "string"},
                    }, "required": ["description"]},
                    "cost_hint": {"type": "number"},
                },
                "required": ["kind", "payload", "cost_hint"],
                "additionalProperties": False,
            },
        },
    },
    "required": ["tasks"],
    "additionalProperties": False,
}

SYSTEM = (
    "Você decompõe pedidos de análise financeira em subtarefas tipadas "
    "(extract, forecast, price). Estime cost_hint como custo computacional "
    "relativo (1.0 = leve). Responda apenas com o JSON pedido."
)


class LLMPlannerAgent(Agent):
    name = "llm_planner"
    handles = (TaskKind.PLAN,)

    def __init__(self) -> None:
        self.client = anthropic.Anthropic()  # ANTHROPIC_API_KEY no ambiente

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        response = self.client.beta.messages.create(
            model=MODEL,
            max_tokens=16000,
            # fallback server-side: se o classificador de segurança recusar,
            # a mesma requisição roda no modelo recomendado automaticamente
            betas=["server-side-fallback-2026-07-01"],
            fallbacks="default",
            system=SYSTEM,
            output_config={"format": {"type": "json_schema", "schema": PLAN_SCHEMA}},
            messages=[{"role": "user", "content": payload["request"]}],
        )
        if response.stop_reason == "refusal":
            raise RuntimeError("LLM recusou a requisição (safety classifier)")

        import json
        text = next(b.text for b in response.content if b.type == "text")
        return json.loads(text)
