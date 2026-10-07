from typing import Optional

from .livro import Livro
from .repository import LivroRepository


class Biblioteca:
    def __init__(self, repository: Optional[LivroRepository] = None) -> None:
        self.repository = repository if repository is not None else LivroRepository()

    def buscar(self, isbn: str) -> Optional[Livro]:
        return self.repository.buscar(isbn)

    def cadastrar(self, livro: Livro) -> None:
        self.repository.cadastrar(livro)

    def remover(self, isbn: str) -> Livro:
        return self.repository.remover(isbn)

    def emprestar(self, isbn: str) -> bool:
        """Retorna False quando não há exemplares disponíveis."""
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
