"""Aprendizado clássico (baselines). Os agentes de domínio em qmas.agents
(forecaster ARIMA, pricer Monte Carlo) são os primeiros baselines naturais
desta camada — reutilizar, não duplicar."""

from __future__ import annotations

from typing import Any

from qmas.core.component import Paradigm, RunOutput


class GradientBoostingClassifier:
    """Baseline forte para tarefas de classificação financeira (sklearn)."""

    name = "gbm"
    paradigm = Paradigm.CLASSICAL

    def run(self, instance: Any) -> RunOutput:
        raise NotImplementedError("formalizar dataset/tarefa após Etapa 1")
