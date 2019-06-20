from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap
from math import modf, fabs, pi, cos, sin
import sys

center = 299

class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("interface.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 600, 600)
        self.canvas.setScene(self.scene)
        self.scene.win = self
        self.image = QImage(600, 600, QImage.Format_ARGB32_Premultiplied)
        
        self.image.fill(Qt.white)
        draw_image_from_pix(self)
        self.pen = QPen()
        self.color_line = QColor(Qt.black)
        s = QtWidgets.QGraphicsScene(0, 0, 0, 0)
        s.setBackgroundBrush(self.color_line)
        
        self.line_color_canvas.setScene(s)
        self.color_bg = QColor(Qt.white)
        self.last_color_bg = QColor(Qt.white)
        
        self.draw_line_button.clicked.connect(lambda: draw_line(self))
        self.clear_canvas_button.clicked.connect(lambda: clear_canvas(self))
        self.change_color_bg_button.clicked.connect(lambda: get_bg_color(self))
        self.change_color_line_button.clicked.connect(lambda: get_line_color(self))
        self.draw_bundle_button.clicked.connect(lambda: draw_bundle(self))
        self.change_color_line2bg_button.clicked.connect(lambda: change_color_line2bg(self))
        self.cda.setChecked(True)

def round_number(x):
    x += 0.5
    fl_x, int_x = modf(x)

    return int_x

def sign(x):
    if x == 0:
        return x

    return x / fabs(x)

def rgba_to_rgb(rgb_background, rgb_color, alpha):
    f = 1 - alpha

    return QColor(f * rgb_background[0] + alpha * rgb_color[0],\
            f * rgb_background[1] + alpha * rgb_color[1],\
            f * rgb_background[2] + alpha * rgb_color[2])

def cda(window, x0, y0, xk, yk):
    dx = xk - x0
    dy = yk - y0

    x = x0
    y = y0

    if fabs(dx) > fabs(dy):
        len_line = fabs(dx)
    else:
        len_line = fabs(dy)

    if len_line == 0:
        window.image.setPixel(x, y, window.pen.color().rgba())
        return

    sx = dx / len_line
    sy = dy / len_line
    i = len_line

    while i > 0:
        window.image.setPixel(round_number(x), round_number(y), window.pen.color().rgba())
        x += sx
        y += sy
        i -= 1

def br_int(window, x0, y0, xk, yk):
    dx = xk - x0
    dy = yk - y0
    x = x0
    y = y0
    change = False

    if dx == 0 and dy == 0:
        window.image.setPixel(x, y, window.pen.color().rgba())
        return

    sx = sign(dx)
    sy = sign(dy)

    dx = fabs(dx)
    dy = fabs(dy)

    if not dx > dy:
        dx, dy = dy, dx
        change = True

    e = 2 * dy - dx
    i = dx

    while i > 0:
        window.image.setPixel(x, y, window.pen.color().rgba())

        if e >= 0:
            if not change:
                y += sy
            else:
                x += sx
            e -= 2 * dx

        if e < 0:
            if not change:
                x += sx
            else:
                y += sy
            e += 2 * dy
        i -= 1

def br_float(window, x0, y0, xk, yk):
    dx = xk - x0
    dy = yk - y0
    x = x0
    y = y0
    change = False

    if dx == 0 and dy == 0:
        window.image.setPixel(x, y, window.pen.color().rgba())
        return

    sx = sign(dx)
    sy = sign(dy)

    dx = fabs(dx)
    dy = fabs(dy)

    if not dx > dy:
        dx, dy = dy, dx
        change = True

    m = dy / dx
    e = m - 0.5
    i = dx

    while i > 0:
        window.image.setPixel(x, y, window.pen.color().rgba())

        if e >= 0:
            if not change:
                y += sy
            else:
                x += sx
            e -= 1

        if e < 0:
            if not change:
                x += sx
            else:
                y += sy
            e += m
        i -= 1

def br_smoothing(window, x0, y0, xk, yk):
    dx = xk - x0
    dy = yk - y0

    x = x0
    y = y0

    if dx == 0 and dy == 0:
        window.image.setPixel(x, y, window.pen.color().rgba())
        return

    I = 1
    sx = sign(dx)
    sy = sign(dy)

    dx = fabs(dx)
    dy = fabs(dy)

    if dx == 0:
        m = 0
    else:
        m = dy / dx

    fl = 0
    if dx <= dy:
        dx, dy = dy, dx
        fl = 1

        if m:
            m = 1 / m

    f = I / 2
    m *= I
    w = I - m
    i = dx

    color_line = window.color_line.getRgb()
    bg_color = window.color_bg.getRgb()

    while i > 0:
        window.image.setPixel(x, y, rgba_to_rgb(bg_color, color_line, f).rgb())

        if f <= w:
            if fl:
                y += sy
            else:
                x += sx
            f += m
        else:
            x += sx
            y += sy
            f -= w

        i -= 1

def draw_pixel_wu(window, x, y, f, swap, bg_color, color_line):
    if swap:
        window.image.setPixel(y, x, rgba_to_rgb(bg_color, color_line, f).rgb())
    else:
        window.image.setPixel(x, y, rgba_to_rgb(bg_color, color_line, f).rgb())

def alg_wu(window, x0, y0, xk, yk):
    swap = False
    color_line = window.color_line.getRgb()
    bg_color = window.color_bg.getRgb()

    if x0 == xk and y0 == yk:
        window.image.setPixel(x0, y0, window.pen.color().rgba())
        return

    if fabs(yk - y0) > fabs(xk - x0):
        x0, y0 = y0, x0
        xk, yk = yk, xk
        swap = True

    if xk < x0:
        x0, xk = xk, x0
        y0, yk = yk, y0

    dx = xk - x0
    dy = yk - y0
    grad = dy / dx

    x = x0
    y = y0

    while x <= xk:
        draw_pixel_wu(window, x, y + 1, y - int(y), swap, bg_color, color_line)
        draw_pixel_wu(window, x, y, 1 - (y - int(y)), swap, bg_color, color_line)

        y += grad
        x += 1

def get_bg_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.last_color_bg = window.color_bg
        window.color_bg = color
        s = QtWidgets.QGraphicsScene(0, 0, 0, 0)
        s.setBackgroundBrush(color)
        window.bg_color_canvas.setScene(s)

def change_color_line2bg(window):
    color = window.color_bg
    window.color_line = color
    window.pen.setColor(color)
    s = QtWidgets.QGraphicsScene(0, 0, 0, 0)
    s.setBackgroundBrush(color)
    window.line_color_canvas.setScene(s)
    window.hide()
    window.show()

def get_line_color(window):
    color = QtWidgets.QColorDialog.getColor()
    if color.isValid():
        window.color_line = color
        window.pen.setColor(color)
        s = QtWidgets.QGraphicsScene(0, 0, 0, 0)
        s.setBackgroundBrush(color)
        window.line_color_canvas.setScene(s)

def draw_line(window):
    x0 = window.x0_entry.value() + center
    y0 = center - window.y0_entry.value()
    xk = window.xk_entry.value() + center
    yk = center - window.yk_entry.value()

    if window.last_color_bg != window.color_bg:
        window.scene.clear()
        window.image.fill(window.color_bg)
        window.last_color_bg = window.color_bg
    else:
        window.image.fill(QColor(0,0,0,alpha=0))

    draw_spec_alg(window, x0, y0, xk, yk)
    draw_image_from_pix(window)

    if window.standart.isChecked():
        window.scene.addLine(x0, y0, xk, yk, window.pen)

def draw_image_from_pix(window):
    pix = QPixmap(600, 600)
    pix.convertFromImage(window.image)
    window.scene.addPixmap(pix)

def draw_spec_alg(window, x0, y0, xk, yk):
    if window.cda.isChecked():
        cda(window, x0, y0, xk, yk)
        return True
    elif window.br_int.isChecked():
        br_int(window, x0, y0, xk, yk)
        return True
    elif window.br_float.isChecked():
        br_float(window, x0, y0, xk, yk)
        return True
    elif window.br_smoothing.isChecked():
        br_smoothing(window, x0, y0, xk, yk)
        return True
    elif window.alg_vu.isChecked():
        alg_wu(window, x0, y0, xk, yk)
        return True
    else:
        return False


def rotate(array, xt, yt, angle):
    __angle = angle * pi / 180
    size = len(array)

    for i in range(0, size, 2):
        x = array[i]
        y = array[i + 1]
        array[i] = xt + (x - xt) * cos(__angle) + (y - yt) * sin(__angle)
        array[i + 1] = yt - (x - xt) * sin(__angle) + (y - yt) * cos(__angle)

    return array

def draw_bundle(window):
    r = window.r_bundle_entry.value()
    angle = window.angle_bundle_entry.value()

    if window.last_color_bg != window.color_bg:
        window.scene.clear()
        window.image.fill(window.color_bg)
        window.last_color_bg = window.color_bg
    else:
        window.image.fill(QColor(0,0,0,alpha=0))

    x0 = center
    y0 = center
    xk = x0
    yk = y0 - r

    line = [x0, y0, xk, yk]

    if angle == 0:
        draw_spec_alg(window, x0, y0, xk, yk)
        draw_image_from_pix(window)

        if window.standart.isChecked():
            window.scene.addLine(x0, y0, xk, yk, window.pen)

        return

    m = 360 // fabs(angle)

    while m > 0:
        if draw_spec_alg(window, line[0], line[1], line[2], line[3]):
            draw_image_from_pix(window)

        if window.standart.isChecked():
            window.scene.addLine(line[0], line[1], line[2], line[3], window.pen)

        line = rotate(line, center, center, angle)
        m -= 1

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
