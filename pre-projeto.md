# Pré-Projeto de Pesquisa — Doutorado

**Título provisório:** Algoritmos Quânticos em Arquiteturas Multiagente: identificação de componentes candidatos e condições para vantagem mensurável

**Candidato(a):** [SEU NOME]

**Programa:** [PROGRAMA DE PÓS-GRADUAÇÃO / INSTITUIÇÃO]

**Linha de pesquisa:** [ex.: Inteligência Artificial / Computação Quântica / Sistemas Distribuídos]

**Orientador(a) pretendido(a):** [NOME]

**Data:** Julho de 2026

---

## 1. Introdução e contextualização

Arquiteturas multiagente baseadas em LLMs (Large Language Models) consolidaram-se como paradigma dominante para sistemas de IA que executam tarefas complexas: um **orquestrador** decompõe o problema, delega subtarefas a **agentes especializados** (extração de dados, busca, previsão, validação), coordena o fluxo de informação entre eles e agrega os resultados. Nessa arquitetura, o LLM é apenas o motor de linguagem; o "raciocínio" do sistema emerge do pipeline ao redor — máquinas de estado, roteamento de tarefas, memória compartilhada, mecanismos de consenso e validação.

É precisamente nesse pipeline — e não no modelo de linguagem em si — que residem problemas computacionais clássicos e bem caracterizados: **alocação de tarefas** (atribuição/matching), **formação de coalizões**, **escalonamento**, **busca em espaços de estados**, **recuperação semântica** e **amostragem/otimização combinatória**. Vários desses problemas são NP-difíceis ou possuem custo que cresce rapidamente com o número de agentes e tarefas, tornando-se gargalos à medida que sistemas multiagente escalam.

Em paralelo, a computação quântica oferece algoritmos com vantagens teóricas comprovadas ou conjecturadas para exatamente essas classes de problemas: busca não estruturada (Grover, ganho quadrático), otimização combinatória (QAOA, quantum annealing), amostragem, e caminhadas quânticas para exploração de grafos. Contudo, a literatura também documenta limites severos: o custo de carregamento de dados (o problema do qRAM), o ruído da era NISQ (Noisy Intermediate-Scale Quantum), a "dequantização" de algoritmos de machine learning quântico por equivalentes clássicos, e o fato de que ganhos assintóticos frequentemente não se traduzem em ganhos práticos para instâncias de tamanho realista.

Existe, portanto, uma lacuna: **não há um mapeamento sistemático entre os componentes de arquiteturas multiagente modernas e os algoritmos quânticos aplicáveis, acompanhado de critérios empíricos e mensuráveis que delimitem quando a substituição do componente clássico pelo quântico (ou híbrido) compensa.** As publicações existentes ou tratam de computação quântica isoladamente, ou de sistemas multiagente isoladamente, ou propõem integrações pontuais (ex.: aprendizado por reforço multiagente quântico) sem uma análise de condições de vantagem.

## 2. Problema de pesquisa

> **Quais componentes de uma arquitetura multiagente podem se beneficiar de algoritmos quânticos, e em quais condições essa substituição produz vantagens mensuráveis sobre as melhores alternativas clássicas?**

Questões secundárias:

1. Quais problemas computacionais internos a uma arquitetura multiagente (orquestração, alocação, roteamento, recuperação, consenso, amostragem) possuem formulação compatível com algoritmos quânticos conhecidos?
2. Para cada par (componente, algoritmo quântico), quais são os regimes — tamanho da instância, estrutura do problema, custo de codificação dos dados, tolerância a erro — em que há vantagem sobre o estado da arte clássico?
3. Como medir essa vantagem de forma justa (time-to-solution, qualidade da solução, custo energético/financeiro), considerando simuladores e hardware NISQ real?
4. Uma arquitetura híbrida clássico-quântica de referência, em que apenas os componentes com vantagem demonstrada são quânticos, supera a arquitetura totalmente clássica em cargas de trabalho realistas?

## 3. Hipóteses

As hipóteses permanecem deliberadamente **abertas** nesta fase: a pesquisa é agnóstica quanto a *onde* — e *se* — a computação quântica traz benefício a arquiteturas multiagente. A revisão sistemática (Etapa 1) as refinará em hipóteses específicas por componente, incluindo a possibilidade de resultados negativos em todas as camadas.

- **H1:** Existem componentes de arquiteturas multiagentes que apresentam vantagens mensuráveis quando implementados com algoritmos quânticos.
- **H2:** As vantagens observadas, quando existirem, dependem do tamanho do problema e da estrutura dos dados (incluindo o custo de codificação de dados clássicos).
- **H3:** Nem todos os componentes se beneficiam igualmente de abordagens quânticas — o mapa de ganhos é heterogêneo entre camadas.
- **H4:** É possível construir um orquestrador híbrido capaz de selecionar dinamicamente entre implementações clássicas e quânticas de um mesmo componente.
- **H5:** Arquiteturas híbridas apresentam melhor relação custo-benefício do que arquiteturas exclusivamente clássicas ou exclusivamente quânticas.

## 4. Objetivos

### 4.1 Objetivo geral

Propor e validar experimentalmente um **framework de decisão** que mapeie componentes de arquiteturas multiagente a algoritmos quânticos aplicáveis e caracterize, de forma mensurável e reprodutível, as condições sob as quais a versão quântica ou híbrida supera a melhor alternativa clássica.

### 4.2 Objetivos específicos

1. **Taxonomia:** decompor arquiteturas multiagente de referência (orquestrador-trabalhadores, blackboard, mercado/leilão, hierárquica) em componentes computacionais formalizáveis, organizados em camadas candidatas — planejamento, recuperação de informação, memória, coordenação, aprendizado e raciocínio — identificando classe de complexidade e estrutura de cada um, **sem privilegiar a priori nenhuma camada**.
2. **Mapeamento:** associar cada componente aos algoritmos quânticos candidatos (Grover e variantes de amplitude amplification, QAOA, annealing, caminhadas quânticas, VQE, amostragem quântica), com análise teórica do ganho esperado e dos custos de codificação.
3. **Baselines fortes:** implementar as melhores soluções clássicas conhecidas para cada componente (solvers exatos, meta-heurísticas, algoritmos aproximados), evitando comparações contra baselines fracos — vício metodológico recorrente na literatura de vantagem quântica.
4. **Bancada experimental:** construir uma bancada de benchmarks reprodutível com instâncias sintéticas e derivadas de cargas reais de sistemas multiagente (traces de orquestração), executando as versões quânticas em simulador (Qiskit/PennyLane) e, quando viável, em hardware real (IBM Quantum, D-Wave via nuvem).
5. **Caracterização de regimes:** determinar empiricamente os limiares (tamanho, densidade de restrições, ruído) em que cada abordagem domina, produzindo curvas de cruzamento (crossover) clássico↔quântico.
6. **Arquitetura de referência:** especificar e prototipar uma arquitetura multiagente híbrida em que o orquestrador decide, em tempo de execução, se despacha o subproblema para o solver clássico ou quântico, com base no framework de decisão.

## 5. Justificativa

Sistemas multiagente estão saindo do papel conceitual para produção: orquestradores comerciais coordenam dezenas de agentes com contratos de entrada/saída, estados e tratamento de erro. O custo computacional da coordenação cresce combinatorialmente e passará a ser gargalo real. Ao mesmo tempo, o acesso a hardware quântico via nuvem tornou-se commodity, mas a decisão de engenharia — *vale a pena usar?* — carece de critérios objetivos. A contribuição desta tese é justamente transformar essa decisão em algo mensurável: em vez de afirmar genericamente que "computação quântica acelera IA", entregar um mapa de **onde**, **quanto** e **sob quais condições**. Cientificamente, o trabalho preenche a lacuna entre duas comunidades (sistemas multiagente e algoritmos quânticos) que raramente dialogam com rigor experimental comum; tecnologicamente, oferece um guia de adoção para arquitetos de sistemas de IA.

## 6. Fundamentação teórica (síntese)

- **Sistemas multiagente:** fundamentos de coordenação, negociação e alocação (Wooldridge, 2009); mecanismos de leilão e formação de coalizões (Shoham & Leyton-Brown, 2009); surveys recentes de agentes baseados em LLM e arquiteturas de orquestração (Wang et al., 2024; Guo et al., 2024).
- **Algoritmos quânticos:** busca de Grover (Grover, 1996); QAOA (Farhi et al., 2014); annealing quântico e formulações QUBO/Ising (Lucas, 2014); caminhadas quânticas; VQE e algoritmos variacionais híbridos (Cerezo et al., 2021).
- **Limites e ceticismo metodológico:** era NISQ e suas restrições (Preskill, 2018); o problema da leitura/escrita de dados e as ressalvas ao QML (Aaronson, 2015); dequantização de algoritmos quânticos de recomendação (Tang, 2019); machine learning quântico e suas promessas condicionais (Biamonte et al., 2017); critérios rigorosos de benchmark de vantagem quântica (Rønnow et al., 2014).
- **Interseção emergente:** aprendizado por reforço multiagente quântico e propostas de coordenação quântica — corpo ainda incipiente, que será objeto da revisão sistemática prevista na metodologia.

*(As referências completas serão consolidadas na revisão sistemática — Etapa 1 do cronograma.)*

## 7. Metodologia

O trabalho segue o ciclo **formalizar → mapear → medir → sintetizar**, em quatro etapas:

**Etapa 1 — Revisão sistemática e taxonomia (semestres 1–2).** Revisão sistemática (protocolo PRISMA adaptado) da literatura nas duas áreas e da interseção. Produto: taxonomia de componentes de arquiteturas multiagente com formalização matemática de cada problema interno (ex.: alocação de tarefas como problema de atribuição generalizada; formação de coalizões como particionamento de conjuntos; roteamento de mensagens como problema em grafos).

**Etapa 2 — Mapeamento teórico e seleção de pares (semestres 2–3).** Para cada componente formalizado, análise de compatibilidade com algoritmos quânticos: existência de formulação QUBO/oráculo, custo de codificação de dados, profundidade de circuito estimada, sensibilidade a ruído. Seleção de 3–5 pares (componente, algoritmo) para investigação experimental profunda, **guiada exclusivamente pelos achados da revisão sistemática** (não por premissa prévia), cobrindo camadas distintas da taxonomia e incluindo ao menos um caso com expectativa negativa na literatura, para teste de falseabilidade.

**Etapa 3 — Bancada experimental e caracterização de regimes (semestres 3–6).** Implementação dos baselines clássicos estado-da-arte e das versões quânticas/híbridas. Execução em simulador (com e sem modelo de ruído) e em hardware real quando o tamanho da instância permitir. Métricas: time-to-solution, qualidade da solução (razão de aproximação), custo monetário/energético, escalabilidade. Análise estatística das curvas de cruzamento. Todos os artefatos (código, instâncias, resultados) publicados em repositório aberto para reprodutibilidade.

**Etapa 4 — Arquitetura híbrida de referência e validação (semestres 6–8).** Consolidação do framework de decisão; prototipação da arquitetura multiagente híbrida com despacho dinâmico clássico/quântico; avaliação end-to-end em cargas de trabalho realistas; redação e defesa da tese.

## 8. Resultados esperados e contribuições

1. **Taxonomia formal** dos problemas computacionais internos a arquiteturas multiagente (contribuição para a comunidade de sistemas multiagente).
2. **Mapa componente→algoritmo quântico** com análise de custos de codificação e regime de vantagem (contribuição para a comunidade de computação quântica aplicada).
3. **Bancada de benchmarks aberta e reprodutível** com baselines clássicos fortes — utilizável por terceiros para avaliar novos dispositivos e algoritmos.
4. **Framework de decisão + arquitetura híbrida de referência**, com protótipo funcional.
5. Publicações-alvo: 1 survey/taxonomia (etapas 1–2), 2 artigos experimentais (etapa 3), 1 artigo de arquitetura/sistema (etapa 4).

## 9. Cronograma (48 meses)

| Atividade | S1 | S2 | S3 | S4 | S5 | S6 | S7 | S8 |
|---|---|---|---|---|---|---|---|---|
| Disciplinas obrigatórias | ● | ● | | | | | | |
| Revisão sistemática e taxonomia | ● | ● | | | | | | |
| Mapeamento teórico e seleção de pares | | ● | ● | | | | | |
| Qualificação | | | ● | | | | | |
| Baselines clássicos | | | ● | ● | | | | |
| Implementações quânticas/híbridas | | | | ● | ● | ● | | |
| Experimentos e caracterização de regimes | | | | ● | ● | ● | | |
| Arquitetura híbrida de referência | | | | | | ● | ● | |
| Redação de artigos | | | ● | ● | ● | ● | ● | |
| Redação e defesa da tese | | | | | | | ● | ● |

## 10. Recursos e viabilidade

- **Software:** Qiskit, PennyLane, D-Wave Ocean (gratuitos); solvers clássicos (OR-Tools, Gurobi acadêmico).
- **Hardware quântico:** acesso via nuvem (IBM Quantum — camada gratuita/acadêmica; D-Wave Leap; possíveis créditos de pesquisa AWS Braket/Azure Quantum).
- **Computação clássica:** cluster institucional para simulação de circuitos e baselines.
- O desenho metodológico não depende de acesso privilegiado a hardware: o núcleo dos resultados (caracterização de regimes) é obtível em simulação com modelos de ruído calibrados, com validação pontual em hardware real.

## 11. Referências preliminares

- AARONSON, S. Read the fine print. *Nature Physics*, v. 11, p. 291–293, 2015.
- BIAMONTE, J. et al. Quantum machine learning. *Nature*, v. 549, p. 195–202, 2017.
- CEREZO, M. et al. Variational quantum algorithms. *Nature Reviews Physics*, v. 3, p. 625–644, 2021.
- FARHI, E.; GOLDSTONE, J.; GUTMANN, S. A Quantum Approximate Optimization Algorithm. *arXiv:1411.4028*, 2014.
- GROVER, L. K. A fast quantum mechanical algorithm for database search. *Proc. 28th ACM STOC*, p. 212–219, 1996.
- GUO, T. et al. Large Language Model based Multi-Agents: A Survey of Progress and Challenges. *IJCAI*, 2024.
- LUCAS, A. Ising formulations of many NP problems. *Frontiers in Physics*, v. 2, 2014.
- PRESKILL, J. Quantum Computing in the NISQ era and beyond. *Quantum*, v. 2, p. 79, 2018.
- RØNNOW, T. F. et al. Defining and detecting quantum speedup. *Science*, v. 345, p. 420–424, 2014.
- SHOHAM, Y.; LEYTON-BROWN, K. *Multiagent Systems: Algorithmic, Game-Theoretic, and Logical Foundations*. Cambridge University Press, 2009.
- TANG, E. A quantum-inspired classical algorithm for recommendation systems. *Proc. 51st ACM STOC*, 2019.
- WANG, L. et al. A survey on large language model based autonomous agents. *Frontiers of Computer Science*, v. 18, 2024.
- WOOLDRIDGE, M. *An Introduction to MultiAgent Systems*. 2. ed. Wiley, 2009.
