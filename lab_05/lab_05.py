from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QPointF, QEventLoop
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap
import sys

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("interface.ui", self)
        self.scene = Scene(0, 0, 4000, 4000)
        self.canvas.setScene(self.scene)

        self.image = QImage(4000, 4000, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        self.pen = QPen(Qt.black)

        self.end_polygon_bt.clicked.connect(lambda: close_polygon())
        self.add_point_bt.clicked.connect(lambda: add_sb_point(self))
        self.clear_bt.clicked.connect(lambda: clear(self))
        self.fill_polygon_bt.clicked.connect(lambda: fill_polygon())

        self.all_polygons = list()
        self.cur_polygon = list()


class Scene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        if event.buttons() == Qt.LeftButton and event.modifiers() == Qt.ShiftModifier:
            add_straight_point(event.scenePos())
        elif event.buttons() == Qt.LeftButton:
            add_point(event.scenePos())
        elif event.buttons() == Qt.RightButton:
            close_polygon()
        else:
            fill_polygon()

def add_point(point):
    global window

    rows = window.all_points_table.rowCount()
    window.all_points_table.insertRow(rows)
    index = rows - 1

    window.all_points_table.setItem(index, 0, QtWidgets.QTableWidgetItem(str(point.x())))
    window.all_points_table.setItem(index, 1, QtWidgets.QTableWidgetItem(str(point.y())))
    window.cur_polygon.append(point)

    size = len(window.cur_polygon)

    if size > 1:
        cda(window, window.cur_polygon[size - 2].x(),
            window.cur_polygon[size - 2].y(),
            window.cur_polygon[size - 1].x(),
            window.cur_polygon[size - 1].y(),
            QPen(Qt.black).color().rgba())
        draw_image_from_pix(window)

def draw_edges(window, edges):
    color = QPen(Qt.black).color().rgba()
    for ed in edges:
        cda(window, ed[0], ed[1], ed[2], ed[3], color)

def add_straight_point(point):
    global window

    size = len(window.cur_polygon)

    if size == 0:
        add_point(point)

    else:
        last_point = window.cur_polygon[size-1]
        k1 = fabs(point.y() - last_point.y())
        k2 = fabs(last_point.x() - point.x())

        if k2 == 0:
            add_point(QPointF(point.x(), last_point.y()))
        elif fabs(degrees(atan(k1 / k2))) <= 45:
            add_point(QPointF(point.x(), last_point.y()))
        else:
            add_point(QPointF(last_point.x(), point.y()))

def add_sb_point(window):
    add_point(QPointF(window.x_sb.value(), window.y_sb.value()))

def close_polygon():
    global window

    size = len(window.cur_polygon)
    if size > 2:
        cda(window, window.cur_polygon[0].x(),
            window.cur_polygon[0].y(),
            window.cur_polygon[size - 1].x(),
            window.cur_polygon[size - 1].y(),
            QPen(Qt.black).color().rgba())

        draw_image_from_pix(window)
        window.all_polygons.insert(0, window.cur_polygon)
        window.cur_polygon = list()

def min_max_y(edges):
    if len(edges) == 0:
        return 0, 0
    y_max = edges[0][1]
    y_min = edges[0][1]

    for ed in edges:
        if ed[1] > y_max:
            y_max = ed[1]
        if ed[3] > y_max:
            y_max = ed[3]

        if ed[1] < y_min:
            y_min = ed[1]
        if ed[3] < y_min:
            y_min = ed[3]

    return y_max, y_min

def fill_polygon():
    global window
    if len(window.all_polygons) != 0:
        edges = get_edges(window.all_polygons)
        x_p = get_partition(window.all_polygons)
        y_max, y_min = min_max_y(edges)

        cda(window, x_p, y_min - 20, x_p, y_max + 20, QPen(Qt.green).color().rgba())
        draw_image_from_pix(window)
        alg_with_partition(window, edges, x_p, y_max, y_min)

def alg_with_partition(window, edges, x_p, y_max, y_min):
    need_delay = window.delay.checkState()

    for ed in edges:
        if ed[1] == ed[3]:
            continue

        if ed[1] > ed[3]:
            ed[0], ed[2] = ed[2], ed[0]
            ed[1], ed[3] = ed[3], ed[1]

        y = ed[1]
        end_y = ed[3]
        x_b = ed[0]
        dx = (ed[2] - ed[0]) / (ed[3] - ed[1])

        while y < end_y:
            x = round_number(x_b)
            if x < x_p:
                fill_pixels(window, x, x_p, y)
            else:
                fill_pixels(window, x_p, x, y)
            x_b += dx
            y += 1

            if need_delay:
                delay()
                window.scene.clear()
                draw_image_from_pix(window)

    draw_edges(window, edges)
    cda(window, x_p, y_min - 20, x_p, y_max + 20, QPen(Qt.green).color().rgba())
    window.scene.clear()
    draw_image_from_pix(window)

def fill_pixels(window, x0, x_end, y):
    x = x0
    white = QPen(Qt.white).color().rgba()
    red = QPen(Qt.red).color().rgba()

    while x < x_end:
        color = QColor(window.image.pixel(x, y))
        if color == Qt.black or color == Qt.green:
            pass
        elif color == Qt.white:
            window.image.setPixel(x, y, red)
        else:
            window.image.setPixel(x, y, white)
        x += 1

def get_edges(all_polygons):
    edges = list()

    for polygon in all_polygons:
        size = len(polygon)
        for i in range(size - 1):
            edges.append([polygon[i].x(), polygon[i].y(), polygon[i + 1].x(), polygon[i + 1].y()])
        if size > 1:
            edges.append([polygon[size - 1].x(), polygon[size - 1].y(), polygon[0].x(), polygon[0].y()])

    return edges

def get_partition(all_polygons):
    x_avg = 0
    new_x = 0
    size_avg = 0

    for polygon in all_polygons:
        size = len(polygon)
        size_avg += size
        for i in range(size):
           x_avg += polygon[i].x()

    if size_avg != 0:
        x = x_avg / size_avg
        delta_min_x = fabs(all_polygons[0][0].x() - x)
        new_x = all_polygons[0][0].x()

        for polygon in all_polygons:
            size = len(polygon)
            for i in range(size):
                tmp_1 = fabs(polygon[i].x() - x)
                if tmp_1 < delta_min_x:
                    delta_min_x = tmp_1
                    new_x = polygon[i].x()

    return new_x

def draw_image_from_pix(window):
    pix = QPixmap(4000, 4000)
    pix.convertFromImage(window.image)
    window.scene.addPixmap(pix)

def clear(window):
    rows = window.all_points_table.rowCount()
    for i in range(rows - 1, -1, -1):
        window.all_points_table.removeRow(i)
    window.all_points_table.insertRow(0)
    window.scene.clear()
    window.image.fill(Qt.white)
    window.all_polygons = list()
    window.cur_polygon = list()

def round_number(number):
    return int(number + 0.5)

def cda(window, x0, y0, xk, yk, color):
    dx = xk - x0
    dy = yk - y0

    x = x0
    y = y0

    if fabs(dx) > fabs(dy):
        len_line = fabs(dx)
    else:
        len_line = fabs(dy)

    if len_line == 0:
        window.image.setPixel(x, y, color)
        return

    sx = dx / len_line
    sy = dy / len_line
    i = len_line

    while i > 0:
        window.image.setPixel(round_number(x), round_number(y), color)
        x += sx
        y += sy
        i -= 1

def delay():
    QtWidgets.QApplication.processEvents(QEventLoop.AllEvents)

def main():
    global window

    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()