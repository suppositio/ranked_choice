import tkinter as tk

from .get_basepath import get_basepath
from .slate_column import SlateColumn
from .ranking_column import RankingColumn
from .voting_saver import VotingSaver

class ResultDisplay(tk.Toplevel):
    def __init__(self, master, title, slate, voter, vote):
        self.__master = master
        self.__title = title
        self.__slate = slate
        self.__voter = voter
        self.__vote = vote

        self.__default_width = len(self.__title) + 75

        self.__create_display_window()
        self.__create_result_display_frame()
        self.__create_display_controls_frame()

        self.wait_window()

    def __create_display_window(self):
        super().__init__(master = self.__master)
        self.iconbitmap(get_basepath("ranked_choice.ico"))
        self.title(self.__title)
        self.geometry("+%d+%d" % (self.winfo_screenwidth() // 3, self.winfo_screenheight() // 3))
        self.protocol("WM_DELETE_WINDOW", self.__handle_close)
        self.resizable(False, False)
        self.transient(self.__master)
        self.grab_set()

        window_stretcher = tk.Label(master = self, text = " " * self.__default_width)
        window_stretcher.grid(row = 0, column = 0, sticky = tk.N) 

    def __create_result_display_frame(self):
        self.__result_display_frame = tk.Frame(master = self)
        self.__result_display_frame.grid(row = 0, column = 0)        

        slate_column = SlateColumn(self.__result_display_frame, "", self.__slate)
        slate_column.pack(side = tk.LEFT, anchor = tk.N)

        ranking_column = RankingColumn(self.__result_display_frame, self.__slate, self.__voter, self.__vote)
        ranking_column.pack(side = tk.LEFT, anchor = tk.N)

    def __create_display_controls_frame(self):
        display_controls_frame = tk.Frame(self)
        display_controls_frame.grid(row = 1, column = 0)

        self.__save_button = tk.Button(master = display_controls_frame, text = "Зберегти")
        self.__save_button.configure(command = self.__handle_save)
        self.__save_button.grid(row = 0, column = 0)

        self.__close_button = tk.Button(master = display_controls_frame, text = "Закрити")
        self.__close_button.configure(command = self.__handle_close)
        self.__close_button.grid(row = 0, column = 1)

    def __handle_save(self):
        result_saver = VotingSaver(self, f"Результат гоосування {self.__voter}", self.__result_display_frame)
        _ = result_saver.result

    def __handle_close(self):
        self.destroy()

