from os.path import dirname
from tkinter import filedialog as fd

class PathEditor:
    def __init__(self, master, file_desc, extension, mode):
        self.__master = master
        self.__extension = extension

        wildcard = "*." + self.__extension
        self.__file_types = ((f"{file_desc} ({wildcard})", wildcard),)

        self.__mode = mode

    SAVE = "save"
    LOAD = "load"

    __last_dir = None

    @property
    def result(self):
        file_name = ""
        if self.__mode == self.SAVE:
            file_name = fd.asksaveasfilename(initialdir = self.__last_dir, filetypes = self.__file_types, defaultextension = self.__extension, parent = self.__master)
        elif self.__mode == self.LOAD:
            file_name = fd.askopenfilename(initialdir = self.__last_dir, filetypes = self.__file_types, defaultextension = self.__extension, parent = self.__master)
        else:
            pass

        if file_name:
            self.__last_dir = dirname(file_name)

        return file_name