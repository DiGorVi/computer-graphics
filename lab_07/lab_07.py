from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QLineF, QPointF
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
        self.pen = QPen(Qt.black)

        self.lines = list()
        self.cutters = list()

        self.cur_line = list()
        self.cur_cutter = list()

        self.cutter_color = QColor(Qt.black)
        self.line_color = QColor(Qt.red)
        self.cut_line_color = QColor(Qt.green)

        self.add_line_bt.clicked.connect(lambda: add_line_sb(self))
        self.add_cutter_bt.clicked.connect(lambda: add_cutter_sb(self))

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
        if event.buttons() == Qt.LeftButton:
            add_line_event(event.scenePos())
        elif event.buttons() == Qt.RightButton:
            add_cutter_event(event.scenePos())

def color_in_str(color):
    return str("(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")")

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
    window.lines.append(line)
    window.scene.addLine(line, QPen(window.line_color))
    cut_all(window)

def add_cutter_event(point):
    global window
    window.cur_cutter.append(point)

    if len(window.cur_cutter) == 2:
        cutter = make_cutter(window.cur_cutter[0].x(), window.cur_cutter[0].y(),
                             window.cur_cutter[1].x(), window.cur_cutter[1].y())
        add_cutter(cutter)
        window.cur_cutter = list()

def add_cutter_sb(window):
    x1 = window.x1_sb.value()
    x2 = window.x2_sb.value()
    y1 = window.y1_sb.value()
    y2 = window.y2_sb.value()

    cutter = make_cutter(x1, y1, x2, y2)
    add_cutter(cutter)

def make_cutter(x1, y1, x2, y2):
    x = min(x1, x2)
    y = min(y1, y2)

    if x == x2:
        x1, x2 = x2, x1

    if y == y2:
        y1, y2 = y2, y1

    cutter = list()
    cutter.append(QLineF(x1, y1, x1, y2))
    cutter.append(QLineF(x2, y1, x2, y2))
    cutter.append(QLineF(x1, y2, x2, y2))
    cutter.append(QLineF(x1, y1, x2, y1))

    return cutter

def add_cutter(cutter):
    global window
    window.cutters.append(cutter)
    cut_all(window)

def get_code(point, cutter):
    code = [0, 0, 0, 0]
    if point.x() < cutter[0].x1():
        code[0] = 1
    if point.x() > cutter[1].x1():
        code[1] = 1
    if point.y() > cutter[2].y1():
        code[2] = 1
    if point.y() < cutter[3].y1():
        code[3] = 1

    return code

def cut_all(window):
    window.scene.clear()

    for j in range(len(window.lines)):
        window.scene.addLine(window.lines[j], QPen(window.line_color))

    for i in range(len(window.cutters)):
        for j in range(len(window.lines)):
            mid_point(window, window.lines[j], window.cutters[i])

    for i in range(len(window.cutters)):
        for j in range(len(window.cutters[i])):
            window.scene.addLine(window.cutters[i][j], QPen(window.cutter_color))

def mid_point(window, line, cutter):
    pen = QPen(window.cut_line_color)
    eps = 0.1
    i = 1
    P_1 = line.p1()
    P_2 = line.p2()

    while True:
        T_1 = get_code(P_1, cutter)
        T_2 = get_code(P_2, cutter)

        S_1 = sum(T_1)
        S_2 = sum(T_2)

        if S_1 == 0 and S_2 == 0:
            window.scene.addLine(QLineF(P_1, P_2), pen)
            return

        P = [T_1[j] * T_2[j] for j in range(4)]

        if sum(P) != 0:
            return

        if i > 2:
            window.scene.addLine(QLineF(P_1, P_2), pen)
            return

        R = P_1

        if S_2 == 0:
            P_1, P_2 = P_2, R
            i += 1
            continue

        while True:
            if sqrt((P_1.x() - P_2.x())**2 + (P_1.y() - P_2.y())**2) < eps:
                P_1, P_2 = P_2, R
                i += 1
                break
            else:
                Psr = QPointF((P_1.x() + P_2.x()) / 2, (P_1.y() + P_2.y()) / 2)
                Pm = P_1
                P_1 = Psr

                T_1 = get_code(P_1, cutter)
                T_2 = get_code(P_2, cutter)

                P = [T_1[j] * T_2[j] for j in range(4)]

                if sum(P) != 0:
                    P_1 = Pm
                    P_2 = Psr

def get_cutter_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cutter_color = color
        window.color_cutter_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.cutter_color.getRgb()))

def get_line_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.line_color = color
        window.color_line_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.line_color.getRgb()))

def get_cut_line_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.cut_line_color = color
        window.color_cut_line_bt.setStyleSheet("background-color:rgb" \
            + color_in_str(window.cut_line_color.getRgb()))

def clear(window):
    window.scene.clear()
    window.cutters = list()
    window.lines = list()
    window.cur_line = list()
    window.cur_cutter = list()

def main():
    global window

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()