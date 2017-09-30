import os
from tkinter import filedialog


def openMap():
    file = filedialog.askopenfilename(filetypes=(("Map file", "*.map"),
                                                  ("All files", "*.*")),
                                      title="Choose a map")

    return file
