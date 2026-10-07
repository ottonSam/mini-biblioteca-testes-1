import sqlite3
from typing import Optional

from .livro import Livro


class Database:
    """Usa SQLite em memória ou em um arquivo informado no construtor."""

    def __init__(self, caminho: str = ":memory:") -> None:
        self.connection = sqlite3.connect(caminho)
        self.connection.row_factory = sqlite3.Row
        with self.connection:
            self.connection.execute(
                """
                CREATE TABLE IF NOT EXISTS livros (
                    isbn TEXT PRIMARY KEY NOT NULL,
                    titulo TEXT NOT NULL,
                    autor TEXT NOT NULL,
                    quantidade_disponivel INTEGER NOT NULL
                        CHECK (quantidade_disponivel >= 0)
                )
                """
            )

    def buscar(self, isbn: str) -> Optional[Livro]:
        registro = self.connection.execute(
            "SELECT isbn, titulo, autor, quantidade_disponivel FROM livros WHERE isbn = ?",
            (isbn,),
        ).fetchone()
        if registro is None:
            return None
        return Livro(
            registro["isbn"],
            registro["titulo"],
            registro["autor"],
            registro["quantidade_disponivel"],
        )

    def salvar(self, livro: Livro) -> None:
        """Insere ou atualiza um livro e confirma a gravação."""
        with self.connection:
            self.connection.execute(
                """
                INSERT INTO livros (isbn, titulo, autor, quantidade_disponivel)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(isbn) DO UPDATE SET
                    titulo = excluded.titulo,
                    autor = excluded.autor,
                    quantidade_disponivel = excluded.quantidade_disponivel
                """,
                (livro.isbn, livro.titulo, livro.autor, livro.quantidade_disponivel),
            )

    def remover(self, isbn: str) -> Livro:
        livro = self.buscar(isbn)
        if livro is None:
            raise ValueError(f"Livro com ISBN {isbn} não encontrado.")
        with self.connection:
            self.connection.execute("DELETE FROM livros WHERE isbn = ?", (isbn,))
        return livro

    def fechar(self) -> None:
        self.connection.close()

    def __enter__(self) -> "Database":
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.fechar()
