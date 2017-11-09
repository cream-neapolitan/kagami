import tkinter as tk
from collections import OrderedDict
from PIL import Image
from PIL.ImageTk import PhotoImage
from tkinter.filedialog import askopenfilename, asksaveasfilename

from kagami.logic import menulogic, reflector


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
        self.master = master
        self.master.configure(menu=self)

        # Construct file menu
        file_menu_entries = OrderedDict([
            ("Open", {
                'entry_type': 'command',
                'command': self.browse
            }),
            ("separator", {
                'entry_type': 'separator'
            }),
            ("Save", {
                'entry_type': 'command',
                'command': self.save
            }),
            ("Quit", {
                'entry_type': 'command',
                'command': self.master.quit
            })
        ])
        MenuCascade(self, file_menu_entries, label="File")

        # Construct reflection menu
        reflection_menu_entries = OrderedDict([
            ('Vertical axis - Left portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': master.reflection_mode,
                'value': 'w'
            }),
            ('Vertical axis - Right portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': master.reflection_mode,
                'value': 'e'
            }),
            ('Horizontal axis - Top portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': master.reflection_mode,
                'value': 'n'
            }),
            ('Horizontal axis - Bottom portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': master.reflection_mode,
                'value': 's'
            }),
            ("separator", {
                'entry_type': 'separator'
            }),
            ('Quadrant 1 - Top-left portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': master.reflection_mode,
                'value': 'nw'
            }),
            ('Quadrant 2 - Top-right portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': master.reflection_mode,
                'value': 'ne'
            }),
            ('Quadrant 3 - Bottom-left portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': master.reflection_mode,
                'value': 'sw'
            }),
            ('Quadrant 4 - Bottom-right portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
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

    def browse(self):
        self.master.path = askopenfilename()
        self.master.generate_images()

    def save(self):
        result = reflector.reflect_image(
            self.master.image_fullsize, self.master.reflection_mode.get())
        save_path = asksaveasfilename()
        result.save(save_path)


class BaseImageContainer(tk.Frame):
    def __init__(self, master, header="Default"):
        super().__init__(master, padx=10, pady=10)
        self.labelframe = tk.LabelFrame(self, text=header)
        self.labelframe.pack()

        # Create thumbnail widget
        width, height = master.thumb_size
        widget = PhotoImage(Image.new('RGB', (1, 1)))

        self.ui_image = tk.Label(
            self.labelframe, image=widget,
            width=width + 20, height=height + 20)
        self.ui_image.image = widget
        self.ui_image.pack()

    def update_thumbnail(self, image):
        widget = PhotoImage(image)
        self.ui_image.configure(image=widget)
        self.ui_image.image = widget
        self.ui_image.pack()


class DualImageContainer(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.thumb_size = (240, 240)

        self.thumb_original = None
        self.thumb_reflected = None

        # Place UI elements
        self.orig_image_container = BaseImageContainer(
            self, header="Original")
        self.refl_image_container = BaseImageContainer(
            self, header="Reflected")
        self.orig_image_container.pack(side="left")
        self.refl_image_container.pack(side="left")

    def refresh_all_thumbnails(self):
        self.thumb_original = self.master.image_fullsize.copy()
        self.thumb_original.thumbnail(self.thumb_size)
        self.orig_image_container.update_thumbnail(self.thumb_original)

        self.thumb_reflected = reflector.reflect_image(
            self.thumb_original, self.master.reflection_mode.get())
        self.refl_image_container.update_thumbnail(self.thumb_reflected)


class MainApps(tk.Tk):
    def __init__(self, basetitle="My Apps"):
        super().__init__()

        # Set up basic working variable
        self.basetitle = basetitle
        self.current_title = basetitle
        self.title(self.current_title)

        self.path = 'kagami/asset/default.png'
        self.reflection_mode = tk.StringVar(self, value='w')

        # Construct UI element
        Menu(self)
        self.image_container = DualImageContainer(self)
        self.image_container.pack()
        self.generate_images()

    def generate_images(self):
        self.image_fullsize = Image.open(self.path)
        self.image_container.refresh_all_thumbnails()
