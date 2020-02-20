import tkinter as tk
from tkinter import messagebox
import pygubu
import json
import Presentation
import ContentCreation
class Application:
    def __init__(self):
        #1: Create a builder
        self.builder = builder = pygubu.Builder()

        #2: Load an ui file
        builder.add_from_file('Desktop.ui')
        
        #3: Create the toplevel widget.
        self.mainwindow = builder.get_object('mainmenu_toplevel')

        #4: Connect callbacks
        builder.connect_callbacks(self)

        #5: Get variables
        self.file_path = self.builder.get_variable("file_path")

        self.curr_presentation = None
        #6: Capture delete window event so we can write the user data to a file at the
        #   end of a presentation
        self.mainwindow.protocol("WM_DELETE_WINDOW", self.on_close_window)

    def quit(self, event=None):
        self.mainwindow.quit()

    def run(self):
        self.mainwindow.mainloop()

    def on_close_window(self):
        if self.curr_presentation is not None:
            self.curr_presentation.on_close_window()
        self.mainwindow.destroy()

    def onclick_open_presentation(self):
        fpath = self.file_path.get()
        try:
            curr_file = open(fpath, 'r')
            presentation_file = json.load(curr_file)
        except (FileNotFoundError, json.JSONDecodeError):
            messagebox.showerror('File Error', 'Invalid MyClicker Presentation File!')
            return
        # Convert integer Question numbers stored as JSON text from text
        # to integers for use in Presentation
        presentation_dict_numbers = {}
        for string_key in presentation_file:
            presentation_dict_numbers[int(string_key)] = presentation_file[string_key]
        self.curr_presentation = Presentation.Presentation(presentation_dict_numbers)

    def onclick_new_presentation(self):
        fpath = self.file_path.get()
        print(fpath)
        content_creation = ContentCreation.ContentCreation(fpath)
        
if __name__ == '__main__':
    app = Application()
    app.run()