# Dashboard de resultados experimentais

Este dashboard lê os resultados experimentais gerados pelos programas em C e Go e exibe tabelas e gráficos para comparar os tempos de execução do algoritmo de geração do conjunto das partes por backtracking.

## Instalação

A partir da raiz do projeto, instale as dependências:

```bash
pip install -r dashboard_teoria/requirements.txt
```

## Como rodar

A partir da raiz do projeto, execute:

```bash
streamlit run dashboard_teoria/dashboard.py
```

## Arquivos lidos

O dashboard procura automaticamente pelos seguintes arquivos:

```text
c/case_tests_c/SMALL_TEST
c/case_tests_c/MIDDLE_TEST
c/case_tests_c/BIG_TEST
go/case_tests_go/SMALL_TEST
go/case_tests_go/MIDDLE_TEST
go/case_tests_go/BIG_TEST
```

As linhas esperadas devem ter formato semelhante a:

```text
len set 20 time: 0.123456789
```

De cada linha válida são extraídos:

- linguagem: C ou Go;
- cenário: SMALL_TEST, MIDDLE_TEST ou BIG_TEST;
- tamanho da entrada, `n`;
- tempo de execução.

## Segurança dos dados

Este dashboard é apenas uma camada de leitura e visualização. Ele não modifica arquivos dentro das pastas `c/` e `go/`, não recompila programas, não executa benchmarks e não altera os arquivos de resultado existentes.

## Observação sobre execuções

Caso algum grupo de linguagem, cenário e tamanho de entrada tenha menos de 30 execuções, o dashboard mostra os dados disponíveis e exibe um aviso, pois a especificação da disciplina recomenda 30 rodadas por tamanho de entrada.

## Escala e barras de erro

Os gráficos principais podem ser exibidos em escala linear ou logarítmica no eixo Y por meio do checkbox **Usar escala logarítmica no eixo Y**. Essa opção altera apenas a escala de visualização, mantendo os dados originais sem transformação.

As barras de erro das séries experimentais de C e Go representam o desvio-padrão das 30 execuções. A curva teórica O(2^n) não possui barras de erro.
