from unittest.mock import Mock, patch
import pytest
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


def test_cadastro_livro_com_fixture(livro_disponivel):
    # Arrange
    biblioteca = Biblioteca()
    livro = livro_disponivel

    # Act
    biblioteca.cadastrar(livro)

    # Assert
    livro_salvo = biblioteca.buscar(livro.isbn)
    assert livro_salvo is not None
    assert livro_salvo.isbn == livro.isbn
    assert livro_salvo.titulo == livro.titulo


def test_cadastro_livro_com_mock():
    # Arrange
    mock_repository = Mock()
    biblioteca = Biblioteca(repository=mock_repository)
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)

    # Act
    biblioteca.cadastrar(livro)

    # Assert
    mock_repository.cadastrar.assert_called_once_with(livro)


def test_cadastrar_livro_ja_cadastrado():
    # Arrange
    biblioteca = Biblioteca()
    livro1 = Livro("97801", "Clean Code", "Robert C. Martin", 3)
    livro2 = Livro("97801", "Clean Code Nova Edicao", "Robert C. Martin", 2)
    biblioteca.cadastrar(livro1)

    # Act
    with pytest.raises(ValueError) as exc_info:
        biblioteca.cadastrar(livro2)

    # Assert
    assert "Livro com ISBN 97801 já cadastrado." in str(exc_info.value)


def test_cadastrar_livro_com_dados_invalidos():
    # Arrange
    biblioteca = Biblioteca()
    livro_invalido = Livro("12345", "Clean Code", "Robert C. Martin", 3)

    # Act
    with pytest.raises(ValueError) as exc_info:
        biblioteca.cadastrar(livro_invalido)

    # Assert
    assert "ISBN deve conter 5 dígitos e começar com 978 ou 979." in str(exc_info.value)


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


def test_consulta_livro_inexistente():
    # Arrange
    biblioteca = Biblioteca()

    # Act
    resultado = biblioteca.buscar("97899")

    # Assert
    assert resultado is None


def test_disponibilidade_livro():
    # Arrange
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 4)
    biblioteca.cadastrar(livro)

    # Act
    quantidade = biblioteca.verificar_quantidade_disponivel("97801")

    # Assert
    assert quantidade == 4


def test_disponibilidade_livro_inexistente():
    # Arrange
    biblioteca = Biblioteca()

    # Act
    with pytest.raises(ValueError) as exc_info:
        biblioteca.verificar_quantidade_disponivel("97899")

    # Assert
    assert "Livro com ISBN 97899 não encontrado." in str(exc_info.value)


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


def test_emprestar_livro_sem_estoque():
    # Arrange
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 0)
    biblioteca.cadastrar(livro)

    # Act
    sucesso = biblioteca.emprestar("97801")

    # Assert
    assert sucesso is False
    assert biblioteca.verificar_quantidade_disponivel("97801") == 0


def test_emprestar_livro_sem_estoque_com_fixture(livro_indisponivel):
    # Arrange
    biblioteca = Biblioteca()
    livro = livro_indisponivel
    biblioteca.cadastrar(livro)

    # Act
    sucesso = biblioteca.emprestar(livro.isbn)

    # Assert
    assert sucesso is False
    assert biblioteca.verificar_quantidade_disponivel(livro.isbn) == 0


def test_emprestar_livro_inexistente():
    # Arrange
    biblioteca = Biblioteca()

    # Act
    with pytest.raises(ValueError) as exc_info:
        biblioteca.emprestar("97899")

    # Assert
    assert "Livro com ISBN 97899 não encontrado." in str(exc_info.value)


def test_devolucao():
    # Arrange
    biblioteca = Biblioteca()
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 1)
    biblioteca.cadastrar(livro)

    # Act
    biblioteca.devolver("97801")

    # Assert
    assert biblioteca.verificar_quantidade_disponivel("97801") == 2


def test_devolver_livro_inexistente():
    # Arrange
    biblioteca = Biblioteca()

    # Act
    with pytest.raises(ValueError) as exc_info:
        biblioteca.devolver("97899")

    # Assert
    assert "Livro com ISBN 97899 não encontrado." in str(exc_info.value)
