# Benchmark de Backtracking: Conjunto das Partes
## Disciplina: Teoria da Computação

Este projeto realiza um benchmark comparativo de desempenho entre duas linguagens de programação, utilizando o algoritmo de **Backtracking** para resolver o problema do **Conjunto das Partes (Power Set)**.

---

## 👥 Integrantes do Grupo
* **Nome do Integrante 1**

---

## 📋 Sobre o Projeto

O objetivo é medir a eficiência computacional ao gerar todos os subconjuntos possíveis de um alfabeto. Como o espaço de solução é exponencial, definido pela fórmula $2^n$, o algoritmo exige muito processamento e memória, sendo ideal para testes de performance.

### Metodologia de Teste
Para garantir a consistência estatística

* **5 execuções** para cada nível de dificuldade.

* **3 níveis de carga**:
    * **Pequeno (Small):** 20 elementos
    * **Médio (Middle):** 25 elementos
    * **Grande (Big):** 30 elementos


---

## 💻 Linguagens Comparadas

### 1. Linguagem C
A implementação em C foca em controle de baixo nível:
* **Memória:** Alocação dinâmica manual via `malloc` e `free`.
* **Estrutura:** Lista encadeada (Linked List) implementada do zero.
* **Tempo:** Medição precisa utilizando a biblioteca `time.h`.

### 2. Linguagem Go
* Implementação equivalente à versão C.
* Backtracking recursivo com lista encadeada da biblioteca padrão (`container/list`), equivalente à pilha/lista usada em C.

---

## ▶️ Como executar

### C
```bash
gcc c/src_c/main.c c/src_c/linked_list.c c/src_c/backtracking.c c/src_c/test.c c/src_c/file.c -o c/programa.exe
./c/programa.exe
```

### Go
```bash
go run ./go
```

---
