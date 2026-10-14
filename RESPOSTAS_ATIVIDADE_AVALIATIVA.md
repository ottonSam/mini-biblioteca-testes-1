# Atividade Avaliativa - Unidade I: Mini Sistema de Biblioteca

**Disciplina:** Testes de Software I | **Curso:** Ciência da Computação

---

## Questão 1 – Construção e organização inicial do sistema

> **Enunciado:**  
> Desenvolva a primeira versão do Mini Sistema de Biblioteca. Implemente, no mínimo, as funcionalidades abaixo:
>
> - classe ou estrutura Livro;
> - classe ou estrutura Biblioteca;
> - cadastro de livro;
> - consulta de livro;
> - verificação de disponibilidade;
> - empréstimo;
> - devolução;
> - validação das regras básicas do domínio.
>
> **Entregue:** (a) a estrutura de diretórios; (b) o código desenvolvido; (c) uma breve explicação da responsabilidade de cada módulo, classe ou função criada.

### (a) Estrutura de diretórios

```text
mini-biblioteca-testes-1/
├── biblioteca/
│   ├── __init__.py
│   ├── livro.py
│   ├── validators.py
│   ├── database.py
│   ├── repository.py
│   └── biblioteca.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    ├── test_livro.py
    ├── test_validators.py
    ├── test_repository.py
    ├── test_biblioteca.py
    └── test_integracao.py
```

### (b) Código desenvolvido

#### `biblioteca/livro.py`

```python
class Livro:
    def __init__(self, isbn: str, titulo: str, autor: str, quantidade_disponivel: int) -> None:
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.quantidade_disponivel = quantidade_disponivel

    def __str__(self) -> str:
        return f"ISBN: {self.isbn}, Título: {self.titulo}, Autor: {self.autor}, Quantidade Disponível: {self.quantidade_disponivel}"

    def emprestar(self) -> bool:
        if self.quantidade_disponivel > 0:
            self.quantidade_disponivel -= 1
            return True
        return False

    def devolver(self) -> None:
        self.quantidade_disponivel += 1

    def info(self) -> dict:
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "quantidade_disponivel": self.quantidade_disponivel
        }
```

#### `biblioteca/validators.py`

```python
import re
from .livro import Livro

def validar_isbn(isbn: str) -> None:
    if not isinstance(isbn, str):
        raise ValueError("ISBN deve ser um texto.")
    if not re.fullmatch(r"97[89][0-9]{2}", isbn):
        raise ValueError("ISBN deve conter 5 dígitos e começar com 978 ou 979.")

def validar_titulo(titulo: str) -> None:
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("Título deve ser um texto não vazio.")

def validar_autor(autor: str) -> None:
    if not isinstance(autor, str) or not autor.strip():
        raise ValueError("Autor deve ser um texto não vazio.")

def validar_quantidade_disponivel(quantidade: int) -> None:
    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade < 0:
        raise ValueError("Quantidade disponível deve ser um inteiro maior ou igual a zero.")

def validar_livro(livro: Livro) -> None:
    if not isinstance(livro, Livro):
        raise ValueError("É necessário informar uma instância de Livro.")
    validar_isbn(livro.isbn)
    validar_titulo(livro.titulo)
    validar_autor(livro.autor)
    validar_quantidade_disponivel(livro.quantidade_disponivel)
```

#### `biblioteca/database.py`

```python
import sqlite3
from typing import Optional
from .livro import Livro

class Database:
    def __init__(self, caminho: str = ":memory:") -> None:
        self.connection = sqlite3.connect(caminho)
        self.connection.row_factory = sqlite3.Row
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS livros (
                    isbn TEXT PRIMARY KEY NOT NULL,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    quantidade_disponivel INTEGER NOT NULL CHECK (quantidade_disponivel >= 0)
                )
                """
            )

    def buscar(self, isbn: str) -> Optional[Livro]:
        registro = self.connection.execute(
            "SELECT isbn, titulo, autor, quantidade_disponivel FROM livros WHERE isbn = ?",
            (isbn,),
        ).fetchone()
        if registro is None:
            return None
        return Livro(
            registro["isbn"],
            registro["titulo"],
            registro["autor"],
            registro["quantidade_disponivel"],
        )

    def salvar(self, livro: Livro) -> None:
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO livros (isbn, titulo, autor, quantidade_disponivel)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(isbn) DO UPDATE SET
                    titulo = excluded.titulo,
                    autor = excluded.autor,
                    quantidade_disponivel = excluded.quantidade_disponivel
                """,
                (livro.isbn, livro.titulo, livro.autor, livro.quantidade_disponivel),
            )

    def remover(self, isbn: str) -> Livro:
        livro = self.buscar(isbn)
        if livro is None:
            raise ValueError(f"Livro com ISBN {isbn} não encontrado.")
        with self.connection:
            self.connection.execute("DELETE FROM livros WHERE isbn = ?", (isbn,))
        return livro

    def fechar(self) -> None:
        self.connection.close()

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.fechar()
```

#### `biblioteca/repository.py`

```python
from typing import Optional
from .database import Database
from .livro import Livro
from .validators import validar_livro

class LivroRepository:
    def __init__(self, database: Optional[Database] = None) -> None:
        self.database = database if database is not None else Database()

    def buscar(self, isbn: str) -> Optional[Livro]:
        return self.database.buscar(isbn)

    def cadastrar(self, livro: Livro) -> None:
        validar_livro(livro)
        if self.database.buscar(livro.isbn) is not None:
            raise ValueError(f"Livro com ISBN {livro.isbn} já cadastrado.")
        self.database.salvar(livro)

    def atualizar(self, livro: Livro) -> None:
        validar_livro(livro)
        if self.database.buscar(livro.isbn) is None:
            raise ValueError(f"Livro com ISBN {livro.isbn} não encontrado.")
        self.database.salvar(livro)

    def remover(self, isbn: str) -> Livro:
        return self.database.remover(isbn)
```

#### `biblioteca/biblioteca.py`

```python
from typing import Optional
from .livro import Livro
from .repository import LivroRepository

class Biblioteca:
    def __init__(self, repository: Optional[LivroRepository] = None) -> None:
        self.repository = repository if repository is not None else LivroRepository()

    def buscar(self, isbn: str) -> Optional[Livro]:
        return self.repository.buscar(isbn)

    def verificar_quantidade_disponivel(self, isbn: str) -> int:
        return self._obter_livro(isbn).quantidade_disponivel

    def cadastrar(self, livro: Livro) -> None:
        self.repository.cadastrar(livro)

    def remover(self, isbn: str) -> Livro:
        return self.repository.remover(isbn)

    def emprestar(self, isbn: str) -> bool:
        livro = self._obter_livro(isbn)
        if not livro.emprestar():
            return False
        self.repository.atualizar(livro)
        return True

    def devolver(self, isbn: str) -> None:
        livro = self._obter_livro(isbn)
        livro.devolver()
        self.repository.atualizar(livro)

    def _obter_livro(self, isbn: str) -> Livro:
        livro = self.buscar(isbn)
        if livro is None:
            raise ValueError(f"Livro com ISBN {isbn} não encontrado.")
        return livro
```

### (c) Breve explicação da responsabilidade de cada módulo, classe ou função criada

- **`Livro` (`biblioteca/livro.py`)**: Entidade de domínio. Guarda os atributos do livro (`isbn`, `titulo`, `autor`, `quantidade_disponivel`) e executa as regras locais de decrementar estoque no empréstimo (`emprestar`) e incrementar na devolução (`devolver`).
- **`validators.py`**: Funções puras de validação. Verifica formato de ISBN (5 dígitos iniciando em 978/979), campos de texto não vazios e quantidade inteira não negativa.
- **`Database` (`biblioteca/database.py`)**: Camada de persistência SQLite. Gerencia conexão, cria a tabela `livros` e executa comandos SQL diretos (`buscar`, `salvar`, `remover`).
- **`LivroRepository` (`biblioteca/repository.py`)**: Camada de acesso a dados. Valida os objetos antes da gravação e impede duplicação de ISBN no cadastro.
- **`Biblioteca` (`biblioteca/biblioteca.py`)**: Fachada de serviços. Expõe as operações de alto nível do sistema (cadastrar, buscar, verificar disponibilidade, emprestar, devolver, remover), orquestrando o repositório e o modelo.

---

## Questão 2 – Primeiros testes unitários com pytest

> **Enunciado:**  
> Crie testes unitários utilizando pytest para testar isoladamente as principais operações do Mini Sistema de Biblioteca: criação de um livro, ISBN, título, autor, quantidade de exemplares, cadastro de livro, consulta de livro existente, disponibilidade de livro, empréstimo e devolução.  
> **Em pelo menos dois testes, identifique explicitamente quais linhas correspondem ao Arrange, Act e Assert.**

### Código desenvolvido com identificação de Arrange, Act e Assert

#### Teste 1: Criação de Livro (`tests/test_livro.py`)

```python
def test_criacao_livro():
    # Arrange
    isbn = "97801"
    titulo = "Clean Code"
    autor = "Robert C. Martin"
    quantidade = 5

    # Act
    livro = Livro(isbn, titulo, autor, quantidade)

    # Assert
    assert isinstance(livro, Livro)
    assert livro.isbn == "97801"
    assert livro.titulo == "Clean Code"
    assert livro.autor == "Robert C. Martin"
    assert livro.quantidade_disponivel == 5
```

#### Teste 2: Empréstimo com Sucesso (`tests/test_livro.py`)

```python
def test_emprestimo_com_sucesso():
    # Arrange
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)

    # Act
    resultado = livro.emprestar()

    # Assert
    assert resultado is True
    assert livro.quantidade_disponivel == 2
```

---

## Questão 3 – Testes utilizando unittest

> **Enunciado:**  
> Escolha pelo menos três funcionalidades do Mini Sistema de Biblioteca que já foram testadas com pytest e implemente novamente seus testes utilizando unittest. Utilize adequadamente recursos como self.assertEqual(), self.assertTrue(), self.assertFalse() e self.assertIsInstance().  
> **Ao final, explique brevemente a principal diferença que você observou entre a escrita de testes utilizando pytest e unittest.**

### Código desenvolvido (`tests/test_livro.py`)

```python
import unittest
from biblioteca.livro import Livro

class TestLivroUnittest(unittest.TestCase):
    def test_criacao_livro(self):
        # Arrange
        isbn = "97801"
        titulo = "Clean Code"
        autor = "Robert C. Martin"
        quantidade = 5

        # Act
        livro = Livro(isbn, titulo, autor, quantidade)

        # Assert
        self.assertIsInstance(livro, Livro)
        self.assertEqual(livro.isbn, "97801")
        self.assertEqual(livro.titulo, "Clean Code")
        self.assertEqual(livro.autor, "Robert C. Martin")
        self.assertEqual(livro.quantidade_disponivel, 5)

    def test_emprestimo_com_sucesso(self):
        # Arrange
        livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)

        # Act
        resultado = livro.emprestar()

        # Assert
        self.assertTrue(resultado)
        self.assertEqual(livro.quantidade_disponivel, 2)

    def test_emprestimo_sem_exemplares(self):
        # Arrange
        livro = Livro("97801", "Clean Code", "Robert C. Martin", 0)

        # Act
        resultado = livro.emprestar()

        # Assert
        self.assertFalse(resultado)
        self.assertEqual(livro.quantidade_disponivel, 0)

    def test_devolucao_livro(self):
        # Arrange
        livro = Livro("97801", "Clean Code", "Robert C. Martin", 1)

        # Act
        livro.devolver()

        # Assert
        self.assertEqual(livro.quantidade_disponivel, 2)
```

### Principal diferença observada entre pytest e unittest

No **unittest**, a escrita é baseada em classes derivadas de `unittest.TestCase`, exigindo métodos de asserção próprios (`self.assertEqual`, `self.assertTrue`, etc.). No **pytest**, a escrita é funcional, sem obrigatoriedade de classes, utilizando a instrução nativa `assert` do Python com mensagens de erro mais concisas e legíveis.

---

## Questão 4 – Parametrização, classes de equivalência e valores-limite

> **Enunciado:**  
> Escolha pelo menos duas regras do sistema de biblioteca e desenvolva testes parametrizados. Uma delas deverá obrigatoriamente estar relacionada à quantidade de exemplares.  
> Considere valores como -1, 0, 1 e 2 e identifique valores válidos, inválidos, valores-limite e classes de equivalência.  
> **Construa os testes utilizando @pytest.mark.parametrize(...) e explique o critério usado para selecionar os dados de teste.**

### Tabela de identificação

#### Regra 1: Quantidade de Exemplares

| Entrada |  Classe  |                Categoria                 | Resultado esperado |
| :-----: | :------: | :--------------------------------------: | :----------------: |
|  `-5`   | Inválida |              Valor negativo              |    `ValueError`    |
|  `-1`   | Inválida |   Valor-limite inferior fora da faixa    |    `ValueError`    |
|   `0`   |  Válida  | Valor-limite mínimo válido (sem estoque) |  Sucesso (`None`)  |
|   `1`   |  Válida  |  Valor-limite superior da borda mínima   |  Sucesso (`None`)  |
|   `2`   |  Válida  |          Valor típico positivo           |  Sucesso (`None`)  |
| `True`  | Inválida |              Tipo booleano               |    `ValueError`    |
|  `"2"`  | Inválida |                Tipo texto                |    `ValueError`    |

#### Regra 2: Validação de ISBN

|  Entrada   |  Classe  |             Categoria             | Resultado esperado |
| :--------: | :------: | :-------------------------------: | :----------------: |
| `"97800"`  |  Válida  | Valor-limite inferior prefixo 978 |  Sucesso (`None`)  |
| `"97801"`  |  Válida  |        Valor válido padrão        |  Sucesso (`None`)  |
| `"97900"`  |  Válida  | Valor-limite inferior prefixo 979 |  Sucesso (`None`)  |
| `"97999"`  |  Válida  | Valor-limite superior prefixo 979 |  Sucesso (`None`)  |
|  `"9781"`  | Inválida |    Tamanho menor que 5 dígitos    |    `ValueError`    |
| `"978001"` | Inválida |    Tamanho maior que 5 dígitos    |    `ValueError`    |
| `"97701"`  | Inválida |       Prefixo fora da faixa       |    `ValueError`    |
| `"978ab"`  | Inválida |     Caracteres não numéricos      |    `ValueError`    |
|  `12345`   | Inválida |           Tipo inteiro            |    `ValueError`    |

### Código dos testes (`tests/test_validators.py`)

```python
import pytest
from biblioteca.validators import validar_isbn, validar_quantidade_disponivel

@pytest.mark.parametrize("quantidade", [0, 1, 2])
def test_quantidade_exemplares_valida_parametrizado(quantidade):
    assert validar_quantidade_disponivel(quantidade) is None

@pytest.mark.parametrize("quantidade_invalida", [-1, -5, True, "2"])
def test_quantidade_exemplares_invalida_parametrizado(quantidade_invalida):
    with pytest.raises(ValueError):
        validar_quantidade_disponivel(quantidade_invalida)

@pytest.mark.parametrize("isbn_valido", ["97800", "97801", "97900", "97999"])
def test_isbn_valido_parametrizado(isbn_valido):
    assert validar_isbn(isbn_valido) is None

@pytest.mark.parametrize("isbn_invalido", ["9781", "978001", "97701", "98000", "978ab", 12345])
def test_isbn_invalido_parametrizado(isbn_invalido):
    with pytest.raises(ValueError):
        validar_isbn(isbn_invalido)
```

### Critério usado para selecionar os dados de teste

Utilizou-se o particionamento em classes de equivalência (entradas válidas e inválidas quanto a tipo, valor e formato) combinado com a análise de valores-limite nas fronteiras de decisão (fronteira entre `-1` inválido e `0` válido; e bordas de prefixo e tamanho do ISBN).

---

## Questão 5 – Testando exceções

> **Enunciado:**  
> Implemente regras no sistema que produzam exceções em situações inválidas e teste os cenários a seguir:
>
> - cadastro com dados inválidos;
> - cadastro duplicado de livro;
> - empréstimo de livro inexistente;
> - empréstimo quando a quantidade disponível for zero;
> - devolução de livro inexistente.
>
> **Utilize pytest.raises() e escolha pelo menos um cenário para implementar também com assertRaises(). Explique por que receber a exceção esperada representa sucesso do teste.**

### Código com `pytest.raises()` (`tests/test_biblioteca.py`)

```python
def test_cadastrar_livro_com_dados_invalidos():
    biblioteca = Biblioteca()
    livro_invalido = Livro("12345", "Clean Code", "Robert C. Martin", 3)
    with pytest.raises(ValueError):
        biblioteca.cadastrar(livro_invalido)

def test_cadastrar_livro_ja_cadastrado():
    biblioteca = Biblioteca()
    livro1 = Livro("97801", "Clean Code", "Robert C. Martin", 3)
    livro2 = Livro("97801", "Clean Code Nova Edicao", "Robert C. Martin", 2)
    biblioteca.cadastrar(livro1)
    with pytest.raises(ValueError) as exc_info:
        biblioteca.cadastrar(livro2)
    assert "Livro com ISBN 97801 já cadastrado." in str(exc_info.value)

def test_emprestar_livro_inexistente():
    biblioteca = Biblioteca()
    with pytest.raises(ValueError) as exc_info:
        biblioteca.emprestar("97899")
    assert "Livro com ISBN 97899 não encontrado." in str(exc_info.value)

def test_emprestar_livro_sem_estoque():
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 0)
    biblioteca.cadastrar(livro)
    assert biblioteca.emprestar("97801") is False

def test_devolver_livro_inexistente():
    biblioteca = Biblioteca()
    with pytest.raises(ValueError) as exc_info:
        biblioteca.devolver("97899")
    assert "Livro com ISBN 97899 não encontrado." in str(exc_info.value)
```

### Código com `assertRaises()` (`tests/test_livro.py`)

```python
def test_devolucao_livro_inexistente_assertRaises(self):
    from biblioteca.biblioteca import Biblioteca
    biblioteca = Biblioteca()
    with self.assertRaises(ValueError):
        biblioteca.devolver("97899")
```

### Por que receber a exceção esperada representa sucesso do teste?

Porque em testes negativos o objetivo é certificar que o sistema impede operações ilegais e protege o estado interno. O lançamento da exceção correta comprova que a regra de proteção foi acionada com sucesso.

---

## Questão 6 – Utilização de fixtures

> **Enunciado:**  
> Crie pelo menos duas fixtures para o sistema de biblioteca e reutilize cada uma em diferentes testes.
>
> - possíveis fixtures: livro, livro_disponivel, livro_indisponivel, biblioteca ou repositorio;
> - mostre o código de cada fixture;
> - utilize cada fixture em pelo menos dois testes;
> - explique qual repetição de código foi eliminada.

### Código de cada fixture (`tests/conftest.py`)

```python
import pytest
from biblioteca.livro import Livro

@pytest.fixture
def livro_disponivel():
    return Livro("97801", "Clean Code", "Robert C. Martin", 3)

@pytest.fixture
def livro_indisponivel():
    return Livro("97802", "Refactoring", "Martin Fowler", 0)
```

### Utilização em pelo menos dois testes cada

#### Utilização da fixture `livro_disponivel`

```python
# Em tests/test_livro.py
def test_emprestimo_com_sucesso_com_fixture(livro_disponivel):
    assert livro_disponivel.emprestar() is True
    assert livro_disponivel.quantidade_disponivel == 2

# Em tests/test_biblioteca.py
def test_cadastro_livro_com_fixture(livro_disponivel):
    biblioteca = Biblioteca()
    biblioteca.cadastrar(livro_disponivel)
    assert biblioteca.buscar(livro_disponivel.isbn) is not None
```

#### Utilização da fixture `livro_indisponivel`

```python
# Em tests/test_livro.py
def test_emprestimo_sem_exemplares_com_fixture(livro_indisponivel):
    assert livro_indisponivel.emprestar() is False
    assert livro_indisponivel.quantidade_disponivel == 0

# Em tests/test_biblioteca.py
def test_emprestar_livro_sem_estoque_com_fixture(livro_indisponivel):
    biblioteca = Biblioteca()
    biblioteca.cadastrar(livro_indisponivel)
    assert biblioteca.emprestar(livro_indisponivel.isbn) is False
```

### Qual repetição de código foi eliminada

Eliminou-se a instanciação repetitiva de objetos `Livro` com dados literais idênticos na fase de Arrange de cada teste, centralizando a criação dos dados de teste em um único ponto.

---

## Questão 7 – Isolamento de dependências com Mock/Patch

> **Enunciado:**  
> Identifique uma dependência existente no Mini Sistema de Biblioteca e utilize Mock ou patch para isolá-la. A dependência pode ser um repositório, uma consulta, a persistência ou outra classe.
>
> - configure pelo menos um return_value;
> - verifique que determinado método foi chamado;
> - utilize, quando adequado, assert_called_once() ou assert_called_once_with(...);
> - explique por que o teste continua sendo unitário mesmo quando o código original possui dependências.

### Código desenvolvido (`tests/test_biblioteca.py`)

```python
from unittest.mock import Mock
from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro

def test_consulta_livro_existente_com_mock():
    # Arrange
    mock_repository = Mock()
    livro_esperado = Livro("97801", "Clean Code", "Robert C. Martin", 3)
    mock_repository.buscar.return_value = livro_esperado
    biblioteca = Biblioteca(repository=mock_repository)

    # Act
    resultado = biblioteca.buscar("97801")

    # Assert
    assert resultado == livro_esperado
    mock_repository.buscar.assert_called_once_with("97801")

def test_emprestimo_com_mock():
    # Arrange
    mock_repository = Mock()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 2)
    mock_repository.buscar.return_value = livro
    biblioteca = Biblioteca(repository=mock_repository)

    # Act
    sucesso = biblioteca.emprestar("97801")

    # Assert
    assert sucesso is True
    assert livro.quantidade_disponivel == 1
    mock_repository.buscar.assert_called_once_with("97801")
    mock_repository.atualizar.assert_called_once_with(livro)
```

### Por que o teste continua sendo unitário mesmo quando o código possui dependências?

Porque a dependência real (`LivroRepository` e o banco de dados) foi substituída por um dublê de teste (`Mock`). Apenas o código da classe `Biblioteca` é executado, testando sua lógica de orquestração de forma totalmente isolada de camadas externas.

---

## Questão 8 – Comportamentos diferentes da dependência

> **Enunciado:**  
> Utilize side_effect ou mecanismo equivalente para testar pelo menos dois comportamentos diferentes de uma dependência do Mini Sistema de Biblioteca. Um deverá representar uma situação normal e outro uma situação de falha.
>
> - indique qual dependência foi simulada;
> - explique por que foi utilizada uma simulação;
> - informe o resultado esperado para cada cenário.

### 1. Dependência simulada

O método `atualizar` e `buscar` de `LivroRepository`.

### 2. Por que foi utilizada uma simulação?

Para reproduzir falhas de infraestrutura (como erro de conexão com o banco) e retornos dinâmicos sem depender do banco de dados real.

### 3. Código desenvolvido e resultado esperado (`tests/test_biblioteca.py`)

#### Cenário Normal

```python
def test_emprestimo_com_side_effect_sucesso():
    # Arrange
    mock_repository = Mock()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 2)
    mock_repository.buscar.side_effect = [livro]
    biblioteca = Biblioteca(repository=mock_repository)

    # Act
    resultado = biblioteca.emprestar("97801")

    # Assert
    assert resultado is True
    assert livro.quantidade_disponivel == 1
    mock_repository.buscar.assert_called_once_with("97801")
    mock_repository.atualizar.assert_called_once_with(livro)
```

- **Resultado esperado:** O empréstimo retorna `True`, a quantidade do livro é decrementada para 1 e o método `atualizar` é chamado uma vez com o livro alterado.

#### Cenário de Falha

```python
def test_emprestimo_com_side_effect_falha_banco():
    # Arrange
    mock_repository = Mock()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 2)
    mock_repository.buscar.return_value = livro
    mock_repository.atualizar.side_effect = RuntimeError("Falha de conexão com o banco de dados")
    biblioteca = Biblioteca(repository=mock_repository)

    # Act & Assert
    with pytest.raises(RuntimeError) as exc_info:
        biblioteca.emprestar("97801")

    assert "Falha de conexão com o banco de dados" in str(exc_info.value)
    mock_repository.buscar.assert_called_once_with("97801")
    mock_repository.atualizar.assert_called_once_with(livro)
```

- **Resultado esperado:** A chamada lança a exceção `RuntimeError` contendo a mensagem de falha de conexão, interrompendo a operação.

---

## Questão 9 – Primeiro teste de integração

> **Enunciado:**  
> Crie um teste de integração para o fluxo abaixo:
>
> - cadastrar um livro;
> - pesquisar o livro cadastrado;
> - confirmar que existem exemplares disponíveis;
> - realizar o empréstimo;
> - consultar novamente o livro;
> - confirmar que a quantidade disponível foi reduzida.
>
> **Não utilize mocks nesse teste. Todos os componentes envolvidos no fluxo deverão ser reais.**

### Código desenvolvido (`tests/test_integracao.py`)

```python
def test_fluxo_integracao_emprestimo():
    # Arrange: componentes reais
    database = Database(":memory:")
    repository = LivroRepository(database=database)
    biblioteca = Biblioteca(repository=repository)
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)

    # Act: cadastrar um livro
    biblioteca.cadastrar(livro)

    # Assert: pesquisar e confirmar exemplares disponíveis
    livro_pesquisado = biblioteca.buscar("97801")
    assert livro_pesquisado is not None
    assert livro_pesquisado.quantidade_disponivel == 3
    assert biblioteca.verificar_quantidade_disponivel("97801") > 0

    # Act: realizar o empréstimo
    resultado_emprestimo = biblioteca.emprestar("97801")

    # Assert: consultar novamente e confirmar redução
    assert resultado_emprestimo is True
    livro_atualizado = biblioteca.buscar("97801")
    assert livro_atualizado is not None
    assert livro_atualizado.quantidade_disponivel == 2
```

---

## Questão 10 – Integração do fluxo completo

> **Enunciado:**  
> Implemente e teste o fluxo completo: cadastrar livro → consultar livro → realizar empréstimo → consultar novamente → realizar devolução → consultar novamente.
>
> - verifique que o livro é cadastrado corretamente;
> - verifique que o livro pode ser encontrado;
> - confirme que o número de exemplares diminui após o empréstimo;
> - confirme que o número de exemplares aumenta após a devolução;
> - verifique que o estado final corresponde ao esperado;
> - explique quais componentes estão sendo integrados.

### Código desenvolvido (`tests/test_integracao.py`)

```python
def test_fluxo_completo_cadastro_consulta_emprestimo_devolucao():
    # Arrange
    database = Database(":memory:")
    repository = LivroRepository(database=database)
    biblioteca = Biblioteca(repository=repository)
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)

    # Cadastrar livro e verificar que foi cadastrado e encontrado
    biblioteca.cadastrar(livro)
    livro_encontrado = biblioteca.buscar("97801")
    assert livro_encontrado is not None
    assert livro_encontrado.isbn == "97801"
    assert livro_encontrado.quantidade_disponivel == 3

    # Realizar empréstimo e confirmar que diminui
    assert biblioteca.emprestar("97801") is True
    livro_pos_emprestimo = biblioteca.buscar("97801")
    assert livro_pos_emprestimo.quantidade_disponivel == 2

    # Realizar devolução e confirmar que aumenta e estado final corresponde ao esperado
    biblioteca.devolver("97801")
    livro_pos_devolucao = biblioteca.buscar("97801")
    assert livro_pos_devolucao is not None
    assert livro_pos_devolucao.quantidade_disponivel == 3
    assert livro_pos_devolucao.titulo == "Clean Code"
    assert livro_pos_devolucao.autor == "Robert C. Martin"
```

### Componentes que estão sendo integrados

Estão integrados a fachada de aplicação (`Biblioteca`), a camada de regras de acesso (`LivroRepository`), a camada de persistência com banco relacional SQLite (`Database`) e o modelo de domínio com suas operações de negócio (`Livro`).

---

## Questão 11 – Teste de integração com persistência

> **Enunciado:**  
> Implemente uma forma simples de persistência utilizando SQLite e um repositório responsável por armazenar livros:
>
> - inicialize o banco de testes;
> - cadastre um livro;
> - persista o livro;
> - realize uma nova consulta ao banco;
> - recupere o livro;
> - compare os dados recuperados com os dados cadastrados.

### Código desenvolvido (`tests/test_repository.py`)

```python
def test_persistencia_livro_com_sqlite_e_repositorio():
    # Arrange: inicializa banco em memória (:memory:) e repositório
    database = Database(":memory:")
    repositorio = LivroRepository(database=database)
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)

    # Act: cadastra e persiste o livro
    repositorio.cadastrar(livro)

    # Act: realiza uma nova consulta diretamente ao banco e recupera o livro
    livro_recuperado = database.buscar("97801")

    # Assert: compara os dados recuperados com os cadastrados
    assert livro_recuperado is not None
    assert livro_recuperado.isbn == livro.isbn
    assert livro_recuperado.titulo == livro.titulo
    assert livro_recuperado.autor == livro.autor
    assert livro_recuperado.quantidade_disponivel == livro.quantidade_disponivel

    database.fechar()
```

---

## Questão 12 – Fixture para testes de integração

> **Enunciado:**  
> Crie uma fixture responsável por preparar o ambiente dos testes de integração. Ela poderá criar o banco, criar tabelas, criar o repositório ou cadastrar dados iniciais:
>
> - utilize a fixture em pelo menos dois testes de integração;
> - explique a função do setup;
> - explique a execução do teste;
> - explique a função do teardown.

### Código da fixture (`tests/test_integracao.py`)

```python
@pytest.fixture
def ambiente_integrado():
    # Setup
    database = Database(":memory:")
    repository = LivroRepository(database=database)
    biblioteca = Biblioteca(repository=repository)

    yield biblioteca

    # Teardown
    database.fechar()
```

### Utilização em pelo menos dois testes de integração

```python
def test_fluxo_integracao_emprestimo_com_fixture(ambiente_integrado):
    biblioteca = ambiente_integrado
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)
    biblioteca.cadastrar(livro)
    assert biblioteca.emprestar("97801") is True
    assert biblioteca.verificar_quantidade_disponivel("97801") == 2

def test_fluxo_completo_cadastro_consulta_emprestimo_devolucao_com_fixture(ambiente_integrado):
    biblioteca = ambiente_integrado
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)
    biblioteca.cadastrar(livro)
    biblioteca.emprestar("97801")
    biblioteca.devolver("97801")
    assert biblioteca.verificar_quantidade_disponivel("97801") == 3
```

### Explicação do setup, execução e teardown

- **Setup (antes do `yield`):** Instancia o banco SQLite `:memory:`, cria as tabelas DDL, instancia o repositório e injeta na `Biblioteca`, preparando o ambiente isolado.
- **Execução do teste (no `yield`):** O pytest entrega a instância de `Biblioteca` pronta para o teste executar suas ações e asserções.
- **Teardown (após o `yield`):** Executa `database.fechar()`, fechando a conexão com o banco e liberando os recursos após a conclusão do teste.

---

## Questão 13 – Investigação de falhas

> **Enunciado:**  
> Escolha uma funcionalidade do Mini Sistema de Biblioteca e introduza propositalmente um erro. Execute novamente os testes e documente a investigação:
>
> - erro introduzido;
> - teste que detectou o problema;
> - mensagem apresentada pelo framework;
> - interpretação da falha;
> - correção realizada.

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

## Questão 14 – Cobertura de testes

> **Enunciado:**  
> Execute uma ferramenta de cobertura sobre o Mini Sistema de Biblioteca. Utilize o nome correspondente ao pacote criado por você:
>
> - apresente o percentual de cobertura obtido;
> - identifique módulos com menor cobertura;
> - identifique linhas ou comportamentos importantes ainda não testados;
> - crie pelo menos um novo teste após analisar o relatório;
> - execute novamente a cobertura e compare os resultados;
> - responda por que uma cobertura elevada, isoladamente, não garante a qualidade dos testes.

### 1. Percentual de cobertura obtido inicialmente

88% de cobertura total sobre o pacote `biblioteca`.

### 2. Módulos com menor cobertura

- `biblioteca/database.py`: 73%
- `biblioteca/livro.py`: 88%
- `biblioteca/repository.py`: 90%

### 3. Linhas ou comportamentos importantes ainda não testados

- `database.py`: linhas 56-61 (remoção no banco) e 67, 70 (context manager `__enter__` e `__exit__`);
- `repository.py`: linha 26 (exceção ao atualizar livro inexistente) e 30 (remoção no repositório);
- `biblioteca.py`: linha 21 (método `remover`);
- `livro.py`: linhas 15 (`__str__`) e 27 (`info()`);
- `validators.py`: linha 31 (exceção se argumento de `validar_livro` não for instância de `Livro`).

### 4. Novos testes criados após analisar o relatório

- `test_remover_livro` em `tests/test_biblioteca.py`;
- `test_remover_persistencia_livro`, `test_atualizar_livro_inexistente_repositorio`, `test_database_context_manager` e `test_database_remover_inexistente` em `tests/test_repository.py`;
- `test_validar_livro_objeto_invalido` em `tests/test_validators.py`;
- `test_livro_str` e `test_livro_info` em `tests/test_livro.py`.

### 5. Reexecução da cobertura e comparação dos resultados

```text
Name                          Stmts   Miss  Cover   Missing
-----------------------------------------------------------
biblioteca/biblioteca.py         29      0   100%
biblioteca/database.py           30      0   100%
biblioteca/livro.py              17      0   100%
biblioteca/livro_com_bug.py       4      1    75%   6
biblioteca/repository.py         21      0   100%
biblioteca/validators.py         23      0   100%
-----------------------------------------------------------
TOTAL                           124      1    99%
```

**Comparação:** A cobertura subiu de **88%** para **99%**, com 100% de cobertura em todos os módulos de produção da biblioteca.

### 6. Por que uma cobertura elevada, isoladamente, não garante a qualidade dos testes?

Porque a cobertura afere somente quais linhas de código foram executadas pelo interpretador, e não a qualidade ou suficiência das asserções (`assert`). Um teste pode executar 100% das linhas sem conter asserções válidas, deixando passar erros lógicos graves. Além disso, a métrica não detecta regras de negócio ausentes no código.

---

## Questão Final de Síntese

> **Enunciado:**  
> Explique, utilizando exemplos do Mini Sistema de Biblioteca desenvolvido por você, a diferença entre um teste unitário e um teste de integração.  
> Na resposta, indique:
>
> - qual componente foi testado isoladamente;
> - quais dependências foram substituídas ou controladas;
> - quais componentes foram utilizados de forma real no teste de integração;
> - qual tipo de defeito cada categoria de teste poderia identificar.

### 1. Qual componente foi testado isoladamente

No teste unitário de `test_emprestimo_com_mock`, apenas a classe `Biblioteca` foi testada isoladamente.

### 2. Quais dependências foram substituídas ou controladas

A dependência `LivroRepository` foi substituída por um dublê `Mock()`, com o método `buscar` controlado via `return_value` e chamadas verificadas com `assert_called_once_with`. O banco de dados SQLite real não foi utilizado.

### 3. Quais componentes foram utilizados de forma real no teste de integração

No teste de integração (`test_fluxo_completo_cadastro_consulta_emprestimo_devolucao`), foram utilizados de forma real:

- a classe `Biblioteca`;
- a classe `LivroRepository`;
- a classe `Database`;
- a conexão e tabelas reais do SQLite em memória (`:memory:`);
- a entidade `Livro`.

### 4. Qual tipo de defeito cada categoria de teste poderia identificar

- **Teste Unitário:** Identifica erros na lógica interna do componente ou falha de protocolo de comunicação, como esquecer de decrementar a quantidade em `Livro.emprestar()` ou não chamar o método `atualizar()` do repositório.
- **Teste de Integração:** Identifica defeitos de compatibilidade entre camadas e infraestrutura real, como erros de sintaxe SQL no SQLite (`CREATE TABLE`, `INSERT`, `ON CONFLICT`), incompatibilidade de tipos de colunas, falhas de constraints relacionais (`CHECK (quantidade_disponivel >= 0)`) ou erros na conversão de registros do banco para objetos `Livro`.
