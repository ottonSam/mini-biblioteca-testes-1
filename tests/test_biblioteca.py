from biblioteca.biblioteca import Biblioteca
from biblioteca.livro import Livro


def test_cadastro_livro():
    # Arrange
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)

    # Act
    biblioteca.cadastrar(livro)

    # Assert
    livro_salvo = biblioteca.buscar("97801")
    assert livro_salvo is not None
    assert livro_salvo.isbn == "97801"
    assert livro_salvo.titulo == "Clean Code"


def test_consulta_livro_existente():
    # Arrange
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)
    biblioteca.cadastrar(livro)

    # Act
    resultado = biblioteca.buscar("97801")

    # Assert
    assert resultado is not None
    assert resultado.isbn == "97801"
    assert resultado.titulo == "Clean Code"


def test_disponibilidade_livro():
    # Arrange
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 4)
    biblioteca.cadastrar(livro)

    # Act
    quantidade = biblioteca.verificar_quantidade_disponivel("97801")

    # Assert
    assert quantidade == 4


def test_emprestimo():
    # Arrange
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 2)
    biblioteca.cadastrar(livro)

    # Act
    sucesso = biblioteca.emprestar("97801")

    # Assert
    assert sucesso is True
    assert biblioteca.verificar_quantidade_disponivel("97801") == 1


def test_devolucao():
    # Arrange
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 1)
    biblioteca.cadastrar(livro)

    # Act
    biblioteca.devolver("97801")

    # Assert
    assert biblioteca.verificar_quantidade_disponivel("97801") == 2
