from fastapi import FastAPI

app = FastAPI()

BOOKS = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category": "Classics"
    },
    {
        "id": 2,
        "title": "1984",
        "author": "George Orwell",
        "category": "Dystopian"
    },
    {
        "id": 3,
        "title": "Don't Look Up",
        "author": "Adam McKay",
        "category": "Science Fiction"
    },
    {
        "id": 4,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "category": "Classics"
    },
    {
        "id": 5,
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "category": "Fantasy"
    },
]

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/books")
def read_all_books():
    return BOOKS

@app.get("/books/{book_title}")
def read_book(book_title: str):
    for book in BOOKS:
        if book.get("title").casefold() == book_title.casefold():
            return book
    return {"message": "Book not found"}
