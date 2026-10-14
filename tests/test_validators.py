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
