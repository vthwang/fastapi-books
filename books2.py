from fastapi import FastAPI
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI()


class Book:
    id: int
    title: str
    author: str
    description: str
    rating: int

    def __init__(self, id, title, author, description, rating):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


class BookRequest(BaseModel):
    id: Optional[int] = None
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)


BOOKS = [
    Book(
        1,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "A classic novel about the American Dream",
        4.5,
    ),
    Book(
        2,
        "1984",
        "George Orwell",
        "A dystopian novel about a totalitarian society",
        4.0,
    ),
    Book(
        3,
        "Don't Look Up",
        "Adam McKay",
        "A science fiction novel about a comet that is heading towards Earth",
        3.5,
    ),
    Book(
        4,
        "The Catcher in the Rye",
        "J.D. Salinger",
        "A novel about a young man's journey of self-discovery",
        4.0,
    ),
    Book(
        5,
        "The Lord of the Rings",
        "J.R.R. Tolkien",
        "A fantasy novel about a journey to destroy a ring",
        5.0,
    ),
]


@app.get("/books")
def read_all_books():
    return BOOKS


@app.post("/books")
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book
