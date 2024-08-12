from datetime import datetime

from db_conn import db
from plot import build_graph
from photo import take_photo


class Tracker:
    def __get_add_time(self) -> tuple[int, int]:
        choice_activity_id = db.select_activity()
        start = datetime.now()
        input('Закончить активность...')
        finish = datetime.now()
        activity_timedelta = self.__format_time(finish - start)
        return choice_activity_id, activity_timedelta

    def __format_time(self, time_: datetime):  # 0:00:02.346950
        time = [*str(time_).split(':')[:-1], (str(time_).split(':')[-1].split('.')[0])]
        time = list(map(int, time))
        return time[0] * 360 + time[1] * 60 + time[2]

    def __str_to_int(self, str_) -> int:  # for the future
        try:
            int_ = int(str_)
        except ValueError:
            print('There is no such activity!')
        else:
            return int_

    def __write_time(self, id_activity: int, time_: int):
        db.add_activity_time(time_, id_activity)

    def start(self):
        choice = input("1. Трекер\n2. get statistic\n==> ")
        match choice:
            case '1':
                self.__write()
            case '2':
                build_graph()
                take_photo()

    def __write(self):
        data_ = self.__get_add_time()
        print(data_)
        id_activity = data_[0]
        time_ = data_[1]
        self.__write_time(id_activity, time_)

if __name__ == '__main__':
    tracker = Tracker()
    if db.week_activity_switch():  # сделать обнуление активности
        build_graph()
        take_photo()
    while True:
        tracker.start()


