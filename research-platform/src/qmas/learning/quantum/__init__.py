"""Aprendizado quântico (candidatos): circuitos variacionais (VQC/QNN),
quantum kernels, amplitude estimation para Monte Carlo (pricing)."""

from __future__ import annotations

from typing import Any

from qmas.core.component import Paradigm, RunOutput


class VQCClassifier:
    """Variational Quantum Classifier (Cerezo et al., 2021). Atenção a
    barren plateaus e ao custo de codificação dos features."""

    name = "vqc"
    paradigm = Paradigm.QUANTUM

    def run(self, instance: Any) -> RunOutput:
        raise NotImplementedError("formalizar após Etapa 1")


class AmplitudeEstimationPricer:
    """Amplitude estimation promete ganho quadrático sobre Monte Carlo em
    pricing — comparar contra o MC do qmas.agents.pricer (mesma instância)."""

    name = "qae_pricer"
    paradigm = Paradigm.QUANTUM

    def run(self, instance: Any) -> RunOutput:
        raise NotImplementedError("formalizar após Etapa 1")
