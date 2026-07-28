"""Agente de previsão de séries temporais (ARIMA como ponto de partida)."""

from __future__ import annotations

from typing import Any

import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from qmas.agents.base import Agent
from qmas.core.contracts import TaskKind


class ForecasterAgent(Agent):
    name = "forecaster"
    handles = (TaskKind.FORECAST,)

    def run(self, payload: dict[str, Any]) -> dict[str, Any]:
        series = pd.Series(payload["values"])
        horizon = int(payload.get("horizon", 5))
        order = tuple(payload.get("order", (1, 1, 1)))

        model = ARIMA(series, order=order).fit()
        forecast = model.get_forecast(steps=horizon)
        ci = forecast.conf_int(alpha=0.05)

        return {
            "mean": forecast.predicted_mean.tolist(),
            "ci_lower": ci.iloc[:, 0].tolist(),
            "ci_upper": ci.iloc[:, 1].tolist(),
            "aic": float(model.aic),
        }
