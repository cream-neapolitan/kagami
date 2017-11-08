from kagami.logic import reflector
from PIL.ImageTk import PhotoImage
'''Code used for modifying UI'''


def update_thumb_container(master):
    thumb = reflector.reflect_image(
        master.infotext.thumb_original, master.reflection_mode.get())
    widget = PhotoImage(thumb)

    master.infotext.refl_image_container.label.image = widget
    master.infotext.refl_image_container.label.configure(image=widget)
