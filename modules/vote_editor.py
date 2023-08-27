import tkinter as tk

from .get_basepath import get_basepath

class VoteEditor(tk.Toplevel):
    def __init__(self, master, title, vote):
        self.__master = master
        self.__title = title
        self.__vote = vote
        self.__default_width = len(self.__title) + 75
        self.__button_width = len(max(self.__vote.keys(), key = len))

    @property
    def result(self):
        self.__process()
        return self.__result

    def __process(self):
        self.__create_editor_window()
        self.__create_ranking_frame()
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

    def __create_ranking_frame(self):
        self.__ranking_frame = tk.Frame(master = self)
        self.__ranking_frame.grid(row = 0, column = 0)

        self.__create_stage_frame()
        self.__create_result_frame()

    def __create_stage_frame(self):
        outer_stage_frame = tk.Frame(master = self.__ranking_frame)
        outer_stage_frame.grid(row = 0, column = 0, sticky = tk.N)

        tk.Label(master = outer_stage_frame, text = "Доступно").grid(row = 0, column = 0, sticky = tk.N)

        self.__stage_frame = tk.Frame(master = outer_stage_frame)
        self.__stage_frame.grid(row = 1, column = 0, sticky = tk.N)

        candidates = self.__ordered_candidates(self.__vote)
        for candidate in candidates:
            stage_button = tk.Button(master = self.__stage_frame, text = candidate, width = self.__button_width)
            stage_button.configure(command = lambda inst = stage_button, event = None: self.__add_result_button(inst))
            stage_button.pack(side = tk.TOP, anchor = tk.N)
        
        self.__stage_frame.update_idletasks()
        self.__frame_width = self.__stage_frame.winfo_width()
        self.__frame_height = self.__stage_frame.winfo_height()

    def __create_result_frame(self):
        outer_result_frame = tk.Frame(master = self.__ranking_frame)
        outer_result_frame.grid(row = 0, column = 1, sticky = tk.N)

        tk.Label(master = outer_result_frame, text = "Проранговано").grid(row = 0, column = 0, sticky = tk.N)
 
        self.__result_frame = tk.Frame(master = outer_result_frame, width = self.__frame_width, height = self.__frame_height)
        self.__result_frame.grid(row = 1, column = 0, sticky = tk.N)
        self.__result_frame.pack_propagate(False)

    def __create_result_controls_frame(self):
        self.__result_controls_frame = tk.Frame(self)
        self.__result_controls_frame.grid(row = 1, column = 0, columnspan = 2)

        self.__ok_button = tk.Button(master = self.__result_controls_frame, text = "OK")
        self.__ok_button.configure(command = self.__handle_ok)
        if self.__stage_frame.slaves():
            self.__ok_button["state"] = tk.DISABLED
        self.__ok_button.grid(row = 0, column = 0)

        self.__cancel_button = tk.Button(master = self.__result_controls_frame, text = "Скасувати")
        self.__cancel_button.configure(command = self.__handle_cancel)
        self.__cancel_button.grid(row = 0, column = 1)

    def __add_result_button(self, stage_button):
        result_button = tk.Button(master = self.__result_frame, text = stage_button["text"], width = self.__button_width)
        result_button.configure(command = lambda inst = result_button, event = None: self.__remove_result_button(inst))
        result_button.pack(side = tk.TOP, anchor = tk.N)
        stage_button.destroy()
        if len(self.__result_frame.slaves()) == len(self.__vote):
            self.__ok_button["state"] = tk.NORMAL

    def __remove_result_button(self, result_button):
        stage_button = tk.Button(master = self.__stage_frame, text = result_button["text"], width = self.__button_width)
        stage_button.configure(command = lambda inst = stage_button, event = None: self.__add_result_button(inst))
        stage_button.pack(side = tk.TOP, anchor = tk.N)
        result_button.destroy()
        self.__ok_button["state"] = tk.DISABLED

    def __handle_ok(self):
        self.__result = {result_button["text"]:rank for rank, result_button in enumerate(self.__result_frame.slaves(), start = 1)}
        self.destroy()

    def __handle_cancel(self):
        self.__result = None
        self.destroy()

    @staticmethod
    def __ordered_candidates(vote):
        ranks_and_candidates = [(rank, i, candidate) for i, (candidate, rank) in enumerate(vote.items())]
        ranks_and_candidates.sort(key = lambda x: (x[0], x[1]))
        for rank, i, candidate in ranks_and_candidates:
            yield candidate
