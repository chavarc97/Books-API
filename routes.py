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
@router.put("/{id}", response_description="Update a book by id", response_model=Book)
def update_book(id: str, request: Request, book: Book_Update = Body(...)):
    # convert the book to a dictionary and remove unwanted keys
    book_data = {k: v for k, v in book.model_dump().items() if v is not None}
    # check if the book_data is not empty
    if len(book_data) >= 1:
        # if book_data is not empty, update the book in the database
        update_res = request.app.database["books"].update_one({"_id": id}, {"set": book_data})
        
        # check if the book was updated successfully
        if update_res.modified_count == 1:
            updated_book = request.app.database["books"].find_one({"_id": id})
            if updated_book:
                return updated_book
            
        if (existing_book := request.app.database["books"].find_one({"_id": id})) is not None:
            return existing_book
        
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id}, not found")


# Delete a book by id
@router.delete("/{id}", response_description="Delete a book") 
def delete_book(id: str, request: Request, response: Response):
    delete_res = request.app.database["books"].delete_one({"_id": id})
    
    if delete_res.deleted_count == 1:
        response.status_code = status.HTTP_204_NO_CONTENT
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Libro con ID {id} no encontrado")

