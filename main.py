from database.accessor import SQLiteAccessor
from database.manager import ReportManager
from excel.parser import ExcelParser
from excel.editor import ExcelTotalEditor


def main():
    db_accessor = SQLiteAccessor("database.sqlite")  # creating an accessor to connect to the database
    db_accessor.delete_tables()  # deleting tables to avoid data repetition after restart
    db_accessor.create_tables()

    db_manager = ReportManager(db_accessor)  # creating a database table manager

    parser = ExcelParser("excel_data.xlsx", "A4:J23")  # creating an excel parser specifying a data range
    parser.set_db_manager(db_manager)
    parser.parse_data()

    db_manager.update_random_date()  # adding a random date to all rows of the main table
    total_data = db_manager.get_total_by_date()  # getting of the settlement total by grouped date
    editor = ExcelTotalEditor()
    editor.data_to_excel(total_data)
    editor.save("result.xlsx")


if __name__ == "__main__":
    main()
