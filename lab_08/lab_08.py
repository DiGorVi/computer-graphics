from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QPointF, QLineF
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import QPen, QColor
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
        self.line_color = QColor(Qt.red)
        self.cut_line_color = QColor(Qt.green)

        self.polygon = list()
        self.lines = list()
        self.cur_line = list()

        self.full_polygon = False
        self.isConvex = False
        self.direction = -1

        self.add_line_bt.clicked.connect(lambda: add_line_sb(self))
        self.add_cutter_bt.clicked.connect(lambda: add_cutter_sb(self))
        self.del_cutter_bt.clicked.connect(lambda: del_cutter(self))
        self.close_bt.clicked.connect(lambda: close_cutter())

        self.color_line_bt.clicked.connect(lambda: get_line_color(self))
        self.color_cutter_bt.clicked.connect(lambda: get_cutter_color(self))
        self.color_cut_line_bt.clicked.connect(lambda: get_cut_line_color(self))
        self.clear_bt.clicked.connect(lambda: clear(self))

        self.first_color_buttons()

    def first_color_buttons(self):
        self.color_line_bt.setStyleSheet("background-color:rgb" \
                + color_in_str(self.line_color.getRgb()))
        self.color_cut_line_bt.setStyleSheet("background-color:rgb" \
                + color_in_str(self.cut_line_color.getRgb()))
        self.color_cutter_bt.setStyleSheet("background-color:rgb" \
                + color_in_str(self.cutter_color.getRgb()))

class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ControlModifier:
            add_cutter_event(event.scenePos())
        elif event.buttons() == Qt.LeftButton:
            add_line_event(event.scenePos())
        elif event.buttons() == Qt.RightButton:
            close_cutter()


    def mouseMoveEvent(self, event):
        change_position(event.scenePos())

def change_position(point):
    global window

    window.position.setText("x: " + str(round(point.x())) + " y: " + str(round(point.y())))

def add_line_event(point):
    global window

    window.cur_line.append(point)
    if len(window.cur_line) == 2:
        add_line(QLineF(window.cur_line[0], window.cur_line[1]))
        window.cur_line = list()

def add_line_sb(window):
    x1 = window.x1_sb.value()
    x2 = window.x2_sb.value()
    y1 = window.y1_sb.value()
    y2 = window.y2_sb.value()

    line = QLineF(x1, y1, x2, y2)
    add_line(line)

def add_line(line):
    global window

    if window.how_draw.currentIndex() == 0:
        window.lines.append(line)
    else:
        window.lines.append(add_paral_line(line))
    cut_all(window)

def add_paral_line(line):
    index = window.how_draw.currentIndex()

    m = window.polygon[index - 1].x() - window.polygon[index].x()

    if m != 0:
        k = (window.polygon[index - 1].y() - window.polygon[index].y()) / m
        b = line.p1().y() - k * line.p1().x()
        return QLineF(QPointF(line.p1().x(), k * line.p1().x() + b), QPointF(line.p2().x(), k * line.p2().x() + b))
    else:
        k = 0
        b1 = line.p1().y() - k * line.p1().x()
        b2 = line.p2().y() - k * line.p1().x()
        return QLineF(QPointF(line.p1().x(), k * line.p1().x() + b1), QPointF(line.p1().x(), k * line.p1().x() + b2))

def add_cutter_event(point):
    global window
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

    window.polygon.append(point)
    size = len(window.polygon)

    if size > 1:
        window.how_draw.addItem("Ввод параллельного отрезка относительно " + str(size - 1) + " ребра")
        window.scene.addLine(QLineF(window.polygon[size - 2], window.polygon[size - 1]), QPen(window.cutter_color))

def cut_all(window):
    window.scene.clear()

    for j in range(len(window.lines)):
        window.scene.addLine(window.lines[j], QPen(window.line_color))

    for i in range(len(window.polygon) - 1):
        window.scene.addLine(QLineF(window.polygon[i], window.polygon[i + 1]), QPen(window.cutter_color))

    if window.full_polygon:
        if not window.isConvex:
            QMessageBox().warning(window, "Ошибка", "Отсекатель невыпуклый")
            return
        i = 0
        for line in window.lines:
            code = kirus_bek(window.polygon, line, window.direction, window)
            i += 1
            if code == 0:
                print(i, ": SUCCESS")
            elif code == 1:
                print(i, ": WSCALAR < 0")
            elif code == 2:
                print(i, ": T > 0")
            elif code == 3:
                print(i, ": T < 0")
            elif code == 4:
                print(i, ": TB > TE")

def close_cutter():
    global window

    size = len(window.polygon)
    if size > 2:
        add_cutter(window.polygon[0])
        window.full_polygon = True
        isConvex, _sign = is_convex(window.polygon)

        if isConvex:
            window.isConvex = True
            window.direction = _sign
            cut_all(window)
        else:
            window.isConvex = False
            QMessageBox().warning(window, "Ошибка", "Отсекатель невыпуклый")

def del_cutter(window):
    window.polygon = list()
    window.full_polygon = False

    size = window.how_draw.count()
    window.how_draw.setCurrentIndex(0)
    for i in range(size, 0, -1):
        window.how_draw.removeItem(i)

    window.scene.clear()
    draw_all_lines(window)

def draw_all_lines(window):
    for line in window.lines:
        window.scene.addLine(line, QPen(window.line_color))

def color_in_str(color):
    return str("(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")")

def get_cutter_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cutter_color = color
        window.color_cutter_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.cutter_color.getRgb()))
        cut_all(window)

def get_line_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.line_color = color
        window.color_line_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.line_color.getRgb()))
        cut_all(window)

def get_cut_line_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cut_line_color = color
        window.color_cut_line_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.cut_line_color.getRgb()))
        cut_all(window)

def clear(window):
    window.how_draw.setCurrentIndex(0)
    size = window.how_draw.count()
    for i in range(size, 0, -1):
        window.how_draw.removeItem(i)

    window.scene.clear()
    window.lines = list()
    window.cur_line = list()
    window.polygon = list()
    window.full_polygon = False
    window.isConvex = False
    window.direction = - 1

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

def scalar(p_1, p_2):
    return p_1.x() * p_2.x() + p_1.y() * p_2.y()

def kirus_bek(polygon, line, n, window):
    tb = 0
    te = 1
    x = line.p1().x()
    y = line.p1().y()
    D = QPointF(line.p2().x() - x, line.p2().y() - y)

    for i in range(len(polygon) - 1):
        W = QPointF(x - polygon[i].x(), y - polygon[i].y())
        N = QPointF(-n * (polygon[i + 1].y() - polygon[i].y()), n * (polygon[i + 1].x() - polygon[i].x()))

        Dscalar = scalar(D, N)
        Wscalar = scalar(W, N)

        if fabs(Dscalar) < 0.001:
            if Wscalar < 0:
                return 1
        else:
            t = -Wscalar / Dscalar

            if Dscalar > 0:
                if t > 1:
                    return 2
                else:
                    tb = max(tb, t)
            elif Dscalar < 0:
                if t < 0:
                    return 3
                else:
                    te = min(te, t)
    if tb <= te:
        window.scene.addLine(x + (line.p2().x() - x) * te,
                             y + (line.p2().y() - y) * te,
                             x + (line.p2().x() - x) * tb,
                             y + (line.p2().y() - y) * tb,
                             QPen(window.cut_line_color))
    else:
        return 4
    return 0

def main():
    global window

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()