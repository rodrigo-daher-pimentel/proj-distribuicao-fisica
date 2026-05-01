#### ENG 4560 – Projeto Integrado VI: Distribuição Física | 2026.1

**Aula 4: Modelagem matemática do CVRP (Parte 2)**

Prof. Marcello Congro

marcellocongro@puc-rio.br

## **Onde estamos no curso?**

- Na **Aula 2**, transformamos os dados operacionais reais em uma instância estruturada do problema logístico
  - ❖ Foram identificados clientes, demandas, distâncias, custos e tempos, permitindo representar matematicamente a operação diária da empresa.
- Na **Aula 3**, implementamos a primeira formulação do CVRP
  - ❖ Foi considerada uma frota homogênea composta exclusivamente por veículos do tipo VUC. O modelo matemático foi implementado em Python e resolvido utilizando um solver de MIP.
- As soluções obtidas demonstraram coerência estrutural local
  - ❖ Cada cliente possuía exatamente uma entrada e uma saída, o fluxo era conservado e os limites agregados de capacidade eram respeitados;
  - ❖ Entretanto, observou-se que soluções matematicamente ótimas ainda poderiam ser logisticamente inválidas devido à formação de ciclos desconectados do depósito.

▪ A **Aula 4** tem como objetivo tornar o modelo estruturalmente correto e **operacionalmente mais realista**.

## **O que aprendemos na aula passada?**

- A formulação matemática implementada em Python na **Aula 3** garantiu que:
  - ❖ Cada cliente é atendido exatamente uma vez;
  - ❖ Existe conservação de fluxo em cada nó;
  - ❖ A demanda total respeita a capacidade agregada disponível.

▪ Essa distinção é central para compreender o comportamento observado nas soluções.

Função objetivo: 
$$\min \sum_{i \in N} \sum_{j \in N, j \neq i} c_{ij} x_{ij} + f \sum_{j \in C} x_{0j}$$
 (frota homogênea, somente VUCs)

▪ Restrições:

*(saída e entrada por cliente)*

$$\sum_{j\in N, j\neq i} x_{ij}=1, \quad \forall i\in C$$
  $\sum_{j\in N, j\neq i} x_{ij}-\sum_{j\in N, j\neq i} x_{ji}=0, \quad \forall i\in C$   $\sum_{j\in N, j\neq i} x_{ij}=1, \quad \forall j\in C$  (conservação de fluxo)

▪ Essas restrições asseguram que cada cliente possui exatamente um predecessor e um sucessor. No entanto, ainda não impusemos que todos esses ciclos estejam conectados ao depósito.

## **Características completas do sistema logístico**

- O sistema logístico do projeto considerado nesta disciplina será caracterizado pelos seguintes parâmetros reais de operação:
  - ❖ Depósito (Centro de Distribuição CD): **CEP 25251-560**
    - ✓ Este ponto será o local de origem e retorno de todas as rotas.
  - ❖ Tipos de veículos disponíveis:
    - ✓ Fiorino: Capacidade máxima **650 kg**, custo fixo diário **R\$ 250,00**;
    - ✓ VUC: Capacidade máxima **3000 kg**, custo fixo diário **R\$ 550,00**.
  - ❖ Custos e tempos adicionais:
    - ✓ Custo variável: R\$ 1,50/km (aplicável a todos os veículos);
    - ✓ Velocidade média: 40 km/h;
    - ✓ Tempo de atendimento por cliente: 15 min;
    - ✓ Jornada máxima diária: 8h (= 480 min).

## **Problema observado:** *subtours*

- Durante os experimentos da Aula 3, observou-se que o solver poderia produzir ciclos formados exclusivamente por clientes, sem ligação com o depósito.
- Esses ciclos são denominados **subtours.**
- Matematicamente, eles satisfazem todas as restrições impostas:
  - ❖ Entrada única;
  - ❖ Saída única;
  - ❖ Conservação de fluxo.

- As restrições de grau **garantem apenas propriedades locais**, assegurando que cada cliente possua exatamente um predecessor e um sucessor.
- No entanto, nada impede que um subconjunto de clientes forme um **ciclo fechado independente.**

## **O solver não errou!**

- É importante compreender que o solver não produz soluções incorretas; ele resolve exatamente o modelo matemático fornecido.
- Se uma solução logística inválida aparece, isso indica que o modelo ainda não capturava completamente as regras da operação.
- A modelagem matemática consiste precisamente em transformar conhecimento operacional em restrições formais.

## **Formulação MTZ**

- Ideia intuitiva: a noção de "ordem de visita"
  - ❖ A formulação Miller-Tucker-Zemlin introduz uma variável auxiliar a cada cliente. Essa variável não representa distância, tempo ou custo;
  - ❖ Ela representa apenas uma posição relativa na sequência de atendimento da rota;
  - ❖ Se um veículo visita o cliente antes do cliente , então o modelo impõe que o nível associado a seja maior do que o nível associado a ;
  - ❖ Dessa forma, cria-se implicitamente uma ordem crescente de visitas;
  - ❖ Dentro de um *subtour* desconectado ao depósito, seria impossível atribuir níveis consistentes a todos os clientes, pois a ordem acabaria formando uma contradição circular.

- Implementação matemática
  - ❖ Para clientes , a restrição utilizada é:

$$u_i - u_j + (n-1)\sum_k x_{ijk} \le n - 2$$

- ⇒ posição do cliente na sequência de visitas;
- ⇒ indica se o veículo do tipo k percorre o arco entre i e j;
- ⇒ número total de nós
- ❖ Interpretação: Se o arco → não é utilizado, a restrição permanece inativa.

Se o arco → é utilizado, o modelo exige que ≥ + 1 (ou seja, o cliente seguinte deve possuir posição superior na ordem)

• Caso 1: 
$$\sum_k x_{ijk} = 1 \Rightarrow u_i - u_j + (n-1) \le n-2 \Rightarrow u_j \ge u_i + 1$$

• *Caso 2:* σ = 0 ⇒ − ≤ − 2 ⇒ *Sempre verdadeira!*

- Implementação computacional (Python)
  - ❖ No notebook, como vamos implementar a formulação?

```
def mtz_rule(model, i, j):
if i == j:
    return Constraint.Skip
return (
    model.u[i]
    - model.u[j]
    + (n-1)*sum(model.x[i,j,k] for k in model.K)
    <= n-2
)
```

❖ A variável auxiliar foi definida como:

```
model.u = Var(model.C, bounds=(1, n-1))
```

- *Os limites garantem que cada cliente receba uma posição válida dentro da sequência possível de visitas;*
- *A restrição é aplicada apenas entre clientes;*
- *O depósito não participa da ordenação;*
- *A soma sobre os tipos de veículo ativa a restrição sempre que qualquer veículo utiliza o arco.*

- Por que utilizar () e não , ?
  - ❖ Formulações completas do VRP frequentemente utilizam variáveis auxiliaries associadas simultaneamente ao cliente e ao veículo. Isso permitiria representar múltiplas sequências independentes.
  - ❖ Entretanto, essa abordagem aumenta significativamente:
    - ✓ Número de variáveis;
    - ✓ Número de restrições;
    - ✓ Esforço computacional.
  - ❖ Como hipótese simplificadora, adotamos uma única variável por cliente.
  - ❖ A soma sobre os veículos na restrição garante que qualquer arco selecionado respeite a ordem global.

- Impacto computacional da formulação MTZ
  - ❖ A introdução do MTZ aumenta o número de restrições aproximadamente de forma quadrática com o número de clientes.
  - ❖ O solver passa a lidar com mais dependências entre decisões. Consequentemente:
    - ✓ O tempo de solução aumenta;
    - ✓ A prova de otimalidade torna-se mais difícil.

## **Atualização do modelo matemático**

- Até a aula passada, todos os veículos eram do tipo VUC.
- Agora introduzimos o caso real: K = {FIO, VUC}, e cada tipo possui ,
- Nova variável de roteamento, definindo:

$$x_{ij}^k \in \{0,1\}, \quad \forall i \neq j, \forall k \in K$$

- Cada arco está associado agora a um tipo de veículo.
- A restrição de visita única torna-se:

$$\sum_{k \in K} \sum_{\substack{j \in N \ j \neq i}} x_{ij}^k = 1$$

• *Para manter o modelo tratável, consideramos decisões por tipo de veículo, e não veículos individualmente identificados.*

## **Atualização do modelo matemático (cont.)**

- Custos fixos x Custos variáveis
  - ❖ Veículos maiores possuem maior custo fixo, mas podem reduzir o número de viagens;
  - ❖ Veículos menores apresentam menor custo inicial, porém podem aumentar o deslocamento total necessário;
  - ❖ O solver precisa equilibrar esses efeitos;
  - ❖ A solução ótima passa a refletir o compromisso entre utilização da frota e custo de deslocamento.

- *Embora exista um limite operacional claro de jornada diária, ele não será incluído diretamente no modelo matemático nesta etapa.*
- *A jornada será avaliada posteriormente durante a validação operacional;*
- *Essa decisão permite observar como o modelo se comporta quando determinadas restrições práticas não são explicitamente impostas.*

## **Validação operacional**

- Após resolver o modelo, devemos verificar:
  - ❖ Tempo total de cada rota;
  - ❖ Separação entre deslocamento e serviço;
  - ❖ Atendimento completo dos clientes.
- Resolver o modelo não encerra o trabalho do engenheiro! **A solução deve ser sempre interpretada criticamente!**

▪ Variáveis de decisão:

$$x_{ijk} = \begin{cases} 1, & \text{se um veículo do tipo } k \text{ percorre o arco } (i,j) \ 0, & \text{caso contrário} \end{cases}$$

$$\blacktriangle$$
 Uso do tipo de veículo:  $m_k \in \mathbb{Z}_+$  (veículos do tipo "k" utilizados)

#### **Conjuntos:**

- N ⇒ nós (depósito + clientes);
- C ⇒ clientes (*i.e*., N {0});
- K ⇒ tipos de veículos disponíveis (ex.: Fiorino, VUC).

# **Atualização do modelo matemático (cont.)**

▪ Função objetivo:

*Custo fixo Custo variável*

#### **Parâmetros**:

- ⇒ custo variável (entre nó i e j);
- ⇒ custo fixo de utilização de veículo do tipo k
- ⇒ demanda do cliente i
- ⇒ capacidade máxima do veículo do tipo k
- = ⇒ número total de nós

▪ Restrições:

$$\sum_{k \in K} \sum_{\substack{i \in N \ i \neq j}} x_{ijk} = 1 \hspace{0.5cm} \forall j \in C$$

*(Atendimento único dos clientes, cada cliente possui exatamente uma entrada)*

$$\sum_{k \in K} \sum_{\substack{i \in N \ i \neq j}} x_{ijk} = \sum_{k \in K} \sum_{\substack{l \in N \ l \neq j}} x_{jlk} \qquad \forall j \in C$$

*(Conservação de fluxo: Entrada = Saída)*

$$\sum_{i \in C} q_i \sum_{\substack{j \in N \ j \neq i}} x_{ijk} \leq Q_k m_k \qquad \forall k \in K$$

*(Capacidade da frota, demanda não pode exceder a capacidade disponível)*

$$\bigg|\sum_{j\in C} x_{0jk} \leq m_k \qquad \forall k \in K$$

*(Número de rotas iniciadas, cada veículo inicia no máximo uma rota)*

$$\sum_{i \in C} x_{i0k} \leq m_k \qquad \forall k \in K$$

*(Retorno ao depósito)*

$$u_i-u_j+(n-1)\sum_{k\in K}x_{ijk}\leq n-2 \qquad \forall i,j\in C,\; i\neq j$$

*(Eliminação de subtours)*

#### **Hands-on**

▪ **2ª parte**: Implementação no ambiente Colab

## **Sprint 1: Experimentos computacionais**

▪ **Avaliação sistemática do comportamento do modelo matemático implementado**

Cada equipe deverá realizar experimentos variando condições, tais como:

- Teste com as instâncias (C1 C4) do problema real (aumento do nº de clientes);
- Solver utilizado;
- Limite de tempo;
- Parâmetros de frota;
- Qualidade da solução obtida;
- Utilização e eliminação da formulação MTZ;
- Variação do custo fixo do VUC (em qual ponto o modelo deixa de usar o VUC?)
- Variação da velocidade média (situações de trânsito pesado x rodovia);
- Variação do tempo de serviço (simulando hospital congestionado, por exemplo);
- Análise do gap x time limit (30s, 60s, 300s). A solução incumbente melhora ou piora?
- Comparar os seus resultados com as soluções das outras equipes da turma.

## **Sprint 1: Experimentos computacionais**

▪ **Avaliação sistemática do comportamento do modelo matemático implementado**

Cada equipe deverá realizar experimentos variando condições, tais como:

- **Teste com as instâncias (C1 – C4) do problema real (aumento do nº de clientes);**
- **Solver utilizado;**
- **Limite de tempo;**
- **Parâmetros de frota;**
- **Qualidade da solução obtida;**
- **Utilização e remoção da formulação MTZ;**
- **Variação do custo fixo do VUC (em qual ponto o modelo deixa de usar o VUC?)**
- **Variação da velocidade média (situações de trânsito pesado x rodovia);**
- **Variação do tempo de serviço (simulando hospital congestionado, por exemplo);**
- **Análise do gap x time limit (30s, 60s, 300s). A solução incumbente melhora significativamente?**
- **Comparar os seus resultados com as soluções das outras equipes da turma.**

Experimento obrigatório

Experimento opcional (cada equipe escolhe pelo menos 1)