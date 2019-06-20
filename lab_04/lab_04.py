from math import *
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap
import sys

canon = 0
param = 1
br = 2
mid = 3
standart = 4

center_x = 275
center_y = 275

def round_num(k):
    return int(k + 0.5);

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("interface.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 550, 550)
        self.canvas.setScene(self.scene)
        self.scene.win = self
        self.image = QImage(4000, 4000, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)

        self.pen_c = QPen()
        self.pen_el = QPen()
        self.pen_c.setColor(Qt.black)
        self.pen_el.setColor(Qt.black)

        self.color_ellipse = QColor(Qt.black)
        self.color_circle = QColor(Qt.black)
        self.color_bg = QColor(Qt.white)
        self.last_color_bg = QColor(Qt.white)

        self.color_circle_button.clicked.connect(lambda: get_circle_color(self))
        self.color_ellipse_button.clicked.connect(lambda: get_ellipse_color(self))
        self.color_bg_button.clicked.connect(lambda: get_bg_color(self))
        self.clear_canvas_button.clicked.connect(lambda: clear_canvas(self))
        self.draw_circle_button.clicked.connect(lambda: draw_circle(self))
        self.draw_ellipse_button.clicked.connect(lambda: draw_ellipse(self))
        self.draw_conc_circles_button.clicked.connect(lambda: draw_conc_circles(self))
        self.draw_conc_ellipses_button.clicked.connect(lambda: draw_conc_ellipses(self))

        self.color_circle_button.setStyleSheet("background-color:rgb(0,0,0)")
        self.color_ellipse_button.setStyleSheet("background-color:rgb(0,0,0)")
        self.color_bg_button.setStyleSheet("background-color:rgb(255,255,255)")
        new_sizes(self)


def circle_param(window, R, x0, y0):

    if R == 0:
        window.image.setPixel(x0, y0, window.pen_c.color().rgba())
        return

    angle = pi / 4
    step = 1 / R

    while angle >= 0:
        x = round_num(R * cos(angle))
        y = round_num(R * sin(angle))

        draw_4_point(window, x0, y0, x, y, window.pen_c.color().rgba())
        draw_4_point(window, y0, x0, y, x, window.pen_c.color().rgba())
        
        angle -= step

def circle_canon(window, R, x0, y0):
    x = 0
    y = R
    R2 = R*R

    while x <= y:
        y = round_num(sqrt(R2 - x * x))

        draw_4_point(window, x0, y0, x, y, window.pen_c.color().rgba())
        draw_4_point(window, y0, x0, y, x, window.pen_c.color().rgba())
        
        x += 1

def circle_br(window, R, x0, y0):
    y = R
    x = 0
    d = 2 - 2 * R

    while x <= y:
        draw_4_point(window, x0, y0, x, y, window.pen_c.color().rgba())
        draw_4_point(window, y0, x0, y, x, window.pen_c.color().rgba())

        if d < 0:
            d1 = 2 * d + 2 * y - 1

            if d1 < 0:
                x += 1
                d += 2 * x + 1
            else:
                x += 1
                y -= 1
                d += 2 * x - 2 * y + 2

        elif d == 0:
            x += 1
            y -= 1
            d += 2 * x - 2 * y + 2
            
        else:
            d1 = 2 * d - 2 * x - 1

            if d1 > 0:
                y -= 1
                d += -2 * y + 1
            else:
                x += 1
                y -= 1
                d += 2 * x - 2 * y + 2

def circle_mid(window, R, x0, y0):
    x = 0
    y = R

    f = 5 / 4 - R
    df = 0
    delta = -2 * y

    while x <= y:
        draw_4_point(window, x0, y0, x, y, window.pen_c.color().rgba())
        draw_4_point(window, y0, x0, y, x, window.pen_c.color().rgba())

        x += 1
        if f >= 0:
            y -= 1
            delta += 2
            f += delta
        df += 2
        f += df + 1

def ellipse_canon(window, A, B, x0, y0):
    x = 0
    B2 = B*B
    A2 = A*A

    if B2 == 0 and A2 == 0:
        window.image.setPixel(x0, y0, window.pen_el.color().rgba())
        return

    end_x = A2 / sqrt(A2 + B2)

    if A2 != 0:
        while x <= end_x:
            y = round_num(sqrt((1 - (x**2 / A2)) * B2))
            draw_4_point(window, x0, y0, x, y, window.pen_el.color().rgba())
            x += 1

    y = 0
    end_y = B2 / sqrt(A2 + B2)

    if B2 != 0:
        while y <= end_y:
            x = round_num(sqrt((1 - (y**2 / B2)) * A2))
            draw_4_point(window, x0, y0, x, y, window.pen_el.color().rgba())
            y += 1

    draw_4_point(window, x0, y0, end_x, end_y, window.pen_el.color().rgba())

def ellipse_param(window, A, B, x0, y0):
    if A == 0 and B == 0:
        window.image.setPixel(x0, y0, window.pen_el.color().rgba())
        return

    step_1 = 1 / A
    step_2 = 1 / B
    end_angle = atan(A*A / sqrt(A*A + B*B))
    angle = pi / 2

    while angle >= end_angle:
        x = round_num(A * cos(angle))
        y = round_num(B * sin(angle))

        draw_4_point(window, x0, y0, x, y, window.pen_el.color().rgba())

        angle -= step_1

    while angle >= 0:
        x = round_num(A * cos(angle))
        y = round_num(B * sin(angle))

        draw_4_point(window, x0, y0, x, y, window.pen_el.color().rgba())

        angle -= step_2


def ellipse_br(window, A, B, x0, y0):
    x = 0
    y = B
    end_y = 0
    A2 = A*A
    B2 = B*B

    d = B2 - 2 * B * A2 + A2

    b2 = 2 * B2
    a2 = 2 * A2
    a2_b2 = A2 + B2

    while y >= end_y:
        draw_4_point(window, x0, y0, x, y, window.pen_el.color().rgba())

        if d < 0:
            d1 = 2 * d + a2 * y - A2

            if d1 < 0:
                x += 1
                d += b2 * x + B2
            else:
                x += 1
                y -= 1
                d += b2 * x - a2 * y + a2_b2

        elif d == 0:
            x += 1
            y -= 1
            d += b2 * x - a2 * y + a2_b2

        else:
            d1 = 2 * d - b2 * x - B2

            if d1 > 0:
                y -= 1
                d += -a2 * y + A2
            else:
                x += 1
                y -= 1
                d += b2 * x - a2 * y + a2_b2

def ellipse_mid(window, A, B, x0, y0):
    x = 0
    y = B

    B2 = B*B
    A2 = A*A
    b2 = 2 * B2
    a2 = 2 * A2
    end_x = A2 / sqrt(A2 + B2)


    f = B2 - A2 * B + A2 / 4
    df = 0
    delta = -a2 * y
    
    while x <= end_x:
        draw_4_point(window, x0, y0, x, y, window.pen_el.color().rgba())

        x += 1
        if f >= 0:
            y -= 1
            delta += a2
            f += delta
        df += b2
        f += df + B2

    delta = b2 * x
    f += 3 / 4 * (A2 - B2) - A2 * y - B2 * x
    df = -a2 * y

    while y >= 0:
        draw_4_point(window, x0, y0, x, y, window.pen_el.color().rgba())
        y -= 1

        if f <= 0:
            x += 1
            delta += b2
            f += delta
        df += a2
        f += df + A2

def draw_4_point(window, x0, y0, x, y, color):
    if window.how_draw.currentIndex() == 1:
        new_pen = QPen()
        new_pen.setColor(window.color_bg)
        color = new_pen.color().rgba()

    window.image.setPixel(x0 + x, y0 - y, color)
    window.image.setPixel(x0 + x, y0 + y, color)
    window.image.setPixel(x0 - x, y0 - y, color)
    window.image.setPixel(x0 - x, y0 + y, color)

def draw_image_from_pix(window):
    pix = QPixmap(center_x * 2, center_y * 2)
    pix.convertFromImage(window.image)
    window.scene.addPixmap(pix)

def draw_spec_alg_circle(window, R, x0, y0):
    if window.algorithms.currentIndex() == canon:
        circle_canon(window, R, x0, y0)
    elif window.algorithms.currentIndex() == param:
        circle_param(window, R, x0, y0)
    elif window.algorithms.currentIndex() == br:
        circle_br(window, R, x0, y0)
    elif window.algorithms.currentIndex() == mid:
        circle_mid(window, R, x0, y0)

def new_sizes(window):
    global center_x, center_y

    w = window.canvas.width()
    h = window.canvas.height()

    center_x = w / 2 - 1
    center_y = h / 2 - 1
    window.scene.setSceneRect(0,0,w,h)

def draw_circle(window):
    new_sizes(window)
    R = window.r_spinbox.value()
    x0 = window.x0_circle_spinbox.value()
    y0 = window.y0_circle_spinbox.value()

    if window.last_color_bg != window.color_bg:
        window.scene.clear()
        window.image.fill(window.color_bg)
        window.last_color_bg = window.color_bg
    else:
        window.image.fill(QColor(0,0,0,alpha=0))

    draw_spec_alg_circle(window, R, x0, y0)
    draw_image_from_pix(window)

    if window.algorithms.currentIndex() == standart:
        p = QRectF(x0 - R, y0 - R, 2*R, 2*R)

        if window.how_draw.currentIndex() == 1:
            new_pen = QPen()
            new_pen.setColor(window.color_bg)
            window.scene.addEllipse(p, new_pen)
        else:
            window.scene.addEllipse(p, window.pen_c)

def draw_conc_circles(window):
    new_sizes(window)
    x0 = center_x
    y0 = center_y

    if window.last_color_bg != window.color_bg:
        window.scene.clear()
        window.image.fill(window.color_bg)
        window.last_color_bg = window.color_bg
    else:
        window.image.fill(QColor(0,0,0,alpha=0))

    rn = window.rn_spinbox.value()
    hr = window.hr_spinbox.value()
    count = window.c_circle_spinbox.value()

    for i in range(count):
        draw_spec_alg_circle(window, rn, x0, y0)
        draw_image_from_pix(window)

        if window.algorithms.currentIndex() == standart:
            p = QRectF(x0 - rn, y0 - rn, 2 * rn, 2 * rn)

            if window.how_draw.currentIndex() == 1:
                new_pen = QPen()
                new_pen.setColor(window.color_bg)
                window.scene.addEllipse(p, new_pen)
            else:
                window.scene.addEllipse(p, window.pen_c)

        rn += hr

def draw_spec_alg_ellipse(window, A, B, x0, y0):
    if window.algorithms.currentIndex() == canon:
        ellipse_canon(window, A, B, x0, y0)
    elif window.algorithms.currentIndex() == param:
        ellipse_param(window, A, B, x0, y0)
    elif window.algorithms.currentIndex() == br:
        ellipse_br(window, A, B, x0, y0)
    elif window.algorithms.currentIndex() == mid:
        ellipse_mid(window, A, B, x0, y0)

def draw_ellipse(window):
    new_sizes(window)
    A = window.a_spinbox.value()
    B = window.b_spinbox.value()
    x0 = window.x0_ellipse_spinbox.value()
    y0 = window.y0_ellipse_spinbox.value()

    if window.last_color_bg != window.color_bg:
        window.scene.clear()
        window.image.fill(window.color_bg)
        window.last_color_bg = window.color_bg
    else:
        window.image.fill(QColor(0,0,0,alpha=0))

    draw_spec_alg_ellipse(window, A, B, x0, y0)
    draw_image_from_pix(window)

    if window.algorithms.currentIndex() == standart:
        p = QRectF(x0 - A, y0 - B, 2*A, 2*B)

        if window.how_draw.currentIndex() == 1:
            new_pen = QPen()
            new_pen.setColor(window.color_bg)
            window.scene.addEllipse(p, new_pen)
        else:
            window.scene.addEllipse(p, window.pen_el)

def draw_conc_ellipses(window):
    new_sizes(window)
    x0 = center_x
    y0 = center_y

    if window.last_color_bg != window.color_bg:
        window.scene.clear()
        window.image.fill(window.color_bg)
        window.last_color_bg = window.color_bg
    else:
        window.image.fill(QColor(0,0,0,alpha=0))

    ha = window.ha_spinbox.value()
    count = window.c_ellipse_spinbox.value()
    an = window.a0_sp.value()
    bn = window.b0_sp.value()

    for i in range(count):
        draw_spec_alg_ellipse(window, an, bn, x0, y0)
        draw_image_from_pix(window)

        if window.algorithms.currentIndex() == standart:
            p = QRectF(x0 - an, y0 - bn, 2 * an, 2 * bn)

            if window.how_draw.currentIndex() == 1:
                new_pen = QPen()
                new_pen.setColor(window.color_bg)
                window.scene.addEllipse(p, new_pen)
            else:
                window.scene.addEllipse(p, window.pen_el)

        if an > bn:
            an += ha
            bn += ha * bn / an
        else:
            an += ha * an / bn
            bn += ha

def color_in_str(color):
    return str("(" + str(color[0]) + "," + str(color[1]) + "," + str(color[2]) + ")")

def get_ellipse_color(window):

    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.color_ellipse = color
        window.color_ellipse_button.setStyleSheet("background-color:rgb"\
            + color_in_str(color.getRgb()))
        window.pen_el.setColor(color)

def get_bg_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.last_color_bg = window.color_bg
        window.color_bg = color
        window.color_bg_button.setStyleSheet("background-color:rgb"\
            + color_in_str(color.getRgb()))

def get_circle_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.color_circle = color
        window.color_circle_button.setStyleSheet("background-color:rgb"\
            + color_in_str(color.getRgb()))
        window.pen_c.setColor(color)

def clear_canvas(window):
    window.image.fill(Qt.color0)
    window.scene.clear()
    window.last_color_bg = QColor(Qt.white)

def main():
    app = QtWidgets.QApplication(sys.argv)
    Window().show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
