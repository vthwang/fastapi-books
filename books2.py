from fastapi import FastAPI, Path, Query, HTTPException
from pydantic import BaseModel, Field
from typing import Optional
from starlette import status

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
    id: Optional[int] = Field(description="The ID of the book", default=None)
    title: str = Field(min_length=3)
    author: str = Field(min_length=1)
    description: str = Field(min_length=1, max_length=100)
    rating: int = Field(gt=0, lt=6)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "The Great Gatsby",
                    "author": "F. Scott Fitzgerald",
                    "description": "A classic novel about the American Dream",
                    "rating": 5,
                }
            ]
        }
    }


BOOKS = [
    Book(
        1,
        "The Great Gatsby",
        "F. Scott Fitzgerald",
        "A classic novel about the American Dream",
        4.0,
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
        3.0,
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


@app.get("/books", status_code=status.HTTP_200_OK)
def read_all_books():
    return BOOKS


@app.get("/books/{book_id}", status_code=status.HTTP_200_OK)
def read_book(book_id: int = Path(gt=0)):
    for book in BOOKS:
        if book.id == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")


@app.get("/books/", status_code=status.HTTP_200_OK)
def read_book_by_rating(rating: int = Query(gt=0, lt=6)):
    books_to_return = []
    for book in BOOKS:
        if book.rating == rating:
            books_to_return.append(book)
    return books_to_return


@app.post("/books", status_code=status.HTTP_201_CREATED)
def create_book(book_request: BookRequest):
    new_book = Book(**book_request.model_dump())
    BOOKS.append(find_book_id(new_book))
    return new_book


def find_book_id(book: Book):
    book.id = 1 if len(BOOKS) == 0 else BOOKS[-1].id + 1
    return book


@app.put("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_book(book_request: BookRequest, book_id: int = Path(gt=0)):
    book_to_update = False
    for book in BOOKS:
        if book.id == book_id:
            book_to_update = True
            book.title = book_request.title
            book.author = book_request.author
            book.description = book_request.description
            book.rating = book_request.rating
            return book
    if not book_to_update:
        raise HTTPException(status_code=404, detail="Book not found")


@app.delete("/books/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(book_id: int = Path(gt=0)):
    book_to_delete = False
    for i in range(len(BOOKS)):
        if BOOKS[i].id == book_id:
            book_to_delete = True
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    if not book_to_delete:
        raise HTTPException(status_code=404, detail="Book not found")
