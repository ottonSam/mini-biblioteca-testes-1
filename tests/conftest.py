import pytest
from biblioteca.livro import Livro


@pytest.fixture
def livro_disponivel():
    return Livro("97801", "Clean Code", "Robert C. Martin", 3)


@pytest.fixture
def livro_indisponivel():
    return Livro("97802", "Refactoring", "Martin Fowler", 0)
