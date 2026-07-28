"""Testes de fumaça: formulação, solvers clássicos e decodificação QUBO."""

import numpy as np

from qmas.coordination.instances import random_allocation_instance
from qmas.coordination.classical.solvers import GreedySolver, SimulatedAnnealingSolver


def test_instance_is_feasible_by_construction():
    p = random_allocation_instance(n_tasks=6, n_agents=3, seed=1)
    assert all(np.isfinite(p.cost[t]).any() for t in range(6))


def test_greedy_solves_small_instance():
    p = random_allocation_instance(n_tasks=6, n_agents=3, seed=1)
    a = GreedySolver().solve(p)
    assert a.feasible
    assert len(a.mapping) == 6


def test_qubo_roundtrip_energy():
    p = random_allocation_instance(n_tasks=3, n_agents=2, seed=2)
    qubo = p.to_qubo()
    x = np.zeros(qubo.n)
    assert np.isfinite(qubo.energy(x))
    h, J, offset = qubo.to_ising()
    assert h.shape == (qubo.n,) and J.shape == (qubo.n, qubo.n)


def test_simulated_annealing_runs():
    p = random_allocation_instance(n_tasks=3, n_agents=2, seed=3)
    a = SimulatedAnnealingSolver(n_sweeps=50, seed=0).solve(p)
    # SA pode não achar solução factível em 50 sweeps; só não pode explodir
    assert a.objective_value is not None


def test_harness_runs_component_without_mlflow():
    """O harness genérico compara implementações do componente de coordenação."""
    from qmas.coordination import task_allocation_component
    from qmas.experiments.harness import ExperimentHarness

    component = task_allocation_component(with_quantum=False)
    component.reference = None  # sem CP-SAT no smoke test (rápido)
    records = ExperimentHarness(component).sweep(
        param_grid={"n_tasks": [3], "n_agents": [2], "constraint_density": [0.8]},
        replications=1,
        log_mlflow=False,
    )
    assert {r.implementation for r in records} == {"greedy", "sim_annealing"}
    assert all(r.paradigm.value == "classical" for r in records)
