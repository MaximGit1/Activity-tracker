import sqlite3
from settings import MAX_ACTIVITIES, MAX_TITLE_LEN, COLORS_TUPLE

table_query = """CREATE TABLE IF NOT EXISTS activities(
    id INTEGER PRIMARY KEY,
    title TEXT,
    color TEXT,
    time INTEGER)"""

with sqlite3.connect('activityTracker.db') as db:
    cursor = db.cursor()
    cursor.execute(table_query)
    db.commit()


# insert

def del_row():
    id = input("the id of the record to change the activity ==> ")
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        record = cursor.execute(f"SELECT * FROM activities WHERE id = {id}").fetchall()
        if record:
            cursor.execute(f"""DELETE FROM activities WHERE id={id}""")
        else:
            print("The record could`t be found")
        db.commit()
    print('The record was successfully deleted')


def select_rows():
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        rows = cursor.execute("SELECT * FROM activities").fetchall()
        db.commit()
    return rows


def select_row(id):
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        row = cursor.execute(f"SELECT * FROM activities WHERE id = {id}").fetchall()
        db.commit()
    return row


def update_row(id, time_):
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE activities SET time =  {time_} WHERE id = {id}")
        db.commit()
    print('The data has been successfully updated')


def select_sum():
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        sum_ = cursor.execute(f"SELECT SUM(time) FROM activities").fetchall()[0][0]
        db.commit()
    return sum_


def reset_time():
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        cursor.execute(f"UPDATE activities SET time =  0")
        db.commit()


def count_of_acts():
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        act_count = cursor.execute(f"SELECT COUNT(*) FROM activities").fetchall()[0][0]
        db.commit()
    return act_count


def select_colors_used():
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        colors = cursor.execute("SELECT color FROM activities").fetchall()
        db.commit()
    colors_list = []
    for c in colors:
        colors_list.append(c[0])
    return colors_list


def insert_values():
    status = True
    if count_of_acts() >= MAX_ACTIVITIES:
        print('You have exceeded the limit on the number of activities!')
        return None
    title = input('Enter the name of the activity==> ')
    if len(title) > MAX_TITLE_LEN or len(title) < 3:
        print('You have exceeded the limit on the length of the activity name. or length <= 3')
        return None
    print('Enter the name of the color.\n all colors can be viewed on the website matplotlib colors or\n'
          'https://matplotlib.org/stable/_images/sphx_glr_named_colors_003.png\n')
    color = input('color ==> ')
    if color in ['', ' ']:
        color = list(set(COLORS_TUPLE).difference(set(select_colors_used())))[0]
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        cursor.execute(f"""INSERT INTO activities(title, color, time)
         VALUES('{title}', '{color}', 0)""")
        db.commit()
    print("A new activity has been successfully added")

def calculate_percentage(id_):
    with sqlite3.connect('activityTracker.db') as db:
        cursor = db.cursor()
        all_time = cursor.execute(f"SELECT SUM(time) FROM activities WHERE not id = {id_}").fetchall()[0][0]
        act_time = cursor.execute(f"SELECT time FROM activities WHERE id = {id_}").fetchall()[0][0]
        db.commit()
    try:
        perc = act_time / all_time * 100
    except ZeroDivisionError:
        perc = 0
    return round(perc, 4)

