import tkinter as tk
from tkinter import messagebox as mb

from .get_basepath import get_basepath
from .name_editor import NameEditor
from .slate_editor import SlateEditor
from .slate_column import SlateColumn
from .vote_editor import VoteEditor
from .ranking_column import RankingColumn
from .borda_count import borda_count
from .result_display import ResultDisplay
from .voting_saver import VotingSaver
from .voting_loader import VotingLoader

class Main(tk.Tk):
    def __init__(self):
        self.__has_voting = False
        self.__need_save = False
        self.__has_votes = False
        self.__button_width = 20
        self.__title = "ДО ВИБОРУ"
        self.__create_main_window()

    def __create_main_window(self):
        super().__init__(className = self.__title)
        self.iconbitmap(get_basepath("ranked_choice.ico"))
        self.geometry("+%d+%d" % (self.winfo_screenwidth() // 20, self.winfo_screenheight() // 6))
        self.protocol("WM_DELETE_WINDOW", self.__handle_quit)
        self.resizable(False, False)

        window_stretcher = tk.Label(master = self, text = " " * (len(self.__title) + 75))
        window_stretcher.grid(row = 0, column = 0, sticky = tk.N)

        self.__create_controls_frame()

    def __create_controls_frame(self):
        self.__controls_frame = tk.Frame(master = self)
        self.__controls_frame.grid(row = 0, column = 0)

        self.__create_voting_manipulation_group()
        self.__create_voting_persistence_group()
        self.__create_quit_group()

    def __create_voting_manipulation_group(self):
        voting_manipulation_group = tk.Frame(self.__controls_frame)

        self.__add_vote_button = tk.Button(master = voting_manipulation_group, width = self.__button_width, text = "Додати голос", state = tk.DISABLED)
        self.__add_vote_button.configure(command = lambda event = None: self.__handle_add_vote())
        self.__add_vote_button.pack(side = tk.TOP, anchor = tk.N)

        self.__show_result_button = tk.Button(master = voting_manipulation_group, width = self.__button_width, text = "Показати результат", state = tk.DISABLED)
        self.__show_result_button.configure(command = lambda event = None: self.__handle_show_result())
        self.__show_result_button.pack(side = tk.TOP, anchor = tk.N)

        voting_manipulation_group.grid(row = 0, column = 0, padx = 10, pady = 10)

    def __create_voting_persistence_group(self):
        voting_persistence_group = tk.Frame(master = self.__controls_frame)

        self.__new_voting_button = tk.Button(master = voting_persistence_group, width = self.__button_width, text = "Нове голосування")
        self.__new_voting_button.configure(command = lambda event = None: self.__handle_new_voting())
        self.__new_voting_button.pack(side = tk.TOP, anchor = tk.N)

        self.__load_voting_button = tk.Button(master = voting_persistence_group, width = self.__button_width, text = "Завантажити голосування")
        self.__load_voting_button.configure(command = lambda event = None: self.__handle_load_voting())
        self.__load_voting_button.pack(side = tk.TOP, anchor = tk.N)

        self.__save_voting_button = tk.Button(master = voting_persistence_group, width = self.__button_width, text = "Зберегти голосування", state = tk.DISABLED)
        self.__save_voting_button.configure(command = lambda event = None: self.__handle_save_voting())
        self.__save_voting_button.pack(side = tk.TOP, anchor = tk.N)

        voting_persistence_group.grid(row = 1, column = 0, padx = 10, pady = 10)

    def __create_quit_group(self):
        quit_group = tk.Frame(master = self.__controls_frame)

        self.__close_voting_button = tk.Button(master = quit_group, width = self.__button_width, text = "Закрити голосування", state = tk.DISABLED)
        self.__close_voting_button.configure(command = lambda event = None: self.__handle_close_voting())
        self.__close_voting_button.pack(side = tk.TOP, anchor = tk.N)

        self.__quit_button = tk.Button(master = quit_group, width = self.__button_width, text = "Вийти")
        self.__quit_button.configure(command = lambda event = None: self.__handle_quit())
        self.__quit_button.pack(side = tk.TOP, anchor = tk.N)      

        quit_group.grid(row = 2, column = 0, padx = 10, pady = 10)

    def __handle_add_vote(self):
        voter = self.__edit_name("Введіть ім'я виборця!")
        if not voter:
            return

        slate = self.__active_voting.slaves()[0].slate

        vote = self.__edit_vote(f"Прорангуйте вибір для {voter}!", {candidate:rank for rank, candidate in enumerate(slate, start = 1)})
        if not vote:
            return
        
        ranking_column = RankingColumn(self.__active_voting, slate, voter, vote)
        ranking_column.pack(side = tk.LEFT, anchor = tk.N)
        
        self.__update_voting_result()
        self.__has_votes = True
        self.__need_save = True
        self.__show_result_button["state"] = tk.NORMAL   

    def __handle_show_result(self):
        slate = self.__active_voting.slaves()[0].slate
        voting_name = self.__active_voting.slaves()[0].voting_name

        result_display = ResultDisplay(self, f"Результат голосування {voting_name}", slate, voting_name, self.__voting_result)

    def __handle_new_voting(self):
        if self.__confirm_no_active_voting():
            self.__create_active_voting()
 
    def __handle_load_voting(self):
        if self.__confirm_no_active_voting():
            self.__load_active_voting()    

    def __handle_save_voting(self):
        voting_name = self.__active_voting.slaves()[0].voting_name
        voting_saver = VotingSaver(self, voting_name, self.__active_voting)
        if voting_saver.result:
            self.__need_save = False

    def __handle_close_voting(self):
        if self.__confirm_no_active_voting():
            self.__discard_active_voting()

    def __handle_quit(self):
        if self.__confirm_no_active_voting():
            self.__discard_active_voting()
            self.destroy()

    def __confirm_no_active_voting(self):
        if self.__has_voting:
            if self.__need_save:
                if self.__confirm("Закрити незбережене голосування?"):
                    return True
                else:
                    return False
            else:
                return True
        else:
            return True

    def __create_active_voting(self):
        voting_name = self.__edit_name("Введіть назву голосування!")
        if not voting_name:
            return

        voting_slate = self.__edit_slate(f"Введіть варіанти вибору для голосування {voting_name}!")
        if not voting_slate:
            return

        self.__discard_active_voting()

        self.__active_voting = tk.Frame(self)
        self.__active_voting.grid(row = 0, column = 1, sticky = tk.N)

        slate_column = SlateColumn(self.__active_voting, voting_name, voting_slate)
        slate_column.pack(side = tk.LEFT, anchor = tk.N)

        self.__has_voting = True
        self.__need_save = True
        self.__add_vote_button["state"] = tk.NORMAL
        self.__save_voting_button["state"] = tk.NORMAL
        self.__close_voting_button["state"] = tk.NORMAL

    def __load_active_voting(self):
        voting_loader = VotingLoader(self)
        loaded_voting = voting_loader.result
        if loaded_voting:
            self.__discard_active_voting()
            self.__active_voting = loaded_voting
            self.__active_voting.grid(row = 0, column = 1, sticky = tk.N)

            self.__has_voting = True
            if len(self.__active_voting.slaves()) > 1:
                self.__has_votes = True
                self.__update_voting_result()
            self.__add_vote_button["state"] = tk.NORMAL
            if self.__has_votes:
                self.__show_result_button["state"] = tk.NORMAL
            self.__save_voting_button["state"] = tk.NORMAL
            self.__close_voting_button["state"] = tk.NORMAL

    def __discard_active_voting(self):
        if self.__has_voting:
            self.__active_voting.destroy()
            del self.__active_voting
        
        if self.__has_votes:
            del self.__voting_result

        self.__need_save = False
        self.__has_voting = False
        self.__has_votes = False
        self.__add_vote_button["state"] = tk.DISABLED
        self.__show_result_button["state"] = tk.DISABLED
        self.__save_voting_button["state"] = tk.DISABLED
        self.__close_voting_button["state"] = tk.DISABLED

    def __confirm(self, message):
        return mb.askokcancel(message = message)

    def __edit_name(self, title, name = None):
        name_editor = NameEditor(self, title, name)
        return name_editor.result
    
    def __edit_slate(self, title, slate = None):
        slate_editor = SlateEditor(self, title, slate)
        return slate_editor.result

    def __edit_vote(self, title, vote):
        vote_editor = VoteEditor(self, title, vote)
        return vote_editor.result

    def __update_voting_result(self):
        votes = [ranking_column.vote for ranking_column in self.__active_voting.slaves()[1:]]
        self.__voting_result = borda_count(votes)
