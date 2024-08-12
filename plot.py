from matplotlib import pyplot as plt

from config import settings, BASE_DIR
from db_conn import db

activities_list = db.show_rows(mode='plot')
activities_correct = []

for activity in activities_list:
    if activity[3] >= settings.min_time and db.calculate_percentage(activity[0]) >= settings.min_percentage:
        activities_correct.append(activity)
activities = activities_correct

act_weight = [act[3] for act in activities]
act_labels = [act[1] for act in activities]
act_colors = [act[2] for act in activities]


def correct_time(time_: int) -> str:
    h = int(time_ // 60 // 60)
    m = int(time_ // 60 - h * 60)
    return f'{h:0>2}:{m:0>2}'


act_labels_time = list(map(correct_time, act_weight))


def draw_pie() -> None:
    plt.pie(act_weight, labels=act_labels_time, colors=act_colors, radius=9)
    plt.legend(bbox_to_anchor=(-0.3, 0.835), loc='upper left', borderaxespad=0, title='Time')  # /////
    plt.pie([10, 10], colors=(['white'] * 2), radius=9)
    plt.pie([13, 7], colors=(['white'] * 2), radius=8)
    plt.pie([17, 48], colors=(['white'] * 2), radius=8)
    plt.pie(act_weight, labels=act_labels, autopct='%1.1f%%', colors=act_colors, radius=0.9)
    plt.savefig(f'{BASE_DIR}/other-files/trash/pie.png', dpi=300)
    # вместо сохранения спопировать в оперативку


def draw_barh() -> None:
    plt.barh(0, settings.goal, color='blue', height=0.2)
    left = 0
    for i in range(0, len(act_weight)):
        plt.barh(1, act_weight[i], color=act_colors[i], left=left, height=0.2)
        left += act_weight[i]
    plt.xticks([])
    plt.yticks([])
    plt.savefig(f'{BASE_DIR}/other-files/trash/barh.png', dpi=300)


def build_graph():
    draw_barh()
    draw_pie()

__all__ = ('build_graph',)


if __name__ == '__main__':
    build_graph()



