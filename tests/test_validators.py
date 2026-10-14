import pytest
from biblioteca.validators import (
    validar_isbn,
    validar_titulo,
    validar_autor,
    validar_quantidade_disponivel,
)


def test_isbn():
    # Arrange
    isbn_invalido = "12345"

    # Act
    with pytest.raises(ValueError) as exc_info:
        validar_isbn(isbn_invalido)

    # Assert
    assert "ISBN deve conter 5 dígitos e começar com 978 ou 979." in str(exc_info.value)


def test_titulo():
    # Arrange
    titulo_invalido = ""

    # Act
    with pytest.raises(ValueError) as exc_info:
        validar_titulo(titulo_invalido)

    # Assert
    assert "Título deve ser um texto não vazio." in str(exc_info.value)


def test_autor():
    # Arrange
    autor_invalido = ""

    # Act
    with pytest.raises(ValueError) as exc_info:
        validar_autor(autor_invalido)

    # Assert
    assert "Autor deve ser um texto não vazio." in str(exc_info.value)


def test_quantidade_exemplares():
    # Arrange
    quantidade_invalida = -1

    # Act
    with pytest.raises(ValueError) as exc_info:
        validar_quantidade_disponivel(quantidade_invalida)

    # Assert
    assert "Quantidade disponível deve ser um inteiro maior ou igual a zero." in str(exc_info.value)


@pytest.mark.parametrize("quantidade", [0, 1, 2])
def test_quantidade_exemplares_valida_parametrizado(quantidade):
    # Arrange
    qtd = quantidade

    # Act
    resultado = validar_quantidade_disponivel(qtd)

    # Assert
    assert resultado is None


@pytest.mark.parametrize("quantidade_invalida", [-1, -5, True, "2"])
def test_quantidade_exemplares_invalida_parametrizado(quantidade_invalida):
    # Arrange
    qtd = quantidade_invalida

    # Act
    with pytest.raises(ValueError) as exc_info:
        validar_quantidade_disponivel(qtd)

    # Assert
    assert "Quantidade disponível deve ser um inteiro maior ou igual a zero." in str(exc_info.value)


@pytest.mark.parametrize("isbn_valido", ["97800", "97801", "97900", "97999"])
def test_isbn_valido_parametrizado(isbn_valido):
    # Arrange
    isbn = isbn_valido

    # Act
    resultado = validar_isbn(isbn)

    # Assert
    assert resultado is None


@pytest.mark.parametrize(
    "isbn_invalido",
    [
        "9781",
        "978001",
        "97701",
        "98000",
        "978ab",
        12345,
    ],
)
def test_isbn_invalido_parametrizado(isbn_invalido):
    # Arrange
    isbn = isbn_invalido

    # Act
    with pytest.raises(ValueError) as exc_info:
        validar_isbn(isbn)

    # Assert
    assert isinstance(exc_info.value, ValueError)
