import datetime
import dataBase
from photo import take_photo
from plot import build_graph


class TimeFormat:
    def __get_time(self, id):
        title = dataBase.select_row(id)[0][1]
        print(f'The {title} activity is running')
        start = datetime.datetime.now()
        input('End the activity...')
        finish = datetime.datetime.now()
        result = self.__format_time(finish - start)
        return result

    def __format_time(self, time_: datetime):  # 0:00:02.346950
        time = [*str(time_).split(':')[:-1], (str(time_).split(':')[-1].split('.')[0])]
        time = list(map(int, time))
        return time[0] * 360 + time[1] * 60 + time[2]

    def __get_activity(self) -> int:  # [(1, 'python', 'red', 0), (2, 'books', 'yellow', 0)]
        activities = dataBase.select_rows()
        string = ''.join(tuple(map(lambda x: f'{x[0]}. {x[1]}\n', activities)))
        print('-' * 40)
        print(string)
        while True:
            choice = input('Your activity ==> ')
            if int(choice) in (range(1, len(activities) + 1)):
                return choice
            print('There is no such activity!')

    def __str_to_int(self, str_) -> int:  # for the future
        try:
            int_ = int(str_)
        except ValueError:
            print('There is no such activity!')
        else:
            return int_

    def __write_time(self, id: int, time_: int):
        dataBase.update_row(id, time_)

    def __write(self):
        id_ = self.__get_activity()
        time_ = dataBase.select_row(id_)[0][3]
        time_add = self.__get_time(id_)
        new_time = time_ + time_add
        self.__write_time(id_, new_time)

    def __sql(self):
        choice = input("What do you want to do?\n1. delete activity\n2. add activity\n3. add the activity time\n"
                       "4. reset the time of all activities\n==> ")
        match choice:
            case '1':
                activities = dataBase.select_rows()
                string = ''.join(tuple(map(lambda x: f'{x[0]}. {x[1]}\n', activities)))
                print('-' * 40)
                print(string)
                dataBase.del_row()
            case '2':
                dataBase.insert_values()
            case '3':
                id_ = self.__get_activity()
                time_ = dataBase.select_row(id_)[0][3]
                time_add = int(input('add activity time ==>'))
                time_new = time_ + time_add
                self.__write_time(id_, time_new)
            case '4':
                if input('Are you sure? Y/N ==> ') == 'Y':
                    dataBase.reset_time()
                    print('You have reset the time!')

    def start(self):
        choice = input("1. tracker\n2. change activities\n3. get statistic\n4. create a database\n==> ")
        match choice:
            case '1':
                self.__write()
            case '2':
                self.__sql()
            case '3':
                build_graph()
                take_photo()
                print('stat.jpg has been saved')
            case '4':
                print('When changing the activities, the database will be created')


tf = TimeFormat()
tf.start()
