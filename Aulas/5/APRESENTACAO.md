# Prompt: Criar Apresentacao Sprint Review #1

Voce e um agente especializado em criar apresentacoes academicas. Sua tarefa e gerar o conteudo completo de uma apresentacao em PowerPoint (.pptx) para a Sprint Review #1 da disciplina ENG 4560 -- Projeto Integrado VI: Distribuicao Fisica, PUC-Rio.

## Restricoes da apresentacao

- Tempo maximo: 15 minutos.
- Idioma: portugues do Brasil.
- Tom: tecnico-academico, direto, sem fluff.
- Sem emojis.
- A apresentacao deve cobrir o que foi concluido na Sprint 1, nao o que sera feito nas proximas.
- Data da apresentacao: 16/04/2026.
- Equipe: Grupo 2 -- Rodrigo Pimentel, Bernardo Caula, Joao Felipe Leal, Lucas Campos, Lucas Terzi.
- Disciplina: ENG 4560, Prof. Marcello Congro, Departamento de Engenharia Industrial, PUC-Rio.
- Empresa parceira: Prolog Transporte e Logistica.

---

## CONTEUDO TECNICO A APRESENTAR

Todo o conteudo abaixo deve estar na apresentacao. Nao omitir nenhuma secao.

### 1. Fundamentacao teorica

A apresentacao deve incluir uma secao de fundamentacao teorica que defina os conceitos centrais do trabalho. O objetivo e mostrar que a equipe domina o referencial. Cada conceito deve ser apresentado de forma concisa (2-4 frases), com a referencia bibliografica. Formulas matematicas devem ser incluidas quando indicadas.

#### 1.1 Distribuicao fisica

Distribuicao fisica e o ramo da logistica que trata do planejamento, implementacao e controle do fluxo fisico de materiais e produtos acabados desde o ponto de origem ate o ponto de consumo. As atividades envolvidas incluem planejamento de rotas, dimensionamento de frota, gestao de estoques e sequenciamento de entregas. O transporte representa cerca de 60% do custo logistico total.

Referencia: Ballou, R. H. Gerenciamento da Cadeia de Suprimentos / Logistica Empresarial. 5. ed. Porto Alegre: Bookman, 2006.

#### 1.2 Classes de problemas em logistica

Tres grandes classes: (1) problemas de localizacao (onde instalar CDs/depositos), (2) problemas de roteirizacao e sequenciamento (rotas e ordem de atendimento), (3) problemas de alocacao e dimensionamento (como usar os recursos). O projeto foca na roteirizacao.

Referencia: Drezner, Z. (Ed.). Facility Location: A Survey of Applications and Methods. New York: Springer-Verlag, 1995.

#### 1.3 Otimizacao combinatoria e complexidade NP-dificil

Otimizacao combinatoria busca a melhor solucao dentre um conjunto finito mas exponencialmente grande de candidatas, envolvendo decisoes discretas (sequencias, rotas, agrupamentos). Um problema e NP-dificil quando nao se conhece algoritmo que o resolva em tempo polinomial. O CVRP e NP-dificil (contem o TSP como caso particular). Implicacao pratica: o tempo de resolucao cresce exponencialmente com o tamanho da instancia, impondo um trade-off entre solucao otima (custo computacional alto) e solucao boa obtida rapidamente (heuristicas).

Referencias:
- Goldbarg, M.; Goldbarg, E.; Luna, H. Otimizacao Combinatoria e Metaheuristicas. Rio de Janeiro: GEN/LTC, 2015.
- Garey, M. R.; Johnson, D. S. Computers and Intractability. San Francisco: W. H. Freeman, 1979.

#### 1.4 Vehicle Routing Problem (VRP)

Determinar rotas de custo minimo para uma frota de veiculos que atenda clientes geograficamente dispersos, com cada rota iniciando e terminando no deposito. Introduzido por Dantzig e Ramser (1959) como "Truck Dispatching Problem". Principais variantes: CVRP (capacidade), VRPTW (janelas de tempo), MDVRP (multiplos depositos), VRPB (backhaul), VRPPD (pickup and delivery), OVRP (rotas abertas).

Referencia: Toth, P.; Vigo, D. Vehicle Routing: Problems, Methods, and Applications. 2nd ed. Philadelphia: SIAM, 2014.

#### 1.5 Definicao formal do CVRP

Dado um grafo completo G = (V, A) onde V = {0, 1, ..., n} (no 0 e o deposito, nos 1..n sao clientes), custos c_ij para cada arco, demandas q_i para cada cliente, e uma frota de K veiculos com capacidade Q, encontrar rotas de custo minimo tal que:
1. Cada cliente e atendido exatamente uma vez.
2. Cada rota comeca e termina no deposito.
3. A soma das demandas em cada rota nao excede Q.

A instancia do projeto e descrita pela tupla I = (N, D, q, K, Q, g, v, s, H), onde:
- N = conjunto de clientes
- D = deposito
- q = vetor de demandas (kg)
- K = tipos de veiculos disponiveis
- Q = capacidade por tipo de veiculo (kg)
- g = custo variavel (R$/km)
- v = velocidade media (km/h)
- s = tempo de atendimento por cliente (h)
- H = jornada maxima (h)

Referencia: Laporte, G. The Vehicle Routing Problem: An Overview of Exact and Approximate Algorithms. European Journal of Operational Research, v. 59, n. 3, p. 345-358, 1992.

#### 1.6 Formulacao MILP

Programacao Linear Inteira Mista (MILP): funcao objetivo e restricoes lineares, com variaveis restritas a valores inteiros ou binarios. Variavel de decisao: x_ijk (binaria, 1 se o veiculo k percorre o arco i->j).

Funcao objetivo: min sum_k sum_i sum_j c_ij * x_ijk

Restricoes classicas: visita unica, conservacao de fluxo, saida do deposito, capacidade.

Referencia: Wolsey, L. A. Integer Programming. New York: Wiley-Interscience, 1998.

#### 1.7 Subtours e eliminacao de subtours (MTZ)

Um subtour e um ciclo na solucao que nao passa pelo deposito -- uma rota desconectada e operacionalmente inviavel. Sem restricoes especificas, o solver encontra subtours como parte da solucao "otima" porque reduzem custo artificialmente.

A formulacao MTZ (Miller, Tucker & Zemlin, 1960) elimina subtours com variaveis auxiliares u_i que representam a carga acumulada em cada no:

    u_j - u_i >= q_j - Q(1 - x_ij),  para todo i, j em V\{0}, i != j
    q_i <= u_i <= Q,                  para todo i em V\{0}

Quando x_ij = 1, a restricao forca u_j >= u_i + q_j, impedindo ciclos desconectados.

Referencia: Miller, C. E.; Tucker, A. W.; Zemlin, R. A. Integer Programming Formulation of Traveling Salesman Problems. Journal of the ACM, v. 7, n. 4, p. 326-329, 1960.

#### 1.8 Metodos exatos: Branch and Bound e Branch and Cut

Branch and Bound explora uma arvore de solucoes, dividindo o problema em subproblemas (branching) e usando limites inferiores via relaxacao linear para podar ramos que nao podem conter o otimo (bounding). Branch and Cut estende isso adicionando planos de corte dinamicamente para apertar a relaxacao.

Conceitos-chave:
- Limite inferior (LB): valor da relaxacao linear.
- Limite superior (UB): melhor solucao inteira viavel encontrada (incumbente).
- Gap de otimalidade: gap = (UB - LB) / UB * 100%. Quando gap = 0, a solucao e comprovadamente otima.

Referencia: Wolsey, L. A. Integer Programming. New York: Wiley-Interscience, 1998.

#### 1.9 Solvers MIP

Um solver MIP implementa Branch and Bound, Branch and Cut e pre-processamento para resolver modelos MILP. Gurobi e o solver comercial de referencia (licenca academica gratuita). HiGHS e o solver open-source mais competitivo (Universidade de Edimburgo). Pyomo e o framework de modelagem em Python usado no projeto, permitindo trocar de solver sem alterar o modelo. Para problemas NP-dificeis, a diferenca de desempenho entre solvers pode chegar a ordens de magnitude.

#### 1.10 Hierarquia de metodos de solucao (contexto)

Os metodos de solucao para o CVRP formam uma hierarquia:
- Metodos exatos (Sprint 1): garantem otimalidade, mas tempo cresce exponencialmente. Exemplo: Branch and Bound/Cut.
- Heuristicas construtivas (Sprint 2): constroem solucao viavel rapidamente, sem garantia de otimalidade. Exemplos: Nearest Neighbor, Clarke & Wright Savings.
- Metaheuristicas (Sprint 3): guiam heuristicas para escapar de otimos locais, equilibrando diversificacao e intensificacao. Exemplos: Simulated Annealing, ILS, Algoritmos Geneticos.

A Sprint 1 foca nos metodos exatos. As sprints seguintes avancarao na hierarquia.

### 2. Contexto do problema

A Prolog Transporte e Logistica e uma empresa brasileira de transporte rodoviario de cargas e logistica last mile, atendendo demandas B2B, B2C e B2D. As entregas partem de um Centro de Distribuicao (CD) em Duque de Caxias (CEP 25251-560) e vao para hospitais, clinicas e farmacias no Rio de Janeiro.

Base de dados real fornecida pela Prolog:
- 1.021 registros brutos de entregas (dia 03/06/2025)
- 243 CEPs repetidos (multiplos pedidos para o mesmo ponto)
- Apos agregacao por CEP: 581 clientes unicos
- Demanda total no dia: 25.324 kg
- Campos: CEP de entrega, quantidade de volumes, peso real (kg), valor da mercadoria (R$)

O problema resolvido e o CVRP: determinar rotas para uma frota de veiculos que minimizem o custo total de transporte, respeitando restricoes de capacidade.

### 3. Preparacao de dados e instancias

Quatro instancias de teste foram geradas a partir da base real, com seed fixa (42) e segundo bloco de 60 clientes (EQUIPE_ID = 2). As instancias sao aninhadas: C1 esta contida em C2, que esta contida em C3, que esta contida em C4.

| Instancia | Clientes | Demanda total (kg) | Media (kg/cliente) |
|-----------|----------|--------------------|--------------------|
| C1_10     | 10       | 141,6              | 14,2               |
| C2_25     | 25       | 754,5              | 30,2               |
| C3_40     | 40       | 1.295,3            | 32,4               |
| C4_60     | 60       | 1.958,1            | 32,6               |

Coordenadas derivadas deterministicamente do CEP. Distancias calculadas por formula de Haversine (aproximacao geometrica, nao distancias viarias reais).

Parametros operacionais (mapeamento para a tupla I):

| Parametro                   | Simbolo | Valor                          |
|-----------------------------|---------|--------------------------------|
| Deposito (CD)               | D       | CEP 25251-560, Duque de Caxias |
| Custo variavel              | g       | R$ 1,50/km                     |
| Velocidade media            | v       | 40 km/h                        |
| Tempo de atendimento        | s       | 15 min/cliente                 |
| Jornada maxima              | H       | 8 h                            |
| Fiorino -- capacidade       | Q_FIO   | 650 kg                         |
| Fiorino -- custo fixo       | f_FIO   | R$ 250/dia                     |
| VUC -- capacidade           | Q_VUC   | 3.000 kg                       |
| VUC -- custo fixo           | f_VUC   | R$ 550/dia                     |

### 4. Primeiro modelo: frota homogenea, sem eliminacao de subtours

Framework: Pyomo + Gurobi 13.0.1 (licenca academica PUC-Rio).

Variavel de decisao: x_ij binaria (1 se o veiculo percorre o arco i->j).

Funcao objetivo: min sum_{(i,j)} c_ij * x_ij + f * m, onde m = numero de veiculos (arcos saindo do deposito).

Restricoes:
1. Visita unica (grau de entrada e saida = 1 para cada cliente)
2. Conservacao de fluxo
3. Balanco no deposito (saidas = retornos)
4. Capacidade agregada (demanda total <= Q * m)

Este modelo nao inclui restricoes MTZ. Sem elas, ciclos desconectados do deposito (subtours) sao solucoes validas para o solver.

Resultados (frota homogenea, somente VUC):

| Instancia | Clientes | Custo (R$) | Veiculos | Subtours | Tempo (s) | Status  |
|-----------|----------|-----------|----------|----------|-----------|---------|
| C1_10     | 10       | 668,80    | 1        | 4        | 0,03      | optimal |
| C2_25     | 25       | 666,15    | 1        | 11       | 0,06      | optimal |
| C3_40     | 40       | 678,34    | 1        | 19       | 0,08      | optimal |
| C4_60     | 60       | 738,63    | 1        | 27       | 0,17      | optimal |

Conclusao: o solver nao errou -- a formulacao e que estava incompleta. Sem MTZ, o solver encontra subtours como "solucoes otimas". Os custos sao artificialmente baixos e as rotas nao sao operacionalmente viaveis. Isso demonstra por que a eliminacao de subtours e indispensavel.

### 5. Modelo completo: frota heterogenea + restricoes MTZ

Evolucao do modelo anterior:
- Frota heterogenea: Fiorino (Q=650kg, f=R$250) + VUC (Q=3.000kg, f=R$550)
- Restricoes MTZ para garantir que todas as rotas passem pelo deposito
- Variavel estendida: x_ijk (arco i->j por tipo de veiculo k)

Restricoes adicionais:
- MTZ: u_j - u_i >= q_j - Q(1 - x_ij), forcando conectividade
- Ativacao de veiculos: se sai do deposito, y[k]=1
- Capacidade por tipo de veiculo
- Conservacao de fluxo por tipo de veiculo

Resultados:

| Instancia | Clientes | Custo (R$) | VUC | FIO | Rotas | Tempo (s) | Status       |
|-----------|----------|-----------|-----|-----|-------|-----------|--------------|
| C1_10     | 10       | 422,38    | 0   | 1   | 1     | 0,27      | optimal      |
| C2_25     | 25       | 754,04    | 1   | 0   | 1     | 52,69     | optimal      |
| C3_40     | 40       | 769,65    | 1   | 0   | 1     | 300,73    | maxTimeLimit |
| C4_60     | 60       | 858,31    | 1   | 0   | 1     | 300,88    | maxTimeLimit |

Pontos a destacar:
- C1 usa Fiorino: demanda de 141,6 kg cabe no Fiorino, que tem custo fixo menor (R$250 vs R$550).
- C2 a C4 usam VUC: demanda excede capacidade do Fiorino (754,5 kg > 650 kg).
- C3 e C4 nao atingiram otimalidade no limite de 300 segundos -- gap aberto (3,56% e 4,37%).
- Jornada maxima de 8h validada em pos-processamento (nao imposta no MIP).

### 6. Experimentos computacionais

Quatro experimentos foram realizados para avaliar sistematicamente o comportamento do modelo.

#### Exp. 1: Impacto da eliminacao de subtours (com vs. sem MTZ)

| Instancia | COM MTZ (R$) | Restricoes | Tempo    | SEM MTZ (R$) | Restricoes | Subtours | Tempo  |
|-----------|-------------|-----------|----------|-------------|-----------|----------|--------|
| C1_10     | 422,38      | 139       | 0,79s    | 368,80      | 49        | 4        | 0,13s  |
| C2_25     | 754,04      | 709       | 65,01s   | 666,15      | 109       | 11       | 0,20s  |
| C3_40     | 769,65      | 1.729     | 300,98s  | 676,69      | 169       | 19       | 0,17s  |
| C4_60     | 858,31      | 3.789     | 300,54s  | 734,59      | 249       | 28       | 0,18s  |

Sem MTZ o custo e menor, mas as solucoes contem subtours e sao inviaveis operacionalmente. O numero de restricoes cresce quadraticamente com MTZ (de 49 para 139 na C1, de 249 para 3.789 na C4), e o tempo de resolucao explode (de 0,18s para 300s na C4).

#### Exp. 2: Sensibilidade ao limite de tempo (gap vs. time limit)

| Instancia | TL=30s  | Gap   | TL=60s  | Gap   | TL=300s | Gap   |
|-----------|---------|-------|---------|-------|---------|-------|
| C1_10     | 422,38  | 0,00% | 422,38  | 0,00% | 422,38  | 0,00% |
| C2_25     | 754,04  | 0,45% | 754,04  | 0,14% | 754,04  | 0,00% |
| C3_40     | 792,17  | 7,79% | 776,20  | 5,80% | 769,65  | 3,56% |
| C4_60     | 875,61  | 7,03% | 862,20  | 5,15% | 858,31  | 4,37% |

C1 e C2 atingem otimalidade rapidamente (gap = 0%). C3 e C4 melhoram com mais tempo mas nao fecham o gap mesmo com 300s. A C2 encontra a mesma solucao em 30s (R$ 754,04), mas so prova otimalidade com 300s (gap cai de 0,45% para 0%). Isso evidencia a diferenca entre encontrar uma boa solucao e provar que ela e otima.

#### Exp. 3: Comparacao de solvers (Gurobi vs. HiGHS)

Executado nas instancias C1 e C2 (C3 e C4 seriam impraticaveis para HiGHS).

| Instancia | Gurobi (R$) | Gap   | Tempo   | HiGHS (R$) | Gap   | Tempo    | Status HiGHS |
|-----------|------------|-------|---------|-----------|-------|----------|--------------|
| C1_10     | 422,38     | 0,00% | 0,58s   | 422,38    | 0,01% | 6,39s    | optimal      |
| C2_25     | 754,04     | 0,00% | 77,05s  | 760,18    | 6,07% | 300,23s  | maxTimeLimit |

Gurobi e significativamente mais rapido e encontra solucoes de melhor qualidade. Na C2, HiGHS nao atingiu otimalidade em 300s e encontrou solucao R$ 6,14 mais cara (gap de 6,07% vs. 0,00%). A diferenca de desempenho e de ordens de magnitude, confirmando que a escolha de solver importa em problemas NP-dificeis.

#### Exp. 4: Analise de sensibilidade de parametros

Duas variacoes testadas sobre a instancia C1_10 (modelo completo com MTZ + frota heterogenea):

| Variacao                        | Custo total (R$) | FIO | VUC | Mudanca vs. base |
|---------------------------------|-------------------|-----|-----|------------------|
| Base (f_VUC=R$550, Q_VUC=3000) | 422,38            | 1   | 0   | --               |
| Custo fixo VUC = R$ 1.500      | 422,38            | 1   | 0   | Nenhuma          |
| Capacidade VUC = 1.000 kg      | 422,38            | 1   | 0   | Nenhuma          |

Resultado: nenhuma das variacoes alterou a solucao. Isso e esperado: a demanda de C1_10 e 141,6 kg, muito abaixo da capacidade do Fiorino (650 kg). O modelo ja prefere Fiorino por ter custo fixo menor (R$ 250 vs. R$ 550). Aumentar o custo do VUC ou reduzir sua capacidade nao tem efeito porque o VUC ja nao e selecionado. A analise seria mais informativa em instancias onde o VUC e escolhido (C2-C4), onde variacoes de custo e capacidade poderiam forcar mudancas na composicao da frota.

### 7. Conclusoes sobre viabilidade do metodo exato

A Sprint 1 permite uma conclusao estruturada sobre a viabilidade do metodo exato (Branch and Cut via Gurobi) para o CVRP nas instancias do projeto:

| Instancia | Clientes | Veredicto           | Evidencia                                                |
|-----------|----------|---------------------|----------------------------------------------------------|
| C1_10     | 10       | Viavel              | Otimo comprovado em < 1s, gap = 0%                       |
| C2_25     | 25       | Viavel              | Otimo comprovado em ~65s, gap = 0%                       |
| C3_40     | 40       | Parcialmente viavel | Solucao boa (gap 3,56%) em 300s, mas sem prova de otimo  |
| C4_60     | 60       | Insuficiente        | Gap de 4,37% apos 300s, tendencia de melhoria lenta      |

O metodo exato resolve com otimalidade comprovada instancias de ate ~25 clientes em tempo aceitavel. Para 40+ clientes, o gap permanece aberto mesmo com 5 minutos de processamento, e a tendencia de convergencia e lenta. Isso motiva a implementacao de heuristicas construtivas (Sprint 2) e metaheuristicas (Sprint 3), que trocam garantia de otimalidade por velocidade.

Comparando com a escala real da Prolog (581 clientes/dia), o metodo exato e inviavel para a operacao completa, mas serve como benchmark: a solucao exata fornece o limite inferior contra o qual as heuristicas serao avaliadas.

### 8. Gestao do projeto

- Metodologia SCRUM adaptada, com sprints de ~20 dias.
- Trello como ferramenta de gestao (listas: Product Backlog, Sprint Backlog, Em Andamento, Em Revisao, Finalizado).
- Product Owner rotativo por sprint.
- EAP orientada a entregaveis: 5 areas no nivel 2, 22 entregaveis no nivel 3.
- Cronograma, Canvas de Projeto e E/Nao E/Faz/Nao Faz elaborados.

---

## ATIVOS VISUAIS — INSTRUCOES DETALHADAS

As imagens abaixo foram geradas nos notebooks do projeto. Caminhos relativos a raiz do projeto. Voce NAO consegue ver as imagens — use as descricoes abaixo para criar o placeholder correto no slide (titulo, legenda, nota de rodape) e indicar ao usuario onde inserir cada imagem.

Para cada imagem: insira um placeholder visual no slide (caixa com borda, titulo descritivo, e instrucao "Inserir imagem: [caminho]"). Dimensione o placeholder de acordo com o aspect ratio indicado.

---

### IMAGEM 1 — Dispersao geografica completa (581 clientes)
**Arquivo:** `Aulas/2/Aula2_Preparacao_Dados/images/notebook_9_0.png`
**Aspect ratio:** ~quadrado (ligeiramente mais largo que alto)
**Usar na secao:** Contexto do problema / Dados

**Descricao visual detalhada:**
Scatter plot matplotlib com fundo branco e grade cinza claro. Titulo: "Nos do problema (clientes e deposito)". Eixo X: Longitude (-44.16 a -44.04). Eixo Y: Latitude (-23.2 a -22.4). Existem ~581 pontos azuis (clientes) e 1 marcador vermelho em forma de X grande (deposito). Os clientes se concentram em duas faixas densas: uma na regiao sul do grafico (latitude -23.05 a -23.20, abrangendo toda a largura de longitude) e outra na faixa de -22.70 a -22.80. A regiao central do grafico (latitude -22.85 a -23.0) e mais esparsa. O deposito (X vermelho) esta posicionado no quadrante leste, em aproximadamente (-44.07, -23.05), ligeiramente acima da faixa densa sul. Legenda no canto superior direito: circulo azul "Clientes", X vermelho "Deposito".

**Proposito no slide:** Mostrar a escala real da operacao da Prolog — 581 pontos de entrega espalhados pelo Rio de Janeiro. O deposito em Duque de Caxias esta no lado leste, e as entregas se espalham para o oeste e norte. Esta imagem introduz a dimensao geografica do problema antes de mostrar as instancias reduzidas C1-C4.

**Sugestao de legenda do slide:** "581 clientes unicos derivados da base de dados da Prolog (03/06/2025). Deposito (CD) em Duque de Caxias."

---

### IMAGEM 2 — Instancia C4_60 (maior instancia de teste)
**Arquivo:** `Aulas/2/Aula2_Preparacao_Dados/images/notebook_18_3.png`
**Aspect ratio:** ~paisagem (ligeiramente mais largo que alto)
**Usar na secao:** Preparacao de dados / Instancias

**Descricao visual detalhada:**
Scatter plot matplotlib similar a Imagem 1, mas com apenas 60 pontos azuis e 1 X vermelho. Titulo: "Instancia C4_60 (60 clientes)". Mesmos eixos de longitude e latitude. Os 60 clientes estao distribuidos pela area metropolitana, mantendo o padrao geral de concentracao na faixa sul (-23.05 a -23.20) com alguns pontos mais ao norte (-22.55 a -22.75). O deposito (X vermelho) esta na mesma posicao (~-44.07, -23.05). Legenda: circulo azul "Clientes", X vermelho "Deposito".

**Proposito no slide:** Mostrar a maior instancia de teste do projeto. Pode ser colocada ao lado da tabela de instancias C1-C4 para dar dimensao espacial ao problema. Opcionalmente, colocar a C1_10 (Imagem 3 abaixo) ao lado para mostrar o contraste de escala (10 vs 60 clientes).

**Sugestao de legenda:** "Instancia C4_60: 60 clientes, 1.958 kg de demanda total. Amostra aninhada da base real."

---

### IMAGEM 3 — Diagnostico de subtours (3 paineis, SEM MTZ)
**Arquivo:** `Aulas/3/Aula3_Modelagem_MILP/images/notebook_19_0.png`
**Aspect ratio:** panoramico horizontal (proporcao ~3:1, muito mais largo que alto)
**Usar na secao:** Modelo sem MTZ — esta e a imagem mais importante da apresentacao para esta secao

**Descricao visual detalhada:**
Figura com TRES paineis lado a lado, gerada com matplotlib subplots. Todos os tres paineis mostram a instancia C1_10 (10 clientes) com mesmos eixos de latitude/longitude. Fundo branco, grade cinza.

- **Painel esquerdo — "Nos do Problema (CVRP)":** Apenas os pontos sem conexao. 10 pontos azuis pequenos (clientes) e 1 circulo vermelho grande (deposito, ~3x o tamanho dos pontos azuis). Deposito posicionado no centro-direita do grafico. E simplesmente a disposicao espacial dos nos antes de qualquer rota.

- **Painel central — "Rotas Reconstruidas":** Os mesmos nos agora conectados por segmentos de reta. Uma unica rota verde conecta o deposito a 2-3 clientes proximos (os unicos que realmente tocam o deposito). Os demais clientes aparecem conectados entre si em pequenos segmentos separados, formando ciclos desconectados do deposito. O resultado visual e uma rota principal curta saindo do deposito e varios fragmentos isolados espalhados pelo mapa.

- **Painel direito — "Diagnostico Visual de Subtours":** Mesmo layout, mas agora os subtours sao destacados em VERMELHO e a rota conectada ao deposito em AZUL/VERDE. Sao visiveis 4 ciclos vermelhos desconectados — pequenos poligonos fechados entre 2-3 clientes cada, sem nenhuma ligacao ao deposito (circulo vermelho grande). Esses ciclos vermelhos sao os subtours: rotas inviaveis onde um veiculo ficticio circularia entre clientes sem nunca voltar ao deposito para carregar.

**Proposito no slide:** Esta e a imagem-chave para explicar POR QUE o MTZ e necessario. O painel central mostra que o solver gerou rotas desconectadas; o painel direito diagnostica explicitamente os subtours em vermelho. A narrativa e: "o solver nao errou — a formulacao e que estava incompleta. Sem restricoes de eliminacao de subtours, o solver encontra esses ciclos como 'solucoes otimas' porque reduzem custo artificialmente."

**Sugestao de legenda:** "Instancia C1_10 sem restricoes MTZ: 4 subtours detectados (ciclos vermelhos). Custo artificialmente baixo (R$ 368,80) com rotas operacionalmente inviaveis."

**IMPORTANTE — dimensionamento:** Esta imagem e panoramica (3:1). Funciona melhor ocupando a LARGURA TOTAL do slide, posicionada na metade inferior, com texto explicativo acima. Nao reduzir para um canto — os detalhes dos paineis ficam ilegiveis.

---

### IMAGEM 4 — Rota correta com MTZ (C1_10, Fiorino)
**Arquivo:** `Aulas/4/Aula4_Modelagem_MILP_Parte2/images/notebook_18_0.png`
**Aspect ratio:** ~quadrado
**Usar na secao:** Modelo com MTZ — contraste direto com a Imagem 3

**Descricao visual detalhada:**
Grafico matplotlib com fundo branco e grade cinza. Titulo: "Rotas com MTZ + Frota Heterogenea — Equipe_2_C1_10". Eixo X: Longitude (-44.16 a -44.04). Eixo Y: Latitude (-23.22 a -22.65). O deposito e um QUADRADO VERMELHO grande (diferente do X das imagens anteriores) posicionado em (~-44.07, -23.05). Os 10 clientes sao CIRCULOS AZUIS. Uma unica linha VERMELHA continua conecta todos os pontos em sequencia, formando uma rota unica: a linha sai do deposito, visita os clientes proximos ao sul, sobe ate os clientes ao norte (a rota se estende ate latitude -22.65, o ponto mais ao norte), e retorna ao deposito. A rota forma um grande circuito sem nenhum cruzamento evidente. Legenda: circulo azul "Clientes", quadrado vermelho "Deposito", linha vermelha "Rota 1 [FIO]".

**Proposito no slide:** Mostrar a solucao CORRETA do modelo com MTZ. A rota unica conectada contrasta diretamente com os subtours da Imagem 3. Ambas usam a mesma instancia (C1_10), entao a comparacao e direta: antes (fragmentos desconectados) vs. depois (rota unica viavel). O fato de usar Fiorino (indicado por [FIO] na legenda) e coerente com a analise de custo (demanda 141,6 kg < 650 kg).

**Sugestao de legenda:** "C1_10 com MTZ: rota unica conectada, Fiorino selecionado. Custo: R$ 422,38 (otimo comprovado em 0,27s)."

**Sugestao de layout:** Colocar lado a lado com o painel direito da Imagem 3 (diagnostico de subtours) para criar o contraste visual SEM MTZ vs COM MTZ na mesma instancia C1_10. Alternativamente, usar a Imagem 5 abaixo que ja traz esse contraste pronto para C2_25.

---

### IMAGEM 5 — Comparacao lado a lado COM vs SEM MTZ (C2_25)
**Arquivo:** `Aulas/4/Aula4_Modelagem_MILP_Parte2/images/notebook_29_0.png`
**Aspect ratio:** panoramico horizontal (~2:1)
**Usar na secao:** Experimento 1 (impacto do MTZ) — A IMAGEM MAIS IMPACTANTE DA APRESENTACAO

**Descricao visual detalhada:**
Figura com DOIS paineis lado a lado, ambos mostrando a instancia C2_25 (25 clientes).

- **Painel esquerdo — "COM MTZ — Custo: R$ 754.04 / Subtours: 0 / Tempo: 64.9s":**
  Fundo branco, grade cinza. Eixos de latitude (-23.2 a -22.7) e longitude (-44.16 a -44.04). O deposito e um QUADRADO VERMELHO grande posicionado em (~-44.07, -23.05). Os 25 clientes sao CIRCULOS AZUIS. Uma LINHA VERMELHA continua conecta TODOS os 25 clientes em uma rota unica, passando pelo deposito. A rota forma um circuito que percorre o mapa de sul a norte: sai do deposito, desce ao sul para clientes na faixa -23.1 a -23.2, sobe pela esquerda passando por clientes em -22.9 a -22.7, cruza para a direita nos clientes ao norte, e retorna ao deposito. E uma rota viavel, conectada, com todos os pontos visitados. Legenda: circulo azul "Clientes", quadrado vermelho "Deposito", linha vermelha "Rota 1 [VUC]".

- **Painel direito — "SEM MTZ — Custo: R$ 666.15 / Subtours: 11 / Tempo: 0.1s":**
  Mesmos eixos. O deposito e o mesmo quadrado vermelho, mas agora esta ISOLADO — praticamente sem conexoes. Os clientes NAO sao circulos azuis: sao LOSANGOS LARANJA/DOURADOS, representando nos em subtours. Apenas 2-3 pontos sao circulos azuis (conectados ao deposito). Os losangos laranja estao espalhados por todo o mapa em pares e trios, formando 11 micro-ciclos desconectados. O efeito visual e dramatico: no painel esquerdo, uma rede organizada; no painel direito, caos total com pontos soltos. A solucao custa R$ 88 a menos, mas e completamente inutil operacionalmente. Legenda: circulo azul "Clientes", quadrado vermelho "Deposito", linha vermelha "Rota 1 [VUC]", losango laranja "Subtour (11 ciclo(s))".

**Proposito no slide:** Esta e a imagem que vende o argumento central da Sprint 1: o custo menor SEM MTZ (R$ 666 < R$ 754) e uma ilusao — a solucao e inviavel. O contraste visual e imediato e nao precisa de explicacao longa. O painel esquerdo e uma rota que um caminhao pode seguir; o painel direito sao fragmentos desconectados que nenhum veiculo real pode executar.

**Sugestao de legenda:** "C2_25: COM MTZ (esquerda) gera rota conectada e viavel; SEM MTZ (direita) gera 11 subtours com custo artificialmente menor."

**IMPORTANTE — dimensionamento:** Panoramica (2:1). Ocupar largura total do slide. Os subtitulos de cada painel (custo, subtours, tempo) ja estao na imagem, entao nao duplicar no texto do slide.

---

### IMAGEM 6 — Custo e gap vs. time limit (Experimento 2)
**Arquivo:** `Aulas/4/Aula4_Modelagem_MILP_Parte2/images/notebook_32_0.png`
**Aspect ratio:** panoramico horizontal (~2.5:1)
**Usar na secao:** Experimento 2 (sensibilidade ao limite de tempo)

**Descricao visual detalhada:**
Figura com DOIS graficos de linha lado a lado. Titulo geral: "Analise de Sensibilidade — Limite de Tempo".

- **Grafico esquerdo — "Custo Incumbente vs Time Limit":**
  Eixo X: Time Limit em segundos (30, 60, 300) — escala nao-linear, com os tres pontos espacados. Eixo Y: Custo Total em R$ (400 a 875). Quatro linhas com marcadores circulares, uma por instancia:
  - **C1_10 (azul):** Linha plana em ~R$ 422, completamente horizontal. Nao muda com mais tempo.
  - **C2_25 (laranja):** Linha plana em ~R$ 754, tambem horizontal.
  - **C3_40 (verde):** Comeca em ~R$ 792 (TL=30s), desce para ~R$ 776 (TL=60s), e para ~R$ 770 (TL=300s). Tendencia descendente com retornos decrescentes.
  - **C4_60 (vermelho):** Comeca em ~R$ 876 (TL=30s), desce para ~R$ 862 (TL=60s), e para ~R$ 858 (TL=300s). Mesma tendencia, partindo de patamar mais alto.
  Legenda no canto superior direito com as 4 instancias.

- **Grafico direito — "Gap de Otimalidade vs Time Limit":**
  Eixo X: Time Limit em segundos (30, 60, 300). Eixo Y: Gap em % (0 a ~8). Mesmas 4 linhas:
  - **C1_10 (azul):** Em 0% constante — otimo comprovado sempre.
  - **C2_25 (laranja):** Comeca em ~0,45% (TL=30s), cai para ~0,14% (TL=60s), chega a 0% (TL=300s). Converge ao otimo.
  - **C3_40 (verde):** Comeca em ~7,8%, cai para ~5,8%, depois ~3,6%. NAO chega a 0%. Tendencia decrescente mas com plateau.
  - **C4_60 (vermelho):** Comeca em ~7,0%, cai para ~5,2%, depois ~4,4%. Tambem nao chega a 0%. A curva do C4 cruza com a do C3 entre TL=60s e TL=300s (C4 termina com gap MAIOR que C3 em TL=300s).
  Legenda identica.

**Proposito no slide:** Quantificar o trade-off entre tempo computacional e qualidade da solucao. O grafico esquerdo mostra que mais tempo melhora o custo marginalmente para C3/C4 mas nao para C1/C2. O grafico direito e o mais revelador: C1/C2 convergem a gap=0%, mas C3/C4 ficam presos em 3-4% mesmo com 300s — evidencia direta da complexidade NP-hard e motivacao concreta para heuristicas.

**Sugestao de legenda:** "Instancias pequenas (C1, C2) atingem otimalidade; instancias maiores (C3, C4) apresentam gaps persistentes mesmo com 5 minutos."

**IMPORTANTE — dimensionamento:** Panoramica (2.5:1). Ocupar largura total do slide. Os rotulos dos eixos sao legíveis em tamanho grande.

---

### IMAGEM 7 — Estrutura Analitica do Projeto (EAP)
**Arquivo:** `EAP.jpg`
**Aspect ratio:** ~paisagem (ligeiramente mais largo que alto)
**Usar na secao:** Gestao do projeto

**Descricao visual detalhada:**
Diagrama hierarquico profissional com fundo branco e caixas retangulares com bordas e headers azul-escuro. No topo, caixa raiz: "1.0 — Projeto de Distribuicao Fisica (CVRP — Prolog)". Abaixo, 5 caixas de nivel 2 alinhadas horizontalmente, conectadas por linhas verticais e horizontais:

1. "1.1 — Gestao de Projeto" → 4 filhos verticais: EAP, Canvas de Projeto, Cronograma, Matriz E-Nao E-Faz-Nao Faz
2. "1.2 — Pesquisa e Modelagem" → 3 filhos: Documento de Revisao Bibliografica, Documento de Descricao do Problema e Base de Dados, Modelo Matematico MILP Formalizado
3. "1.3 — Implementacao Computacional" → 4 filhos: Codigo do Modelo Exato (Gurobi), Codigo das Heuristicas Construtivas, Codigo dos Algoritmos de Busca Local, Codigo das Metaheuristicas
4. "1.4 — Analise de Resultados" → 3 filhos: Relatorio de Resultados — Metodo Exato, Relatorio Comparativo Heuristicas vs. Exato, Relatorio de Analise Comparativa Final
5. "1.5 — Documentacao e Apresentacoes" → 7 filhos: Relatorio Parcial #1, Apresentacao Sprint Review #1, Relatorio Consolidado G1, Apresentacao Sprint Review #2, Relatorio Final, Apresentacao Sprint Review #3, Apresentacao Final para Banca

Total: 5 areas, 21 entregaveis. As caixas de nivel 3 estao dispostas verticalmente abaixo de cada area, conectadas por linhas. O diagrama ocupa toda a largura da imagem.

**Proposito no slide:** Mostrar a visao geral do projeto e seus entregaveis. Na Sprint Review #1, os entregaveis concluidos sao os de 1.1 (gestao), 1.2 (pesquisa e modelagem), 1.3.1 (modelo exato), e 1.4.1 (resultados do exato). Pode-se destacar os itens concluidos visualmente no slide (ex: borda verde ou check) vs. os que serao feitos nas sprints 2 e 3.

**Sugestao de legenda:** "EAP orientada a entregaveis: 5 areas, 21 itens. Destaques em [cor] indicam itens concluidos na Sprint 1."

---

## NARRATIVA SUGERIDA (com posicionamento de imagens)

A historia da Sprint 1 segue uma progressao natural. Entre colchetes, a imagem que deve acompanhar cada momento.

1. **Fundamentacao** -- posicionar o CVRP: distribuicao fisica, classes de problemas, VRP e variantes, por que e NP-dificil, hierarquia de metodos (exatos -> heuristicas -> metaheuristicas). Slides de texto/formulas, sem imagem do projeto.
2. **Problema real** -- apresentar a Prolog, os dados, o desafio logistico concreto. [IMAGEM 1: scatter 581 clientes — mostra a escala real da operacao].
3. **Definicao formal** -- instancia I = (N, D, q, K, Q, g, v, s, H), tabela de parametros, instancias C1-C4. [IMAGEM 2: scatter C4_60 — mostra a maior instancia de teste, ao lado da tabela de instancias].
4. **Modelo incompleto** -- formulacao MILP sem MTZ. Demonstrar o problema: subtours. [IMAGEM 3: tres paineis de diagnostico de subtours — a imagem que mostra rotas desconectadas e diagnostica os ciclos em vermelho]. A mensagem central: "o solver nao errou, o modelo e que estava incompleto."
5. **Modelo completo** -- adicao de MTZ + frota heterogenea. [IMAGEM 4: rota C1_10 com MTZ — rota unica conectada, contraste direto com a Imagem 3 na mesma instancia]. Explicar a intuicao do MTZ (variaveis u_i forcam ordem de visita).
6. **Experimentos** -- [IMAGEM 5: comparacao lado a lado COM vs SEM MTZ para C2_25 — a imagem mais impactante, usada para o Exp. 1]. [IMAGEM 6: graficos de custo e gap vs. time limit — usada para o Exp. 2]. Os Exp. 3 e 4 sao apresentados em tabelas, sem imagem.
7. **Conclusoes de viabilidade** -- tabela de veredicto por instancia, conexao com a escala real (581 clientes), motivacao para as proximas sprints. Slide de texto.
8. **Gestao** -- [IMAGEM 7: EAP — diagrama hierarquico do projeto, com destaque para itens concluidos na Sprint 1].

---

## REFERENCIAS BIBLIOGRAFICAS

Incluir um slide final com as referencias utilizadas na fundamentacao:

1. Ballou, R. H. Gerenciamento da Cadeia de Suprimentos / Logistica Empresarial. 5. ed. Porto Alegre: Bookman, 2006.
2. Drezner, Z. (Ed.). Facility Location: A Survey of Applications and Methods. New York: Springer-Verlag, 1995.
3. Goldbarg, M.; Goldbarg, E.; Luna, H. Otimizacao Combinatoria e Metaheuristicas. Rio de Janeiro: GEN/LTC, 2015.
4. Garey, M. R.; Johnson, D. S. Computers and Intractability. San Francisco: W. H. Freeman, 1979.
5. Toth, P.; Vigo, D. Vehicle Routing: Problems, Methods, and Applications. 2nd ed. Philadelphia: SIAM, 2014.
6. Dantzig, G. B.; Ramser, J. H. The Truck Dispatching Problem. Management Science, v. 6, n. 1, p. 80-91, 1959.
7. Miller, C. E.; Tucker, A. W.; Zemlin, R. A. Integer Programming Formulation of Traveling Salesman Problems. Journal of the ACM, v. 7, n. 4, p. 326-329, 1960.
8. Laporte, G. The Vehicle Routing Problem: An Overview of Exact and Approximate Algorithms. European Journal of Operational Research, v. 59, n. 3, p. 345-358, 1992.
9. Wolsey, L. A. Integer Programming. New York: Wiley-Interscience, 1998.

---

## FERRAMENTAS UTILIZADAS

- Python, Pyomo, Gurobi 13.0.1, HiGHS
- numpy, pandas, matplotlib, folium, geopy
- Trello (gestao), SCRUM (metodologia)
