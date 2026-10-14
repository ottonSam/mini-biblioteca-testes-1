# Atividade Avaliativa - Unidade I: Mini Sistema de Biblioteca

**Disciplina:** Testes de Software I

## Questão 3 – Testes utilizando unittest

### Principal diferença observada entre pytest e unittest

No **unittest**, a escrita é baseada em classes derivadas de `unittest.TestCase`, exigindo métodos de asserção próprios (`self.assertEqual`, `self.assertTrue`, etc.). No **pytest**, a escrita é funcional, sem obrigatoriedade de classes, utilizando a instrução nativa `assert` do Python com mensagens de erro mais concisas e legíveis.

---

## Questão 4 – Parametrização, classes de equivalência e valores-limite

### Critério usado para selecionar os dados de teste

Utilizou-se o particionamento em classes de equivalência (entradas válidas e inválidas quanto a tipo, valor e formato) combinado com a análise de valores-limite nas fronteiras de decisão (fronteira entre `-1` inválido e `0` válido; e bordas de prefixo e tamanho do ISBN).

---

## Questão 5 – Testando exceções

### Por que receber a exceção esperada representa sucesso do teste?

Porque em testes negativos o objetivo é certificar que o sistema impede operações ilegais e protege o estado interno. O lançamento da exceção correta comprova que a regra de proteção foi acionada com sucesso.

---

## Questão 6 – Utilização de fixtures

### Qual repetição de código foi eliminada

Eliminou-se a instanciação repetitiva de objetos `Livro` com dados literais idênticos na fase de Arrange de cada teste, centralizando a criação dos dados de teste em um único ponto.

---

## Questão 13 – Investigação de falhas

### 1. Erro introduzido

Na classe `LivroComBug` (`biblioteca/livro_com_bug.py`), o método `devolver` foi alterado para somar 2 exemplares em vez de 1:

```python
class LivroComBug(Livro):
    def devolver(self) -> None:
        self.quantidade_disponivel += 2
```

### 2. Teste que detectou o problema

`test_devolucao_livro_com_bug_integracao` em `tests/test_integracao.py`.

### 3. Mensagem apresentada pelo framework

```text
FAILED tests/test_integracao.py::test_devolucao_livro_com_bug_integracao - assert 3 == 2
E       assert 3 == 2
E        +  where 3 = <biblioteca.livro_com_bug.LivroComBug object at 0x...>.quantidade_disponivel
```

### 4. Interpretação da falha

O teste iniciou com 1 exemplar e realizou uma devolução. Era esperado que o estoque se tornasse 2 (`1 + 1`), mas o valor obtido foi 3 (`1 + 2`), comprovando que a mutação no método gerou inconsistência de estoque.

### 5. Correção realizada

Restaurar a implementação original no método `devolver`:

```python
def devolver(self) -> None:
    self.quantidade_disponivel += 1
```

---
