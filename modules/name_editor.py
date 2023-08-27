import tkinter as tk

from .get_basepath import get_basepath

class NameEditor(tk.Toplevel):
    def __init__(self, master, title, name = None):
        self.__master = master
        self.__title = title
        self.__name = name
        self.__default_width = len(self.__title) + 75
        if name:
            self.__entry_width = max(self.__default_width, len(name))
        else:
            self.__entry_width = self.__default_width

    @property
    def result(self):
        self.__process()
        return self.__result

    def __process(self):
        self.__create_editor_window()
        self.__create_entry()
        self.__create_result_controls_frame()

        self.wait_window()

    def __create_editor_window(self):
        super().__init__(master = self.__master)
        self.iconbitmap(get_basepath("ranked_choice.ico"))
        self.title(self.__title)
        self.geometry("+%d+%d" % (self.winfo_screenwidth() // 3, self.winfo_screenheight() // 3))
        self.protocol("WM_DELETE_WINDOW", self.__handle_cancel)
        self.resizable(False, False)
        self.transient(self.__master)
        self.grab_set()

        window_stretcher = tk.Label(master = self, text = " " * self.__default_width)
        window_stretcher.grid(row = 0, column = 0, sticky = tk.N)

    def __create_entry(self):
        self.__entry_string = tk.StringVar(master = self, value = self.__name)
        self.__entry_string.trace("w", lambda name, index, mode: self.__handle_change_entry())

        name_entry = tk.Entry(master = self, width = self.__entry_width, textvariable = self.__entry_string)
        name_entry.grid(row = 0, column = 0, padx = 10, pady = 10)

    def __create_result_controls_frame(self):
        self.__result_controls_frame = tk.Frame(self)
        self.__result_controls_frame.grid(row = 2, column = 0)

        self.__ok_button = tk.Button(master = self.__result_controls_frame, text = "OK")
        self.__ok_button.configure(command = self.__handle_ok)
        if not self.__entry_string.get():
            self.__ok_button["state"] = tk.DISABLED
        self.__ok_button.grid(row = 0, column = 0)

        self.__cancel_button = tk.Button(master = self.__result_controls_frame, text = "Скасувати")
        self.__cancel_button.configure(command = self.__handle_cancel)
        self.__cancel_button.grid(row = 0, column = 1)

    def __handle_change_entry(self):
        if self.__entry_string.get():
            self.__ok_button["state"] = tk.NORMAL
        else:
            self.__ok_button["state"] = tk.DISABLED

    def __handle_ok(self):
        self.__result = self.__entry_string.get()
        self.destroy()

    def __handle_cancel(self):
        self.__result = None
        self.destroy()
