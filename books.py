from fastapi import Body, FastAPI

app = FastAPI()

BOOKS = [
    {
        "id": 1,
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "category": "Classics",
    },
    {"id": 2, "title": "1984", "author": "George Orwell", "category": "Dystopian"},
    {
        "id": 3,
        "title": "Don't Look Up",
        "author": "Adam McKay",
        "category": "Science Fiction",
    },
    {
        "id": 4,
        "title": "The Catcher in the Rye",
        "author": "J.D. Salinger",
        "category": "Classics",
    },
    {
        "id": 5,
        "title": "The Lord of the Rings",
        "author": "J.R.R. Tolkien",
        "category": "Fantasy",
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


@app.get("/books/")
def read_books_by_category(category: str):
    books_to_return = []
    for book in BOOKS:
        if book.get("category").casefold() == category.casefold():
            books_to_return.append(book)
    return books_to_return


@app.get("/books/{book_author}/")
def read_author_category_by_query(book_author: str, category: str):
    books_to_return = []
    for book in BOOKS:
        if (
            book.get("author").casefold() == book_author.casefold()
            and book.get("category").casefold() == category.casefold()
        ):
            books_to_return.append(book)
    return books_to_return


@app.post("/books")
def create_book(new_book: dict = Body()):
    BOOKS.append(new_book)
    return new_book


@app.put("/books/{book_id}")
def update_book(book_id: int, updated_book: dict = Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == book_id:
            BOOKS[i] = updated_book
            return BOOKS[i]
    return {"message": "Book not found"}


@app.delete("/books/{book_id}")
def delete_book(book_id: int):
    for i in range(len(BOOKS)):
        if BOOKS[i].get("id") == book_id:
            BOOKS.pop(i)
            return {"message": "Book deleted successfully"}
    return {"message": "Book not found"}
