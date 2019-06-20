import lab_04
from PyQt5.QtGui import QImage
import time
import matplotlib.pyplot as plt

circle = 0
ellipse = 1
step_b = 1.2
n = 10

def count_time_circle(window):
    r0 = 10
    step = 1.21
    r_end = 15000
    r = r0

    window.image = QImage(30000, 30000, QImage.Format_ARGB32_Premultiplied)
    center = 15000

    all_time = dict()
    all_time["br"] = list()
    all_time["mid"] = list()
    all_time["canon"] = list()
    all_time["param"] = list()
    all_time["standart"] = list()
    all_time["r"] = list()

    while r <= r_end:
        all_time["r"].append(r)

        _time = 0
        for i in range(n):
            b = time.time()
            lab_04.circle_param(window, r, center, center)
            end = time.time()
            _time += end - b
        _time /= n
        all_time["param"].append(_time)

        _time = 0
        for i in range(n):
            b = time.time()
            lab_04.circle_canon(window, r, center, center)
            end = time.time()
            _time += end - b
        _time /= n
        all_time["canon"].append(_time)

        _time = 0
        for i in range(n):
            b = time.time()
            lab_04.circle_br(window, r, center, center)
            end = time.time()
            _time += end - b
        _time /= n

        all_time["br"].append(_time)

        _time = 0
        for i in range(n):
            b = time.time()
            lab_04.circle_mid(window, r, center, center)
            end = time.time()
            _time += end - b
        _time /= n

        all_time["mid"].append(_time)

        _time = 0
        for i in range(n):
            b = time.time()
            window.scene.addEllipse(center - r, center - r, 2*r, 2*r, window.pen_c)
            end = time.time()
            _time += end - b
        _time /= n

        all_time["standart"].append(_time)

        r *= step
        r = round(r)

    return all_time

def count_time_ellipse(window):
    a = 10
    b = 10
    step_a = 1.21
    end_int = 15000

    window.image = QImage(30000, 30000, QImage.Format_ARGB32_Premultiplied)
    center = 15000

    all_time = dict()
    all_time["br"] = list()
    all_time["mid"] = list()
    all_time["canon"] = list()
    all_time["param"] = list()
    all_time["standart"] = list()
    all_time["r"] = list()

    while a <= end_int and b <= end_int:
        all_time["r"].append(a)

        _time = 0
        for i in range(n):
            beg = time.time()
            lab_04.ellipse_param(window, a, b, center, center)
            end = time.time()
            _time += end - beg
        _time /= n

        all_time["param"].append(_time)

        _time = 0
        for i in range(n):
            beg = time.time()
            lab_04.ellipse_canon(window, a, b, center, center)
            end = time.time()
            _time += end - beg
        _time /= n

        all_time["canon"].append(_time)

        _time = 0
        for i in range(n):
            beg = time.time()
            lab_04.ellipse_br(window, a, b, center, center)
            end = time.time()
            _time += end - beg
        _time /= n

        all_time["br"].append(_time)

        _time = 0
        for i in range(n):
            beg = time.time()
            lab_04.ellipse_mid(window, a, b, center, center)
            end = time.time()
            _time += end - beg
        _time /= n

        all_time["mid"].append(_time)

        _time = 0
        for i in range(n):
            beg = time.time()
            window.scene.addEllipse(center - a, center - b, 2*a, 2*b, window.pen_c)
            end = time.time()
            _time += end - beg
        _time /= n

        all_time["standart"].append(_time)

        a *= step_a
        a = round(a)

        b *= step_b
        b = round(b)
    return all_time

def save_gr(time, figure):
    plt.plot(time["r"], time["canon"], "b.:", label="Каноническое")
    plt.plot(time["r"], time["param"], "g.:", label="Параметрическое")
    plt.plot(time["r"], time["br"], "r.:", label="Брезенхем")
    plt.plot(time["r"], time["mid"], "y.:", label="Средняя точка")
    plt.plot(time["r"], time["standart"], "m.:", label="Библиотечный")

    if figure == circle:
        plt.xlabel('Радиус окружности, пикс')
    else:
        plt.xlabel("A эллипса, пикс, B *= " + str(step_b) + ", B0 = 10")
    plt.ylabel('Время построения, c')
    plt.grid()
    plt.legend(loc="best")

    if figure == circle:
        plt.savefig('circle_time.png', format='png')
    else:
        plt.savefig('ellipse_time.png', format='png')

    plt.clf()

if __name__ == "__main__":
    app = lab_04.QtWidgets.QApplication(lab_04.sys.argv)
    window = lab_04.Window()

    circle_time = count_time_circle(window)
    save_gr(circle_time, circle)

    ellipse_time = count_time_ellipse(window)
    save_gr(ellipse_time, ellipse)
