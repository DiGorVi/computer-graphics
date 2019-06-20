from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPen, QColor
import numpy as np
import sys

max_size_x = 1150
max_size_y = 900

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("interface.ui", self)
        self.scene = Scene(0, 0, max_size_x, max_size_y)
        self.canvas.setScene(self.scene)

        self.cutter_color = QColor(Qt.black)
        self.polygon_color = QColor(Qt.red)
        self.cut_polygon_color = QColor(Qt.green)

        self.cutter = list()
        self.polygons = list()
        self.cur_polygon = list()

        self.full_polygon = False
        self.isConvex = False
        self.direction = -1

        self.add_polygon_bt.clicked.connect(lambda: add_polygon_sb(self))
        self.add_cutter_bt.clicked.connect(lambda: add_cutter_sb(self))
        self.del_cutter_bt.clicked.connect(lambda: del_cutter(self))
        self.close_bt.clicked.connect(lambda: close_cutter())
        self.close_polygon_bt.clicked.connect(lambda: close_polygon())
        self.del_polygon_bt.clicked.connect(lambda: del_last_polygon(self))

        self.color_polygon_bt.clicked.connect(lambda: get_polygon_color(self))
        self.color_cutter_bt.clicked.connect(lambda: get_cutter_color(self))
        self.color_cut_polygon_bt.clicked.connect(lambda: get_cut_polygon_color(self))
        self.clear_bt.clicked.connect(lambda: clear(self))

        self.first_color_buttons()

    def first_color_buttons(self):
        self.color_polygon_bt.setStyleSheet("background-color:rgb" \
                + color_in_str(self.polygon_color.getRgb()))
        self.color_cut_polygon_bt.setStyleSheet("background-color:rgb" \
                + color_in_str(self.cut_polygon_color.getRgb()))
        self.color_cutter_bt.setStyleSheet("background-color:rgb" \
                + color_in_str(self.cutter_color.getRgb()))

class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
            add_cutter_event(event.scenePos())
        elif  event.buttons() == Qt.RightButton and event.modifiers() == Qt.ControlModifier:
            close_cutter()
        elif event.buttons() == Qt.LeftButton:
            add_polygon_event(event.scenePos())
        elif event.buttons() == Qt.RightButton:
            close_polygon()

def add_polygon_event(point):
    add_polygon(point)

def add_polygon_sb(window):
    x = window.x1_sb.value()
    y = window.y1_sb.value()

    add_polygon(QPointF(x, y))

def add_polygon(point):
    global window

    if window.how_draw.currentIndex() == 0:
        window.cur_polygon.append(point)
    else:
        window.cur_polygon.append(draw_on_rib(point))
    cut_all(window)

def draw_on_rib(point):
    index = window.how_draw.currentIndex()

    m = window.cutter[index - 1].x() - window.cutter[index].x()

    if m != 0:
        k = (window.cutter[index - 1].y() - window.cutter[index].y()) / m
        b = window.cutter[index - 1].y() - k * window.cutter[index - 1].x()
        return QPointF(point.x(), k * point.x() + b)
    else:
        b = point.y()
        return QPointF(point().x(), b)


def add_cutter_event(point):
    add_cutter(point)

def add_cutter_sb(window):
    x = window.x_sb.value()
    y = window.y_sb.value()

    add_cutter(QPointF(x, y))

def add_cutter(point):
    global window

    if window.full_polygon:
        QMessageBox.warning(window, "Ошибка", "Отсекатель уже введен")
        return

    window.cutter.append(point)
    size = len(window.cutter)

    if size > 1:
        window.how_draw.addItem("Ввод на " + str(size - 1) + " ребре")
        window.scene.addLine(QLineF(window.cutter[size - 2], window.cutter[size - 1]), QPen(window.cutter_color))

def cut_all(window):
    window.scene.clear()

    for polygon in window.polygons:
        for i in range(len(polygon) - 1):
            window.scene.addLine(QLineF(polygon[i], polygon[i + 1]), QPen(window.polygon_color))

    for i in range(len(window.cutter) - 1):
        window.scene.addLine(QLineF(window.cutter[i], window.cutter[i + 1]), QPen(window.cutter_color))

    if len(window.cur_polygon) > 1:
        for i in range(len(window.cur_polygon) - 1):
            window.scene.addLine(QLineF(window.cur_polygon[i], window.cur_polygon[i + 1]), QPen(window.polygon_color))

    if window.full_polygon:
        if not window.isConvex:
            QMessageBox().warning(window, "Ошибка", "Отсекатель невыпуклый")
            return
        else:
            for polygon in window.polygons:
                new_polygon = sazerland_hod(window, polygon, window.cutter)
                for i in range(len(new_polygon) - 1):
                    window.scene.addLine(QLineF(new_polygon[i], new_polygon[i + 1]), QPen(window.cut_polygon_color))

def close_cutter():
    global window

    size = len(window.cutter)
    if size > 2:
        add_cutter(window.cutter[0])
        window.full_polygon = True
        isConvex, _sign = is_convex(window.cutter)

        if isConvex:
            window.isConvex = True
            window.direction = _sign
            cut_all(window)
        else:
            window.isConvex = False
            QMessageBox().warning(window, "Ошибка", "Отсекатель невыпуклый")

def close_polygon():
    global window

    size = len(window.cur_polygon)
    if size > 2:
        add_polygon(window.cur_polygon[0])
        window.polygons.append(window.cur_polygon)
        window.cur_polygon = list()
        cut_all(window)

def del_cutter(window):
    if len(window.cutter) == 0:
        QMessageBox.warning(window, "Предупреждение", "Нет введенного отсекателя")
        return

    size = window.how_draw.count()
    window.how_draw.setCurrentIndex(0)
    for i in range(size, 0, -1):
        window.how_draw.removeItem(i)

    window.cutter = list()
    window.full_polygon = False
    cut_all(window)

def del_last_polygon(window):
    if len(window.cur_polygon) != 0:
        window.cur_polygon = list()
    elif len(window.polygons) != 0:
        window.polygons.pop()
    else:
        QMessageBox.warning(window, "Предупреждение", "Нет введенных многоугольников")
        return
    cut_all(window)

def color_in_str(color):
    return str("(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")")

def get_cutter_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cutter_color = color
        window.color_cutter_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.cutter_color.getRgb()))
        cut_all(window)

def get_polygon_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.polygon_color = color
        window.color_polygon_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.polygon_color.getRgb()))
        cut_all(window)

def get_cut_polygon_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cut_polygon_color = color
        window.color_cut_polygon_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.cut_polygon_color.getRgb()))
        cut_all(window)

def clear(window):
    size = window.how_draw.count()
    window.how_draw.setCurrentIndex(0)
    for i in range(size, 0, -1):
        window.how_draw.removeItem(i)

    window.scene.clear()
    window.polygons = list()
    window.cur_polygon = list()
    window.cutter = list()
    window.full_polygon = False
    window.isConvex = False
    window.direction = -1

def sign(x):
    if x == 0:
        return 0

    return x / fabs(x)

def is_convex(polygon):
    size = len(polygon)
    array_vector = list()
    _sign = 0

    if size < 3:
        return False, _sign

    for i in range(1, size):
        if i < size - 1:
            ab = QPointF(polygon[i].x() - polygon[i - 1].x(), polygon[i].y() - polygon[i - 1].y())
            bc = QPointF(polygon[i + 1].x() - polygon[i].x(), polygon[i + 1].y() - polygon[i].y())
        else:
            ab = QPointF(polygon[i].x() - polygon[i - 1].x(), polygon[i].y() - polygon[i - 1].y())
            bc = QPointF(polygon[1].x() - polygon[0].x(), polygon[1].y() - polygon[0].y())

        array_vector.append(ab.x() * bc.y() - ab.y() * bc.x())

    exist_sign = False
    for i in range(len(array_vector)):
        if array_vector[i] == 0:
            continue

        if exist_sign:
            if sign(array_vector[i]) != _sign:
                return False, _sign
        else:
            _sign = sign(array_vector[i])
            exist_sign = True

    return True, _sign

def visible(p0, p1, p2):
    Pab1 = (p0.x() - p1.x()) * (p2.y() - p1.y())
    Pab2 = (p0.y() - p1.y()) * (p2.x() - p1.x())

    return sign(Pab1 - Pab2)

def fact_sech(p0, pk, w1, w2):
    vis_1 = visible(p0, w1, w2)
    vis_2 = visible(pk, w1, w2)

    if (vis_1 < 0 and vis_2 > 0) or (vis_1 > 0 and vis_2 < 0):
        return True

    return False

def intersection(p1, p2, w1, w2):
    d_1 = (p2.x() - p1.x()) * (w1.y() - w2.y()) - (w1.x() - w2.x()) * (p2.y() - p1.y())
    d_2 = (w1.x() - p1.x()) * (w1.y() - w2.y()) - (w1.x() - w2.x()) * (w1.y() - p1.y())
    t = d_2 / d_1

    return QPointF(p1.x() + (p2.x() - p1.x()) * t,
                   p1.y() + (p2.y() - p1.y()) * t)

def sazerland_hod(window, polygon_0, cutter):
    polygon = polygon_0.copy()
    Np = len(polygon)
    Nw = len(cutter)

    S = QPointF()
    F = QPointF()
    for i in range(Nw - 1):
        Nq = 0
        Q = list()

        for j in range(Np):
            if j != 0:
                if fact_sech(S, polygon[j], cutter[i], cutter[i + 1]):
                    I = intersection(S, polygon[j], cutter[i], cutter[i + 1])
                    Q.append(I)
                    Nq += 1
            else:
                F = polygon[j]

            S = polygon[j]
            is_visible = visible(S, cutter[i], cutter[i + 1])

            if (is_visible >= 0 and window.direction == -1) or (is_visible <= 0 and window.direction == 1):
                Q.append(S)
                Nq += 1
        if Nq != 0:
            if fact_sech(S, F, cutter[i], cutter[i + 1]):
                I = intersection(S, F, cutter[i], cutter[i + 1])
                Q.append(I)
                Nq += 1

        Np = Nq
        polygon = Q.copy()

    if len(polygon) > 0:
        polygon.append(polygon[0])
    return polygon

def main():
    global window

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()