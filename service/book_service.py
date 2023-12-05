class BooksService:
    def __init__(self, repository):
        self.repository = repository

    # Create a book entry using book_info as a single string
    def create_book(self, book_info):
        self.repository.create_book(book_info)

    # Get all books from the repository
    def get_all_books(self):
        return self.repository.read_all_books()

    # Create a book entry with detailed information (title, author, publish_year, isbn)
    def create_book(self, title, author, publish_year, isbn):
        return self.repository.create_book_with_details(
            title, author, publish_year, isbn
        )

    # Update a book's information using detailed parameters (title, author, publish_year, isbn)
    def update_book(self, book_id, title, author, publish_year, isbn):
        return self.repository.update_book_with_details(
            book_id, title, author, publish_year, isbn
        )

    # Delete a book entry by its ID
    def delete_book(self, book_id):
        return self.repository.delete_book(book_id)
