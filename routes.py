#!/usr/bin/env python3
from fastapi import APIRouter, Body, Request, Response, HTTPException, status
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
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
    # Convert the incoming book data to a dictionary, excluding the None values
    update_data = {k: v for k, v in book.model_dump(exclude_unset=True).items() if v is not None}
    
    # check if the data is empty
    if len(update_data) < 1:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="At least one field must be provided") 
    
    # perform the update query
    res = request.app.database["books"].update_one(
        {"_id": id}, {"$set": update_data}
    )
    
    # if no document was modified, raise an HTTPException
    if res.modified_count == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")
    
    # Then return the updated book
    if (book := request.app.database["books"].find_one({"_id": id})) is not None:
        return book

    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with ID {id} not found")

# Delete a book by id
@router.delete("/{id}", response_description="Delete a book") 
def delete_book(id: str, request: Request, response: Response):
    # First find the book
    book = request.app.database["books"].find_one({"_id": id})
    
    if book is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"Book with ID {id} not found")
        
    # If the book exists, delete it
    delete_res = request.app.database["books"].delete_one({"_id": id})
    
    if delete_res.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_200_OK,
                            content={
                                "message": f"Book with ID {id} was successfully deleted",
                                "deleted_book": {
                                    "id": id,
                                    "title": book.get("title"),
                                    "authors": book.get("authors"),
                                }
                            })
        
    # This case should rarely happen - the book was found but couldn't be deleted
    raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, 
                        detail="Failed to delete the book")
   
