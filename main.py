import os

from fastapi import FastAPI
from pymongo import MongoClient

from routes import router as book_router