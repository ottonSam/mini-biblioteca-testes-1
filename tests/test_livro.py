import unittest
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
    assert isinstance(livro, Livro)
    assert livro.isbn == "97801"
    assert livro.titulo == "Clean Code"
    assert livro.autor == "Robert C. Martin"
    assert livro.quantidade_disponivel == 5


def test_emprestimo_com_sucesso():
    # Arrange
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 3)

    # Act
    resultado = livro.emprestar()

    # Assert
    assert resultado is True
    assert livro.quantidade_disponivel == 2


def test_emprestimo_sem_exemplares():
    # Arrange
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 0)

    # Act
    resultado = livro.emprestar()

    # Assert
    assert resultado is False
    assert livro.quantidade_disponivel == 0


def test_devolucao_livro():
    # Arrange
    livro = Livro("97801", "Clean Code", "Robert C. Martin", 1)

    # Act
    livro.devolver()

    # Assert
    assert livro.quantidade_disponivel == 2


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


if __name__ == "__main__":
    unittest.main()
