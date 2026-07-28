"""Classe base dos agentes.

Um agente é um serviço com contrato explícito: recebe Task, devolve Message.
O raciocínio do sistema não está aqui — está no orquestrador que decide
quem chama quem e quando.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from qmas.core.contracts import Message, Task, TaskKind


class Agent(ABC):
    name: str = "agent"
    handles: tuple[TaskKind, ...] = ()

    def __call__(self, task: Task) -> Message:
        if task.kind not in self.handles:
            return Message(
                task_id=task.id, sender=self.name, ok=False,
                error=f"{self.name} não trata {task.kind}",
            )
        try:
            result = self.run(task.payload)
            return Message(task_id=task.id, sender=self.name, ok=True, result=result)
        except Exception as exc:  # noqa: BLE001 — erro vira mensagem, não crash
            return Message(task_id=task.id, sender=self.name, ok=False, error=str(exc))

    @abstractmethod
    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        """Implementação específica do agente."""
