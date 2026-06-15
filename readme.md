# Benchmark de Backtracking: Conjunto das Partes

## Disciplina: Teoria da Computação

Este projeto realiza um benchmark comparativo de desempenho entre duas linguagens de programação, utilizando o algoritmo de **Backtracking** para resolver o problema do **Conjunto das Partes (Power Set)**.

Além das implementações em **C** e **Go**, o projeto possui um **dashboard em Python** para visualizar os resultados experimentais por meio de tabelas, gráficos comparativos, boxplots e curva teórica de complexidade.

---

## 👥 Integrantes do Grupo

* **Nome do Integrante 1**
* **Nome do Integrante 2**
* **Nome do Integrante 3**
* **Nome do Integrante 4**

---

## 📋 Sobre o Projeto

O objetivo é medir a eficiência computacional ao gerar todos os subconjuntos possíveis de um conjunto de entrada. Como cada elemento pode estar presente ou ausente em um subconjunto, o número total de combinações possíveis é definido por:

```text
2^n
```

Por esse motivo, o algoritmo possui crescimento exponencial, sendo adequado para análise prática de complexidade de tempo e comparação de desempenho entre linguagens.

---

## 🧠 Algoritmo Utilizado

O algoritmo utiliza **backtracking recursivo** para explorar todas as combinações possíveis dos elementos de entrada.

Para cada elemento, existem duas decisões possíveis:

```text
1. incluir o elemento no subconjunto atual;
2. não incluir o elemento no subconjunto atual.
```

Esse processo forma uma árvore de decisão binária. Para uma entrada de tamanho `n`, o algoritmo percorre `2^n` possibilidades.

### Complexidade Teórica

```text
Melhor caso: Θ(2^n)
Caso médio: Θ(2^n)
Pior caso: Θ(2^n)
```

Como o algoritmo gera todos os subconjuntos e não utiliza poda ou parada antecipada, a quantidade de combinações exploradas é exponencial em todos os casos.

---

## 🧪 Metodologia de Teste

Para garantir maior consistência estatística, foram executadas:

* **30 execuções** para cada tamanho de entrada;
* **30 execuções** para cada linguagem;
* **3 níveis de carga**:

```text
Pequeno (SMALL_TEST): 20 elementos
Médio   (MIDDLE_TEST): 25 elementos
Grande  (BIG_TEST): 30 elementos
```

Para cada grupo de testes, foram calculados:

* tempo médio de execução;
* desvio-padrão;
* tempo mínimo;
* tempo máximo;
* quantidade de execuções realizadas.

Os resultados são salvos em arquivos separados para C e Go, e posteriormente lidos pelo dashboard em Python.

---

## 💻 Linguagens Comparadas

### 1. Linguagem C

A implementação em C foca em controle de baixo nível:

* **Memória:** alocação dinâmica manual via `malloc` e `free`;
* **Estrutura:** lista encadeada implementada manualmente;
* **Execução:** implementação direta do backtracking;
* **Medição de tempo:** coleta do tempo de execução para análise experimental.

### 2. Linguagem Go

A implementação em Go busca manter equivalência lógica com a versão em C:

* **Estrutura:** uso de lista encadeada com `container/list`;
* **Execução:** backtracking recursivo equivalente;
* **Runtime:** gerenciamento automático de memória pelo garbage collector;
* **Medição de tempo:** coleta do tempo de execução para comparação com C.

---

## 📊 Dashboard de Resultados

O projeto inclui um dashboard em Python localizado na pasta:

```text
dashboard_teoria/
```

A estrutura do dashboard é:

```text
dashboard_teoria/
├── dashboard.py
├── requirements.txt
└── README.md
```

O dashboard foi desenvolvido com:

* **Python**
* **Streamlit**
* **Pandas**
* **Plotly**

Ele funciona apenas como uma camada de leitura e visualização. Ou seja, ele **não modifica os arquivos das pastas `c/` e `go/`**.

---

## 📁 Arquivos Lidos pelo Dashboard

O dashboard lê automaticamente os arquivos de resultado gerados pelas implementações em C e Go.

### Resultados da implementação em C

```text
c/case_tests_c/SMALL_TEST
c/case_tests_c/MIDDLE_TEST
c/case_tests_c/BIG_TEST
```

### Resultados da implementação em Go

```text
go/case_tests_go/SMALL_TEST
go/case_tests_go/MIDDLE_TEST
go/case_tests_go/BIG_TEST
```

O formato esperado das linhas é semelhante a:

```text
len set 20 time: 0.123456789
```

A partir desses arquivos, o dashboard extrai:

* linguagem;
* cenário;
* tamanho da entrada `n`;
* tempo de execução.

---

## 📈 Visualizações do Dashboard

O dashboard apresenta:

### 1. Tabela consolidada

A tabela mostra, para cada linguagem e tamanho de entrada:

* quantidade de execuções;
* média do tempo;
* desvio-padrão;
* tempo mínimo;
* tempo máximo.

### 2. Gráfico de tempo médio

Compara o tempo médio de execução entre C e Go para os tamanhos:

```text
n = 20
n = 25
n = 30
```

Esse gráfico evidencia o crescimento do tempo conforme o tamanho da entrada aumenta.

### 3. Curva teórica O(2^n)

O dashboard também exibe uma curva teórica `O(2^n)` escalada sobre os dados reais, permitindo comparar o comportamento experimental com a complexidade esperada.

### 4. Distribuição das execuções

O boxplot mostra a variação das 30 execuções em cada cenário, permitindo analisar a estabilidade dos tempos medidos.

### 5. Exportação CSV

O dashboard permite baixar a tabela consolidada em formato `.csv`.

---

## ▶️ Como executar os benchmarks

### C

```bash
gcc c/src_c/main.c c/src_c/linked_list.c c/src_c/backtracking.c c/src_c/test.c c/src_c/file.c -o c/programa.exe
./c/programa.exe
```

### Go

> [!CAUTION]
> ### ⚠️ Requisito de Sistema (Linux)

```bash
go run ./go
```

Após executar os benchmarks, os arquivos de resultado serão gerados nas pastas correspondentes de C e Go.

---

## ▶️ Como executar o dashboard

A partir da raiz do projeto, crie e ative um ambiente virtual Python:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Instale as dependências:

```bash
python -m pip install --upgrade pip
python -m pip install -r dashboard_teoria/requirements.txt
```

Execute o dashboard:

```bash
python -m streamlit run dashboard_teoria/dashboard.py
```

Depois disso, o Streamlit abrirá uma interface no navegador com os gráficos e tabelas dos resultados experimentais.

---

## 📌 Interpretação dos Resultados

Os resultados experimentais indicam crescimento exponencial do tempo de execução conforme o tamanho da entrada aumenta. Esse comportamento é esperado, pois o algoritmo de backtracking para geração do conjunto das partes explora duas possibilidades para cada elemento: incluir ou não incluir.

Assim, para uma entrada de tamanho `n`, o número total de subconjuntos gerados é:

```text
2^n
```

Na comparação entre as linguagens, a implementação em C apresentou tempos médios menores que a implementação em Go em todos os tamanhos testados. Apesar disso, ambas seguem a mesma tendência de crescimento assintótico, confirmando que a diferença prática está relacionada principalmente a fatores de implementação, runtime e gerenciamento de memória, não à complexidade teórica do algoritmo.

---

## ✅ Organização do Projeto

```text
backtraking_conjunto_das_partes/
├── c/
│   ├── src_c/
│   └── case_tests_c/
├── go/
│   ├── main.go
│   └── case_tests_go/
├── dashboard_teoria/
│   ├── dashboard.py
│   ├── requirements.txt
│   └── README.md
└── README.md
```

---

