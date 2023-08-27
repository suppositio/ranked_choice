from tkinter import messagebox as mb
from openpyxl import Workbook

from .path_editor import PathEditor

class VotingSaver:
    def __init__(self, master, name, voting):
        self.__master = master
        self.__name = name
        self.__voting = voting
    
    @property
    def result(self):
        self.__save_path = self.__get_save_path()
        if not self.__save_path:
            return False
        self.__create_data_array()
        if not self.__data_array:
            return False
        while not (write_result := self.__write_data()):
            if self.__confirm_retry():
                self.__save_path = self.__get_save_path()
                if not self.__save_path:
                    return False
            else:
                return False
 
        mb.showinfo(message = f"{self.__name} збережено")
        return write_result
    
    def __get_save_path(self):
        save_path_editor = PathEditor(self.__master, "Excel", "xlsx", PathEditor.SAVE)
        return save_path_editor.result
    
    def __create_data_array(self):
        self.__data_array = [list(data_row) for data_row in zip(*self.__voting.slaves())]

    def __write_data(self):
        try:
            workbook = Workbook()
            sheet = workbook.active
            sheet.title = self.__name

            for row_index, row in enumerate(self.__data_array, start = 1):
                for col_index, value in enumerate(row, start = 1):
                    cell = sheet.cell(row = row_index, column = col_index)
                    cell.value = value

            workbook.save(self.__save_path)
            return True

        except Exception:
            return False

    def __confirm_retry(self):
        return mb.askokcancel(message = "Не вдалося зберегти файл.\nСпробувати ще раз?")
