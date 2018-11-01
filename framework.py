"""
    Chapter 6: Paint Application
        Developing a Tiny Framework
Tkinter GUI Application Development Blueprints
"""
import tkinter as tk


class Framework():

    """
    GUIFramework is a class that provides a higher level of abstraction for
    the development of Tkinter graphic user interfaces (GUIs).
    Every class that uses this GUI framework must inherit from this class
    and should pass the root window as an argument to this class by calling 
    the super method as follows:
        super().__init__(root)
    Building Menus:
    To build a menu, call build_menu() method with one argument for
    menu_definition, where menu_definition is a tuple where each item is a string of the
    format:
        'Top Level Menu Name - MenuItemName/Accelrator/Commandcallback/Underlinenumber'.
        MenuSeparator is denoted by a string 'sep'.
    For instance, passing this tuple as an argument to this method
        menu_definition = (
                      'File - &New/Ctrl+N/new_file, &Open/Ctrl+O/openfile, &Save/Ctrl+S/save, Save&As//saveas, sep, Exit/Alt+F4/close', 
                      'Edit - Cut/Ctrl+X/cut, Copy/Ctrl+C/copy, Paste/Ctrl+V/paste, Sep',
                      )
    will generate a File and Edit Menu Buttons with listed menu items for each of the buttons.
    """
    menu_items = None

    def __init__(self, root):
        self.root = root

    def build_menu(self, menu_definitions):
        menu_bar = tk.Menu(self.root)
        for definition in menu_definitions:
            menu = tk.Menu(menu_bar, tearoff=0)
            top_level_menu, pull_down_menus = definition.split('-')
            menu_items = map(str.strip, pull_down_menus.split(','))
            for item in menu_items:
                self._add_menu_command(menu, item)
            menu_bar.add_cascade(label=top_level_menu, menu=menu)
        self.root.config(menu=menu_bar)

    def _add_menu_command(self, menu, item):
        if item == 'sep':
            menu.add_separator()
        else:
            menu_label, accelrator_key, command_callback = item.split('/')
            try:
                underline = menu_label.index('&')
                menu_label = menu_label.replace('&', '', 1)
            except ValueError:
                underline = None
            menu.add_command(label=menu_label, underline=underline,
                             accelerator=accelrator_key, command=eval(command_callback))


class TestThisFramework(Framework):

    def new_file(self):
        print('new tested OK')

    def open_file(self):
        print ('open tested OK')

    def undo(self):
        print ('undo tested OK')

    def options(self):
        print ('options tested OK')

    def about(self):
        print ('about tested OK')

if __name__ == '__main__':

    root = tk.Tk()
    menu_items = (
        'File- &New/Ctrl+N/self.new_file, &Open/Ctrl+O/self.open_file',
        'Edit- Undo/Ctrl+Z/self.undo, sep, Options/Ctrl+T/self.options',
        'About- About//self.about'
    )
    app = TestThisFramework(root)
    app.build_menu(menu_items)
    root.mainloop()