class Livro:
    def __init__(
        self,
        isbn: str,
        titulo: str,
        autor: str,
        quantidade_disponivel: int,
    ) -> None:
        self.isbn = isbn
        self.titulo = titulo
        self.autor = autor
        self.quantidade_disponivel = quantidade_disponivel

    def __str__(self) -> str:
        return f"ISBN: {self.isbn}, Título: {self.titulo}, Autor: {self.autor}, Quantidade Disponível: {self.quantidade_disponivel}"

    def emprestar(self) -> bool:
        if self.quantidade_disponivel > 0:
            self.quantidade_disponivel -= 1
            return True
        return False

    def devolver(self) -> None:
        self.quantidade_disponivel += 1

    def info(self) -> dict:
        return {
            "isbn": self.isbn,
            "titulo": self.titulo,
            "autor": self.autor,
            "quantidade_disponivel": self.quantidade_disponivel
        }