import tkinter as tk

class RankingColumn(tk.Frame):
    def __init__(self, master, slate, voter = "", vote = None):
        super().__init__(master)
        self.__slate = slate
        self.__voter = voter

        if not vote:
            self.__vote = {candidate:rank for rank, candidate in enumerate(self.__slate, start = 1)}
        else:
            self.__vote = vote

        self.__max_width = max(len(self.__voter), max(len(str(rank)) for rank in self.__vote.values()))

        tk.Label(master = self).pack(side = tk.TOP, anchor = tk.N)

        for candidate in self.__slate:
            tk.Label(master = self, bg = "white").pack(side = tk.TOP, anchor = tk.N)

        self.__update_display()

    @property
    def vote(self):
        return self.__vote 

    @vote.setter
    def vote(self, vote):
        self.__vote = vote
        self.__max_width = max(self.__max_width, max(len(str(rank)) for rank in self.__vote.values()))
        self.__update_display()

    @property
    def voter(self):
        return self.__voter
    
    @voter.setter
    def voter(self, voter):
        self.__voter = voter
        self.__max_width = max(self.__max_width, len(self.__voter))
        self.__update_display()

    def __getitem__(self, index):
        if index == 0:
            return self.__voter
        else:
            return self.__vote[self.__slate[index - 1]]

    def __update_display(self):
        self.slaves()[0]["text"] = self.__voter
        self.slaves()[0]["width"] = self.__max_width
        for candidate, rank_label in zip(self.__slate, self.slaves()[1:]):
            rank_label["text"] = str(self.__vote[candidate])
            rank_label["width"] = self.__max_width