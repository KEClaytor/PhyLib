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
# For the custom textinput class
from kivy.uix.textinput import TextInput
# Library needed modules
import pickle

class LibraryScreen(Screen):
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

    # On initalization try to load the pickled users and books
    try:
        data_books = pickle.load( open('librarybooks.pld','rw') )
    except IOError:
        data_books = []
    try:
        data_users = pickle.load( open('libraryusers.pld','rw') )
    except IOError:
        data_users = []

    def build(self):
        Clock.schedule_interval(self._update_clock, 1 / 60.)
        self.screens = {}
        self.available_screens = ['login', 'user',
            'librarian', 'newuser', 'newbook']
        self.sidx = {'login':0, 'user':1,
            'librarian':2, 'newuser':3, 'newbook':4]
        curdir = dirname(__file__)
        self.available_screens = [join(curdir, 'screens',
            '{}.kv'.format(fn)) for fn in self.available_screens]
        self.go_screen(self.sidx['login'],'left')
        return

    def go_screen(self,screen_index,direction):
        screen = self.load_screen(screen_index)
        sm = self.root.ids.sm
        sm.switch_to(screen, direction=direction)
        self.current_title = screen.name
        return
    def go_add_user_screen(self):
        self.go_screen(self.sidx['newuser'],'left')
        return
    def go_add_book_screen(self):
        self.go_screen(self.sidx['newbookx'],'left')
        return

    def load_screen(self, index):
        if index in self.screens:
            return self.screens[index]
        screen = Builder.load_file(self.available_screens[index])
        self.screens[index] = screen
        return screen

    def login(self):
        # Get the text box contents and pass them to
        #    our authentication agent.
        # Check to see if the user is a librarian
        # If they are then give them that screen
        username = self.screens[0].ids.username_text.text
        password = self.screens[0].ids.password_text.text
        # TODO: Get user info
        lib = get_login_info(username)
        lib = 0
        if (username == 'kec30'):
            lib = 1
        if (lib):
            self.go_screen(self.sidx['librarian'],'left')
        else:
            self.go_screen(self.sidx['user'],'left')
        return

    def logout(self):
        # Return us to the login screen
        self.go_screen(0,'right')
        # Clear username and password
        self.screens[self.sidx['login']].ids.username_text.text = ''
        self.screens[self.sidx['login']].ids.password_text.text = ''
        return

    # Librarian screens, creating users and books
    def add_user(self,create):
        if create:
            pass
        else:
            self.go_screen(self.sidx['librarian'],'right')
        return
    def add_book(self,create):
        if create:
            pass
        else:
            self.go_screen(self.sidx['librarian'],'right')
        return

    def _update_clock(self, dt):
        self.time = time()

if __name__ == '__main__':
    #Window.toggle_fullscreen()
    LibraryApp().run()
