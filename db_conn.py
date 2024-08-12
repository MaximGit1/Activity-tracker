import sqlite3

from config import settings


class DataBase:
    """
    Это класс базы данных, если нужно изменить настройки, то стоит изменить settings в config.py
    """
    __table_query = ("CREATE TABLE IF NOT EXISTS %table_name%( "
                     "id INTEGER PRIMARY KEY, title TEXT, color TEXT, time INTEGER )")

    def __init__(self):
        self._db_name = settings.db_name
        self._table_name = settings.table_name

    def __execute_sql(self, command: str) -> sqlite3.Cursor:
        with sqlite3.connect(f'other-files/{self._table_name}.db') as db:
            cursor = db.cursor()
            res = cursor.execute(command)
            db.commit()
        return res

    def create_table(self) -> None:
        command = self.__table_query.replace('%table_name%', self._table_name)
        self.__execute_sql(command)
        week_table_command = ("CREATE TABLE IF NOT EXISTS weekTable( "
                              "id INTEGER PRIMARY KEY, week_number INTEGER, last_commit date )")
        self.__execute_sql(week_table_command)
        self.__check_week_table_value()

    def add_row(self) -> None:
        # проверка на кол-во активностей
        title = input('Имя вашей активности==> ')
        # проверка на длинну
        color = input('Цвет активности ==> ')
        # проверка цвета
        command = f"INSERT INTO {self._table_name}(title, color, time) VALUES('{title}', '{color}', 0)"
        try:
            self.__execute_sql(command)
        except Exception as e:
            print('Произошла ошибка', e)
        else:
            print("Добавлена новая запись")

    def show_rows(self, mode: str) -> list[tuple[int, str, str, int]] | None:
        """
        :param mode: 'print' or 'plot'
        :return:
        """
        command = f"SELECT * FROM {self._table_name}"
        rows_all = (self.__execute_sql(command)).fetchall()
        if mode == 'plot':
            return rows_all
        rows = tuple(f'{activity[0]}. {activity[1]}' for activity in rows_all)
        print('=' * 30)
        for activity in rows:
            print(activity)
        print('=' * 30)

    def select_activity(self) -> int | None:
        self.show_rows(mode='print')
        activity = input('Активность ==> ')
        try:
            id_activity = int(activity)
        except Exception as e:
            print('Ошибка', e)
        else:
            return id_activity

    def __check_activity(self, id_activity: int) -> list[int, str, str, int]:
        command = f"SELECT * FROM {self._table_name} WHERE id = {id_activity}"
        activity: list[int, str, str, int] = self.__execute_sql(command).fetchall()
        return activity

    def delete_row(self) -> None:
        print("Удалить")
        id_activity: int = self.select_activity()
        if not id_activity or (self.__check_activity(id_activity) is None):
            print('Запись не удалена')
            return None
        print('step 3')
        command = f"DELETE FROM {self._table_name} WHERE id={id_activity}"
        self.__execute_sql(command)
        print('Запись удалена')

    def add_activity_time(self, seconds: int, activity: list[int, str, str, int] | int = None) -> None:
        if activity is None:
            activity = (self.select_activity())[0]
        elif type(activity) is int:
            activity = (self.__check_activity(activity))[0]
        print(activity)
        try:
            activity_time = activity[-1] + seconds
            activity_id = activity[0]
            command = f"UPDATE {self._table_name} SET time =  {activity_time} WHERE id = {activity_id}"
            self.__execute_sql(command)
        except Exception as e:
            print('Ошибка', e)
        else:
            print('Запись, вроде, обновлена')

    def calculate_percentage(self, id_activity: int) -> float:
        all_time_command = f"SELECT SUM(time) FROM {self._table_name}"
        activity_time_command = f"SELECT time FROM {self._table_name} WHERE id = {id_activity}"
        all_time = (self.__execute_sql(all_time_command)).fetchall()[0][0]
        activity_time = (self.__execute_sql(activity_time_command)).fetchall()[0][0]

        try:
            if all_time == activity_time:
                perc = 100
            else:
                perc = activity_time / all_time * 100
        except ZeroDivisionError:
            perc = 0
        return round(perc, 4)

    def get_all_activities_time(self) -> int:
        command = f"SELECT SUM(time) FROM {self._table_name}"
        time_sum = self.__execute_sql(command).fetchall()[0][0]
        return time_sum

    def reset_activities_time(self) -> None:
        command = f"UPDATE {self._table_name} SET time = 0"
        self.__execute_sql(command)

    def count_of_activities(self) -> int:
        command = f"SELECT COUNT(*) FROM {self._table_name}"
        activities_count = (self.__execute_sql(command)).fetchall()[0][0]
        return activities_count

    def select_colors_used(self) -> list[str]:
        command = f"SELECT color FROM {self._table_name}"
        colors = (self.__execute_sql(command)).fetchall()
        colors_list = []
        for c in colors:
            colors_list.append(c[0])
        return colors_list

    def __check_week_table_value(self) -> None:
        command1 = "Select * from weekTable"
        week = (self.__execute_sql(command1)).fetchall()
        if not week:
            command2 = f"INSERT INTO weekTable(week_number, last_commit) VALUES(1, '{self.__get_date()}')"
            self.__execute_sql(command2)

    @staticmethod
    def __get_date() -> str:
        from datetime import datetime
        return str(datetime.now().date())

    def get_delta_days(self, date_in_db: str | None = None) -> int:
        from datetime import datetime

        today = datetime.now().date()
        if date_in_db is None:
            date_in_db = self.__get_date_in_db()
        old = datetime.strptime(date_in_db, '%Y-%m-%d').date()
        res: int = (today - old).days
        return res

    def __get_date_in_db(self):
        command = "Select last_commit From weekTable"
        res: str = (self.__execute_sql(command)).fetchall()[0][0]
        return res

    def week_activity_switch(self) -> bool:
        if self.get_delta_days() >= 7:
            self.reset_activities_time()
            self.update_week_number()
            self.__update_last_commit()
            return True
        return False

    def get_week_number(self) -> int:
        command = "Select week_number From weekTable"
        while True:
            try:
                res = (self.__execute_sql(command)).fetchall()[0][0]
                return res
            except Exception as e:
                self.__check_week_table_value()
                print('Произошла ошибка', e)

    def update_week_number(self) -> None:
        number: int = self.get_week_number()
        command = f"UPDATE weekTable SET week_number = {number + 1}"
        self.__execute_sql(command)

    def __update_last_commit(self) -> None:
        command = f"UPDATE weekTable SET last_commit = '{self.__get_date()}'"
        print(command)
        self.__execute_sql(command)




db = DataBase()
db.create_table()

__all__ = ('db',)
