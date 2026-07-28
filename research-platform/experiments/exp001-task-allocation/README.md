# exp001 — Alocação de tarefas (camada: coordenação)

**Status:** implementado (baselines clássicos funcionais; QAOA em simulador).
**Papel científico:** caso particular / exercício do protocolo experimental.
**Não é a hipótese principal da tese** — a priorização de componentes será
definida pela revisão sistemática (Etapa 1).

## Pergunta

A alocação de tarefas a agentes (Generalized Assignment Problem) apresenta
vantagem mensurável quando resolvida por QAOA/quantum annealing versus os
melhores baselines clássicos, e em qual regime (tamanho × densidade × ruído)?

## Protocolo

1. Instâncias sintéticas: `qmas.coordination.instances.random_allocation_instance`
   (grade em `configs/exp001_task_allocation.yaml`).
2. Referência de ótimo: CP-SAT com limite de 300 s.
3. Implementações comparadas: greedy, simulated annealing (clássicas);
   QAOA p∈{1..3} em simulador, depois hardware (quânticas).
4. Métricas: time-to-solution, quality_ratio vs. ótimo, factibilidade.
5. Registro: MLflow (`mlruns/`), uma run por (implementação × instância × seed).

## Resultados

(pendente — preencher após primeira campanha de execução)

## Ameaças à validade

- Penalidade do QUBO não calibrada (restrição de capacidade ainda ausente).
- SA sem delta-energy → wall time superestimado no baseline clássico.
- Simulador ≠ hardware: conclusões NISQ exigem modelo de ruído calibrado.
