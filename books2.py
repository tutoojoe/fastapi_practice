from typing import Optional
from fastapi import FastAPI, HTTPException, Request, status, Form
from pydantic import BaseModel, Field
from uuid import UUID
from starlette.responses import JSONResponse


class NegativeNumberException(Exception):
    def __init__(self, books_to_return):
        self.books_to_return = books_to_return


app = FastAPI()


## The below class has basic validations. But it accepts null values and integers in string field.
## In order to tackle this we have to use Field()
# class Book(BaseModel):
#     id: UUID
#     title: str
#     author: str
#     description: str
#     rating: int


## class using field. Field is a
class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1, max_length=100)
    description: Optional[str] = Field(title="Description of the book",
                                       max_length=100, min_length=1)
    rating: int = Field(gt=-1, lt=101)

    # adding predefined values to models
    class Config:
        schema_extra = {
            "example": {
                "id": "a12d756f-4ca3-46ee-a5dc-4d81000c36f7",
                "title": "book1 title",
                "author": "author1",
                "description": "description1",
                "rating": 90
            }
        }


class BooksNoRating(BaseModel):
    id: UUID
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    description: Optional[str] = Field(
        None,
        title="Description about the book.",
        min_length=1,
        max_length=200
    )


BOOKS = []


@app.exception_handler(NegativeNumberException)
async def negative_number_exception_handler(request: Request,
                                            exception: NegativeNumberException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Hey, the input {exception.books_to_return} is a Negative Number."
                            f"Negative number is not a valid input"}
    )


@app.post('/books/login')
async def books_login(username: str = Form(...), password: str = Form(...)):
    return {'username': username, 'password': password}


@app.get('/')
async def read_all_books():
    if len(BOOKS) < 1:
        create_books_no_api()
    return BOOKS


@app.get('/read_some_books/')
async def read_some_books(books_to_return: Optional[int] = None):
    if books_to_return and books_to_return < 0:
        raise NegativeNumberException(books_to_return)
    if len(BOOKS) < 1:
        create_books_no_api()
    if books_to_return and len(BOOKS) >= books_to_return > 0:
        i = 1
        new_books = []
        while i <= books_to_return:
            new_books.append(BOOKS[i-1])
            i += 1
        return new_books
    return BOOKS


@app.get('/books/no_rating/{book_id}', response_model=BooksNoRating)
async def read_book_no_rating(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_not_found_exception()


@app.get('/book/{book_id}')
async def get_book_by_id(book_id: UUID):
    for x in BOOKS:
        if x.id == book_id:
            return x
    raise raise_item_not_found_exception()


@app.put('/book/{book_id}')
async def update_book(book_id: UUID, book: Book):
    counter = 0
    for item in BOOKS:
        counter += 1
        if item.id == book_id:
            BOOKS[counter - 1] = book
            return BOOKS[counter - 1]
    # raise HTTPException(status_code=404,
    #                     detail="Book not found",
    #                     headers={"X-Header-Error": "Nothing to be seen at UUID"})
    raise raise_item_not_found_exception()


@app.delete('/book/{book_id}')
async def delete_book(book_id: UUID):
    counter = 0
    for item in BOOKS:
        counter += 1
        if item.id == book_id:
            del BOOKS[counter-1]
            return f'ID: {book_id} deleted.'
    raise raise_item_not_found_exception()


@app.post('/create', status_code=status.HTTP_201_CREATED)
async def create_book(book: Book):  # argument name: Model Name(type)
    BOOKS.append(book)
    return book


@app.post('/create_books_no_api')
def create_books_no_api():
    book_1 = Book(id="e57d756f-4ca3-46ee-a5dc-4d81000c36f7",
                  title="book1 title",
                  author="author1",
                  description="description1",
                  rating=90)
    book_2 = Book(id="6690321d-0882-4304-b38e-0a1d816d978a",
                  title="book2 title",
                  author="author2",
                  description="description2",
                  rating=95)
    book_3 = Book(id="48a6af8e-82f9-4f11-a8d3-21f0c738f5fa",
                  title="book3 title",
                  author="author3",
                  description="description3",
                  rating=100)
    book_4 = Book(id="b75caa34-45bf-46e1-ad98-67e8396bd370",
                  title="book4 title",
                  author="author4",
                  description="description4",
                  rating=75)
    BOOKS.append(book_1)
    BOOKS.append(book_2)
    BOOKS.append(book_3)
    BOOKS.append(book_4)


def raise_item_not_found_exception():
    return HTTPException(status_code=404,
                         detail="Book not found",
                         headers={"X-Header-Error": "Nothing to be seen at UUID"})

