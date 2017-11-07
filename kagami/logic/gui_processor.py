def update_thumb(master):
    master.infotext.proc_image_container.label.configure(
        text=master.reflection_mode.get())
