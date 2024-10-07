#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from typing import List

router = APIRouter()
from model import Book, Book_Update

@router.post("/", response_description="Post a new book", status_code=status.HTTP_201_CREATED, 
             response_model=Book)
def create_book(request: Request, book: Book = Body(...)):
    book = jsonable_encoder(book)
    new_book = request.app.database["books"].insert_one(book)
    created_book = request.app.database["books"].find_one(
        {"_id": new_book.inserted_id}
    )
    return created_book


# Get all books 
@router.get("/", response_description="Get all books", response_model=List[Book])
def list_books(request: Request, rating: float = 0):
    books = list(request.app.database["books"].find({"average_rating": {"$gte": rating}}))
    return books


# Get a single book by id
@router.get("/{id}", response_description="Get a single book by id", response_model=Book)
def find_book(id: str, request: Request):
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")


# Update a book by id



# Delete a book by id