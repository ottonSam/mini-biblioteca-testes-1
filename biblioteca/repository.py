from typing import Optional

from .database import Database
from .livro import Livro
from .validators import validar_livro


class LivroRepository:
    """Valida e gerencia os livros armazenados no Database."""

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
