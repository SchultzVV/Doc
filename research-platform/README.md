# qmas-bench — Quantum Multi-Agent System Benchmark

Bancada experimental do pré-projeto de doutorado: *"Quais componentes de uma
arquitetura multiagente podem se beneficiar de algoritmos quânticos e em quais
condições isso traz vantagens mensuráveis?"*

A carga de trabalho realista vem de **engenharia financeira**: agentes de
extração de documentos (PyMuPDF/regex/OCR), previsão de séries temporais e
precificação de derivativos, coordenados por um orquestrador cujos problemas
internos (alocação de tarefas, escalonamento) são formulados como QUBO e
despachados para solvers clássicos ou quânticos.

## Levantamento da stack

| Camada | Ferramenta | Papel |
|---|---|---|
| Contratos | `pydantic` | Schemas de Task, AgentSpec, Message — o "protocolo" entre agentes |
| Agentes de domínio | `pymupdf`, `pytesseract`, `re` | Extração de dados de PDFs financeiros |
| | `statsmodels`, `pandas` | Forecasting (ARIMA/ETS) |
| | `numpy`, `scipy` | Pricing (Black-Scholes, Monte Carlo) |
| Agente LLM | `anthropic` (Claude API) | Planejamento/decomposição de tarefas em linguagem natural |
| Orquestração | máquina de estados própria | O "cérebro" do pipeline: etapas, roteamento, erro |
| Formulação | `qmas.problems` | Alocação de tarefas (GAP) → QUBO/Ising |
| Solvers clássicos | `ortools` (CP-SAT), heurísticas próprias | Baselines fortes (exato + greedy + simulated annealing) |
| Solvers quânticos | `qiskit`, `qiskit-aer` (QAOA), `dwave-ocean-sdk` (annealing) | Candidatos à vantagem |
| Benchmark | `qmas.bench` + `mlflow` | Geradores de instância, métricas, tracking reprodutível |

## Estrutura

```
src/qmas/
├── contracts.py        # Task, AgentSpec, Message (pydantic)
├── agents/             # base + doc_extractor, forecaster, pricer, llm_planner
├── orchestrator/       # state_machine (fluxo) + dispatcher (clássico vs quântico)
├── problems/           # qubo.py (QUBO/Ising) + allocation.py (GAP → QUBO)
├── solvers/            # base (protocolo) + classical + quantum
└── bench/              # generators, metrics (TTS, approx ratio), runner (MLflow)
```

## Instalação

```bash
pip install -e ".[dev]"          # núcleo
pip install -e ".[quantum]"      # + qiskit, dwave
```

## Uso (alvo)

```bash
python -m qmas.bench.runner --config configs/experiment.yaml
```

## Mapeamento para o pré-projeto

- **H1** → `problems/allocation.py` + `solvers/` (crossover clássico↔quântico)
- **H3** → `bench/generators.py` (varredura de tamanho de instância)
- **Etapa 3** → `bench/runner.py` (métricas: time-to-solution, razão de aproximação)
