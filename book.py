# Class for storing book information

class Book():
    def __init__(self, title, author):
        self.title = title
        self.author = author
        self.book_id = 0
        return

    # Get book information
    def get_title(self):
        return self.title
    def get_author(self):
        return self.author
    def get_book_id(self):
        return self.book_id

    # Reset the book ID
    # (in the case of a tag change)
    def change_id(self, new_id):
        self.book_id = new_id
        return

