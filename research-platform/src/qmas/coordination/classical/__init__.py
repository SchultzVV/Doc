"""Implementações clássicas da camada de coordenação (baselines fortes)."""

from qmas.coordination.classical.solvers import (
    CpSatSolver, GreedySolver, SimulatedAnnealingSolver,
)

__all__ = ["CpSatSolver", "GreedySolver", "SimulatedAnnealingSolver"]
