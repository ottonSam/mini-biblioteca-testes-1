import re

from .livro import Livro


def validar_isbn(isbn: str) -> None:
    if not isinstance(isbn, str):
        raise ValueError("ISBN deve ser um texto.")

    if not re.fullmatch(r"97[89][0-9]{2}", isbn):
        raise ValueError("ISBN deve conter 5 dígitos e começar com 978 ou 979.")


def validar_titulo(titulo: str) -> None:
    if not isinstance(titulo, str) or not titulo.strip():
        raise ValueError("Título deve ser um texto não vazio.")


def validar_autor(autor: str) -> None:
    if not isinstance(autor, str) or not autor.strip():
        raise ValueError("Autor deve ser um texto não vazio.")


def validar_quantidade_disponivel(quantidade: int) -> None:
    if isinstance(quantidade, bool) or not isinstance(quantidade, int) or quantidade < 0:
        raise ValueError("Quantidade disponível deve ser um inteiro maior ou igual a zero.")


def validar_livro(livro: Livro) -> None:
    if not isinstance(livro, Livro):
        raise ValueError("É necessário informar uma instância de Livro.")
    validar_isbn(livro.isbn)
    validar_titulo(livro.titulo)
    validar_autor(livro.autor)
    validar_quantidade_disponivel(livro.quantidade_disponivel)
