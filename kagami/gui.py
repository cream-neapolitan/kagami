import tkinter as tk
from collections import OrderedDict
from kagami.logic import menulogic, gui_processor


class MenuCascade(tk.Menu):
    def __init__(self, master, entries, label="Menu Entries"):
        super().__init__(master, tearoff=False)
        master.add_cascade(label=label, menu=self)
        for label, options in entries.items():
            self.generate_entry(label=label, **options)

    def generate_entry(self, label="My Label", **options):
        if options['entry_type'] == "separator":
            self.add_separator()
        elif options['entry_type'] == "command":
            self.add_command(label=label, command=options['command'])
        elif options['entry_type'] == "radio":
            self.add_radiobutton(
                label=label,
                command=options['command'],
                variable=options['variable'],
                value=options['value'])
        else:
            raise KeyError("Wrong type of menu entries")


class Menu(tk.Menu):
    def __init__(self, master):
        super().__init__()
        master.configure(menu=self)

        # Construct file menu
        file_menu_entries = OrderedDict([
            ("Open", {
                'entry_type': 'command',
                'command': menulogic.browse_file
            }),
            ("separator", {
                'entry_type': 'separator'
            }),
            ("Save", {
                'entry_type': 'command',
                'command': menulogic.save_file
            }),
            ("Quit", {
                'entry_type': 'command',
                'command': master.quit
            })
        ])
        MenuCascade(self, file_menu_entries, label="File")

        # Construct reflection menu
        reflection_menu_entries = OrderedDict([
            ('Vertical axis - Left portion', {
                'entry_type': 'radio',
                'command': lambda: gui_processor.update_thumb(master),
                'variable': master.reflection_mode,
                'value': 'w'
            }),
            ('Vertical axis - Right portion', {
                'entry_type': 'radio',
                'command': lambda: gui_processor.update_thumb(master),
                'variable': master.reflection_mode,
                'value': 'e'
            }),
            ('Horizontal axis - Top portion', {
                'entry_type': 'radio',
                'command': lambda: gui_processor.update_thumb(master),
                'variable': master.reflection_mode,
                'value': 'n'
            }),
            ('Horizontal axis - Bottom portion', {
                'entry_type': 'radio',
                'command': lambda: gui_processor.update_thumb(master),
                'variable': master.reflection_mode,
                'value': 's'
            }),
            ("separator", {
                'entry_type': 'separator'
            }),
            ('Cartesian Quadrant 1 - Top-right portion', {
                'entry_type': 'radio',
                'command': lambda: gui_processor.update_thumb(master),
                'variable': master.reflection_mode,
                'value': 'ne'
            }),
            ('Cartesian Quadrant 2 - Top-left portion', {
                'entry_type': 'radio',
                'command': lambda: gui_processor.update_thumb(master),
                'variable': master.reflection_mode,
                'value': 'nw'
            }),
            ('Cartesian Quadrant 3 - Bottom-left portion', {
                'entry_type': 'radio',
                'command': lambda: gui_processor.update_thumb(master),
                'variable': master.reflection_mode,
                'value': 'sw'
            }),
            ('Cartesian Quadrant 4 - Bottom-right portion', {
                'entry_type': 'radio',
                'command': lambda: gui_processor.update_thumb(master),
                'variable': master.reflection_mode,
                'value': 'se'
            }),
        ])
        MenuCascade(self, reflection_menu_entries, label="Reflection")

        # Construct about menu
        about_menu_entries = OrderedDict([
            ("Twitter", {
                'entry_type': 'command',
                'command': menulogic.open_twitter
            }),
            ("Github Repo", {
                'entry_type': 'command',
                'command': menulogic.open_github
            }),
        ])
        MenuCascade(self, about_menu_entries, label="About")


class BaseImageContainer(tk.Frame):
    def __init__(self, master, header="Default", content="text"):
        super().__init__(master, padx=10, pady=10)
        self.labelframe = tk.LabelFrame(self, text=header)
        self.labelframe.pack()

        self.label = tk.Label(self.labelframe, text=content, width=20)
        self.label.pack()


class DualImageContainer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.orig_image_container = BaseImageContainer(
            self, header="Original")
        self.proc_image_container = BaseImageContainer(
            self, header="Processed", content=master.reflection_mode.get())
        self.orig_image_container.pack(side="left")
        self.proc_image_container.pack(side="left")


class MainApps(tk.Tk):
    def __init__(self, basetitle="My Apps"):
        super().__init__()

        # Set up basic working variable
        self.basetitle = basetitle
        self.current_title = basetitle
        self.title(self.current_title)
        self.reflection_mode = tk.StringVar(self, value='w')

        # Construct UI element
        Menu(self)
        self.infotext = DualImageContainer(self)

        self.infotext.pack()
