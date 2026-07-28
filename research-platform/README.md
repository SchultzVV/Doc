# research-platform — Quântica em Arquiteturas Multiagente

Plataforma experimental do doutorado: *"Quais componentes de arquiteturas
multiagentes baseadas em LLMs podem se beneficiar de computação quântica e
sob quais condições isso produz ganhos mensuráveis?"*

**A plataforma é agnóstica quanto a ONDE a vantagem quântica está (se estiver
em algum lugar).** A revisão bibliográfica determinará quais componentes viram
objeto de experimento; o código não assume a resposta. Todo experimento segue
o mesmo desenho:

```
Multi-Agent System
    ↓
Component Under Study          (qmas.core.component.ComponentUnderStudy)
    ↓
Classical Implementation       (<camada>/classical/)
    ↓
Quantum Implementation         (<camada>/quantum/)
    ↓
Experimental Comparison        (qmas.experiments.ExperimentHarness)
```

## Camadas candidatas (nenhuma é a hipótese principal)

| Camada | Pergunta | Status |
|---|---|---|
| 1. `planning/` | Planejador quântico gera planos melhores/mais rápido? (tree search, MCTS, HTN) | stub |
| 2. `retrieval/` | Quântica acelera busca dos agentes? (RAG, vetorial, semântica) — expectativa negativa NISQ (qRAM) a testar | stub |
| 3. `memory/` | Memória quântica melhora recuperação contextual? (episódica, longo prazo) | stub |
| 4. `coordination/` | Quântica ajuda coordenação? (consenso, alocação, negociação, roteamento) | **exp001 implementado** |
| 5. `learning/` | QML melhora modelos dos agentes? (classificação, forecast, portfólio) | stub |
| 6. `reasoning/` | Circuitos quânticos como etapas de raciocínio? (mais exploratória) | stub |

## Estrutura

```
src/qmas/
├── core/            # contracts, ComponentUnderStudy, Orchestrator, HybridSelector
├── agents/          # agentes de domínio: doc_extractor, forecaster, pricer, llm_planner
├── planning/        ├── classical/  └── quantum/
├── retrieval/       ├── classical/  └── quantum/
├── memory/          ├── classical/  └── quantum/
├── coordination/    ├── problems/ (GAP→QUBO)  ├── classical/  └── quantum/
├── learning/        ├── classical/  └── quantum/
├── reasoning/       ├── classical/  └── quantum/
└── experiments/     # harness genérico, métricas, exp001
experiments/         # protocolos e registros de cada experimento
papers/              # artigos em produção
```

## Experimento 001 — alocação de tarefas (caso particular)

O benchmark GAP → QUBO → {CP-SAT, greedy, SA} × {QAOA, D-Wave} foi o primeiro
componente formalizado e serve de exercício completo do protocolo. **Ele não
define o escopo científico da pesquisa** — ver `experiments/exp001-task-allocation/`.

```bash
pip install -e ".[dev]"                       # núcleo
pip install -e ".[quantum]"                   # + qiskit, dwave
python -m qmas.experiments.exp001_task_allocation --no-quantum   # só baselines
```

## Hipóteses (abertas — a revisão sistemática as refina)

- **H1** Existem componentes com vantagem mensurável em implementação quântica.
- **H2** As vantagens dependem do tamanho do problema e da estrutura dos dados.
- **H3** Nem todos os componentes se beneficiam igualmente.
- **H4** É possível um orquestrador híbrido que seleciona dinamicamente
  clássico/quântico (`qmas.core.orchestrator.HybridSelector`).
- **H5** Arquiteturas híbridas têm melhor custo-benefício que puras.
