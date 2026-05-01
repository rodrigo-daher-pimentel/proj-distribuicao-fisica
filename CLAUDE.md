# CLAUDE.md

## Projeto

Disciplina ENG 4560 — Projeto Integrado VI: Distribuição Física, PUC-Rio.

O projeto resolve o Capacitated Vehicle Routing Problem (CVRP) aplicado a dados reais da Prolog Transporte e Logística. O centro de distribuição fica em Duque de Caxias (CEP 25251-560) e as entregas vão para hospitais, clínicas e farmácias no Rio de Janeiro.

O trabalho se divide em 3 sprints. As aulas do professor guiam o desenvolvimento tecnico; cada conversa de implementacao se enquadra em uma sprint.

### Sprint 1 — 12/03 a 16/04/2026

Pesquisa conceitual sobre VRP/CVRP, formulacao do modelo MILP, implementacao em Python com Gurobi e experimentos com metodos exatos nas instancias C1 a C4.

- Entregas: apresentacao Sprint Review #1 (.pptx, ate 16/04), relatorio parcial #1 (.docx/.pdf, ate 18/04), ata da Retrospective 1 (ate 18/04).
- Relatorio deve conter: revisao da literatura, descricao do problema, formulacao matematica, resultados computacionais (tempo, custo, cenarios), conclusoes sobre viabilidade, codigos Python, ferramentas de gestao (EAP, cronograma, canvas).

### Sprint 2 — 30/04 a 21/05/2026

Heuristicas construtivas (Nearest Neighbor, Clarke & Wright), busca local (2-opt, relocate, exchange) e comparacao com resultados exatos.

- Entregas: apresentacao Sprint Review #2 (.pptx, ate 21/05), relatorio consolidado G1 (.docx/.pdf, ate 23/05), ata da Retrospective 2 (ate 23/05), avaliacao 360 (ate 23/05), codigos Python (ate 23/05).

### Sprint 3 — 28/05 a 09/07/2026

Metaheuristicas (Simulated Annealing, ILS, Algoritmos Geneticos), analise comparativa completa de todas as abordagens.

- Entregas: apresentacao Sprint Review #3 (.pptx, ate 02/07), relatorio final (.docx/.pdf, ate 04/07), ata da Retrospective 3 (ate 04/07), apresentacao final para banca (.pptx, ate 04/07), codigos Python (ate 04/07), avaliacao 360 (ate 09/07).

Observacoes gerais: Sprint Review e apresentacao de ate 15 min. Retrospective e ata individual por aluno. Todo aluno sera P.O. em uma sprint. Todos os entregaveis sao submetidos via Moodle.

### EAP (Estrutura Analitica do Projeto)

A EAP e orientada a entregaveis (nao a atividades). Organizada em 5 areas no nivel 2, com entregaveis no nivel 3:

- **1.1 — Gestao de Projeto**
  - 1.1.1 — EAP
  - 1.1.2 — Canvas de Projeto
  - 1.1.3 — Cronograma
  - 1.1.4 — E-Nao E-Faz-Nao Faz
- **1.2 — Pesquisa e Modelagem**
  - 1.2.1 — Documento de Revisao da Literatura
  - 1.2.2 — Documento de Descricao do Problema e Dados
  - 1.2.3 — Modelo Matematico MILP
- **1.3 — Implementacao Computacional**
  - 1.3.1 — Modelo Exato (Gurobi)
  - 1.3.2 — Codigo de Heuristicas Construtivas
  - 1.3.3 — Codigo de Busca Local
  - 1.3.4 — Codigo de Metaheuristicas
- **1.4 — Analise de Resultados**
  - 1.4.1 — Resultados do Metodo Exato
  - 1.4.2 — Relatorio Comparativo Heuristicas vs. Exato
  - 1.4.3 — Relatorio de Analise Comparativa Final
- **1.5 — Documentacao e Apresentacoes**
  - 1.5.1 — Relatorio Parcial #1
  - 1.5.2 — Apresentacao Sprint Review #1
  - 1.5.3 — Relatorio Consolidado G1
  - 1.5.4 — Apresentacao Sprint Review #2
  - 1.5.5 — Relatorio Final
  - 1.5.6 — Apresentacao Sprint Review #3
  - 1.5.7 — Apresentacao Final para Banca

### Cronograma

| ID    | Entregavel                                  | Inicio | Termino |
| ----- | ------------------------------------------- | ------ | ------- |
| 1.1.1 | EAP                                         | 19/03  | 25/03   |
| 1.1.2 | Canvas de Projeto                           | 19/03  | 01/04   |
| 1.1.3 | Cronograma                                  | 19/03  | 25/03   |
| 1.1.4 | E-Nao E-Faz-Nao Faz                         | 19/03  | 25/03   |
| 1.2.1 | Documento de Revisao da Literatura          | 12/03  | 25/03   |
| 1.2.2 | Documento de Descricao do Problema e Dados  | 12/03  | 18/03   |
| 1.2.3 | Modelo Matematico MILP                      | 19/03  | 01/04   |
| 1.3.1 | Modelo Exato (Gurobi)                       | 26/03  | 09/04   |
| 1.3.2 | Codigo de Heuristicas Construtivas          | 30/04  | 13/05   |
| 1.3.3 | Codigo de Busca Local                       | 07/05  | 20/05   |
| 1.3.4 | Codigo de Metaheuristicas                   | 28/05  | 25/06   |
| 1.4.1 | Resultados do Metodo Exato                  | 02/04  | 15/04   |
| 1.4.2 | Relatorio Comparativo Heuristicas vs. Exato | 14/05  | 20/05   |
| 1.4.3 | Relatorio de Analise Comparativa Final      | 18/06  | 02/07   |
| 1.5.1 | Relatorio Parcial #1                        | 09/04  | 18/04   |
| 1.5.2 | Apresentacao Sprint Review #1               | 09/04  | 16/04   |
| 1.5.3 | Relatorio Consolidado G1                    | 14/05  | 23/05   |
| 1.5.4 | Apresentacao Sprint Review #2               | 14/05  | 21/05   |
| 1.5.5 | Relatorio Final                             | 18/06  | 04/07   |
| 1.5.6 | Apresentacao Sprint Review #3               | 25/06  | 02/07   |
| 1.5.7 | Apresentacao Final para Banca               | 25/06  | 04/07   |

## Estrutura de pastas

- `Base de Dados.xlsx` — base de dados real da Prolog com informações de entregas.
- `Mateiriais Auxiliares/` — notebooks (.ipynb) e slides (.pdf) das aulas do professor. Contém os métodos, formulações e abordagens que devem ser seguidos no projeto. Antes de implementar qualquer modelo ou algoritmo, consultar essa pasta para alinhar com o que foi ensinado em aula. O professor sempre fornece exemplos de código do que deve ser feito; a implementação deve seguir exatamente a estrutura e o código do professor, copiando e colando literalmente. Não inventar abordagens alternativas nem reescrever a lógica por conta própria.
- `Aulas/` — organizada por aula (subpastas `1/`, `2/`, `3/`, `4/`, `5/`). Cada subpasta contém o notebook do grupo, o template do professor, slides e README. A numeração começa em 2 para notebooks porque a Aula 1 foi introdutória.
  - `2/` — Preparação de dados e geração das instâncias C1–C4.
  - `3/` — Modelagem MILP (Parte 1): frota homogênea, sem MTZ.
  - `4/` — Modelagem MILP (Parte 2): frota heterogênea, MTZ, e todos os experimentos computacionais da Sprint 1 (Aula 5). Notebook principal: `Aula4_Modelagem_MILP_Parte2/notebook.ipynb`.
  - `5/` — Acompanhamento Sprint 1 (apenas slides; experimentos implementados no notebook da Aula 4).

## Equipe — Grupo 2

- Rodrigo Pimentel
- Bernardo Caula
- João Felipe Leal
- Lucas Campos
- Lucas Terzi

## Trello

O Trello está configurado como MCP server (`.claude/mcp.json`). O board ativo é `69bbf2901873b0e9b957d4c8`.

Regras de uso:

- Consultar o board antes de iniciar qualquer tarefa para entender o estado atual do projeto.
- Atualizar cartões proativamente: mover entre listas, marcar itens de checklist. Não adicionar comentários nos cartões a menos que o usuário peça explicitamente.
- Ao concluir uma entrega ou subtarefa, marcar o item correspondente como concluído no Trello.
- Ao criar código, documentos ou qualquer artefato do projeto, verificar qual cartão se relaciona e manter o board sincronizado.

Listas do board (da esquerda para a direita):

1. Product Backlog — tarefas ainda não selecionadas para execução
2. Sprint Backlog — tarefas selecionadas para a sprint atual
3. Em Andamento — tarefas em execução
4. Em Revisão — tarefas concluídas aguardando validação
5. Finalizado — tarefas aprovadas

## Jupyter MCP Server

O Jupyter está configurado como MCP server (`.claude/mcp.json`) para execução interativa de notebooks. Isso permite criar, editar e executar células diretamente, sem o usuário precisar rodar manualmente.

Para usar, o JupyterLab precisa estar rodando localmente:

```
jupyter lab --port 8888 --IdentityProvider.token 427fe4d67f724674110862ccee05d08a --ip 127.0.0.1
```

Práticas de uso:

- Ao desenvolver notebooks do projeto, usar as ferramentas do Jupyter MCP para executar células e validar resultados em tempo real.
- Sempre que possível, executar o notebook completo após finalizar para garantir que tudo roda sem erro do início ao fim.
- Os notebooks ficam em `Aulas/<n>/` e devem ser executados com o diretório de trabalho correto para que caminhos relativos funcionem (ex: `../../Base de Dados.xlsx`).

## Estilo

Não usar emojis. Escrever em português do Brasil, com acentos e grafia correta. Linguagem direta e natural, sem fluff nem frases típicas de texto gerado por IA.

## Convenções Gerais

- **Python path**: `py`

## graphify

This project has a graphify knowledge graph at graphify-out/.

Rules:

- Before answering architecture or codebase questions, read graphify-out/GRAPH_REPORT.md for god nodes and community structure
- If graphify-out/wiki/index.md exists, navigate it instead of reading raw files
- After modifying code files in this session, run `python3 -c "from graphify.watch import _rebuild_code; from pathlib import Path; _rebuild_code(Path('.'))"` to keep the graph current

## Diretrizes de Escrita

Todas as regras abaixo são obrigatórias ao produzir ou revisar qualquer texto do relatório, Google Docs ou documento acadêmico deste projeto.

### Linguagem Direta e Natural

Escreva como um especialista conversando com um colega. Tom profissional, porém acessível e fluido. Prefira voz ativa. Construa frases que o leitor absorva em uma única leitura.

### Sem Fluff

Vá direto ao ponto. Elimine introduções longas, advérbios e adjetivos desnecessários. Cada frase deve agregar valor real. Se uma frase pode ser removida sem perda de significado, remova-a.

### Acentos e Grafia Correta

Siga estritamente a norma culta da língua portuguesa (Brasil). Gramática, concordância verbal e nominal, regência e pontuação impecáveis. Acentue todas as palavras corretamente.

### Zero Emojis

Não utilize emojis em nenhuma parte do texto, sob nenhuma circunstância.

### Proibido o "Caronte da IA"

Nunca use jargões ou frases clichês típicas de IA. Lista proibida (incluindo variações):

- "mergulhar", "desvendar", "revolucionário", "potencializar"
- "em resumo", "por fim", "em suma"
- "no cenário atual", "desempenha um papel", "teia", "jornada"
- "vale ressaltar", "é importante destacar", "nesse sentido"
- "diante do exposto", "dessa forma", "sendo assim"

Quando sentir vontade de usar qualquer uma dessas expressões, reformule com vocabulário original e específico ao contexto.

### Estrutura Dinâmica

Alterne o tamanho das frases para criar ritmo natural de leitura. Misture frases curtas e incisivas com frases mais longas e explicativas. Evite sequências com a mesma estrutura sintática.

### Sem Pseudo-Títulos em Negrito

Nunca usar negrito inline como substituto de título de seção (ex.: "**Análise de correlação.** A relação linear..."). Em relatório acadêmico formal, a hierarquia de conteúdo é feita exclusivamente por seções e subseções numeradas. Se o conteúdo merece destaque próprio, crie uma subseção com numeração adequada. Se não merece, integre-o ao fluxo do parágrafo sem destaque artificial.

### Uso de Listas (Bullet Points)

Listas são permitidas em relatórios acadêmicos, mas sob condições restritas:

- Usar apenas quando a enumeração de itens efetivamente facilita a compreensão (componentes, etapas de um processo, variáveis, critérios).
- Cada lista deve ser precedida por uma frase introdutória completa.
- Análise e interpretação vêm sempre em prosa corrida, nunca dentro de bullets. A lista apresenta os itens; os parágrafos seguintes os analisam.
- Não usar listas em introduções, conclusões ou formulações de tese.
- Listas não devem ultrapassar ~25% do conteúdo total do documento.
- Preferir bullets a números, exceto quando há ordem sequencial ou hierarquia explícita entre os itens.

### Convenções Adicionais de Escrita

- Terceira pessoa ou primeira do plural ("este trabalho propõe", "os resultados indicam").
- Termos técnicos com precisão; defina-os na primeira ocorrência.
- Citações no formato (Autor, Ano) conforme ABNT.
- Prefira dados e evidências a afirmações genéricas.
- Parágrafos entre 3 e 7 frases.

### Formatação de Figuras, Tabelas e Quadros (ABNT NBR 14724)

Regras obrigatórias para todas as ilustrações do relatório:

- **Título/Legenda**: sempre **acima** do elemento. Formato: `Figura N – Descrição` (com travessão, não hífen). Numeração sequencial e independente por tipo.
- **Fonte**: sempre **abaixo** do elemento. Formato: `Fonte: Elaboração própria` ou `Fonte: Adaptado de Autor (Ano)`.
- **Notas explicativas**: abaixo da fonte, se houver.
- **Tamanho da fonte**: 10pt para título, fonte e notas (menor que o corpo do texto de 12pt).
- **Espaçamento**: simples nas legendas e fontes.

Distinção entre tipos:

| Tipo   | Uso                                                              | Bordas                                           |
| ------ | ---------------------------------------------------------------- | ------------------------------------------------ |
| Figura | Gráficos, diagramas, fluxogramas, imagens, screenshots de código | Livre                                            |
| Tabela | Dados quantitativos/estatísticos (NBR do IBGE)                   | Laterais abertas (sem bordas verticais externas) |
| Quadro | Dados qualitativos/textuais                                      | Fechado (bordas em todos os lados)               |

Exemplo de estrutura no documento:

```
Figura 7 – Histogramas e boxplots das variáveis de CRM.

   [ ilustração ]

Fonte: Elaboração própria
```
