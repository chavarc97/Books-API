import uuid
from typing import List, Optional
from pydantic import BaseModel, Field

class Book(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias='_id')
    title: str = Field(...)
    authors: list = Field(...)
    average_rating: float = Field(...)
    isbn: str = Field(...)
    isbn13: str = Field(...)
    language_code: str = Field(...)
    num_pages: int = Field(...)
    ratings_count: int = Field(...)
    text_reviews_count: int = Field(...)
    publication_date: str = Field(...)
    publisher: str = Field(...)
    
    class Config:
        allow_population_by_field_name = True
        scheme_extra = {
            "example" : {
                "_id": "066de609-b04a-4b30-b46c-32537c7f1f6e",
                "title": "Poor People",
                "authors": ["William T. Vollmann"],
                "average_rating": 3.5,
                "isbn": "0060878827",
                "isbn13": "9780060878825",
                "language_code": "eng",
                "num_pages": 434,
                "ratings_count": 769,
                "text_reviews_count": 139,
                "publication_date": "2/27/2007",
                "publisher": "Ecco"
            }
        }


class Book_Update(BaseModel):
    title: Optional[str] = None
    authors: Optional[List[str]] = None
    average_rating: Optional[float] = None
    isbn: Optional[str] = None
    isbn13: Optional[str] = None
    language_code: Optional[str] = None
    num_pages: Optional[int] = None
    ratings_count: Optional[int] = None
    text_reviews_count: Optional[int] = None
    publication_date: Optional[str] = None
    publisher: Optional[str] = None
    
    class Config:
        schema_extra = {
            "example" : {
                "title": "Poor People",
                "authors": ["William T. Vollmann"],
                "average_rating": 3.5,
                "isbn": "0060878827",
                "isbn13": "9780060878825",
                "language_code": "eng",
                "num_pages": 434,
                "ratings_count": 769,
                "text_reviews_count": 139,
                "publication_date": "2/27/2007",
                "publisher": "Ecco"
            }
        }
