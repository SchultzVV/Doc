"""Experimento 001 — alocação de tarefas (camada de coordenação).

CASO PARTICULAR, não hipótese principal: primeiro exercício completo do
protocolo experimental da plataforma, escolhido por já estar formalizado
(GAP -> QUBO), não por prioridade científica estabelecida.

Uso: python -m qmas.experiments.exp001_task_allocation --config configs/exp001_task_allocation.yaml
"""

from __future__ import annotations

import argparse

import yaml

from qmas.coordination import task_allocation_component
from qmas.experiments.harness import ExperimentHarness


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="configs/exp001_task_allocation.yaml")
    parser.add_argument("--no-quantum", action="store_true",
                        help="roda só os baselines clássicos (sem qiskit)")
    args = parser.parse_args()

    with open(args.config) as f:
        cfg = yaml.safe_load(f)

    exp, inst = cfg["experiment"], cfg["instances"]
    component = task_allocation_component(with_quantum=not args.no_quantum)
    harness = ExperimentHarness(component, tracking_uri=exp.get("tracking_uri"))

    records = harness.sweep(
        param_grid={
            "n_tasks": inst["n_tasks"],
            "n_agents": inst["n_agents"],
            "constraint_density": inst["constraint_density"],
        },
        replications=inst["replications"],
        base_seed=exp["seed"],
    )
    for r in records:
        print(r)


if __name__ == "__main__":
    main()
