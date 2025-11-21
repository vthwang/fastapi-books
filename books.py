from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/books")
def get_books():
    return {"message": "Books!"}

@app.get("/books/{book_id}")
def get_book(book_id: int):
    return {"message": f"Book {book_id}"}
