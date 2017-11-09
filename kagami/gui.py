import os.path
import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from collections import OrderedDict
from PIL import Image
from PIL.ImageTk import PhotoImage

from kagami.logic import menulogic, reflector


class MenuCascade(tk.Menu):
    def __init__(self, master, entries, label="Menu Entries"):
        super().__init__(master, tearoff=False)
        master.add_cascade(label=label, menu=self)
        for label, kwargs in entries.items():
            self.generate_entry(label=label, **kwargs)

    def generate_entry(self, label="My Label", **kwargs):
        options = {
            'entry_type': 'separator',
            'label': 'Entry',
            'command': None,
            'variable': None,
            'value': None,
            'accelerator': None,
            'underline': None
        }
        options.update(kwargs)

        if options['entry_type'] == "separator":
            self.add_separator()
        elif options['entry_type'] == "command":
            self.add_command(
                label=label, command=options['command'],
                underline=options['underline'],
                accelerator=options['accelerator'])
        elif options['entry_type'] == "radio":
            self.add_radiobutton(
                label=label,
                command=options['command'],
                variable=options['variable'],
                value=options['value'],
                underline=options['underline'],
                accelerator=options['accelerator'])
        else:
            raise KeyError("Wrong type of menu entries")


class Menu(tk.Menu):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.configure(menu=self)
        self.menu_construct()
        self.menu_bind_keys()

    def menu_construct(self):
        file_menu_entries = OrderedDict([
            ("Open", {
                'entry_type': 'command',
                'command': self.master.browse,
                'accelerator': 'ctrl+O'
            }),
            ("Open Default", {
                'entry_type': 'command',
                'command': self.master.default_image_load
            }),
            ("Save", {
                'entry_type': 'command',
                'command': self.master.save,
                'accelerator': 'ctrl+S'
            }),
            ("separator", {
                'entry_type': 'separator'
            }),
            ("Quit", {
                'entry_type': 'command',
                'command': self.master.quit,
                'accelerator': 'ctrl+Q'
            })
        ])
        MenuCascade(self, file_menu_entries, label="File")

        # Construct reflection menu
        reflection_menu_entries = OrderedDict([
            ('Vertical axis - Left portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': self.master.reflection_mode,
                'value': 'w'
            }),
            ('Vertical axis - Right portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': self.master.reflection_mode,
                'value': 'e'
            }),
            ('Horizontal axis - Top portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': self.master.reflection_mode,
                'value': 'n'
            }),
            ('Horizontal axis - Bottom portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': self.master.reflection_mode,
                'value': 's'
            }),
            ("separator", {
                'entry_type': 'separator'
            }),
            ('Quadrant 1 - Top-left portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': self.master.reflection_mode,
                'value': 'nw'
            }),
            ('Quadrant 2 - Top-right portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': self.master.reflection_mode,
                'value': 'ne'
            }),
            ('Quadrant 3 - Bottom-left portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': self.master.reflection_mode,
                'value': 'sw'
            }),
            ('Quadrant 4 - Bottom-right portion', {
                'entry_type': 'radio',
                'command': lambda:
                    self.master.image_container.refresh_all_thumbnails(),
                'variable': self.master.reflection_mode,
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

    def menu_bind_keys(self):
        self.master.bind_all("<Control-o>", self.master.browse)
        self.master.bind_all("<Control-s>", self.master.save)
        self.master.bind_all("<Control-q>", self.master.quit)


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

    def refresh_all_thumbnails(self, event=None):
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

        # Set up image related variable
        self.reflection_mode = tk.StringVar(self, value='w')
        self.allowed_types = [
            ('Supported Extension', ('.png', '.jpg')),
            ('PNG File', '.png'),
            ('JPG File', '.jpg')
        ]

        # Construct UI element
        Menu(self)
        self.image_container = DualImageContainer(self)
        self.image_container.pack()
        self.default_image_load()

    def generate_images(self):
        self.image_fullsize = Image.open(self.path)
        self.image_container.refresh_all_thumbnails()

    def default_image_load(self):
        import sys

        if hasattr(sys, '_MEIPASS'):
            self.path = os.path.join(sys._MEIPASS, "asset/default.png")
        else:
            self.path = 'asset/default.png'

        self.current_title = self.basetitle
        self.title(self.current_title)
        self.generate_images()

    def browse(self, event=None):
        self.path = askopenfilename(filetypes=self.allowed_types)
        self.title('Kagami - {}'.format(os.path.split(self.path)[1]))
        self.generate_images()

    def save(self, event=None):
        ext = ''
        save_path = 'pass'

        while ext not in ('.jpg', '.png') and save_path:
            # Get new filename by splitting filename and extension of original
            # file and then slip current reflection mode inbetween
            default_filename = '{0}_{2}{1}'.format(
                *os.path.splitext(os.path.split(self.path)[1]),
                self.reflection_mode.get())

            save_path = asksaveasfilename(
                initialfile=default_filename,
                filetypes=self.allowed_types,
                defaultextension='.png'
            )

            # Check if extension if entered. Dialog will open again if
            # extension is not entered properly.
            try:
                ext = os.path.splitext(save_path)[1]
            except TypeError:
                break

        if save_path:
            result = reflector.reflect_image(self.image_fullsize,
                                             self.reflection_mode.get())
            result.save(save_path)
