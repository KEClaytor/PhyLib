# The user data type and associated methods

class User():
    def __init__(self, name, netid):
        self.name = name
        self.netid = netid
        self.librarian = 0
        self.books = [] # Books checked out
        self.times = [] # Checkout times
        return

    # Get user information
    def get_name(self):
        return self.name
    def get_netid(self):
        return self.netid
    def get_checkedout(self):
        return self.books
    def get_checkouttimes(self):
        return self.times

    # Is this user a librarian?
    def is_librarian(self):
        return self.librarian
    def make_librarian(self):
        self.librarian = 1
        return
    def remove_librarian(self):
        self.librarian = 1
        return

    # Checking out and in books
    def checkout(self, book_id):
        self.books.append(book)
        self.times.append(datetime.now)
        return

    def checkin(self, book_id):
        book_idx = self.books.index(book_id)
        self.books.pop(book_idx)
        self.times.pop(book_idx)
        return

