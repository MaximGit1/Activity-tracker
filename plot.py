from matplotlib import pyplot as plt
from dataBase import select_rows as s_rows, calculate_percentage as calc
from settings import GOAL, MIN_TIME, MIN_PERCENTAGE

activities = s_rows()  ##[(1, 'python', 'red', 100), (2, 'books', 'yellow', 126)]
activities_correct = []
for i in activities:
    if i[3] >= MIN_TIME and calc(i[0]) >= MIN_PERCENTAGE:
        activities_correct.append(i)
activities = activities_correct
act_weight = [act[3] for act in activities]
act_labels = [act[1] for act in activities]
act_colors = [act[2] for act in activities]



def correct_time(time_):
    h = int(time_ // 3600)
    m = int((time_ - h * 3600) / 60)
    return f'{h:0>2}:{m:0>2}'


act_labels_time = list(map(correct_time, act_weight))


def draw_pie():
    plt.pie(act_weight, labels=act_labels_time, colors=act_colors, radius=9)
    plt.legend(bbox_to_anchor=(-0.3, 0.835), loc='upper left', borderaxespad=0, title='Time')
    plt.pie([10, 10], colors=(['white'] * 2), radius=9)
    plt.pie([13, 7], colors=(['white'] * 2), radius=8)
    plt.pie([17, 48], colors=(['white'] * 2), radius=8)
    plt.pie(act_weight, labels=act_labels, autopct='%1.1f%%', colors=act_colors, radius=0.9)
    plt.savefig('./fig/pie.png', dpi=300)


def draw_barh():
    plt.barh(0, GOAL, color='blue', height=0.2)
    left = 0
    for i in range(0, len(act_weight)):
        plt.barh(1, act_weight[i], color=act_colors[i], left=left, height=0.2)
        left += act_weight[i]
    plt.xticks([])
    plt.yticks([])
    plt.savefig('./fig/barh.png', dpi=300)


def build_graph():
    draw_barh()
    draw_pie()

