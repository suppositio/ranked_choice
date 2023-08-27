import tkinter as tk
from tkinter import messagebox as mb

from .get_basepath import get_basepath

class SlateEditor(tk.Toplevel):
    def __init__(self, master, title, slate = None):
        self.__master = master
        self.__title = title
        self.__default_width = len(self.__title) + 75
        if slate:
            self.__slate = slate
        else:
            self.__slate = []

    @property
    def result(self):
        self.__process()
        return self.__result

    def __process(self):
        self.__create_editor_window()
        self.__create_entry_frame()
        self.__create_slate_frame()
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

    def __create_entry_frame(self):
        self.__entry_frame = tk.Frame(master = self)
        self.__entry_frame.grid(row = 0, column = 0)        

        self.__create_entry()
        self.__create_add_button()

    def __create_entry(self):
        self.__entry_string = tk.StringVar(master = self)
        self.__entry_string.trace("w", lambda name, index, mode: self.__handle_change_entry())

        slate_entry = tk.Entry(master = self.__entry_frame, width = self.__default_width, textvariable = self.__entry_string)
        slate_entry.bind("<Return>", lambda event: self.__handle_add())
        slate_entry.grid(row = 0, column = 0)

    def __create_add_button(self):
        self.__add_button = tk.Button(master = self.__entry_frame, text = "Додати варіант вибору")
        self.__add_button.configure(command = self.__handle_add)
        if not self.__entry_string.get():
            self.__add_button["state"] = tk.DISABLED
        self.__add_button.grid(row = 1, column = 0)

    def __create_slate_frame(self):
        self.__slate_frame = tk.Frame(master = self)
        self.__slate_frame.grid(row = 1, column = 0, sticky = tk.NW)

        for slate_item in self.__slate:
            slate_label = tk.Label(master = self.__slate_frame, text = slate_item)
            slate_label.pack(side = tk.TOP, anchor = tk.N)

    def __create_result_controls_frame(self):
        self.__result_controls_frame = tk.Frame(self)
        self.__result_controls_frame.grid(row = 2, column = 0)

        self.__ok_button = tk.Button(master = self.__result_controls_frame, text = "OK")
        self.__ok_button.configure(command = self.__handle_ok)
        if not self.__slate_frame.slaves():
            self.__ok_button["state"] = tk.DISABLED
        self.__ok_button.grid(row = 0, column = 0)

        self.__cancel_button = tk.Button(master = self.__result_controls_frame, text = "Скасувати")
        self.__cancel_button.configure(command = self.__handle_cancel)
        self.__cancel_button.grid(row = 0, column = 1)

    def __handle_change_entry(self):
        if self.__entry_string.get():
            self.__add_button["state"] = tk.NORMAL
        else:
            self.__add_button["state"] = tk.DISABLED

    def __handle_add(self):
        candidate = self.__entry_string.get()
        if candidate not in self.__slate:
            self.__slate.append(candidate)
            slate_label = tk.Label(master = self.__slate_frame, text = candidate, justify = tk.LEFT)
            slate_label.pack(side = tk.TOP, anchor = tk.NW)
            self.__ok_button["state"] = tk.NORMAL
        else:
            mb.showerror("Помилка!", "Варіанти вибору не можуть повторюватися!")
 
        self.__entry_string.set("")
        self.__add_button["state"] = tk.DISABLED
 
    def __handle_ok(self):
        self.__result = self.__slate
        self.destroy()        

    def __handle_cancel(self):
        self.__result = None
        self.destroy()      
