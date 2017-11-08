'''Code used for modifying UI'''


def update_thumb_container(master):
    master.infotext.proc_image_container.label.configure(
        text=master.reflection_mode.get())
