class TextBooksRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    # Create a book entry and append it to the file
    def create_book(self, book_info):
        with open(self.file_path, "a") as file:
            file.write(book_info + "\n")

    # Read all book entries from the file
    def read_all_books(self):
        with open(self.file_path, "r") as file:
            return file.readlines()

    # Create a book entry with detailed information
    def create_book_with_details(self, title, author, publish_year, isbn):
        book_info = f"Title: {title}, Author: {author}, PublishYear: {publish_year}, ISBN: {isbn}"
        self.create_book(book_info)

    # Update an existing book entry with detailed information
    def update_book_with_details(
        self, book_id, title=None, author=None, publish_year=None, isbn=None
    ):
        books = self.read_all_books()
        if 0 <= book_id < len(books):
            book_info = books[book_id].strip().split(", ")

            # Prepare updated information based on provided or existing data
            updated_info = {
                "Title": title if title else book_info[0].split(": ")[1],
                "Author": author if author else book_info[1].split(": ")[1],
                "PublishYear": publish_year
                if publish_year
                else book_info[2].split(": ")[1],
                "ISBN": isbn if isbn else book_info[3].split(": ")[1],
            }

            # Construct updated book information
            updated_book_info = f"Title: {updated_info['Title']}, Author: {updated_info['Author']}, PublishYear: {updated_info['PublishYear']}, ISBN: {updated_info['ISBN']}\n"

            # Update the book entry in the file
            books[book_id] = updated_book_info
            with open(self.file_path, "w") as file:
                file.writelines(books)
        else:
            print("Book ID out of range")

    # Delete a book entry based on the provided book_id
    def delete_book(self, book_id):
        books = self.read_all_books()
        if 0 <= book_id < len(books):
            del books[book_id]
            with open(self.file_path, "w") as file:
                file.writelines(books)
        else:
            print("Book ID out of range.")
