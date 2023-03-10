from abc import ABC, abstractmethod
import openpyxl

from database.manager import DbManager


class Parser(ABC):
    @abstractmethod
    def parse_data(self):
        pass


class ExcelParser(Parser):
    _db_manager = None

    def __init__(self, filepath, interval):
        self._sheet = openpyxl.load_workbook(filepath).active[interval]

    def set_db_manager(self, db_manager: DbManager):
        self._db_manager = db_manager

    def parse_data(self):
        if isinstance(self._db_manager, DbManager):
            self._db_manager.create_data_from_sheet(self._sheet)
