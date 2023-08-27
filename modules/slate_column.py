import tkinter as tk

class SlateColumn(tk.Frame):
    def __init__(self, master, voting_name, slate):
        super().__init__(master)
        self.__voting_name = voting_name
        self.__slate = slate
 
        tk.Label(master = self, text = self.__voting_name, justify = tk.LEFT).pack(side = tk.TOP, anchor = tk.NW)
        for candidate in self.__slate:
            tk.Label(master = self, text = candidate, justify = tk.LEFT).pack(side = tk.TOP, anchor = tk.NW)

    @property
    def voting_name(self):
        return self.__voting_name

    @property
    def slate(self):
        return self.__slate
    
    def __getitem__(self, index):
        if index == 0:
            return self.__voting_name
        else:
            return self.__slate[index - 1]
