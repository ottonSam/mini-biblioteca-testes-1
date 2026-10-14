from biblioteca.livro import Livro


def test_criacao_livro():
    # Arrange
    isbn = "97801"
    titulo = "Clean Code"
    autor = "Robert C. Martin"
    quantidade = 5

    # Act
    livro = Livro(isbn, titulo, autor, quantidade)

    # Assert
    assert livro.isbn == "97801"
    assert livro.titulo == "Clean Code"
    assert livro.autor == "Robert C. Martin"
    assert livro.quantidade_disponivel == 5
