import pytest
from biblioteca.biblioteca import Biblioteca
from biblioteca.database import Database
from biblioteca.livro import Livro
from biblioteca.livro_com_bug import LivroComBug
from biblioteca.repository import LivroRepository


@pytest.fixture
def ambiente_integrado():
    # Setup
    database = Database(":memory:")
    repository = LivroRepository(database=database)
    biblioteca = Biblioteca(repository=repository)

    yield biblioteca

    # Teardown
    database.fechar()


def test_fluxo_integracao_emprestimo():
    # Arrange
    database = Database(":memory:")
    repository = LivroRepository(database=database)
    biblioteca = Biblioteca(repository=repository)
    livro = Livro(
        isbn="97801",
        titulo="Clean Code",
        autor="Robert C. Martin",
        quantidade_disponivel=3,
    )

    # Act: Cadastrar um livro
    biblioteca.cadastrar(livro)

    # Assert: Pesquisar o livro cadastrado e confirmar que existem exemplares disponíveis
    livro_pesquisado = biblioteca.buscar("97801")
    assert livro_pesquisado is not None
    assert livro_pesquisado.isbn == "97801"
    assert livro_pesquisado.titulo == "Clean Code"
    assert livro_pesquisado.quantidade_disponivel == 3
    assert biblioteca.verificar_quantidade_disponivel("97801") > 0

    # Act: Realizar o empréstimo
    resultado_emprestimo = biblioteca.emprestar("97801")

    # Assert: Consultar novamente o livro e confirmar que a quantidade disponível foi reduzida
    assert resultado_emprestimo is True
    livro_atualizado = biblioteca.buscar("97801")
    assert livro_atualizado is not None
    assert livro_atualizado.quantidade_disponivel == 2
    assert biblioteca.verificar_quantidade_disponivel("97801") == 2


def test_fluxo_integracao_emprestimo_com_fixture(ambiente_integrado):
    # Arrange
    biblioteca = ambiente_integrado
    livro = Livro(
        isbn="97801",
        titulo="Clean Code",
        autor="Robert C. Martin",
        quantidade_disponivel=3,
    )

    # Act: Cadastrar um livro
    biblioteca.cadastrar(livro)

    # Assert: Pesquisar o livro cadastrado e confirmar que existem exemplares disponíveis
    livro_pesquisado = biblioteca.buscar("97801")
    assert livro_pesquisado is not None
    assert livro_pesquisado.isbn == "97801"
    assert livro_pesquisado.titulo == "Clean Code"
    assert livro_pesquisado.quantidade_disponivel == 3
    assert biblioteca.verificar_quantidade_disponivel("97801") > 0

    # Act: Realizar o empréstimo
    resultado_emprestimo = biblioteca.emprestar("97801")

    # Assert: Consultar novamente o livro e confirmar que a quantidade disponível foi reduzida
    assert resultado_emprestimo is True
    livro_atualizado = biblioteca.buscar("97801")
    assert livro_atualizado is not None
    assert livro_atualizado.quantidade_disponivel == 2
    assert biblioteca.verificar_quantidade_disponivel("97801") == 2


def test_fluxo_completo_cadastro_consulta_emprestimo_devolucao():
    # Arrange
    database = Database(":memory:")
    repository = LivroRepository(database=database)
    biblioteca = Biblioteca(repository=repository)
    livro = Livro(
        isbn="97801",
        titulo="Clean Code",
        autor="Robert C. Martin",
        quantidade_disponivel=3,
    )

    # Act 1: Cadastrar livro
    biblioteca.cadastrar(livro)

    # Assert 1: Consultar livro e verificar que foi cadastrado e encontrado
    livro_encontrado = biblioteca.buscar("97801")
    assert livro_encontrado is not None
    assert livro_encontrado.isbn == "97801"
    assert livro_encontrado.titulo == "Clean Code"
    assert livro_encontrado.autor == "Robert C. Martin"
    assert livro_encontrado.quantidade_disponivel == 3

    # Act 2: Realizar empréstimo
    sucesso_emprestimo = biblioteca.emprestar("97801")

    # Assert 2: Consultar novamente e confirmar que o número de exemplares diminuiu
    assert sucesso_emprestimo is True
    livro_pos_emprestimo = biblioteca.buscar("97801")
    assert livro_pos_emprestimo is not None
    assert livro_pos_emprestimo.quantidade_disponivel == 2
    assert biblioteca.verificar_quantidade_disponivel("97801") == 2

    # Act 3: Realizar devolução
    biblioteca.devolver("97801")

    # Assert 3: Consultar novamente e confirmar que o número de exemplares aumentou e o estado final é o esperado
    livro_pos_devolucao = biblioteca.buscar("97801")
    assert livro_pos_devolucao is not None
    assert livro_pos_devolucao.quantidade_disponivel == 3
    assert biblioteca.verificar_quantidade_disponivel("97801") == 3
    assert livro_pos_devolucao.isbn == "97801"
    assert livro_pos_devolucao.titulo == "Clean Code"
    assert livro_pos_devolucao.autor == "Robert C. Martin"


def test_fluxo_completo_cadastro_consulta_emprestimo_devolucao_com_fixture(ambiente_integrado):
    # Arrange
    biblioteca = ambiente_integrado
    livro = Livro(
        isbn="97801",
        titulo="Clean Code",
        autor="Robert C. Martin",
        quantidade_disponivel=3,
    )

    # Act 1: Cadastrar livro
    biblioteca.cadastrar(livro)

    # Assert 1: Consultar livro e verificar que foi cadastrado e encontrado
    livro_encontrado = biblioteca.buscar("97801")
    assert livro_encontrado is not None
    assert livro_encontrado.isbn == "97801"
    assert livro_encontrado.titulo == "Clean Code"
    assert livro_encontrado.autor == "Robert C. Martin"
    assert livro_encontrado.quantidade_disponivel == 3

    # Act 2: Realizar empréstimo
    sucesso_emprestimo = biblioteca.emprestar("97801")

    # Assert 2: Consultar novamente e confirmar que o número de exemplares diminuiu
    assert sucesso_emprestimo is True
    livro_pos_emprestimo = biblioteca.buscar("97801")
    assert livro_pos_emprestimo is not None
    assert livro_pos_emprestimo.quantidade_disponivel == 2
    assert biblioteca.verificar_quantidade_disponivel("97801") == 2

    # Act 3: Realizar devolução
    biblioteca.devolver("97801")

    # Assert 3: Consultar novamente e confirmar que o número de exemplares aumentou e o estado final é o esperado
    livro_pos_devolucao = biblioteca.buscar("97801")
    assert livro_pos_devolucao is not None
    assert livro_pos_devolucao.quantidade_disponivel == 3
    assert biblioteca.verificar_quantidade_disponivel("97801") == 3
    assert livro_pos_devolucao.isbn == "97801"
    assert livro_pos_devolucao.titulo == "Clean Code"
    assert livro_pos_devolucao.autor == "Robert C. Martin"


class DatabaseLivroComBug(Database):
    def buscar(self, isbn: str):
        livro = super().buscar(isbn)
        if livro is None:
            return None
        return LivroComBug(livro.isbn, livro.titulo, livro.autor, livro.quantidade_disponivel)


def test_devolucao_livro_com_bug_integracao():
    # Arrange
    database = DatabaseLivroComBug(":memory:")
    repository = LivroRepository(database=database)
    biblioteca = Biblioteca(repository=repository)
    livro = LivroComBug(
        isbn="97801",
        titulo="Clean Code",
        autor="Robert C. Martin",
        quantidade_disponivel=1,
    )
    biblioteca.cadastrar(livro)

    # Act
    biblioteca.devolver("97801")

    # Assert
    livro_consultado = biblioteca.buscar("97801")
    assert livro_consultado is not None
    assert livro_consultado.quantidade_disponivel == 2

