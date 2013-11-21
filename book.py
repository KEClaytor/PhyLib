# Class for storing book information

class Book():
    def __init__(self, title, author, year, copy, rfid):
        self.title = title
        self.author = author
        self.year = year
        self.copy = copy
        self.rfid = rfid
        # status 1 = in library
        #        0 = checked out
        self.status = 1
        return

    # Get book information
    def get_title(self):
        return self.title
    def get_author(self):
        return self.author
    def get_year(self):
        return self.year
    def get_rfid(self):
        return self.rfid

    def checkout(self):
        self.status = 0
        return
    def checkin(self):
        self.status = 1
        return

    # Reset the book ID
    # (in the case of a tag change)
    def change_id(self, new_rfid):
        self.rfid = new_rfid
        return

