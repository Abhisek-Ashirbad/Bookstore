from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange

app = FastAPI()

class Book(BaseModel):
    title: str
    author: str
    desc: Optional[str] = "Not Available!"

my_books = [{"title": "Midnight's Children", "author": "Salman Rushdie", "id": 1}, \
            {"title": "A piece of peace", "author": "Anamaa", "id": 2}]

def get_book(id):
    for b in my_books:
        if b['id'] == id:
            return b


@app.get("/")
async def root():
    return {"msg": "Hello World!"}

@app.get("/books")
async def get_books():
    return {"data": my_books}

@app.get("/books/{id}")
async def get_book(id):
    book = get_book(id)
    return {"Book detail": book}

@app.post("/books")
def create_books(book: Book):
    print("New book created.")
    book_dict = book.dict()
    book_dict['id'] = randrange(0, 1000000)
    my_books.append(book_dict)
    return {"New book": book_dict}


