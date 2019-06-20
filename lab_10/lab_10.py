from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGraphicsScene
from PyQt5.QtGui import QPen
import sys

max_size_x = 1150
max_size_y = 900

angle_x = 0
angle_y = 0
angle_z = 0

step_angle = 20

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("interface.ui", self)
        self.scene = QGraphicsScene(0, 0, max_size_x, max_size_y)
        self.canvas.setScene(self.scene)

        self.x_dict = dict()
        self.z_dict = dict()

        self.draw.clicked.connect(lambda: plot(self))

    def keyPressEvent(self, ev):
        global angle_y, angle_x, angle_z

        if ev.key() == 87: #W
            angle_y += step_angle
        elif ev.key() == 83: #S
            angle_y -= step_angle
        elif ev.key() == 65: #D
            angle_x -= step_angle
        elif ev.key() == 68: #A
            angle_x += step_angle
        elif ev.key() == 82: #R
            angle_z += step_angle
        elif ev.key() == 70: #F
            angle_z -= step_angle

        plot(self)


def func_1(x, z):
    return (sin(z))**2 - (cos(x))**2

def func_2(x, z):
    return sin(x) * cos(z)

def func_3(x, z):
    return fabs(sqrt((z**2 / 16 - x**2 / 25 + 1)*36))

def get_all(window):
    window.x_dict["x_min"] = window.x_min_sb.value()
    window.x_dict["x_max"] = window.x_max_sb.value()
    window.x_dict["x_step"] = window.x_step_sb.value()

    window.z_dict["z_min"] = window.z_min_sb.value()
    window.z_dict["z_max"] = window.z_max_sb.value()
    window.z_dict["z_step"] = window.z_step_sb.value()

def plot(window):
    plot_with_angles(window, angle_x, angle_y, angle_z)

def plot_with_angles(window, angle_x, angle_y, angle_z):
    window.scene.clear()
    if window.functions.currentIndex() == 0:
        draw_horizont(window, func_1, angle_x, angle_y, angle_z)
    elif window.functions.currentIndex() == 1:
        draw_horizont(window, func_2, angle_x, angle_y, angle_z)
    elif window.functions.currentIndex() == 2:
        draw_horizont(window, func_3, angle_x, angle_y, angle_z)

def sign(x):
    if x == 0:
        return 0

    return x / fabs(x)

def rotate_x(horiz, angle):
    angle *= pi / 180
    new_horiz = horiz.copy()
    new_horiz[1] = horiz[1] * cos(angle) - horiz[2] * sin(angle)
    new_horiz[2] = horiz[1] * sin(angle) + horiz[2] * cos(angle)

    return new_horiz

def rotate_y(horiz, angle):
    angle *= pi / 180
    new_horiz = horiz.copy()
    new_horiz[0] = horiz[0] * cos(angle) - horiz[2] * sin(angle)
    new_horiz[2] = horiz[0] * sin(angle) + horiz[2] * cos(angle)

    return new_horiz

def rotate_z(horiz, angle):
    angle *= pi / 180
    new_horiz = horiz.copy()
    new_horiz[0] = horiz[0] * cos(angle) - horiz[1] * sin(angle)
    new_horiz[1] = horiz[0] * sin(angle) + horiz[1] * cos(angle)

    return new_horiz

def transform(x, y, z, angle_x, angle_y, angle_z):
    global window
    arr = rotate_x([x, y, z], angle_x)
    arr = rotate_y(arr, angle_y)
    arr = rotate_z(arr, angle_z)

    # x1 = max_size_x / (window.x_dict["x_max"] - window.x_dict["x_min"]) * (arr[0] * window.x_dict["x_min"])
    # y1 = max_size_y - max_size_y / 10 * (arr[1] + 5)

    x1 = arr[0] * 48 + max_size_x / 2 - 200
    y1 = arr[1] * 48 + max_size_y / 2 - 200

    return int(x1 + 0.5), int(y1 + 0.5)

def draw_horizont(window, f, angle_x, angle_y, angle_z):
    h_screen = max_size_x
    v_screen = max_size_y

    top = [0 for i in range(h_screen)]
    bottom = [v_screen for i in range(h_screen)]

    x_left = -1
    y_left = -1
    x_right = -1
    y_right = -1

    get_all(window)

    z = window.z_dict["z_max"]
    while z >= window.z_dict["z_min"]:
        _x_prev = window.x_dict["x_min"]
        _y_prev = f(window.x_dict["x_min"], z)

        x_prev, y_prev = transform(_x_prev, _y_prev, z, angle_x, angle_y, angle_z)
        x_left, y_left, top, bottom = treatment_edge(x_prev, y_prev, x_left, y_left, top, bottom)
        p_flag = visible(x_prev, y_prev, top, bottom)

        _x = window.x_dict["x_min"]
        while _x <= window.x_dict["x_max"]:
            _y = f(_x, z)
            x, y = transform(_x, _y, z, angle_x, angle_y, angle_z)

            t_flag = visible(x, y, top, bottom)
            if t_flag == p_flag:
                if t_flag:
                    top, bottom = horizont(x_prev, y_prev, x, y, top, bottom)
            elif t_flag == 0:
                if p_flag == 1:
                    x_inter, y_inter = intersection(x_prev, y_prev, x, y, top)
                else:
                    x_inter, y_inter = intersection(x_prev, y_prev, x, y, bottom)
                top, bottom = horizont(x_prev, y_prev, x_inter, y_inter, top, bottom)
            elif t_flag == 1:
                if p_flag == 0:
                    x_inter, y_inter = intersection(x_prev, y_prev, x, y, top)
                    top, bottom = horizont(x_prev, y_prev, x_inter, y_inter, top, bottom)
                else:
                    x_inter, y_inter = intersection(x_prev, y_prev, x, y, top)
                    top, bottom = horizont(x_prev, y_prev, x_inter, y_inter, top, bottom)

                    x_inter, y_inter = intersection(x_prev, y_prev, x, y, bottom)
                    top, bottom = horizont(x_inter, y_inter, x, y, top, bottom)
            else:
                if p_flag == 0:
                    x_inter, y_inter = intersection(x_prev, y_prev, x, y, bottom)
                    top, bottom = horizont(x_prev, y_prev, x_inter, y_inter, top, bottom)
                else:
                    x_inter, y_inter = intersection(x_prev, y_prev, x, y, top)
                    top, bottom = horizont(x_prev, y_prev, x_inter, y_inter, top, bottom)
                    x_inter, y_inter = intersection(x_prev, y_prev, x, y, bottom)
                    top, bottom = horizont(x_inter, y_inter, x, y, top, bottom)

            p_flag = t_flag
            x_prev = x
            y_prev = y
            _x += window.x_dict["x_step"]

        x_right, y_right, top, bottom = treatment_edge(x_prev, y_prev, x_right, y_right, top, bottom)
        z -= window.z_dict["z_step"]

def draw(x1, y1, x2, y2):
    global window

    window.scene.addLine(x1, y1, x2, y2, QPen(Qt.black))

def treatment_edge(x, y, x_edge, y_edge, top, bottom):
    if x_edge == -1:
        x_edge = x
        y_edge = y
    else:
        top, bottom = horizont(x_edge, y_edge, x, y, top, bottom)
        x_edge = x
        y_edge = y

    return x_edge, y_edge, top, bottom

def visible(x, y, top, bottom):
    t_flag = 0

    if x < 0 or x >= len(bottom):
        return t_flag

    if y < top[x] and y > bottom[x]:
        t_flag = 0

    if y >= top[x]:
        t_flag = 1

    if y <= bottom[x]:
        t_flag = -1

    return t_flag

def horizont(x1, y1, x2, y2, top, bottom):
    if x2 < 0 or x2 >= len(top) or x1 < 0 or x1 >= len(top):
        return top, bottom
    x1 = int(x1)
    x2 = int(x2)

    if x2 < x1:
        x1, x2 = x2, x1
        y1, y2 = y2, y1

    if x2 - x1 == 0:
        top[x2] = max(top[x2], y2)
        bottom[x2] = min(bottom[x2], y2)
        draw(x1, y1, x2, y2)
    else:
        k = (y2 - y1) / (x2 - x1)
        x = x1
        while x < x2:
            y = int(k * (x - x1) + y1)
            top[x] = max(top[x], y)
            bottom[x] = min(bottom[x], y)

            if x >= 0 and x <= max_size_x :
                draw(x1, y1, x, y)
            x += 1

    return top, bottom

def intersection(x1, y1, x2, y2, horiz):
    if x2 < 0 or x2 >= len(horiz) or x1 < 0 or x1 >= len(horiz):
        return x1, y1

    x1 = int(x1)
    x2 = int(x2)

    d_y = y2 - y1
    d_x = x2 - x1
    d_a = horiz[x2] - horiz[x1]

    if d_x == 0:
        x_inter = x2
        y_inter = horiz[x2]
    elif d_y == d_a:
        x_inter = x1
        y_inter = y1
    else:
        #y_prev_inter = y_prev + k_prev*(x_inter - x)
        #y_cur_inter = y_cur + k_cur*(x_prev - x)
        #y_prev + k_prev(x_inter - x) = y_cur + m_cur*(x_inter - x)
        #x_inter*(k_prev - k_cur) = y_cur - y_prev + x_inter(k_prev - k_cur)
        #x_inter = x + (y_cur - y_prev) / (k_prev - k_cur) = x - (y_cur - y_prev) / (k_cur - k_prev)
        #x_inter = (y_cur - y_prev)*d_x / (d_y_cur - d_y_prev)

        k = d_y / d_x

        x_inter = x1 - int((d_x * (y1 - horiz[x1])) / (d_y - d_a))
        y_inter = int((x_inter - x1) * k + y1)

    return x_inter, y_inter

def main():
    global window

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()