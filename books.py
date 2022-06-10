from fastapi import FastAPI
from enum import Enum
from typing import Optional

app = FastAPI()

BOOKS = {
    "book_1": {"title": "Title One", "author": "Author One"},
    "book_2": {"title": "Title Two", "author": "Author Two"},
    "book_3": {"title": "Title Three", "author": "Author Three"},
    "book_4": {"title": "Title Four", "author": "Author Four"},
    "book_5": {"title": "Title Five", "author": "Author Five"}
}


class DirectionName(str, Enum):
    north = "North"
    south = "South"
    east = "East"
    west = "West"


@app.get('/')
async def read_all_books():
    return BOOKS


@app.get('/books/{book_id}/')
async def read_book(book_id: int):
    return {'book_title': book_id}


@app.get('/directions/{direction_name}')
async def get_direction(direction_name: DirectionName):
    if direction_name == DirectionName.north:
        return {'Direction': direction_name, "sub": "Up"}
    if direction_name == DirectionName.south:
        return {'Direction': direction_name, "sub": "Down"}
    if direction_name == DirectionName.east:
        return {'Direction': direction_name, "sub": "Right"}
    return {'Direction': direction_name, "sub": "Left  "}


@app.get("/{book_name}")
async def read_book(book_name: str):
    return BOOKS[book_name]


@app.get("/skip/")
async def skip_book(skip_book: str = "book_3"):
    new_books = BOOKS.copy()
    del new_books[skip_book]
    return new_books


@app.get("/skip_book/")
async def skip_book(skip_book: Optional[str] = None):
    if skip_book:
        new_books = BOOKS.copy()
        del new_books[skip_book]
        return new_books
    return BOOKS

