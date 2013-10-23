# Main Physics Library Class
from Tkinter import *

def login(user,password):
    print "click!"
    return

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

