#!//bin/kivy
from time import time
from kivy.app import App
from os.path import dirname, join
from kivy.lang import Builder
from kivy.properties import NumericProperty, StringProperty, BooleanProperty, ObjectProperty
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.uix.screenmanager import Screen
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
# For the custom textinput class
from kivy.uix.textinput import TextInput
# Library needed modules
import pickle
import user
import book
import rfid

def read_library_data(data_filenames):
    # Locate and open our users file and our books file
    # If no file exists, then we can make a new one
    filename_users = data_filenames[0]
    filename_books = data_filenames[1]
    try:
        file_users = open(filename_users, 'r')
        try:
            data_users = pickle.load( file_users )
            file_users.close()
            print "Loaded user data file"
        except EOFError:
            data_users = {}
            print "File found, unable to load, creating new users"
    except IOError:
        data_users = {}
        print "File not found, creating user data"
    print data_users
    # Now for the book file
    try:
        file_books = open(filename_books, 'r')
        try:
            data_books = pickle.load( file_books )
            file_books.close()
            print "Loaded book data file"
        except EOFError:
            data_books = {}
            print "File found, unable to load, creating new books"
    except IOError:
        data_books = {}
        print "File not found, creating book data"
    print data_books
    return (data_users,data_books)

def write_library_data(data_users, data_books, data_filenames):
    filename_users = data_filenames[0]
    filename_books = data_filenames[1]
    file_users = open(filename_users,'w')
    pickle.dump(data_users, file_users)
    file_users.close()
    file_books = open(filename_books,'w')
    pickle.dump(data_books, file_books)
    file_books.close()
    return
        
class LibraryScreen(Screen):
    # TODO: When done make this fullscreen
    # TODO: Remap escape to go back a screen
    fullscreen = BooleanProperty(False)

    def add_widget(self, *args):
        if 'content' in self.ids:
            return self.ids.content.add_widget(*args)
        return super(LibraryScreen, self).add_widget(*args)

# This allows us to tab from one text field to the next
class TabTextInput(TextInput):

    def __init__(self, *args, **kwargs):
        self.next = kwargs.pop('next', None)
        super(TabTextInput, self).__init__(*args, **kwargs)

    def set_next(self, next):
        self.next = next

    def _keyboard_on_key_down(self, window, keycode, text, modifiers):
        key, key_str = keycode
        if key in (9, 13) and self.next is not None:
            self.next.focus = True
            self.next.select_all()
        else:
            super(TabTextInput, self)._keyboard_on_key_down(window, keycode, text, modifiers)

class LibraryApp(App):

    index = NumericProperty(-1)
    current_title = StringProperty()
    time = NumericProperty(0)
    current_user = StringProperty()
    data_users = {}
    data_books = {}
    data_filenames = ['libraryusers.pld','librarybooks.pld']
    failed_login_attempts = 0

    def build(self):
        # Initalize screen info
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        # These correspond to the kivy screen files
        self.available_screens = ['login', 'user',
            'librarian', 'newuser', 'newbook']
        # Allows us to refer to screen by name instead of number
        self.sidx = {'login':0, 'user':1,
            'librarian':2, 'newuser':3, 'newbook':4}
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'screens',
            '{}.kv'.format(fn)) for fn in self.available_screens]
        self.go_screen('login')
        # Get the user data
        (self.data_users, self.data_books) = read_library_data(self.data_filenames)
        return

    # Element get/set routines
    # Should allow for easier/clearer get/set from textboxes
    #   elem_name is the kivy id, eg. 'newbook_title_text'
    #   and field_name is what you want, eg; 'text'
    # This allows it to be somewhat more general too
    def get_kvattr(self, screen_name, elem_name, field_name):
        ids = self.screens[self.sidx[screen_name]].ids
        return getattr( getattr(ids, elem_name), field_name )
    def set_kvattr(self, screen_name, elem_name, field_name, new_data):
        ids = self.screens[self.sidx[screen_name]].ids
        setattr( getattr(ids,elem_name), field_name, new_data )
        return

    # Screen loading
    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    # Transitions between screens
    def go_screen(self,screen_name):
        old_idx = self.index
        self.index = self.sidx[screen_name]
        screen = self.load_screen(self.sidx[screen_name])
        sm = self.root.ids.sm
        if self.index > old_idx:
            direction = 'left'
        else:
            direction = 'right'
        sm.switch_to(screen, direction=direction)
        self.current_title = screen.name
        # Check to see if we need to update any layouts on this screen
        # eg. put down a list of books / users
        self.update_layout(screen_name)
        return

    def update_layout(self, sn):
        # TODO: Figure out why this isn't loading with 
        #   the correct height. Eg. scrollview is too short
        # TODO: Delete the old scrollview child on entering.
        #   we can only have one active at a time.
        ids = self.screens[self.sidx[sn]].ids
        if (sn == 'newuser'):
            content = ids.newuser_list_sv
            content.clear_widgets()
            # Delete any old children from the scroll view
            layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))
            for user in self.data_users:
                ud = self.data_users[user]
                sublayout = GridLayout(cols=2, size_hint_y=None)
                userlayout = BoxLayout(orientation='vertical')
                userlayout.add_widget( Label(text=ud.name) )
                userlayout.add_widget( Label(text=ud.netid) )
                sublayout.add_widget(userlayout)
                sublayout.add_widget( Button(text='Del',size_hint=(.25,1)))
                #TODO: Add a promote and remove librarian option
                layout.add_widget(sublayout)
            # Finally add to the screen
            content.add_widget(layout)
        elif (sn == 'user'):
            content = ids.user_list_sv
            content.clear_widgets()
            layout = GridLayout(cols=1, spacing=10, size_hint_y=None)
            layout.bind(minimum_height=layout.setter('height'))
            # Get the user checkedout books and display them
            ud = self.data_users[self.current_user]
            for book_id in ud.books:
                book = data_books[book_id]
                sublayout = GridLayout(cols=2, size_hint_y=None)
                sublayout.add_widget( Label(text="Title: ") )
                sublayout.add_widget( Label(text=book.title) )
                sublayout.add_widget( Label(text="Author: ") )
                sublayout.add_widget( Label(text=book.author) )
                sublayout.add_widget( Label(text="Year: ") )
                sublayout.add_widget( Label(text=book.year) )
                sublayout.add_widget( Label(text="Copy #: ") )
                sublayout.add_widget( Label(text=book.copy) )
                layout.add_widget(sublayout)
            # Finally add to the screen
            content.add_widget(layout)
        else: #All other screen names
            pass
        return

    # ==============================================
    # ================Callbacks=====================
    # ==============================================
    def login(self):
        # Okay, the one easter egg I'm putting in
        failed_login_str = ["You're not a recognized user",
                            "Try again, k thx",
                            "You're pretty bad at this, hunh?",
                            "Are you supposed to be here?",
                            "I'm calling the cops next time",
                            "That's it! Really! This is it!",
                            "...",
                            "Well that didn't work",
                            "Maybe you can find the librarian?",
                            "I can't help you anymore, but a librarian could."]
        # Get the text box contents and pass them to
        #    our authentication agent.
        # Check to see if the user is a librarian
        # If they are then give them that screen
        username = self.get_kvattr('login', 'username_text', 'text')
        password = self.get_kvattr('login', 'password_text', 'text')
        self.current_user = username
        # TODO: Get user info
        #lib = self.get_login_info(username)
        lib = 0
        if (username == 'kec30'):
            lib = 1
        if (username in self.data_users) or (username == 'kec30'):
            if (lib):
                self.go_screen('librarian')
            else:
                self.go_screen('user')
            self.failed_login_attempts = 0
        else:
            self.set_kvattr('login', 'username_text', 'text', failed_login_str[self.failed_login_attempts % len(failed_login_str)])
            self.set_kvattr('login', 'password_text', 'text', "")
            self.failed_login_attempts += 1
        return

    def logout(self):
        # Return us to the login screen
        self.go_screen('login')
        # Clear username and password
        self.set_kvattr('login', 'username_text', 'text', '')
        self.set_kvattr('login', 'password_text', 'text', '')
        self.current_user = ''
        return

    # Checkin / out of books
    def checkout(self):
        # Get the toggle state of the buton.
        # If we are off, then turn on and start looking for books
        # Also modify the checkin toggle state
        # Wait for a little while and then loop, this way we can catch UI updates
        # Unfortunately, we have to do this for user and librarian screens
        self.set_kvattr('user', 'user_checkin', 'state', 'normal')
        self.set_kvattr('user', 'user_checkout', 'state', 'down')
        #self.set_kvattr('librarian', 'librarian_checkout', 'state', 'down')
        user = self.data_users[self.current_user]
        while 1:
            # Get a book id
            book_id = rfid.get_rfid()
            # Make sure it isn't already checkedout
            if book_id in self.data_books:
                book = self.data_books[book_id]
                if book.status:
                    # Check the book out to this user
                    user.checkout(book_id)
                    book.checkout()
                    # Update the user screen
                    self.set_kvattr('user','user_status_text','text','Checkout successful!')
                    self.set_kvattr('user','user_status_text','background_color',[0,1,0,1])
                    # Pickle book and user data in case of a crash
                    write_library_data(self.data_users, self.data_books, self.data_filenames)
                else:
                    self.set_kvattr('user','user_status_text','text','Book already checked out.')
                    self.set_kvattr('user','user_status_text','background_color',[1,0,0,1])
            else:
                self.set_kvattr('user','user_status_text','text','Book not in system!')
                self.set_kvattr('user','user_status_text','background_color',[1,0,0,1])
        pass
    # Same but for checking books in
    def checkin(self):
        self.set_kvattr('user', 'user_checkout', 'state', 'up')
        self.set_kvattr('user', 'user_checkin', 'state', 'down')
        pass

    # List users/books in the layout specified
    def load_content(self, layout):
        # Create the gridlayout
        for but in range(20):
            layout.add_widget(Button(
                                text=str(but)))
        # Attach the grid view to the layout
        return

    # Librarian screens, creating users and books
    def add_user(self, create):
        self.set_kvattr('newuser','newuser_status_text','background_color',[1,1,1,1])
        if create:
            try:
                # Create a new user with the provided values
                names = self.get_kvattr('newuser','newuser_name_text','text')
                netid = self.get_kvattr('newuser','newuser_netid_text','text')
                newuser = user.User(names, netid)
                self.data_users[netid] = newuser
                write_library_data(self.data_users, self.data_books, self.data_filenames)
                self.set_kvattr('newuser','newuser_status_text','text','Success!')
                self.set_kvattr('newuser','newuser_status_text','background_color',[0,1,0,1])
            except:
                # TODO: Log this in an error system
                self.set_kvattr('newuser','newuser_status_text','text','Create Failed!')
                self.set_kvattr('newuser','newuser_status_text','background_color',[1,0,0,1])
        else:
            # Reset text and let the user know this worked
            self.set_kvattr('newuser','newuser_name_text','text','')
            self.set_kvattr('newuser','newuser_netid_text','text','')
            self.go_screen('librarian')
        self.update_layout('librarian')
        return

    def add_book(self,create):
        # Set background color on status back to white
        self.set_kvattr('newbook','newbook_status_text','background_color',[1,1,1,1])
        rfidcode = -99
        if create:
            try:
                # Create a new book with the provided values
                # TODO: Need to do some value checking, eg year, copy
                title = self.get_kvattr('newbook','newbook_title_text','text')
                author = self.get_kvattr('newbook','newbook_author_text','text')
                year = self.get_kvattr('newbook','newbook_year_text','text')
                copy = self.get_kvattr('newbook','newbook_copy_text','text')
            except:
                # TODO: Log this in an error system
                self.set_kvattr('newbook','newbook_status_text','text','No book info!')
                self.set_kvattr('newbook','newbook_status_text','background_color',[1,0,0,1])
            self.set_kvattr('newbook','newbook_status_text','text','Awaiting RFID Code....')
            self.set_kvattr('newbook','newbook_status_text','background_color',[1,0.7,0,1])
            try:
                #TODO: get a real RFID code here
                rfidcode = rfid.get_rfid()
                print rfidcode
                self.set_kvattr('newbook','newbook_rfid_text','text',str(rfidcode))
                while rfidcode in self.data_books:
                    self.set_kvattr('newbook','newbook_status_text','text','RFID Code in use!')
                    self.set_kvattr('newbook','newbook_status_text','background_color',[1,0,0,1])
                    rfidcode = rfid.get_rfid()
                    self.set_kvattr('newbook','newbook_rfid_text','text',str(rfidcode))
            except:
                # TODO: Log this in an error system
                self.set_kvattr('newbook','newbook_status_text','text','Bad RFID Read!')
                self.set_kvattr('newbook','newbook_status_text','background_color',[1,0,0,1])
            try:
                # Now add the book to our list
                print title, author, year, copy, rfidcode
                newbook = book.Book(title, author, year, copy, rfidcode)
                print newbook
                self.data_books[rfidcode] = newbook
            except:
                print "could not add data"
            try:
                write_library_data(self.data_users, self.data_books, self.data_filenames)
                self.set_kvattr('newbook','newbook_status_text','text','Success!')
                self.set_kvattr('newbook','newbook_status_text','background_color',[0,1,0,1])
            except:
                # TODO: Log this in an error system
                self.set_kvattr('newbook','newbook_status_text','text',"Can't save book data!")
                self.set_kvattr('newbook','newbook_status_text','background_color',[1,0,0,1])
        else:
            # Reset text and let the user know this worked
            self.set_kvattr('newbook','newbook_title_text','text','')
            self.set_kvattr('newbook','newbook_author_text','text','')
            self.set_kvattr('newbook','newbook_year_text','text','')
            self.set_kvattr('newbook','newbook_copy_text','text','1')
            self.set_kvattr('newbook','newbook_rfid_text','text','')
            self.go_screen('librarian')
        return

    def _update_clock(self, dt):
        self.time = time()

if __name__ == '__main__':
    #Window.toggle_fullscreen()
    LibraryApp().run()
