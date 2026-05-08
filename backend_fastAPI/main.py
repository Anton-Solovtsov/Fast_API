from fastapi import FastAPI

app = FastAPI()

Book = []


@app.get("/")
def get_books():
    return f'Любимая книга: {Book}'


@app.post("/book")
def create_book(book:str):
    Book.append(book)
    return book
