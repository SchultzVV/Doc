"""Solvers quânticos: QAOA (Qiskit, gate-based) e annealing (D-Wave).

Imports adiados de propósito — o pacote `quantum` é opcional
(pip install -e ".[quantum]").
"""

from __future__ import annotations

import numpy as np

from qmas.core.contracts import Assignment
from qmas.coordination.problems.allocation import AllocationProblem
from qmas.coordination.base import TimedSolver
from qmas.coordination.classical.solvers import _decode_qubo_solution


class QAOASolver(TimedSolver):
    """QAOA sobre o Ising derivado do QUBO (Farhi et al., 2014).

    Simulador por padrão; hardware IBM via troca de backend.
    Profundidade `reps` (p) é hiperparâmetro central da caracterização de regimes.
    """

    name = "qaoa"

    def __init__(self, reps: int = 3, shots: int = 4096, backend: str = "aer_simulator") -> None:
        self.reps = reps
        self.shots = shots
        self.backend_name = backend

    def solve(self, problem: AllocationProblem) -> Assignment:
        from qiskit_aer.primitives import SamplerV2
        from qiskit.circuit.library import QAOAAnsatz
        from qiskit.quantum_info import SparsePauliOp
        from scipy.optimize import minimize

        qubo = problem.to_qubo()
        h, J, offset = qubo.to_ising()
        hamiltonian = _ising_to_pauli(h, J)

        ansatz = QAOAAnsatz(hamiltonian, reps=self.reps)
        ansatz.measure_all()
        sampler = SamplerV2()

        def objective(params: np.ndarray) -> float:
            bound = ansatz.assign_parameters(params)
            counts = sampler.run([bound], shots=self.shots).result()[0].data.meas.get_counts()
            return _expected_energy(counts, qubo)

        x0 = np.random.default_rng(0).uniform(0, np.pi, ansatz.num_parameters)
        res = minimize(objective, x0, method="COBYLA", options={"maxiter": 200})

        # amostra final: melhor bitstring observado
        bound = ansatz.assign_parameters(res.x)
        counts = sampler.run([bound], shots=self.shots).result()[0].data.meas.get_counts()
        best = min(counts, key=lambda b: qubo.energy(_bits(b)))
        x = _bits(best)
        return _decode_qubo_solution(x, problem, qubo.energy(x))


class DWaveSolver(TimedSolver):
    """Quantum annealing via D-Wave Leap. Esqueleto — requer conta/token."""

    name = "dwave"

    def solve(self, problem: AllocationProblem) -> Assignment:
        from dwave.system import DWaveSampler, EmbeddingComposite  # noqa: F401

        raise NotImplementedError(
            "configurar DWAVE_API_TOKEN e mapear QUBO -> BinaryQuadraticModel"
        )


def _ising_to_pauli(h: np.ndarray, J: np.ndarray):
    """Monta o Hamiltoniano de custo sum h_i Z_i + sum J_ij Z_i Z_j."""
    from qiskit.quantum_info import SparsePauliOp

    n = len(h)
    terms = []
    for i in range(n):
        if abs(h[i]) > 1e-12:
            terms.append(("Z" * 1, [i], float(h[i])))
    for i in range(n):
        for j in range(i + 1, n):
            if abs(J[i, j]) > 1e-12:
                terms.append(("ZZ", [i, j], float(J[i, j])))
    return SparsePauliOp.from_sparse_list(terms, num_qubits=n)


def _bits(bitstring: str) -> np.ndarray:
    # Qiskit devolve little-endian: inverter para casar com a indexação do QUBO
    return np.array([int(b) for b in reversed(bitstring)], dtype=float)


def _expected_energy(counts: dict[str, int], qubo) -> float:
    total = sum(counts.values())
    return sum(c * qubo.energy(_bits(b)) for b, c in counts.items()) / total
