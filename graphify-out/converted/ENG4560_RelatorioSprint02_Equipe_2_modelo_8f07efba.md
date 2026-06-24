<!-- converted from ENG4560_RelatorioSprint02_Equipe_2_modelo.docx -->




ENG 4560
Projeto Integrado VI – Distribuição Física



# Resumo
Este relatório consolida os resultados das Sprints 1 e 2 do projeto de distribuição física desenvolvido em parceria com a Prolog Transporte e Logística. O problema tratado é o Capacitated Vehicle Routing Problem (CVRP), aplicado à roteirização de entregas do centro de distribuição da empresa em Duque de Caxias para hospitais, clínicas e farmácias no Rio de Janeiro. A Sprint 1 concentrou-se em revisão conceitual sobre VRP e métodos exatos, formulação de um modelo de Programação Linear Inteira Mista (MILP) com restrições de eliminação de subtours no estilo Miller, Tucker e Zemlin (1960), e implementação em Pyomo com Gurobi 13.0.1. Os experimentos em quatro instâncias aninhadas C1 a C4 (10 a 60 clientes) indicaram otimalidade comprovada até 25 clientes em menos de 65 segundos e gap persistente de 3,56% e 4,37% para 40 e 60 clientes após 300 segundos. A Sprint 2 implementou heurísticas construtivas (Nearest Neighbor e Clarke-Wright Savings) adaptadas a frota heterogênea, seguidas de busca local com 2-opt e Relocate. Os resultados mostram que a heurística refinada iguala o ótimo global em C1, supera o método exato em C2 em 5,57% — efeito de uma restrição implícita da formulação MILP empregada — e produz soluções em milissegundos onde o exato esgota o limite de tempo. As evidências sustentam um pipeline operacional concreto para a Prolog (Nearest Neighbor + Clarke-Wright em paralelo, busca local em ambas, seleção da melhor) e motivam a próxima etapa do projeto, baseada em metaheurísticas e refatoração da formulação MILP.
Palavras-chave: CVRP. Frota heterogênea. Programação linear inteira mista. Heurística Nearest Neighbor. Clarke-Wright Savings. Busca local. 2-opt. Relocate.

# Lista de Figuras
(Pressione F9 no Word para atualizar)
# Lista de Tabelas
(Pressione F9 no Word para atualizar)
# Lista de Quadros
(Pressione F9 no Word para atualizar)
# Lista de Siglas e Abreviaturas
ABNT – Associação Brasileira de Normas Técnicas
B&B – Branch and Bound
B&C – Branch and Cut
CD – Centro de Distribuição
CEP – Código de Endereçamento Postal
CVRP – Capacitated Vehicle Routing Problem
EAP – Estrutura Analítica do Projeto
FIO – Fiorino (tipo de veículo)
GA – Genetic Algorithm (Algoritmo Genético)
HiGHS – High performance software for linear optimization
ILS – Iterated Local Search
LB – Lower Bound (limite inferior)
LRP – Location-Routing Problem
MDVRP – Multi-Depot Vehicle Routing Problem
MILP – Mixed-Integer Linear Programming
MIP – Mixed-Integer Programming
MTZ – Miller, Tucker e Zemlin
NP – Non-deterministic Polynomial
OVRP – Open Vehicle Routing Problem
P.O. – Product Owner
PMI – Project Management Institute
PUC-Rio – Pontifícia Universidade Católica do Rio de Janeiro
SA – Simulated Annealing
SEC – Subtour Elimination Constraints
TSP – Traveling Salesman Problem
UB – Upper Bound (limite superior)
VRP – Vehicle Routing Problem
VRPPD – Vehicle Routing Problem with Pickup and Delivery
VRPTW – Vehicle Routing Problem with Time Windows
VUC – Veículo Urbano de Carga

# Sumário
(Pressione F9 no Word para atualizar)
# 1 Introdução
## Contexto e motivação
O transporte rodoviário responde por cerca de 60% do custo logístico total das empresas brasileiras (BALLOU, 2006), e em operações de last mile a composição entre custo variável (distância) e custo fixo (frota) define a margem por entrega. A Prolog Transporte e Logística opera diariamente do centro de distribuição em Duque de Caxias (CEP 25251-560) atendendo hospitais, clínicas e farmácias na Região Metropolitana do Rio de Janeiro.
A base fornecida pela empresa registra 1.021 entregas em 03/06/2025 que, após agregação por CEP, resultam em 581 pontos únicos e 25.324 kg de demanda diária. O planejamento atual depende de avaliação intuitiva do operador e enfrenta condições adversas — congestionamento metropolitano, barreiras geográficas, janelas restritas em hospitais — combinadas com frota heterogênea (Fiorino de 650 kg e VUC de 3.000 kg) e jornada máxima de 8 h. O projeto desenvolve uma alternativa quantitativa em três sprints metodologicamente progressivas: métodos exatos (Sprint 1), heurísticas construtivas e busca local (Sprint 2) e metaheurísticas (Sprint 3).
## Objetivos das Sprints 1 e 2
A Sprint 1 cobriu a etapa exata: revisão conceitual sobre VRP/CVRP, formulação MILP em duas versões (frota homogênea sem MTZ e frota heterogênea com MTZ), implementação em Pyomo com Gurobi e experimentos sobre as instâncias C1 a C4. Os entregáveis mapeiam-se aos itens 1.1, 1.2, 1.3.1, 1.4.1, 1.5.1 e 1.5.2 da EAP (Anexo A).
A Sprint 2 (30/04 a 21/05/2026) estendeu o escopo metodológico com heurísticas construtivas adaptadas a frota heterogênea (Nearest Neighbor e Clarke-Wright Savings) e busca local (2-opt intra-rota e Relocate inter-rota). Os objetivos foram comparar criteriosamente as duas heurísticas, quantificar o ganho marginal da busca local, identificar o ponto de partida que converge para o melhor ótimo local em cada instância e contrastar os resultados com o benchmark exato. Os entregáveis mapeiam-se aos itens 1.3.2, 1.3.3, 1.4.2, 1.5.3 e 1.5.4 da EAP.
# 2 Revisão da Literatura
## 2.1 Distribuição física

A distribuição física é o segmento da logística responsável pelo planejamento, implementação e controle do fluxo físico de produtos acabados do ponto de origem ao ponto de consumo, ao menor custo total compatível com o nível de serviço desejado (BALLOU, 2006). Suas atividades centrais abrangem planejamento de rotas, dimensionamento e alocação de frota, gestão de estoques de distribuição, processamento de pedidos e sequenciamento de entregas (NOVAES, 2007).
O transporte é o componente de maior peso financeiro, correspondendo a cerca de 60% do custo logístico total no Brasil. Em operações urbanas de last mile, caso da Prolog, essa proporção tende a ser ainda mais elevada em função da fragmentação das entregas e da baixa consolidação de cargas. Otimizar a roteirização é, portanto, a alavanca de maior retorno para reduzir o custo da operação.
## 2.2 Classes de problemas em logística

Os problemas de otimização aplicados à logística agrupam-se em três grandes classes: localização de instalações, roteirização e sequenciamento, e alocação e dimensionamento de recursos (DREZNER, 1995; TOTH; VIGO, 2014). Os problemas de localização definem onde instalar centros de distribuição, fábricas ou hubs, buscando minimizar custos fixos e de transporte ou maximizar cobertura. Os problemas de roteirização decidem as rotas e a ordem de atendimento de clientes dispersos geograficamente. Os problemas de alocação tratam do uso dos recursos disponíveis, como capacidade de armazenagem, escala de motoristas e composição de frota.
Essas classes combinam-se em problemas integrados, como o Location-Routing Problem (LRP), que decide simultaneamente a localização dos depósitos e as rotas. Este projeto concentra-se na classe de roteirização, tomando o centro de distribuição da Prolog em Duque de Caxias como fixo.
## 2.3 Otimização combinatória
A otimização combinatória trata da busca pela melhor solução em um conjunto discreto e finito de alternativas (GOLDBARG; GOLDBARG; LUNA, 2015). Formalmente, um problema combinatório é a tupla (S, f), com S finito e f: S → ℝ a objetivo (PAPADIMITRIOU; STEIGLITZ, 1982).
A característica distintiva é o crescimento explosivo de |S| com o tamanho da entrada. No VRP, o número de sequências possíveis para n clientes é da ordem de n!, o que significa aproximadamente 3,6 milhões para n = 10 e valores inviáveis para n superior a 20. Essa explosão inviabiliza enumeração exaustiva e motiva formulações compactas, algoritmos de enumeração implícita como Branch and Bound e heurísticas que exploram estrutura local. Para os 581 clientes da Prolog, o espaço de busca ultrapassa qualquer escala computável, e mesmo C4 (60 clientes) já não admite planejamento intuitivo.
## 2.4 Complexidade computacional e problemas NP-difíceis
A teoria da complexidade computacional classifica problemas de decisão pelo tempo necessário à sua resolução em função do tamanho da entrada (GAREY; JOHNSON, 1979). A classe P reúne problemas resolvíveis em tempo polinomial; NP contém problemas cujas soluções candidatas são verificáveis em tempo polinomial; um problema é NP-difícil quando toda instância de qualquer problema em NP pode ser reduzida a ele em tempo polinomial.
O CVRP é NP-difícil por redução direta do TSP: quando todos os clientes têm demanda unitária e a capacidade Q ≥ n, o CVRP degenera em um TSP (LENSTRA; RINNOOY KAN, 1981). A melhor cota superior conhecida para algoritmos exatos do TSP é O(n² · 2ⁿ), o que confirma a ordem exponencial. A consequência prática é o trade-off entre garantia de otimalidade e tempo de execução: métodos exatos operam até cerca de 25 clientes nas condições testadas, heurísticas escalam até centenas e metaheurísticas avançam sobre milhares de pontos em tempo controlado.
## 2.5 Vehicle Routing Problem (VRP)

O Vehicle Routing Problem consiste em determinar um conjunto de rotas de custo mínimo para uma frota de veículos que atenda um conjunto de clientes geograficamente dispersos, respeitando restrições operacionais (TOTH; VIGO, 2014). O problema foi introduzido por Dantzig e Ramser (1959) sob o nome Truck Dispatching Problem, aplicado ao abastecimento de combustível em postos de gasolina. Desde então, surgiram diversas variantes para tratar restrições típicas de contextos reais, entre elas o CVRP (capacidade), o VRPTW (janelas de tempo), o MDVRP (múltiplos depósitos), o VRPPD (coleta e entrega) e o OVRP (rotas abertas) (LAPORTE, 2009).
A definição da variante adequada depende das restrições do problema prático. Para o caso da Prolog, a principal restrição operacional é a capacidade dos veículos, o que posiciona o CVRP como a variante pertinente. A jornada máxima de oito horas é tratada em pós-processamento e poderá ser incorporada como restrição explícita em sprints futuras.
## 2.6 Capacitated Vehicle Routing Problem (CVRP)

Dado um grafo completo G = (V, A) com V = {0, 1, ..., n}, em que o nó 0 representa o depósito e os nós 1 a n representam clientes, custos c_ij associados a cada arco e demandas q_i para cada cliente, o CVRP busca um conjunto de rotas de custo total mínimo tal que cada cliente seja atendido exatamente uma vez, cada rota inicie e termine no depósito e a soma das demandas atendidas em uma rota não ultrapasse a capacidade Q do veículo (LAPORTE, 1992; TOTH; VIGO, 2014). A instância completa do problema, considerando frota heterogênea e restrições operacionais adicionais, pode ser descrita pela tupla I = (N, D, q, K, Q, g, v, s, H), em que N é o conjunto de clientes, D o depósito, q o vetor de demandas, K o conjunto de tipos de veículo, Q o vetor de capacidades, g o custo variável em R$/km, v a velocidade média, s o tempo de atendimento por cliente e H a jornada máxima.
Aplicações práticas do CVRP incluem operações de distribuição de grandes integradores logísticos como DHL, UPS e FedEx, além de operadores regionais e empresas de last mile especializadas, caso da Prolog.
## 2.7 Formulação MILP do CVRP

A Programação Linear Inteira Mista é uma técnica de otimização em que a função objetivo e as restrições são lineares e um subconjunto das variáveis assume valores inteiros ou binários (WOLSEY, 1998). Na formulação clássica do CVRP, a variável de decisão principal é x_ijk ∈ {0, 1}, indicando se o veículo k percorre o arco (i, j). A função objetivo minimiza o custo total das rotas:
min ∑_k ∑_i ∑_j c_ij · x_ijk
As restrições clássicas são: (i) visita única — cada cliente é atendido por exatamente um veículo; (ii) conservação de fluxo — o grau de entrada iguala o grau de saída em cada nó visitado; (iii) saída do depósito — cada veículo ativado parte do nó 0; e (iv) capacidade — a soma das demandas atendidas por cada veículo não excede Q. A formulação detalhada com frota heterogênea, específica deste projeto, é apresentada na seção 4.
## 2.8 Subtours e eliminação de subtours

Um subtour é um ciclo na solução que não passa pelo depósito, resultando em uma rota desconectada da operação. Na ausência de restrições específicas, o solver encontra subtours como parte da solução ótima da relaxação, já que ciclos fechados entre clientes reduzem o custo total sem violar as restrições clássicas (TOTH; VIGO, 2014). A consequência prática é uma solução matematicamente válida, porém inexequível do ponto de vista operacional.
Duas abordagens são usuais para eliminar subtours. A formulação MTZ, proposta por Miller, Tucker e Zemlin (1960), introduz variáveis auxiliares u_i que representam a carga acumulada ou a ordem de visita em cada nó e impõe:
u_j − u_i ≥ q_j − Q(1 − x_ij),   ∀ i, j ∈ V \ {0}, i ≠ j
q_i ≤ u_i ≤ Q,   ∀ i ∈ V \ {0}
Quando x_ij = 1, a restrição força u_j ≥ u_i + q_j, impedindo ciclos desconectados. A alternativa clássica são as restrições SEC (Subtour Elimination Constraints) de Dantzig, Fulkerson e Johnson (1954), que proíbem explicitamente qualquer subconjunto fechado. As SEC produzem relaxação linear mais forte, mas seu número cresce exponencialmente, exigindo geração dinâmica via lazy constraints. Este trabalho adota a formulação MTZ, alinhada ao material de aula do professor. No contexto da Prolog, a eliminação de subtours é pré-requisito de executável: rotas operacionais precisam partir e retornar ao CD de Duque de Caxias para abastecimento e troca de carga, e ciclos fechados entre clientes simplesmente não se traduzem em itinerários reais de Fiorino ou VUC. O Experimento 1 da seção 6 quantifica o impacto direto dessa decisão de modelagem nas instâncias C1 a C4.
## 2.9 Métodos exatos: Branch and Bound e Branch and Cut

O Branch and Bound é uma técnica de enumeração implícita que percorre uma árvore de subproblemas. Em cada nó, resolve-se a relaxação linear do problema e utiliza-se o valor obtido como limite inferior. Se esse limite for pior do que a melhor solução inteira já encontrada (incumbente), o nó é podado (WOLSEY, 1998). O Branch and Cut estende o B&B com a adição dinâmica de planos de corte, desigualdades válidas para todas as soluções inteiras viáveis porém violadas pela solução fracionária atual, o que aperta a relaxação e acelera a convergência (NEMHAUSER; WOLSEY, 1988).
Três indicadores são centrais na análise de desempenho: o limite inferior LB (valor da relaxação), o limite superior UB (melhor solução inteira encontrada) e o gap de otimalidade, definido como gap = (UB − LB) / UB. Quando o gap atinge zero, a solução incumbente é comprovadamente ótima. Caso o solver atinja o limite de tempo antes disso, a solução obtida é viável, porém sem prova de otimalidade.

## 2.10 Solvers MIP: Gurobi, HiGHS e Pyomo
Um solver MIP combina Branch and Bound, Branch and Cut e técnicas de pré-processamento para resolver modelos de programação linear inteira mista. O Gurobi é o solver comercial de referência, com licença acadêmica gratuita pela PUC-Rio; o HiGHS é o open source mais competitivo (HUANGFU; HALL, 2018). O Pyomo é o framework de modelagem algébrica em Python adotado neste projeto (HART et al., 2017), e permite formular o modelo uma única vez e trocar de solver com uma linha de código — recurso explorado no Experimento 3.
## 2.11 Heurísticas construtivas

Heurísticas construtivas são algoritmos que constroem uma solução viável passo a passo, adicionando elementos segundo um critério guloso, em tempo tipicamente polinomial e sem garantia de otimalidade. Para o VRP, dois métodos clássicos são relevantes. O Nearest Neighbor inicia no depósito e, a cada iteração, insere na rota o cliente viável mais próximo, encerrando a rota quando a capacidade se esgota. O algoritmo de economias, proposto por Clarke e Wright (1964), parte de uma configuração trivial com uma rota dedicada por cliente e funde progressivamente pares de rotas de maior economia de distância, respeitando as restrições de capacidade.
O Nearest Neighbor parte do depósito e, a cada iteração, escolhe o cliente mais próximo entre os que ainda mantêm a rota viável em capacidade e tempo total. Quando nenhum cliente atende a esses critérios, a rota é fechada com retorno ao depósito e uma nova rota é iniciada. A versão para frota heterogênea adicionalmente simula a construção com cada tipo de veículo ao abrir cada rota e seleciona aquele que minimiza o critério adotado. A natureza gulosa do método produz soluções rapidamente, mas tende a deixar clientes geograficamente mal posicionados para as últimas rotas — um fenômeno discutido em detalhe na Seção 8.
O algoritmo de Clarke-Wright Savings (CLARKE; WRIGHT, 1964) opera por fusão controlada de rotas. Parte de uma configuração inicial com uma rota dedicada por cliente, calcula a economia de distância para cada par S_ij = d_0i + d_0j − d_ij, ordena os pares em ordem decrescente e tenta fundir as rotas associadas, sempre que ambos os clientes estiverem em extremidades e a fusão preservar a viabilidade. A adaptação a frota heterogênea re-simula cada fusão candidata com Fiorino e VUC, mantendo a escolha que minimiza o critério adotado. Diferentemente do Nearest Neighbor, o Clarke-Wright avalia a economia global da fusão, tendendo a produzir rotas geograficamente coerentes e a usar VUC apenas quando a capacidade consolidada extrapola o Fiorino.
Essas heurísticas são complementadas, na Sprint 2 deste projeto, por movimentos de busca local. O 2-opt (CROES, 1958; LIN, 1965) opera dentro de uma rota removendo dois arcos não adjacentes e invertendo o segmento entre eles, garantindo redução estrita de distância pela desigualdade triangular sempre que dois arcos se cruzam. O Relocate atua entre rotas, removendo um cliente de uma rota e o reinserindo em outra; pode redistribuir geograficamente, balancear carga ou consolidar rotas (quando uma rota é esvaziada). Ambos são tipicamente aplicados sob critério de melhoria estrita — característica que será discutida na Seção 9 em conexão com a barreira entre regimes de frota observada nos experimentos.
## 2.12 Metaheurísticas

Metaheurísticas são estruturas algorítmicas de alto nível que coordenam heurísticas subordinadas para escapar de ótimos locais. O princípio central é o equilíbrio entre diversificação (exploração de novas regiões do espaço de soluções) e intensificação (refinamento em regiões promissoras) (GENDREAU; POTVIN, 2010). Diferentemente das heurísticas construtivas, que encerram ao produzir a primeira solução viável, metaheurísticas iteram por centenas ou milhares de passos, avaliando grandes quantidades de soluções candidatas ao longo de sua execução.
O Simulated Annealing (SA) inspira-se no processo físico de recozimento de metais. A cada iteração, uma solução vizinha é gerada por uma pequena perturbação na solução corrente. Se for melhor, é aceita; se for pior, é aceita com probabilidade P = exp(−ΔE/T), em que ΔE é a piora e T é a temperatura. A temperatura decresce ao longo da execução, de modo que o algoritmo inicia aceitando muitas soluções piores (exploração ampla) e, gradualmente, passa a aceitar apenas melhorias (intensificação). O SA é historicamente uma das metaheurísticas mais estudadas para o VRP.
O Iterated Local Search (ILS) alterna entre perturbações controladas de uma solução base e a aplicação de uma busca local. Após cada perturbação, a busca local converge para um novo ótimo local, e o melhor entre os ótimos visitados é mantido como solução incumbente. O ILS é eficaz quando o espaço de soluções apresenta muitos ótimos locais de qualidade similar, característica frequente em problemas de roteirização.
Algoritmos Genéticos (GA) mantêm uma população de soluções candidatas que evolui ao longo das iterações. Operadores de seleção escolhem pais da população atual, operadores de crossover combinam pares de pais para gerar filhos, e operadores de mutação introduzem variações aleatórias. A pressão seletiva favorece indivíduos de maior qualidade, e a população converge lentamente para regiões promissoras do espaço. A força dos GAs está na capacidade de manter diversidade ao longo da busca, reduzindo o risco de convergência prematura (GOLDBARG; GOLDBARG; LUNA, 2015).
A Sprint 3 do projeto implementará essas metaheurísticas e realizará a análise comparativa final entre todas as abordagens.
## 2.13 Hierarquia dos métodos de solução
Os três grupos de métodos posicionam-se em uma hierarquia clara quanto ao trade-off entre qualidade e tempo. Métodos exatos garantem otimalidade mas crescem exponencialmente. Heurísticas construtivas produzem soluções viáveis em tempo polinomial, sem garantia. Metaheurísticas partem de soluções heurísticas e aplicam mecanismos de busca sofisticados para aproximar-se do ótimo em tempo controlado. A Sprint 1 estabelece o benchmark exato em instâncias pequenas; as Sprints 2 e 3 desenvolvem métodos escaláveis avaliados contra esse benchmark.
# 3 Descrição do Problema e Dados
## 3.1 Empresa parceira e contexto operacional

A Prolog Transporte e Logística é uma empresa brasileira de transporte rodoviário de cargas e logística last mile, com operações B2B, B2C e B2D. A operação relevante para este projeto parte do centro de distribuição localizado em Duque de Caxias (CEP 25251-560) e direciona-se a hospitais, clínicas e farmácias distribuídos pela Região Metropolitana do Rio de Janeiro. A frota disponível para o recorte considerado é composta por dois tipos de veículos: Fiorino, com capacidade de 650 kg e custo fixo diário de R$ 250, e VUC (Veículo Urbano de Carga), com capacidade de 3.000 kg e custo fixo diário de R$ 550.
## 3.2 Base de dados bruta

A base recebida contém 1.021 registros de entregas realizadas em 03/06/2025. Cada registro carrega o CEP de destino, a quantidade de volumes, o peso real em quilogramas e o valor da mercadoria em reais. O arquivo original encontra-se na raiz do repositório como Base de Dados.xlsx e foi preservado sem modificações diretas; todas as transformações ocorrem nos notebooks de preparação.
## 3.3 Pré-processamento e agregação por CEP
A análise identificou 243 CEPs com múltiplos pedidos no mesmo dia. Como o CEP delimita uma área geográfica reduzida e admite atendimento em uma única parada, os registros foram agregados, reduzindo de 1.021 entregas para 581 clientes únicos (-43%) com 25.324 kg de demanda total. O pipeline está implementado em Aulas/2/Aula2_Preparacao_Dados/notebook.ipynb e segue cinco etapas: limpeza (exclusão de CEPs inválidos e registros com peso ≤ 0), padronização para o formato XXXXX-XXX, agregação por CEP, geocodificação determinística sobre tabela auxiliar de CEPs cariocas e cálculo da matriz Haversine 582×582 persistida em pickle. A amostragem aninhada das instâncias C1 a C4 utiliza seed 42 e bloco da EQUIPE_ID = 2.


## 3.4 Geocodificação e cálculo de distâncias

Cada CEP é convertido em um par (latitude, longitude) por meio de geocodificação determinística baseada no próprio código postal. As distâncias entre pontos são calculadas pela fórmula de Haversine, que mede a menor distância em uma esfera entre dois pontos dados por coordenadas geográficas. A escolha privilegia simplicidade e reprodutibilidade em detrimento da precisão viária: Haversine subestima distâncias reais em malhas urbanas, especialmente em regiões com barreiras geográficas relevantes, como é o caso do Rio de Janeiro. O impacto dessa aproximação é discutido nas limitações apresentadas na seção 7.
A Figura 1 apresenta a distribuição espacial dos 581 clientes únicos e a localização do centro de distribuição da Prolog.

Figura 1 – Dispersão geográfica dos 581 clientes únicos e do centro de distribuição

Fonte: Elaboração própria a partir de dados da Prolog (03/06/2025).

Os clientes concentram-se em duas faixas densas da Região Metropolitana do Rio de Janeiro. A faixa ao sul, com latitude entre -23,05 e -23,20, cobre a maior extensão longitudinal e concentra o maior volume de entregas. Uma segunda faixa, entre -22,70 e -22,80, reúne clientes no eixo norte-nordeste da região. O centro de distribuição, marcado em vermelho, está posicionado no quadrante leste da área coberta, em coordenadas próximas a (-44,07, -23,05).
## 3.5 Geração das instâncias de teste C1 a C4

Para viabilizar o uso de métodos exatos, a base completa foi reduzida a quatro instâncias de teste aninhadas. A construção seguiu as regras do material da Aula 2: seed fixa igual a 42, bloco de 60 clientes correspondente ao EQUIPE_ID igual a 2 (segundo bloco), e amostras incrementais de 10, 25, 40 e 60 clientes. A propriedade de aninhamento C1 ⊂ C2 ⊂ C3 ⊂ C4 garante que resultados em instâncias maiores podem ser comparados diretamente com as menores. O Quadro 1 apresenta as características das instâncias.

Quadro 1 – Características das instâncias de teste C1 a C4


Fonte: Elaboração própria.

As demandas médias por cliente em C2, C3 e C4 são semelhantes (entre 30 e 33 kg), enquanto C1 apresenta média substancialmente menor (14 kg). Essa diferença tem impacto direto na composição da frota ótima: em C1 a demanda total cabe no Fiorino, enquanto em C2, C3 e C4 ela excede a capacidade do menor veículo, forçando o uso do VUC.
A Figura 2 apresenta a dispersão espacial da maior instância de teste, C4_60.

Figura 2 – Dispersão espacial da instância C4_60

Fonte: Elaboração própria.

## 3.6 Parâmetros operacionais

Os parâmetros da tupla I = (N, D, q, K, Q, g, v, s, H) foram fornecidos pelo professor e aplicam-se uniformemente a todas as instâncias de teste. O Quadro 2 apresenta os valores adotados.

Quadro 2 – Parâmetros operacionais do problema
Fonte: Elaboração própria a partir do material da Aula 4.

# 4 Formulação Matemática do Modelo MILP
## 4.1 Conjuntos, parâmetros e variáveis de decisão
O modelo opera sobre os seguintes conjuntos e parâmetros. O conjunto de nós é V = {0, 1, ..., n}, em que 0 representa o depósito e 1 a n representam os clientes. O conjunto de arcos é A = {(i, j) ∈ V × V : i ≠ j}. O conjunto de tipos de veículo é K = {FIO, VUC}. Os parâmetros são c_ij (custo variável do arco), q_i (demanda do cliente i), Q_k (capacidade do veículo tipo k), f_k (custo fixo diário do veículo tipo k) e M (constante suficientemente grande para a formulação MTZ, tomada como Q_k da maior capacidade).
Três grupos de variáveis de decisão compõem o modelo. A variável binária x_ijk vale 1 se o arco (i, j) é percorrido por um veículo do tipo k. A variável contínua u_i representa a carga acumulada ao chegar no nó i e é o mecanismo da formulação MTZ. A variável binária y_k vale 1 se o tipo de veículo k é ativado na solução.
## 4.2 Função objetivo
A função objetivo minimiza o custo total, composto pela soma dos custos variáveis e dos custos fixos dos veículos ativados:
min Z = ∑_(k ∈ K) ∑_((i,j) ∈ A) c_ij · x_ijk + ∑_(k ∈ K) f_k · y_k
O primeiro termo captura o custo proporcional à distância percorrida e traduz diretamente o custo variável g em R$/km. O segundo termo introduz o custo fixo diário de cada tipo de veículo ativado, penalizando soluções que superdimensionam a frota.

## 4.3 Modelo 1: frota homogênea sem eliminação de subtours

A primeira versão do modelo, desenvolvida na Aula 3, considera apenas um tipo de veículo (frota homogênea) e omite as restrições de eliminação de subtours. Seu propósito é pedagógico: explicitar o efeito dos subtours antes de corrigi-lo na versão completa. As restrições são:
(i) Visita única: cada cliente j ∈ V \ {0} recebe exatamente um arco de entrada e um arco de saída.
∑_(i ∈ V, i ≠ j) x_ij = 1,   ∀ j ∈ V \ {0}
∑_(j ∈ V, j ≠ i) x_ij = 1,   ∀ i ∈ V \ {0}
(ii) Conservação de fluxo: em cada nó visitado, a soma dos arcos de entrada iguala a soma dos arcos de saída.
(iii) Balanço no depósito: o número de saídas do depósito iguala o número de retornos e corresponde ao número m de veículos utilizados.
(iv) Capacidade agregada: a demanda total atendida não ultrapassa m vezes a capacidade Q do veículo.
∑_(i ∈ V \ {0}) q_i ≤ Q · m
Na ausência da restrição (v) apresentada adiante, soluções formadas por ciclos desconectados do depósito tornam-se válidas para o solver, como se detalha na análise do experimento 1 na seção 6.
## 4.4 Modelo 2: frota heterogênea com restrições MTZ

O modelo completo, desenvolvido na Aula 4, incorpora dois elementos em relação ao Modelo 1. Primeiro, distingue os tipos de veículo (Fiorino e VUC), o que torna x_ijk dependente de k e acrescenta a variável y_k para ativação. Segundo, inclui as restrições MTZ, que eliminam subtours e forçam todas as rotas a passarem pelo depósito. As restrições adicionais são:
(v) Eliminação de subtours (MTZ):
u_j − u_i ≥ q_j − Q · (1 − x_ij),   ∀ i, j ∈ V \ {0}, i ≠ j
q_i ≤ u_i ≤ Q,   ∀ i ∈ V \ {0}
(vi) Capacidade por tipo de veículo:
∑_((i,j) ∈ A) q_j · x_ijk ≤ Q_k · y_k,   ∀ k ∈ K
(vii) Ativação de veículo: se x_0jk = 1 para algum j, então y_k = 1. Na prática, a relação é imposta por uma restrição big-M que garante consistência entre o uso dos arcos e a ativação do tipo correspondente.
(viii) Conservação de fluxo por tipo de veículo: em cada nó e para cada k, o grau de entrada iguala o grau de saída.
A jornada máxima H de 8 horas não é imposta como restrição linear no MILP, pois exigiria a inclusão de variáveis contínuas adicionais de tempo acumulado e aumentaria substancialmente a complexidade do modelo. Em vez disso, o cumprimento de H é verificado em pós-processamento, somando o tempo de deslocamento (função de v) e o tempo de atendimento (s) de cada rota e comparando com o limite.
## 4.5 Discussão crítica da formulação
A formulação MTZ foi escolhida por compacidade (acrescenta restrições da ordem de n² e n − 1 variáveis contínuas, dispensando técnicas como lazy constraints), alinhamento ao material de aula e interpretação direta de u_i como carga acumulada.
A principal limitação é a relaxação linear mais fraca em comparação às restrições SEC de Dantzig, Fulkerson e Johnson (1954), que aumenta o número de nós explorados pelo Branch and Cut. O efeito prático fica claro no Experimento 1: o número de restrições cresce de 49 (Modelo 1, C1) para 3.789 (Modelo 2, C4), e o tempo de resolução sobe de décimos de segundo para o teto de 300 s. Em instâncias com 60 ou mais clientes, a combinação de relaxação fraca e crescimento quadrático inviabiliza a otimalidade dentro do limite disponível. Para o recorte desta sprint, o MTZ oferece equilíbrio aceitável entre simplicidade e qualidade.
Uma segunda limitação, não detectada nos experimentos da Sprint 1 e revelada empiricamente pela Sprint 2, é a restrição implícita de saída única por tipo de veículo — formalizada na Seção 4.6 a seguir.
## 4.6 Restrição implícita de saída única por tipo de veículo
A variável y_k declarada na seção 4.1 é indexada apenas pelo tipo de veículo (Fiorino ou VUC), não pela unidade individual. A leitura operacional dessa escolha é que o modelo decide, para cada tipo, se ele será ou não usado, mas não quantos veículos daquele tipo serão ativados. Combinado com a restrição (vi) de capacidade por tipo, isso impede configurações como dois Fiorinos em paralelo: o solver é forçado a escolher entre usar exatamente um Fiorino, exatamente um VUC, ou um de cada — nunca duas unidades do mesmo tipo.
A consequência empírica é mais visível na instância C2_25. A heurística Clarke-Wright (Seção 8) encontra uma solução com dois Fiorinos em paralelo a custo R$ 712,06, R$ 41,98 abaixo do ótimo do MILP (R$ 754,04 com um VUC). A predição analítica do ponto de inflexão R$ 540–R$ 545 apresentada na Seção 6.9 dependia justamente dessa configuração proibida ao MILP atual, e a sua materialização pelo Clarke-Wright confirma que o problema possui esse regime ótimo que o exato não consegue acessar.
A correção passa por reindexar y_(k,v) por unidade v de cada tipo k ou substituir y_k por uma variável inteira n_k que contabiliza quantas unidades do tipo k são ativadas. Em qualquer das duas reformulações, as restrições de capacidade por tipo e os termos de custo fixo precisam ser ajustados para somar sobre as unidades. A refatoração está prevista para o início da Sprint 3, onde permitirá comparação simétrica entre o MILP e as heurísticas em C3 e C4.

# 5 Implementação Computacional
## 5.1 Ambiente e dependências
Python como linguagem principal, Pyomo como framework de modelagem (HART et al., 2017), Gurobi 13.0.1 como solver padrão (licença acadêmica PUC-Rio) e HiGHS como comparativo no Experimento 3. Bibliotecas auxiliares: numpy, pandas, matplotlib, folium e geopy.
## 5.2 Organização dos notebooks
Sprint 1: Aulas/2/Aula2_Preparacao_Dados/notebook.ipynb (preparação, agregação e geração de C1–C4), Aulas/3/Aula3_Modelagem_MILP/notebook.ipynb (Modelo 1, diagnóstico de subtours) e Aulas/4/Aula4_Modelagem_MILP_Parte2/notebook.ipynb (Modelo 2 e os quatro experimentos da Seção 6).
Sprint 2: Aulas/7/Aula7_Heuristicas_Construtivas/notebook.ipynb (Nearest Neighbor e Clarke-Wright Savings heterogêneos) e Aulas/8/Aula8_Busca_Local/notebook.ipynb (pipeline 2-opt + Relocate sobre as oito soluções construtivas, salvando refinadas em JSON como entrada para a Sprint 3).
## 5.3 Métricas coletadas
Cada execução do solver registra: custo total (função objetivo), número de veículos por tipo, subtours detectados em pós-processamento, tempo de resolução, gap de otimalidade e status final (optimal, maxTimeLimit, infeasible). A detecção de subtours percorre o grafo dos arcos x_ij = 1 a partir do depósito e identifica componentes desconectadas.
# 6 Resultados Computacionais
## 6.1 Setup experimental

Todas as execuções desta seção utilizaram o mesmo ambiente computacional. O solver padrão foi o Gurobi 13.0.1 com limite de tempo de 300 segundos, exceto nos experimentos que variaram esse parâmetro. O cálculo de distâncias seguiu a fórmula de Haversine, e a seed de geração das instâncias foi fixada em 42 para reprodutibilidade. Os experimentos obrigatórios definidos na Aula 5 foram executados integralmente; além desses, o grupo implementou três experimentos opcionais, cobrindo sensibilidade temporal, comparação de solvers e sensibilidade de parâmetros de frota.
## 6.2 Modelo 1: frota homogênea sem MTZ

A Tabela 1 apresenta os resultados do Modelo 1 nas quatro instâncias. Em todas, o solver declara status "optimal" e encontra a solução em menos de um segundo. Porém, o número de subtours detectados no pós-processamento cresce monotonicamente com o tamanho da instância.

Tabela 1 – Resultados do Modelo 1 (frota homogênea, sem MTZ)



Fonte: Elaboração própria.

A Figura 3 mostra o diagnóstico visual dos subtours gerados pelo Modelo 1 na instância C1_10.


Figura 3 – Diagnóstico de subtours na instância C1_10 sem MTZ

Fonte: Elaboração própria.

O painel esquerdo apresenta os nós do problema sem qualquer ligação. O painel central reconstrói as rotas produzidas pelo solver: uma rota curta sai do depósito e conecta dois ou três clientes próximos, enquanto os demais formam ciclos fechados sem passar pelo depósito. O painel direito destaca em vermelho os quatro subtours detectados. Do ponto de vista do solver, a solução é "ótima" porque respeita todas as restrições declaradas e minimiza a soma dos custos dos arcos selecionados. Do ponto de vista operacional, é inexequível: nenhum veículo real conseguiria executar ciclos desconectados do depósito sem voltar para se abastecer.
Esse resultado é a evidência empírica mais direta da necessidade das restrições MTZ, motivando a evolução para o Modelo 2.
## 6.3 Modelo 2: frota heterogênea com MTZ

Os resultados do Modelo 2 estão consolidados na Tabela 2. O solver comprova otimalidade em C1 e C2 e atinge o limite de tempo em C3 e C4, encerrando com gap de otimalidade aberto.

Tabela 2 – Resultados do Modelo 2 (frota heterogênea, com MTZ)




Fonte: Elaboração própria.

A seleção da frota segue o perfil de demanda esperado. Em C1, com demanda total de 141,6 kg, o Fiorino é escolhido por ter custo fixo menor (R$ 250 contra R$ 550 do VUC). Nas demais instâncias, a demanda ultrapassa a capacidade do Fiorino, o que força o uso do VUC.
A Figura 4 mostra a rota ótima obtida para C1_10 no Modelo 2.

Figura 4 – Rota ótima da instância C1_10 com MTZ e frota heterogênea

Fonte: Elaboração própria.

A rota é única, conectada e operacionalmente viável: sai do depósito, atende os dez clientes em sequência e retorna ao ponto de partida. O custo de R$ 422,38 reflete o custo fixo do Fiorino (R$ 250) somado ao custo variável da distância total percorrida, aproximadamente 115 km. A comparação direta com a Figura 3, que mostra a mesma instância sem MTZ, evidencia o contraste entre o que o solver entrega com e sem restrições de conectividade.
## 6.4 Experimento 1: impacto da eliminação de subtours

O primeiro experimento mede o impacto quantitativo das restrições MTZ, comparando, para as quatro instâncias, os custos, o número de restrições e o tempo de resolução dos dois modelos. A Tabela 3 reúne os valores.

Tabela 3 – Comparação entre os modelos COM e SEM restrições MTZ



Fonte: Elaboração própria.

Três leituras emergem dos dados. Primeiro, o número de restrições cresce aproximadamente com o quadrado de n, passando de 49 restrições em C1 sem MTZ para 3.789 em C4 com MTZ, confirmando a ordem O(n²) inerente à formulação. Segundo, o tempo de resolução explode: em C4, salta de décimos de segundo (sem MTZ) para o teto de 300 segundos (com MTZ). Terceiro, e mais importante, o custo inferior do modelo sem MTZ é ilusório, porque as rotas produzidas incluem subtours e não podem ser executadas na operação real.
A Figura 5 consolida visualmente o contraste entre as duas formulações na instância C2_25.

Figura 5 – Comparação lado a lado COM e SEM MTZ na instância C2_25

Fonte: Elaboração própria.

O painel esquerdo, COM MTZ, exibe uma rota única que percorre todos os 25 clientes e retorna ao depósito. O painel direito, SEM MTZ, mostra o depósito praticamente isolado: a maioria dos pontos figura em losangos alaranjados, representando os onze ciclos desconectados. O custo declarado para a solução sem MTZ (R$ 666,15) é R$ 88 inferior à solução correta, mas essa diferença não tem correspondente operacional: nenhum caminhão da frota Prolog executaria a rota fragmentada entregue pelo solver.
## 6.5 Experimento 2: sensibilidade ao limite de tempo

O segundo experimento explora como o gap de otimalidade e o custo da solução incumbente evoluem à medida que o limite de tempo cresce. Foram testados três tetos: 30 s, 60 s e 300 s. A Tabela 4 apresenta os resultados.

Tabela 4 – Sensibilidade ao limite de tempo (Modelo 2)



Fonte: Elaboração própria.

C1 e C2 convergem para a solução ótima nos limites de tempo testados. O caso de C2 é instrutivo: a solução incumbente não muda entre 30 s e 300 s, mas o gap cai de 0,45% para 0%, revelando a diferença entre encontrar uma boa solução e provar que ela é ótima. Em C3 e C4, tanto o custo quanto o gap melhoram com mais tempo, porém com retornos decrescentes e sem atingir otimalidade. Mesmo após 300 s, C3 mantém gap de 3,56% e C4 de 4,37%, indicando que a convergência para o ótimo seria lenta e, provavelmente, inviável em escalas de tempo aceitáveis para a operação real.
A Figura 6 ilustra graficamente o comportamento do custo incumbente e do gap em função do limite de tempo.

Figura 6 – Custo incumbente e gap de otimalidade em função do limite de tempo

Fonte: Elaboração própria.

As curvas de C3 e C4 no gráfico de gap cruzam-se entre 60 s e 300 s, com C4 apresentando gap maior que C3 ao final. Esse cruzamento reforça que o tempo computacional não cresce linearmente com a dificuldade da instância, comportamento característico de problemas NP-difíceis.
## 6.6 Experimento 3: comparação de solvers

O terceiro experimento compara o desempenho de Gurobi e HiGHS nas duas menores instâncias. Instâncias maiores não foram testadas porque o tempo esperado do HiGHS seria proibitivo. A Tabela 5 apresenta os resultados.

Tabela 5 – Comparação entre Gurobi e HiGHS (Modelo 2)




Fonte: Elaboração própria.

Em C1_10, ambos os solvers chegam à mesma solução, mas o Gurobi é cerca de onze vezes mais rápido. Em C2_25, a diferença se aprofunda: o Gurobi comprova otimalidade em 77 s, enquanto o HiGHS atinge o teto de 300 s com gap de 6,07% e solução R$ 6,14 mais cara. Em problemas NP-difíceis, essas diferenças tendem a se ampliar com o tamanho da instância, reforçando o Gurobi como opção padrão para o benchmark exato do projeto.
## 6.7 Experimento 4: sensibilidade dos parâmetros de frota

O quarto experimento avalia a sensibilidade da solução a variações nos parâmetros do VUC, aplicadas sobre a instância C1_10. A Tabela 6 apresenta os casos testados.

Tabela 6 – Sensibilidade da solução aos parâmetros do VUC (C1_10)



Fonte: Elaboração própria.

O resultado é degenerado para esta instância: nenhuma variação altera a solução ótima. A razão é estrutural — a demanda total de 141,6 kg já cabe no Fiorino, cujo custo fixo é menor que o do VUC mesmo na configuração base. Tornar o VUC mais caro ou menos capacitado não tem efeito porque o VUC já não é selecionado. Análises desse tipo tornam-se informativas em C2 a C4, onde o VUC é efetivamente usado; esse desdobramento está previsto para sprints posteriores, junto às heurísticas, que permitirão cenários com frota composta.
## 6.8 Síntese dos resultados

Quatro conclusões consolidam a evidência dos experimentos. A restrição MTZ é indispensável: sem ela, o solver produz soluções de custo aparente menor, porém com subtours que inviabilizam a execução. O Gurobi apresenta desempenho superior ao HiGHS em ordens de magnitude nas instâncias testadas, justificando sua adoção como solver padrão. O tempo de resolução cresce rapidamente com o número de clientes e o gap não fecha em 300 s para instâncias de 40 e 60 clientes. A seleção da frota ótima é determinada principalmente pela demanda total, que fixa o tipo mínimo de veículo necessário.
## 6.9 Ponto de inflexão do custo fixo do VUC
Em C2_25 o exato seleciona um VUC (R$ 754,04) porque a demanda total (754,5 kg) ultrapassa a capacidade do Fiorino. A alternativa estrutural é a configuração com dois Fiorinos em paralelo: custo fixo combinado de R$ 500 mais custo variável. O ponto de inflexão analítico, calculado pela igualdade f_VUC* = R$ 500 + (C_var^2FIO − C_var^VUC), situa-se entre R$ 540 e R$ 545 — próximo do valor de catálogo da Prolog (R$ 550).
A predição foi confirmada empiricamente pela Sprint 2. O Clarke-Wright, sem conhecimento da formulação MILP, encontrou em C2 a configuração com dois Fiorinos (custo total R$ 712,06), R$ 41,98 abaixo do ótimo do MILP. A discrepância tem causa estrutural e não numérica: o modelo da Aula 4 não admite múltiplas unidades do mesmo tipo (Seção 4.6). Esse resultado é discutido em detalhe nas Seções 7.6, 7.8 e 9.2.
## 6.10 Sensibilidade à velocidade média
A velocidade média v não integra a função objetivo e afeta apenas a validação da jornada H em pós-processamento. Reduzir v (trânsito pesado) eleva o tempo total da rota e pode tornar rotas inicialmente viáveis em inexequíveis — em C2_25 com v = 25 km/h, a jornada total já ultrapassa as 8 h, demandando particionamento ou regime de hora extra. A incorporação de H como restrição linear é recomendação para sprints futuras.
## 6.11 Sensibilidade ao tempo de serviço
O tempo de atendimento s também não aparece na função objetivo e afeta apenas a validação de H. Aumentar s de 15 para 25 minutos em C2_25 adiciona 4,2 h ao tempo total, agravando o quadro discutido em 6.10. O tratamento quantitativo desse cenário será conduzido nas sprints seguintes, com maior flexibilidade nas heurísticas para explorar configurações com múltiplas rotas.
# 7 Heurísticas Construtivas
## 7.1 Objetivo do estágio construtivo
A Seção 7 estabeleceu que o método exato resolve com otimalidade comprovada até 25 clientes e não converge no limite de tempo a partir de 40. A Sprint 2 aborda essa lacuna por meio de heurísticas construtivas seguidas de busca local. O estágio construtivo, objeto desta seção, produz uma solução viável em tempo polinomial sobre as quatro instâncias C1 a C4 e fornece o ponto de partida para as heurísticas de melhoria descritas na Seção 9.
Foram implementadas duas heurísticas clássicas adaptadas a frota heterogênea, conforme apresentado pelo professor no slide 25 da Aula 7B: Nearest Neighbor (NN) e Clarke-Wright Savings (CW). Cada heurística foi executada sobre as quatro instâncias e os dois critérios de seleção do veículo previstos no material da disciplina (total_cost e cost_per_client), totalizando dezesseis execuções. Os parâmetros operacionais permaneceram idênticos aos da Sprint 1 (Quadro 2), o que garante que diferenças observadas refletem exclusivamente o método de solução.
## 7.2 Algoritmo Nearest Neighbor com frota heterogênea
A heurística Nearest Neighbor constrói rotas de forma incremental a partir do depósito. A cada passo, escolhe o cliente viável mais próximo do nó atual e o agrega à rota corrente. Considera-se viável o cliente cuja inserção mantenha simultaneamente a carga acumulada abaixo da capacidade do veículo e o tempo total da rota — incluindo o retorno ao depósito — abaixo da jornada de 8 h. Quando nenhum cliente remanescente atende a esses critérios, a rota é fechada e uma nova rota é aberta com os clientes ainda não atendidos.
A extensão para frota heterogênea segue o slide 24 da Aula 7B: ao abrir cada nova rota, o algoritmo simula a construção com Fiorino e com VUC e seleciona o veículo que minimiza o critério adotado. Essa decisão é local a cada rota e não revisita escolhas anteriores. A natureza gulosa do método é responsável tanto por sua velocidade quanto por sua principal limitação: o esgotamento dos clientes próximos ao depósito tende a deixar rotas-resíduo geograficamente mal posicionadas.
## 7.3 Algoritmo Clarke-Wright Savings com frota heterogênea
A heurística Clarke-Wright Savings (CLARKE; WRIGHT, 1964) parte do extremo oposto do Nearest Neighbor: cada cliente inicia atendido por uma rota dedicada [0, i, 0]. O algoritmo calcula, para todos os pares de clientes, a economia S_ij = d_0i + d_0j - d_ij, ordena os pares em ordem decrescente e funde as rotas dos clientes envolvidos sempre que ambos estão em extremidades de suas respectivas rotas e a fusão preserva a viabilidade. Cada fusão candidata é re-simulada com Fiorino e VUC, e o veículo escolhido é aquele que minimiza o critério adotado.
Diferentemente do Nearest Neighbor, o CW é guiado pela economia global proveniente da eliminação de retornos ao depósito, não pela proximidade local. A consequência operacional é uma maior consolidação das rotas geograficamente coerentes e o uso pontual do VUC apenas quando a capacidade acumulada na fusão extrapola o limite do Fiorino.
## 7.4 Critérios de seleção do veículo
O slide 25 da Aula 7B prevê dois critérios para a escolha do veículo: total_cost (minimiza custo total da rota candidata) e cost_per_client (minimiza custo por cliente). A execução das 16 combinações instância × heurística × critério revelou equivalência completa entre os critérios para o conjunto de dados da Equipe 2 — custos, número de rotas e composição da frota idênticos em todas as execuções. O Quadro 3 sintetiza o achado e a justificativa estrutural.
Quadro 3 – Equivalência observada entre critérios total_cost e cost_per_client

Fonte: Elaboração própria.
## 7.5 Resultados nas instâncias C1 a C4
As Tabelas 7 e 8 apresentam os resultados de cada heurística sobre as quatro instâncias, executadas com critério total_cost. A coluna n_fusões da Tabela 8 registra o número de fusões aceitas pelo Clarke-Wright; o NN não tem equivalente porque cresce rotas sequencialmente. Todos os tempos de execução permaneceram abaixo de 20 ms, e nenhuma solução violou capacidade ou jornada.

Tabela 7 – Resultados do Nearest Neighbor heterogêneo em C1–C4

Fonte: Elaboração própria.

Tabela 8 – Resultados do Clarke-Wright Savings heterogêneo em C1–C4

Fonte: Elaboração própria.
O Nearest Neighbor utiliza exclusivamente Fiorinos em todas as instâncias e escala o número de rotas linearmente com o tamanho da instância (uma rota em C1, duas em C2, três em C3 e quatro em C4). O Clarke-Wright reduz o número de rotas em C3 (de três para duas) e em C4 (de quatro para três) ao mobilizar um VUC para absorver a carga consolidada, o que sinaliza que o custo fixo adicional de R$ 300 por VUC é compensado pela economia em rotas evitadas e em distância percorrida.
## 7.6 Comparação Nearest Neighbor × Clarke-Wright
A Tabela 9 consolida a comparação direta entre as duas heurísticas. O Clarke-Wright supera o Nearest Neighbor em todas as quatro instâncias, com reduções de custo entre 1,62% (C1) e 11,11% (C2).

Tabela 9 – Comparação Nearest Neighbor × Clarke-Wright (critério total_cost)

Fonte: Elaboração própria.
O ganho mais expressivo aparece em C2 (-11,11%), instância em que ambas as heurísticas usam exclusivamente Fiorino e a vantagem do CW vem de uma distribuição geográfica mais eficiente dos 25 clientes em duas rotas. As Figuras 9, 10 e 11 mostram essas diferenças espacialmente para C2, C3 e C4. A instância C1 é omitida visualmente porque os dois algoritmos convergem para uma rota única quase idêntica.

Figura 7 – Comparação das rotas Nearest Neighbor × Clarke-Wright na instância C2_25


Fonte: Elaboração própria.
Em C2 (Figura 7) a vantagem do Clarke-Wright é visualmente clara: as duas rotas Fiorino delimitam regiões compactas, enquanto o Nearest Neighbor deixa cruzamentos que aumentam a distância em 60 km. Em C3 (Figura 8) o CW separa a malha em duas regiões coerentes — Fiorino atende a região norte e VUC consolida a região sul mais densa —, ao passo que o NN gera três rotas Fiorino com sobreposição central. Em C4 (Figura 7) o padrão se repete: o CW divide a malha em três zonas com VUC para a porção mais consolidada, enquanto o NN mantém quatro rotas Fiorino, incluindo uma rota-resíduo de 135,67 km para apenas dois clientes geograficamente distantes.

Figura 8 – Comparação das rotas Nearest Neighbor × Clarke-Wright na instância C3_40


Fonte: Elaboração própria.

Figura 7 – Comparação das rotas Nearest Neighbor × Clarke-Wright na instância C4_60


Fonte: Elaboração própria.
## 7.7 Diagnóstico da restrição de jornada
A jornada máxima de 8 h emerge como restrição ativa nas duas heurísticas. A Tabela 10 distribui as rotas geradas por faixa de tempo total e identifica as rotas que operam acima de 7 h, ou seja, com folga inferior a 1 h.

Tabela 10 – Distribuição das rotas por faixa de tempo (limite H = 8 h)

Fonte: Elaboração própria.
Sete das dezoito rotas geradas pelos dois algoritmos operam acima de 7 h, com folgas mínimas de 8 minutos em C4. O Nearest Neighbor preenche rotas de forma mais agressiva — quatro rotas próximas do limite — porque seu critério guloso continua inserindo clientes enquanto houver folga suficiente para o retorno. O Clarke-Wright, por operar via fusão controlada pelo saving, rejeita fusões que aproximariam o tempo da rota do teto operacional, mesmo quando o saving envolvido seria atrativo. Essa diferença explica diretamente as rotas-resíduo observadas em C3 e C4 no Nearest Neighbor: à medida que a primeira rota se preenche até o limite, os clientes remanescentes herdam rotas que precisam percorrer longas travessias para alcançar pontos geograficamente inconvenientes.
## 7.8 Comparação com o método exato — assimetria estrutural
A Tabela 11 compara as heurísticas construtivas com a solução do MILP da Sprint 1 (Aula 4). A Figura 8 apresenta o mesmo conteúdo em gráfico de barras com rótulos de gap percentual.

Tabela 11 – Heurísticas construtivas × método exato (MILP Aula 4)

Fonte: Elaboração própria.

Figura 8 – Comparação de custos entre o método exato e as heurísticas construtivas


Fonte: Elaboração própria.
A leitura precisa ser feita com cuidado. Em C1 as três soluções praticamente coincidem (gap CW de 0,30%). Em C2 o Clarke-Wright supera o exato em 5,57%, distribuindo os 25 clientes em duas rotas Fiorino (custo combinado R$ 712,06), enquanto o MILP da Aula 4 fica preso a uma única rota VUC (R$ 754,04). Esse resultado é a confirmação empírica direta da limitação predita na Seção 6.9 e formalizada na nova Seção 4.6: a formulação atual proíbe configurações com mais de uma rota por tipo de veículo, configuração justamente preferida pelo CW em C2.
Em C3 e C4 os gaps aparentes (+36% e +64%) refletem a mesma assimetria estrutural em sentido oposto: o exato consolida toda a demanda em uma única rota VUC, regime fora do espaço de busca das heurísticas com a granularidade atual de frota. Esses gaps não indicam falha do método heurístico; indicam que as duas formulações operam em regimes diferentes de frota. A comparação simétrica entre os dois métodos depende da refatoração da formulação MILP discutida na Seção 4.6, prevista para a Sprint 3.
# 8 Busca Local: Heurísticas de Melhoria
## 8.1 Posicionamento no pipeline da Sprint 2
O slide 25 da Aula 8 estrutura a Sprint 2 em dois estágios: um construtivo (Seção 8) e um de melhoria, objeto desta seção. A busca local recebe as oito soluções construtivas (quatro do NN e quatro do CW, no critério total_cost) e aplica, em sequência, dois movimentos clássicos: 2-opt intra-rota e Relocate inter-rota. O pipeline mantém o critério de aceitação por melhoria estrita — um movimento só é aceito se reduzir o custo (ou a distância, no caso do 2-opt) mantendo viabilidade de capacidade e jornada. Não há aceitação de pioras temporárias; esse mecanismo é específico das metaheurísticas da Sprint 3.
## 8.2 Movimento 2-opt intra-rota
O 2-opt, descrito originalmente por Croes (1958) e formalizado por Lin (1965), opera dentro de uma única rota. Dada uma rota [0, ..., 0], o movimento remove dois arcos não adjacentes e reconecta os segmentos invertendo o trecho intermediário. O slide 14 da Aula 8 demonstra que, quando dois arcos se cruzam, a desigualdade triangular garante que a reconexão sem cruzamentos é estritamente mais curta. O 2-opt portanto nunca aumenta a distância de uma rota: o pior caso é não encontrar movimento melhorante.
A implementação seguiu o gabarito do professor: para cada par de índices (i, k) na rota, gera-se a candidata route[:i] + route[i:k+1][::-1] + route[k+1:] e aceita-se o primeiro candidato viável que reduza a distância. Como o veículo da rota é mantido fixo, o custo fixo é preservado e a redução de custo provém exclusivamente da redução de distância (a R$ 1,50/km). A complexidade é O(n²) por rota.
## 8.3 Movimento Relocate inter-rota
O Relocate altera não a ordem mas a alocação dos clientes às rotas: remove um cliente de uma rota de origem e o reinsere em uma posição de outra rota. O slide 15 da Aula 8 enumera três efeitos potenciais — redistribuição geográfica de clientes mal alocados, balanceamento de carga e consolidação de rotas (quando o esvaziamento de uma rota a elimina). A função objetivo da aceitação é o custo total da solução, somando custos variáveis e fixos. Como o movimento envolve duas rotas, a viabilidade é validada simultaneamente em ambas (capacidade e jornada).
A estratégia adotada é first improvement, conforme o slide 21 da Aula 8: o algoritmo varre pares ordenados (rota_origem, rota_destino) com origem diferente do destino, posições internas idx_from e idx_to, e aceita o primeiro movimento que reduza estritamente o custo total. Após cada aceitação, a busca reinicia até que nenhum movimento melhore — caracterizando convergência ao ótimo local da vizinhança Relocate. A complexidade é O(k² × n²) por iteração, onde k é o número de rotas e n o número de clientes.
## 8.4 Critério de aceitação e first improvement
A aceitação por melhoria estrita implica que o ponto de chegada da busca local depende integralmente do ponto de partida: movimentos que exigem aceitar piora temporária — como abrir uma rota VUC com custo fixo de R$ 550 antes que a consolidação reduza distância — ficam por construção fora do alcance do método. Esse fenômeno é tratado em detalhe na Seção 7.8.
## 8.5 Resultados do 2-opt
A Tabela 12 apresenta, para cada uma das oito soluções construtivas, o ganho obtido pelo 2-opt em distância e em custo. O custo cai menos que a distância porque o custo fixo dos veículos (R$ 250 por FIO, R$ 550 por VUC) é preservado.

Tabela 12 – Resultados do 2-opt sobre as oito soluções construtivas

Fonte: Elaboração própria.
A assimetria entre os dois pontos de partida é nítida e confirma o argumento do slide 24 da Aula 8. Sobre o Nearest Neighbor o 2-opt remove cruzamentos remanescentes com ganhos de distância entre 4,08% e 13,36%; sobre o Clarke-Wright o ganho fica entre 0,01% e 0,72%, indicando que as fusões por economia da Seção 7.3 já entregaram rotas localmente ótimas no sentido 2-opt. Em todas as oito execuções o tempo permaneceu abaixo de 30 ms e nenhuma viabilidade foi violada.
## 8.6 Resultados do Relocate
A Tabela 13 aplica o Relocate sobre as soluções já refinadas pelo 2-opt. O efeito é seletivo: ganhos relevantes aparecem apenas sobre as soluções oriundas do Nearest Neighbor.

Tabela 13 – Resultados do Relocate sobre as soluções pós-2-opt

Fonte: Elaboração própria.
Os destaques são as reduções em NN-C2 (-6,36% sobre o 2-opt; R$ 760,86 → R$ 712,49) e NN-C4 (-4,95%; R$ 1.506,04 → R$ 1.431,50). Sobre as quatro soluções Clarke-Wright o Relocate não encontra movimento melhorante: as rotas já constituem ótimo local da vizinhança definida. Em nenhum dos oito casos o Relocate reduziu o número de rotas — o efeito de consolidação descrito no slide 17 da Aula 8 não se materializou porque a capacidade ociosa nas rotas Fiorino é insuficiente para absorver uma rota inteira sem violar a jornada de 8 h. O tempo computacional do Relocate é dominado por NN-C4 (1,22 s), única chamada do pipeline em escala de segundos; em CW-C4 cai para 86 ms porque o algoritmo termina sem encontrar melhoria.
## 8.7 Pipeline completo: visão consolidada
A Tabela 14 consolida as três etapas (inicial → 2-opt → Relocate) e expressa os ganhos percentuais sobre a solução inicial, permitindo leitura direta do efeito acumulado do pipeline.

Tabela 14 – Pipeline completo: ganhos acumulados sobre a solução inicial

Fonte: Elaboração própria.
A leitura consolidada confirma o padrão observado nas seções anteriores. O ganho marginal do Relocate é significativo apenas sobre o Nearest Neighbor: em NN-C2 o pipeline reduz custo em 11,06% (R$ 89 absolutos), em NN-C4 reduz em 6,29% (R$ 96 absolutos). Sobre o Clarke-Wright o ganho total não excede 0,29%, o que indica que as fusões por economia já entregam, na prática, rotas em ótimo local da vizinhança 2-opt + Relocate sob melhoria estrita.
## 8.8 Vencedor por instância: NN+BL × CW+BL
A Tabela 15 compara o custo final obtido a partir de cada uma das duas soluções iniciais. A pergunta central do slide 23 da Aula 8 é qual ponto de partida leva, após a busca local, ao melhor ótimo local em cada instância.

Tabela 15 – Vencedor por instância: NN+BL × CW+BL

Fonte: Elaboração própria.
O Clarke-Wright + busca local vence em três das quatro instâncias e empata em C1, no ótimo global de R$ 422,38. A vantagem do CW cresce com o tamanho da instância (0,06% em C2, 1,35% em C3, 1,49% em C4). O resultado materializa empiricamente o argumento dos slides 22 a 24 da Aula 8: como a busca local sob melhoria estrita nunca aceita pioras, o ponto de chegada é função do ponto de partida. Em C3 e C4 o NN+BL permanece preso a uma configuração "só FIO" com três e quatro rotas respectivamente; o CW+BL preserva a configuração mista FIO+VUC já encontrada na fase construtiva. A diferença final equivale ao custo de uma rota Fiorino adicional que o Relocate é incapaz de eliminar — a transição exigiria abrir uma rota VUC (piora momentânea de R$ 550 em custo fixo) antes que a consolidação compensasse.
As Figuras 13 e 14 ilustram visualmente esse aprisionamento em C3 e C4: a coluna esquerda mostra a solução inicial Clarke-Wright (sem busca local); a coluna direita mostra a solução NN + 2-opt + Relocate. Em C3, o CW divide a malha em duas regiões coerentes (Fiorino ao norte, VUC consolidando o sul), enquanto o NN+BL mantém três rotas Fiorino com bordas entremeadas. Em C4, o CW separa em três zonas com VUC para a área mais densa, ao passo que o NN+BL permanece em quatro rotas Fiorino. A busca local reduziu cruzamentos internos em ambos os casos, mas a fronteira entre regimes de frota não é atravessada.

Figura 7 – Clarke-Wright inicial × Nearest Neighbor após busca local na instância C3_40


Fonte: Elaboração própria.

Figura 8 – Clarke-Wright inicial × Nearest Neighbor após busca local na instância C4_60


Fonte: Elaboração própria.
## 8.9 Comparação com o método exato após busca local
A Tabela 16 atualiza a comparação com o método exato considerando agora a melhor solução heurística refinada por instância. A Figura 7 traz o gráfico de barras correspondente.

Tabela 16 – Comparação após busca local × método exato

Fonte: Elaboração própria.

Figura 7 – Comparação de custos entre o método exato e as heurísticas refinadas por busca local


Fonte: Elaboração própria.
Em C1 a heurística refinada iguala o ótimo global comprovado pelo MILP. Em C2 supera o exato em 5,57%, pelos mesmos motivos estruturais discutidos na Seção 7.8: o MILP da Aula 4 não admite configurações com mais de uma rota Fiorino, e justamente essa configuração é a que o Clarke-Wright encontra. Em C3 e C4 o gap aparente positivo continua refletindo o regime "tudo em um único VUC" inacessível à heurística — e o gap pouco mudou em relação à fase construtiva, evidência adicional de que a busca local sob melhoria estrita captura ganhos apenas onde a vizinhança é suficiente, ficando neutra onde o ótimo local depende de uma transição de regime.
## 8.10 Custo computacional do pipeline
O 2-opt é O(n²) por rota e completa em sub-30 ms em todas as oito execuções. O Relocate, com complexidade O(k² × n²), domina o tempo total quando há desbalanceamento entre rotas — caso do NN-C4, único cenário do projeto que ultrapassa um segundo (1,22 s). Sobre as soluções Clarke-Wright o Relocate termina rapidamente por não encontrar melhoria. Mesmo no pior caso, o pipeline completo (NN + 2-opt + Relocate em C4) executa em 1,53 s, cinco ordens de grandeza abaixo dos 300 s de tempo-limite do exato.
# 9 Análise Comparativa Consolidada
## 9.1 Tabela-payoff consolidada
A Tabela 17 reúne, em um único painel, todos os resultados produzidos pelas Sprints 1 e 2. As colunas seguem a ordem metodológica: solução do MILP da Aula 4, construtiva Nearest Neighbor, construtiva Clarke-Wright, e as duas soluções refinadas por busca local. A última coluna identifica o método recomendado em cada instância.

Tabela 17 – Custos finais por instância e método (Sprints 1 e 2)

Fonte: Elaboração própria. * Solução do MILP com status maxTimeLimit (gap aberto após 300 s) e sujeita à restrição implícita de saída única por tipo de veículo (ver Seções 4.6 e 10.2).
Três leituras emergem da Tabela 17. Em C1 todos os métodos comprovados convergem para o mesmo valor, R$ 422,38, validando-se mutuamente. Em C2 a heurística refinada supera o ótimo da formulação MILP em 5,57%. Em C3 e C4 a aparência inverte-se — o exato apresenta custos menores —, mas, como discutido nas próximas duas subseções, o regime de operação acessado por cada método é estruturalmente diferente.
## 9.2 Quando a heurística supera o exato — C2 e a restrição implícita
O caso de C2 é a confirmação mais direta da limitação predita analiticamente na Seção 6.9 e formalizada na Seção 4.6. A demanda total de C2 (754,5 kg) excede a capacidade do Fiorino (650 kg) mas é confortavelmente acomodada por dois Fiorinos em paralelo (combinados, 1.300 kg de capacidade). A solução ótima sob essa configuração tem custo fixo combinado de 2 × R$ 250 = R$ 500 e custo variável que, no Clarke-Wright, totaliza R$ 712,06. A solução do MILP da Aula 4, restringida a no máximo uma rota por tipo de veículo, paga R$ 550 de custo fixo do VUC mais o custo variável da rota única, fechando em R$ 754,04 — R$ 41,98 acima da heurística.
O resultado não indica desempenho superior das heurísticas frente a métodos exatos: indica que a formulação MILP da Aula 4 não captura o regime ótimo de C2. A refatoração proposta na Seção 4.6 (reindexar y_(k,v) por unidade de cada tipo, ou substituir y_k por uma variável inteira n_k) corrige a assimetria. Após essa correção, espera-se que o MILP atinja em C2 o mesmo valor encontrado empiricamente pelo Clarke-Wright. A previsão é teste previsto para o início da Sprint 3.
## 9.3 Quando o exato vence — C3, C4 e o regime de frota inacessível
Em C3 e C4 a aparência se inverte: o MILP da Aula 4 entrega custos significativamente menores (R$ 769,65 e R$ 858,31) do que as heurísticas refinadas (R$ 1.047,99 e R$ 1.410,21). A leitura ingênua seria que o método exato vence em escala, mas a análise dos regimes de frota revela uma situação distinta.
O MILP em C3 e C4 consolida toda a demanda em uma única rota VUC, com custo fixo de R$ 550 e o restante em custo variável. As heurísticas, com sua granularidade fina de frota, encontram configurações com dois ou três veículos (CW-C3 usa um FIO e um VUC; CW-C4 usa dois FIO e um VUC). O consolidado "tudo em um VUC" é mais barato porque paga apenas um custo fixo, mas exige uma rota de mais de 1.295 kg e quase 8 h em C3 e de 1.958 kg em C4. As heurísticas não acessam esse regime porque cada decisão de fusão é avaliada localmente: ao crescer uma rota, o algoritmo verifica capacidade e jornada e fecha a rota quando algum dos limites é atingido. Sem mecanismo de busca global que aceite reagrupamentos custosos, o consolidado em rota única não é alcançável.
Os gaps de +36,16% (C3) e +64,30% (C4) refletem essa diferença de regime, não desvantagem genuína das heurísticas. Em uma formulação MILP simétrica — permitindo múltiplas rotas por tipo — esperamos que o exato também produza configurações mistas, e o gap se aproxime de zero. Nas instâncias maiores, porém, o tempo de convergência ao ótimo do MILP refatorado pode tornar a comparação operacionalmente desvantajosa para o método exato.
## 9.4 Trade-off tempo × qualidade
O contraste de tempo computacional é a diferença operacional mais marcante entre as três abordagens. O MILP da Aula 4 resolve C1 em 0,27 s, C2 em 52,69 s e atinge o tempo-limite de 300 s em C3 e C4 sem provar otimalidade. As heurísticas construtivas resolvem qualquer instância abaixo de 20 ms. O pipeline completo de busca local sobre o Clarke-Wright executa entre 0,7 ms (C1) e 116 ms (C4); sobre o Nearest Neighbor, atinge 1,53 s em C4 — ainda duzentas vezes mais rápido do que o exato no mesmo caso.
Em termos práticos, o método exato fica restrito a auditorias e validações em instâncias pequenas; o pipeline construtivo + busca local é compatível com a rotina diária de planejamento da Prolog, mesmo que escalado para os 581 clientes da operação completa. A próxima sprint avaliará se as metaheurísticas (SA, ILS, GA) conseguem fechar o gap em C3 e C4 sem comprometer esse perfil de execução.
## 9.5 Pipeline operacional recomendado para a Prolog
A combinação dos resultados desta sprint sustenta um protocolo operacional concreto, formalizado no Quadro 4. A robustez da recomendação vem da observação de que o custo combinado do Nearest Neighbor e do Clarke-Wright permanece abaixo de 40 ms mesmo na maior instância testada, o que torna trivial gerar ambos e selecionar o melhor.

Quadro 4 – Pipeline operacional recomendado para a Prolog

Fonte: Elaboração própria.
Sob esse protocolo, o vencedor para as instâncias testadas é o Clarke-Wright + busca local em C2, C3 e C4, com empate em C1. O custo computacional total do protocolo em C4 é de aproximadamente 1,55 s — ordens de grandeza abaixo do exato e suficientemente rápido para permitir múltiplas reexecuções diárias em resposta a mudanças no perfil de demanda.
# 10 Conclusões e Trabalhos Futuros
A Sprint 1 concluiu os onze entregáveis previstos no seu escopo, cobrindo pesquisa, modelagem, implementação, experimentação e documentação do método exato. O modelo MILP com restrições MTZ e frota heterogênea ficou operacional, com resultados reprodutíveis para as quatro instâncias de teste e veredicto explícito sobre a viabilidade do método em função do tamanho da instância.
A Sprint 2 estendeu o escopo metodológico ao implementar heurísticas construtivas (Nearest Neighbor e Clarke-Wright Savings com frota heterogênea) e movimentos de busca local (2-opt e Relocate). A combinação das duas etapas produziu três resultados centrais. Primeiro, em C1 a heurística refinada igualou o ótimo global comprovado pelo MILP (R$ 422,38), validando o pipeline contra o benchmark exato. Segundo, em C2 a heurística superou o exato em 5,57% (R$ 712,05 contra R$ 754,04), revelando uma limitação da formulação MILP da Aula 4: a restrição implícita de saída única por tipo de veículo impede configurações com dois Fiorinos em paralelo, que são justamente as preferidas pelo Clarke-Wright em C2. Terceiro, em C3 e C4 os gaps aparentes em favor do exato (36,16% e 64,30%) refletem regimes operacionais distintos — o exato consolida em uma única rota VUC, configuração inacessível às heurísticas atuais — e não desempenho inferior do método heurístico.
Duas descobertas estruturais da Sprint 2 organizam o trabalho da Sprint 3. A primeira é a necessidade de refatorar a formulação MILP da Aula 4 para permitir múltiplas unidades por tipo de veículo, eliminando a assimetria que distorce a comparação em C3 e C4. A segunda é a barreira entre regimes de frota que a busca local sob melhoria estrita não atravessa: o Nearest Neighbor refinado permanece preso a configurações "só Fiorino" em C3 e C4 porque a transição para a configuração mista exigiria pagar momentaneamente R$ 550 de custo fixo do VUC antes que a consolidação compensasse. As metaheurísticas previstas para a Sprint 3 — Simulated Annealing, Iterated Local Search e Algoritmos Genéticos — aceitam pioras temporárias de forma controlada e são desenhadas exatamente para esse tipo de transição. A integração será operacionalmente direta: as oito soluções refinadas pela Sprint 2 servem como ponto de partida para todas as metaheurísticas.
Como contribuição operacional concreta, a Sprint 2 formalizou um pipeline recomendado para a Prolog (Quadro 4): gerar soluções iniciais com Nearest Neighbor e Clarke-Wright em paralelo (custo combinado abaixo de 40 ms na maior instância), aplicar 2-opt e Relocate em ambas, e selecionar a de menor custo total. Os riscos identificados na Sprint 1 — aproximação Haversine, jornada validada em pós-processamento e amostra de um único dia — permanecem como itens de backlog para tratamento ao longo da Sprint 3 ou em extensões futuras. As soluções refinadas estão persistidas nos oito arquivos JSON da pasta Aulas/8/Aula8_Busca_Local/files/.

# Referências Bibliográficas
BALLOU, R. H. Gerenciamento da cadeia de suprimentos / logística empresarial. 5. ed. Porto Alegre: Bookman, 2006.
CLARKE, G.; WRIGHT, J. W. Scheduling of vehicles from a central depot to a number of delivery points. Operations Research, v. 12, n. 4, p. 568-581, 1964.
CROES, G. A. A method for solving traveling-salesman problems. Operations Research, v. 6, n. 6, p. 791-812, 1958.
DANTZIG, G. B.; FULKERSON, D. R.; JOHNSON, S. M. Solution of a large-scale traveling-salesman problem. Operations Research, v. 2, n. 4, p. 393-410, 1954.
DANTZIG, G. B.; RAMSER, J. H. The truck dispatching problem. Management Science, v. 6, n. 1, p. 80-91, 1959.
DREZNER, Z. (Ed.). Facility location: a survey of applications and methods. New York: Springer-Verlag, 1995.
GAREY, M. R.; JOHNSON, D. S. Computers and intractability: a guide to the theory of NP-completeness. San Francisco: W. H. Freeman, 1979.
GENDREAU, M.; POTVIN, J.-Y. (Eds.). Handbook of metaheuristics. 2. ed. New York: Springer, 2010.
GOLDBARG, M.; GOLDBARG, E.; LUNA, H. Otimização combinatória e metaheurísticas: algoritmos e aplicações. Rio de Janeiro: GEN/LTC, 2015.
HART, W. E. et al. Pyomo: optimization modeling in Python. 2. ed. Cham: Springer, 2017.
HUANGFU, Q.; HALL, J. A. J. Parallelizing the dual revised simplex method. Mathematical Programming Computation, v. 10, n. 1, p. 119-142, 2018.
LAPORTE, G. The vehicle routing problem: an overview of exact and approximate algorithms. European Journal of Operational Research, v. 59, n. 3, p. 345-358, 1992.
LAPORTE, G. Fifty years of vehicle routing. Transportation Science, v. 43, n. 4, p. 408-416, 2009.
LENSTRA, J. K.; RINNOOY KAN, A. H. G. Complexity of vehicle routing and scheduling problems. Networks, v. 11, n. 2, p. 221-227, 1981.
LIN, S. Computer solutions of the traveling salesman problem. Bell System Technical Journal, v. 44, n. 10, p. 2245-2269, 1965.
MILLER, C. E.; TUCKER, A. W.; ZEMLIN, R. A. Integer programming formulation of traveling salesman problems. Journal of the ACM, v. 7, n. 4, p. 326-329, 1960.
NEMHAUSER, G. L.; WOLSEY, L. A. Integer and combinatorial optimization. New York: Wiley-Interscience, 1988.
NOVAES, A. G. Logística e gerenciamento da cadeia de distribuição: estratégia, operação e avaliação. 3. ed. Rio de Janeiro: Elsevier, 2007.
PAPADIMITRIOU, C. H.; STEIGLITZ, K. Combinatorial optimization: algorithms and complexity. Englewood Cliffs: Prentice-Hall, 1982.
PROJECT MANAGEMENT INSTITUTE. A guide to the project management body of knowledge (PMBOK guide). 7. ed. Newtown Square: PMI, 2021.
TOTH, P.; VIGO, D. Vehicle routing: problems, methods, and applications. 2. ed. Philadelphia: SIAM, 2014.
WOLSEY, L. A. Integer programming. New York: Wiley-Interscience, 1998.

# Anexos
Este apartado consolida, em formato de anexos, as ferramentas de gestão utilizadas na Sprint 1 e mencionadas ao longo do relatório. Os arquivos-fonte permanecem disponíveis no repositório do projeto e são referenciados nominalmente em cada anexo.
## ANEXO A – Estrutura Analítica do Projeto (EAP)
A EAP foi construída com orientação a entregáveis (PROJECT MANAGEMENT INSTITUTE, 2021) e organiza-se em cinco áreas no nível 2 e 21 entregáveis no nível 3. As áreas são: 1.1 Gestão de Projeto; 1.2 Pesquisa e Modelagem; 1.3 Implementação Computacional; 1.4 Análise de Resultados; e 1.5 Documentação e Apresentações. O diagrama completo é o registrado na Figura 7 da seção 9.2 e está também persistido no arquivo EAP.jpg, na raiz do repositório.
## ANEXO B – Cronograma de Entregáveis
O cronograma consolidado mapeia os 21 entregáveis da EAP às datas de início e término acordadas em Sprint Planning. A versão vigente está registrada no arquivo Cronograma.xlsx, na raiz do repositório. As datas dos entregáveis ativos na Sprint 1 já constam no Quadro 4 da seção 9.3 e abrangem os itens 1.1.1, 1.1.2, 1.1.3, 1.1.4, 1.2.1, 1.2.2, 1.2.3, 1.3.1, 1.4.1, 1.5.1 e 1.5.2.
## ANEXO C – Canvas de Projeto
O Canvas estrutura a proposta em cinco blocos. Problema: tomada de decisão baseada em intuição, gerando rotas ineficientes, custos elevados e baixo aproveitamento da frota. Objetivo: desenvolver um modelo CVRP que minimize distância percorrida e número de veículos, respeitando restrições operacionais. Funcionamento: pipeline em cinco etapas — preparação de dados, matriz de custos, modelo exato, heurísticas e análise comparativa. Benefícios: redução de custos logísticos, melhor uso da capacidade dos veículos e método replicável para planejamento de rotas. Diferencial: sistema híbrido que combina precisão de modelos exatos com eficiência das heurísticas, viável em escala real. Stakeholders: Prolog, equipe do projeto, coordenação acadêmica da PUC-Rio e clientes finais atendidos pela operação.
## ANEXO D – Matriz É / Não É – Faz / Não Faz
É: trabalho de CVRP voltado a minimizar custo total respeitando restrições operacionais; aplicação acadêmica de otimização combinatória a um caso real; exercício de modelagem MIP com programação linear inteira estruturada; experimento computacional testado em múltiplas instâncias.
Não É: estudo de localização de centros de distribuição; modelo estocástico; solução baseada em intuição; software comercial pronto para entrega.
Faz: resolve roteirização com métodos exatos e heurísticos; escala para cenários reais com metaheurísticas; equilibra custo logístico com restrições operacionais; transforma dados em planos de rota executáveis.
Não Faz: não se limita a uma única técnica de solução; não ignora restrições reais como jornada de trabalho; não realiza monitoramento em tempo real (não é GPS); não trata a execução das rotas, apenas o planejamento prévio.
## ANEXO E – Configuração Scrum e Trello
O ciclo Scrum adotado contempla três sprints de aproximadamente vinte dias, cada uma encerrada por Sprint Review pública (apresentação ao professor) e Sprint Retrospective interna (ata individual). O papel de Product Owner é rotativo entre os cinco integrantes do Grupo 2: Bernardo Caula, João Felipe Leal, Lucas Campos, Lucas Terzi e Rodrigo Pimentel. O acompanhamento operacional ocorre no Trello, com cinco listas: Product Backlog, Sprint Backlog, Em Andamento, Em Revisão e Finalizado. Cada cartão corresponde a um entregável do nível 3 da EAP ou a uma subtarefa técnica. As atas das Sprint Retrospectives são submetidas individualmente via Moodle conforme calendário da disciplina.
| PROJETO INTEGRADO VI – DISTRIBUIÇÃO FÍSICA | PROJETO INTEGRADO VI – DISTRIBUIÇÃO FÍSICA | PROJETO INTEGRADO VI – DISTRIBUIÇÃO FÍSICA |
| --- | --- | --- |
| Matrícula | Aluno | Professor: |
| [MATRÍCULA] | Bernardo Caula | Marcello Congro |
| [MATRÍCULA] | João Felipe Leal |  |
| [MATRÍCULA] | Lucas Campos |  |
| [MATRÍCULA] | Lucas Terzi |  |
| [MATRÍCULA] | Rodrigo Pimentel |  |
| Rio de Janeiro
Maio / 2026 | Rio de Janeiro
Maio / 2026 | Rio de Janeiro
Maio / 2026 |
|  |  |  |
| Instância | Clientes | Demanda total (kg) | Média (kg/cliente) |
| --- | --- | --- | --- |
| C1_10 | 10 | 141,6 | 14,2 |
| C2_25 | 25 | 754,5 | 30,2 |
| C3_40 | 40 | 1.295,3 | 32,4 |
| C4_60 | 60 | 1.958,1 | 32,6 |
| Parâmetro | Símbolo | Valor |
| --- | --- | --- |
| Depósito (CD) | D | CEP 25251-560, Duque de Caxias |
| Custo variável | g | R$ 1,50/km |
| Velocidade média | v | 40 km/h |
| Tempo de atendimento | s | 15 min/cliente |
| Jornada máxima | H | 8 h |
| Fiorino – capacidade | Q_FIO | 650 kg |
| Fiorino – custo fixo | f_FIO | R$ 250/dia |
| VUC – capacidade | Q_VUC | 3.000 kg |
| VUC – custo fixo | f_VUC | R$ 550/dia |
| Instância | Clientes | Custo (R$) | Veículos | Subtours | Tempo (s) | Status |
| --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 10 | 668,80 | 1 | 4 | 0,03 | optimal |
| C2_25 | 25 | 666,15 | 1 | 11 | 0,06 | optimal |
| C3_40 | 40 | 678,34 | 1 | 19 | 0,08 | optimal |
| C4_60 | 60 | 738,63 | 1 | 27 | 0,17 | optimal |
| Instância | Clientes | Custo (R$) | VUC | FIO | Rotas | Tempo (s) | Status |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 10 | 422,38 | 0 | 1 | 1 | 0,27 | optimal |
| C2_25 | 25 | 754,04 | 1 | 0 | 1 | 52,69 | optimal |
| C3_40 | 40 | 769,65 | 1 | 0 | 1 | 300,73 | maxTimeLimit |
| C4_60 | 60 | 858,31 | 1 | 0 | 1 | 300,88 | maxTimeLimit |
| Instância | Custo COM MTZ (R$) | Restrições COM | Tempo COM (s) | Custo SEM MTZ (R$) | Subtours SEM | Tempo SEM (s) |
| --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 422,38 | 139 | 0,79 | 368,80 | 4 | 0,13 |
| C2_25 | 754,04 | 709 | 65,01 | 666,15 | 11 | 0,20 |
| C3_40 | 769,65 | 1.729 | 300,98 | 676,69 | 19 | 0,17 |
| C4_60 | 858,31 | 3.789 | 300,54 | 734,59 | 28 | 0,18 |
| Instância | Custo TL=30s (R$) | Gap 30s | Custo TL=60s (R$) | Gap 60s | Custo TL=300s (R$) | Gap 300s |
| --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 422,38 | 0,00% | 422,38 | 0,00% | 422,38 | 0,00% |
| C2_25 | 754,04 | 0,45% | 754,04 | 0,14% | 754,04 | 0,00% |
| C3_40 | 792,17 | 7,79% | 776,20 | 5,80% | 769,65 | 3,56% |
| C4_60 | 875,61 | 7,03% | 862,20 | 5,15% | 858,31 | 4,37% |
| Instância | Custo Gurobi (R$) | Gap | Tempo (s) | Custo HiGHS (R$) | Gap | Tempo (s) | Status HiGHS |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1_10 | 422,38 | 0,00% | 0,58 | 422,38 | 0,01% | 6,39 | optimal |
| C2_25 | 754,04 | 0,00% | 77,05 | 760,18 | 6,07% | 300,23 | maxTimeLimit |
| Variação | Custo (R$) | FIO | VUC | Mudança |
| --- | --- | --- | --- | --- |
| Base (f_VUC = R$ 550, Q_VUC = 3.000) | 422,38 | 1 | 0 | — |
| f_VUC = R$ 1.500 | 422,38 | 1 | 0 | nenhuma |
| Q_VUC = 1.000 kg | 422,38 | 1 | 0 | nenhuma |
| Aspecto | Observação |
| --- | --- |
| Resultado empírico | Custo, número de rotas e composição da frota idênticos nas 16 execuções |
| Justificativa NN | Nenhum cliente isolado excede 650 kg (Fiorino); NN nunca abre rota VUC |
| Justificativa CW | VUC só é selecionado por extrapolação de capacidade na fusão; Fiorino deixa de ser candidato e a comparação entre critérios é vazia |
| Implicação operacional | Para a Equipe 2, basta executar o pipeline com total_cost |
| Inst. | Clientes | Rotas | Frota | Dist. (km) | Custo (R$) | Tempo (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 10 | 1 | 1 FIO | 120,40 | 430,60 | 0,4 |
| C2 | 25 | 2 | 2 FIO | 200,72 | 801,08 | 3,0 |
| C3 | 40 | 3 | 3 FIO | 223,24 | 1.084,86 | 7,3 |
| C4 | 60 | 4 | 4 FIO | 351,70 | 1.527,56 | 17,4 |
| Inst. | Clientes | Rotas | Frota | Dist. (km) | Custo (R$) | Fusões | Tempo (ms) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| C1 | 10 | 1 | 1 FIO | 115,75 | 423,63 | 9 | 0,4 |
| C2 | 25 | 2 | 2 FIO | 141,38 | 712,06 | 23 | 1,4 |
| C3 | 40 | 2 | 1 FIO + 1 VUC | 165,53 | 1.048,29 | 38 | 3,5 |
| C4 | 60 | 3 | 2 FIO + 1 VUC | 240,26 | 1.410,39 | 57 | 8,5 |
| Inst. | Custo NN (R$) | Custo CW (R$) | Δ Custo | Dist. NN (km) | Dist. CW (km) | Δ Dist. |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 430,60 | 423,63 | -1,62% | 120,40 | 115,75 | -3,86% |
| C2 | 801,08 | 712,06 | -11,11% | 200,72 | 141,38 | -29,57% |
| C3 | 1.084,86 | 1.048,29 | -3,37% | 223,24 | 165,53 | -25,85% |
| C4 | 1.527,56 | 1.410,39 | -7,67% | 351,70 | 240,26 | -31,69% |
| Heurística | Folgada (< 4 h) | Média (4–7 h) | Próxima do limite (> 7 h) | Total |
| --- | --- | --- | --- | --- |
| Nearest Neighbor | 3 | 3 | 4 | 10 |
| Clarke-Wright | 0 | 5 | 3 | 8 |
| Inst. | Exato (R$) | Status | CW (R$) | Gap CW | NN (R$) | Gap NN |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 422,38 | optimal | 423,63 | +0,30% | 430,60 | +1,95% |
| C2 | 754,04 | optimal | 712,06 | -5,57% | 801,08 | +6,24% |
| C3 | 769,65 | maxTimeLimit | 1.048,29 | +36,21% | 1.084,86 | +40,95% |
| C4 | 858,31 | maxTimeLimit | 1.410,39 | +64,32% | 1.527,56 | +77,97% |
| Heur. | Inst. | Dist. ini. (km) | Dist. 2-opt (km) | Ganho dist. | Custo ini. (R$) | Custo 2-opt (R$) | Ganho custo |
| --- | --- | --- | --- | --- | --- | --- | --- |
| NN | C1 | 120,40 | 114,92 | -4,55% | 430,60 | 422,38 | -1,91% |
| NN | C2 | 200,72 | 173,91 | -13,36% | 801,08 | 760,86 | -5,02% |
| NN | C3 | 223,24 | 210,44 | -5,73% | 1.084,86 | 1.065,66 | -1,77% |
| NN | C4 | 351,70 | 337,36 | -4,08% | 1.527,56 | 1.506,04 | -1,41% |
| CW | C1 | 115,75 | 114,92 | -0,72% | 423,63 | 422,38 | -0,29% |
| CW | C2 | 141,38 | 141,37 | -0,01% | 712,06 | 712,05 | 0,00% |
| CW | C3 | 165,53 | 165,33 | -0,12% | 1.048,29 | 1.047,99 | -0,03% |
| CW | C4 | 240,26 | 240,14 | -0,05% | 1.410,39 | 1.410,21 | -0,01% |
| Heur. | Inst. | Custo 2-opt (R$) | Custo final (R$) | Ganho custo | Tempo (ms) |
| --- | --- | --- | --- | --- | --- |
| NN | C1 | 422,38 | 422,38 | 0,00% | 0,0 |
| NN | C2 | 760,86 | 712,49 | -6,36% | 42,6 |
| NN | C3 | 1.065,66 | 1.062,31 | -0,31% | 74,1 |
| NN | C4 | 1.506,04 | 1.431,50 | -4,95% | 1.505,3 |
| CW | C1 | 422,38 | 422,38 | 0,00% | 0,0 |
| CW | C2 | 712,05 | 712,05 | 0,00% | 9,6 |
| CW | C3 | 1.047,99 | 1.047,99 | 0,00% | 23,9 |
| CW | C4 | 1.410,21 | 1.410,21 | 0,00% | 98,0 |
| Heur. | Inst. | Custo ini. (R$) | Custo 2-opt (R$) | Custo final (R$) | Ganho total | Tempo total (ms) |
| --- | --- | --- | --- | --- | --- | --- |
| NN | C1 | 430,60 | 422,38 | 422,38 | -1,91% | 1,6 |
| NN | C2 | 801,08 | 760,86 | 712,49 | -11,06% | 56,4 |
| NN | C3 | 1.084,86 | 1.065,66 | 1.062,31 | -2,08% | 87,6 |
| NN | C4 | 1.527,56 | 1.506,04 | 1.431,50 | -6,29% | 1.530,2 |
| CW | C1 | 423,63 | 422,38 | 422,38 | -0,29% | 0,7 |
| CW | C2 | 712,06 | 712,05 | 712,05 | 0,00% | 13,1 |
| CW | C3 | 1.048,29 | 1.047,99 | 1.047,99 | -0,03% | 37,3 |
| CW | C4 | 1.410,39 | 1.410,21 | 1.410,21 | -0,01% | 116,2 |
| Inst. | NN+BL (R$) | CW+BL (R$) | Vencedor | Vantagem (R$) | Vantagem (%) |
| --- | --- | --- | --- | --- | --- |
| C1 | 422,38 | 422,38 | empate | 0,00 | 0,00% |
| C2 | 712,49 | 712,05 | CW+BL | 0,44 | -0,06% |
| C3 | 1.062,31 | 1.047,99 | CW+BL | 14,33 | -1,35% |
| C4 | 1.431,50 | 1.410,21 | CW+BL | 21,29 | -1,49% |
| Inst. | Exato (R$) | Status | Melhor heur+BL (R$) | Origem | Gap |
| --- | --- | --- | --- | --- | --- |
| C1 | 422,38 | optimal | 422,38 | CW+BL (empate NN+BL) | 0,00% |
| C2 | 754,04 | optimal | 712,05 | CW+BL | -5,57% |
| C3 | 769,65 | maxTimeLimit | 1.047,99 | CW+BL | +36,16% |
| C4 | 858,31 | maxTimeLimit | 1.410,21 | CW+BL | +64,30% |
| Inst. | Exato (R$) | NN (R$) | CW (R$) | NN+BL (R$) | CW+BL (R$) | Recomendado |
| --- | --- | --- | --- | --- | --- | --- |
| C1 | 422,38 | 430,60 | 423,63 | 422,38 | 422,38 | Empate (Exato/CW+BL/NN+BL) |
| C2 | 754,04 | 801,08 | 712,06 | 712,49 | 712,05 | CW+BL |
| C3 | 769,65* | 1.084,86 | 1.048,29 | 1.062,31 | 1.047,99 | CW+BL |
| C4 | 858,31* | 1.527,56 | 1.410,39 | 1.431,50 | 1.410,21 | CW+BL |
| Passo | Ação | Tempo esperado em C4 |
| --- | --- | --- |
| 1 | Gerar a solução inicial Nearest Neighbor heterogêneo | ~17 ms |
| 2 | Gerar a solução inicial Clarke-Wright Savings heterogêneo | ~9 ms |
| 3 | Aplicar 2-opt + Relocate sobre cada solução inicial | ~1,5 s (NN) / ~0,12 s (CW) |
| 4 | Selecionar a solução de menor custo total para execução | desprezível |