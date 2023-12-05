from fastapi import APIRouter, HTTPException, Depends
from dto.book import Book
from repository.book_repository import TextBooksRepository
from service.book_service import BooksService
from middleware.auth import get_current_user


text_books_repository = TextBooksRepository("books.txt")
books_service = BooksService(text_books_repository)
book_router = APIRouter(prefix="/book", tags=["Books"])


@book_router.post("/create")
def create_book(book: Book, current_user=Depends(get_current_user)):
    books_service.create_book(book.title, book.author, book.publish_year, book.isbn)
    return {"message": "Book created successfully"}


@book_router.get("/")
def get_all_books(current_user=Depends(get_current_user)):
    return books_service.get_all_books()


@book_router.put("/update/{book_id}")
def update_book(book_id: int, book: Book, current_user=Depends(get_current_user)):
    updated = books_service.update_book(
        book_id,
        book.title,
        book.author,
        book.publish_year,
        book.isbn,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book with ID {book_id} updated successfully"}


@book_router.delete("/{book_id}")
def delete_book(book_id: int, current_user=Depends(get_current_user)):
    deleted = books_service.delete_book(book_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Book not found")
    return {"message": f"Book with ID {book_id} deleted successfully"}
