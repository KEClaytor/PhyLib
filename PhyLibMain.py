# Main Physics Library Class
from Tkinter import *

def login(user,password):
    # Bring up the user book checkout / in screen
    pass

def user_home(user):
    # List the books the user has checked out
    # Mention that they only have to scan a book for autocheckout / in
    # Add a button for when they are done

    # If the user is a librarian
    #  add a buton for adding a book
    #  another for removing a book
    #  and a final one for adding a user
    pass

def makeentry(parent, caption, width=None, **options):
    Label(parent, text=caption).pack(side=LEFT)
    entry = Entry(parent, **options)
    if width:
        entry.config(width=width)
    entry.pack(side=LEFT)
    return entry

# Runs if we can't load up existing user data
def first_time_launch():
    master = Tk()
    w = Label(master, text="Welcome to PhysLib 1.0\nNo users detected. You will become The Librarian.")
    w.pack()
    
    user = makeentry(master, "User name:", 10)
    password = makeentry(master, "Password:", 10, show="*")

    b = Button(master, text="OK", command=adduser(user,password,1))
    b.pack()
    mainloop()
    return

def main():
    master = Tk()

    w = Label(master, text="Welcome to PhysLib 1.0\nLogin to begin.")
    w.pack()

    user = makeentry(master, "User name:", 10)
    password = makeentry(master, "Password:", 10, show="*")

    b = Button(master, text="OK", command=login(user,password))
    b.pack()

    mainloop()
    return

if __name__ == "__main__":
    # Try to load up the old data
    # If we can't go to the first time launch
    main()

