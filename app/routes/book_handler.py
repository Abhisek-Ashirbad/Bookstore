# ==============================================================================
# -*- coding: utf-8 -*-
# ==============================================================================
# Created By: Abhisek Ashirbad Sethy
# Created Date: 05/09/2023 (DD/MM/YYYY)
# Copyright: Apache License v2.0
# ==============================================================================

# Imports
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models import Book
from app.db import get_db, init_session
from app.db.db_tables import Books

class BookHandler():
    router = APIRouter()

    # Initialize the database schema
    init_session()

    # POST endpoint for "/books"
    @router.post("/books/", response_model=Book)
    async def create_book(book: Book, db: Session = Depends(get_db)):
        async with db.transaction():
            db_book = Books(**book.dict())
            await db.execute(Books.insert().values(**book.dict()))
            await db.commit()
            return db_book

    # GET endpoint for "/books/{book_id}"
    @router.get("/books/{book_id}", response_model=Book)
    async def read_book(book_id: int, db: Session = Depends(get_db)):
        db_book = await db.execute(Books.select().where(Books.c.id == book_id))
        book = db_book.fetchone()
        if book is None:
            raise HTTPException(status_code=404, detail="Book not found")
        return book

    # GET endpoint for fetching all books in database
    @router.get("/books/", response_model=list[Book])
    async def read_books(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
        db_books = await db.execute(Books.select().offset(skip).limit(limit))
        return db_books.fetchall()

    # PUT endpoint for updating a book with "book_id"
    @router.put("/books/{book_id}", response_model=Book)
    async def update_book(book_id: int, book: Book, db: Session = Depends(get_db)):
        async with db.transaction():
            db_book = await db.execute(Books.select().where(Books.c.id == book_id))
            existing_book = db_book.fetchone()
            if existing_book is None:
                raise HTTPException(status_code=404, detail="Book not found")

            update_values = book.dict(exclude_unset=True)
            for key, value in update_values.items():
                setattr(existing_book, key, value)

            await db.commit()
            return existing_book

    # DELETE endpoint for deleting a book with "book_id"
    @router.delete("/books/{book_id}", response_model=Book)
    async def delete_book(book_id: int, db: Session = Depends(get_db)):
        async with db.transaction():
            db_book = await db.execute(Books.select().where(Books.c.id == book_id))
            existing_book = db_book.fetchone()
            if existing_book is None:
                raise HTTPException(status_code=404, detail="Book not found")

            await db.execute(Books.delete().where(Books.c.id == book_id))
            await db.commit()

            return existing_book
