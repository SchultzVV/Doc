"""Harness experimental genérico.

Recebe QUALQUER ComponentUnderStudy e executa o mesmo protocolo:

    grade de instâncias -> todas as implementações -> métricas -> MLflow

É a materialização do desenho: Component Under Study -> Classical
Implementation -> Quantum Implementation -> Experimental Comparison.
O harness não sabe (nem deve saber) de qual camada o componente veio.
"""

from __future__ import annotations

import itertools
from dataclasses import asdict
from typing import Any, Iterable

from qmas.core.component import ComponentUnderStudy, timed
from qmas.experiments.metrics import ComparisonRecord, quality_ratio


class ExperimentHarness:
    def __init__(self, component: ComponentUnderStudy, tracking_uri: str | None = None) -> None:
        self.component = component
        self.tracking_uri = tracking_uri

    def sweep(
        self,
        param_grid: dict[str, Iterable[Any]],
        replications: int = 10,
        base_seed: int = 42,
        log_mlflow: bool = True,
    ) -> list[ComparisonRecord]:
        """Varre o produto cartesiano de param_grid x replicações."""
        if log_mlflow:
            import mlflow
            if self.tracking_uri:
                mlflow.set_tracking_uri(self.tracking_uri)
            mlflow.set_experiment(f"{self.component.layer.value}/{self.component.name}")

        records: list[ComparisonRecord] = []
        keys = list(param_grid)
        for combo in itertools.product(*(param_grid[k] for k in keys)):
            params = dict(zip(keys, combo))
            for rep in range(replications):
                seed = base_seed + rep
                instance = self.component.instance_generator(**params, seed=seed)
                reference = (
                    timed(self.component.reference, instance)
                    if self.component.reference else None
                )
                for impl in self.component.implementations:
                    run = timed(impl, instance)
                    record = ComparisonRecord(
                        component=self.component.name,
                        layer=self.component.layer.value,
                        implementation=run.implementation,
                        paradigm=run.paradigm,
                        instance_params=params,
                        seed=seed,
                        wall_time_s=run.wall_time_s,
                        quality=run.output.quality,
                        feasible=run.output.feasible,
                        quality_ratio=quality_ratio(run, reference),
                    )
                    records.append(record)
                    if log_mlflow:
                        self._log(record)
        return records

    def _log(self, record: ComparisonRecord) -> None:
        import mlflow

        with mlflow.start_run():
            mlflow.log_params({
                "implementation": record.implementation,
                "paradigm": record.paradigm.value,
                "seed": record.seed,
                **{f"inst_{k}": v for k, v in record.instance_params.items()},
            })
            metrics = {
                "wall_time_s": record.wall_time_s,
                "feasible": float(record.feasible),
            }
            if record.quality is not None:
                metrics["quality"] = record.quality
            if record.quality_ratio is not None:
                metrics["quality_ratio"] = record.quality_ratio
            mlflow.log_metrics(metrics)


# TODO (H4): a saída acumulada destes sweeps é o dataset que treina a
# política do HybridSelector — curvas de crossover por componente.
