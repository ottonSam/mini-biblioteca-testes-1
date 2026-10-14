from .livro import Livro


class LivroComBug(Livro):
    def devolver(self) -> None:
        self.quantidade_disponivel += 2
