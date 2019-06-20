from tkinter import *
from tkinter import messagebox
from math import cos, sin, pi, sqrt

first_scale = 20
rx = 3 * first_scale
ry = 3 * first_scale

xm = 0
ym = 0
kx = 1
ky = 1

x_offset = 0
y_offset = 0

xt = 0
yt = 0
angle = 0
center = 349

treangle = [-7, 0, 0, 3, 0, -3]
for i in range(len(treangle)):
    treangle[i] *= first_scale
    
lines = [-1.25, 2.5, 1.5, -2.6, -3.7, 1.4, -1.95,\
         -2.15, -5, 0.9, -4, -1.2, 0, -3, -2.5, 1.9,
        0, 3, 2.5, -1.7]
for i in range(len(lines)):
    lines[i] *= first_scale
    
ellipse = list()
x = -rx + 0.001

while x < rx:
    ellipse.append(x)
    ellipse.append(sqrt((1 - (x**2 / rx**2)) * ry**2))
    x+= 0.001

actions = list()

def create_root():
    root = Tk()
    root.geometry("1200x705")
    root.title("Лабораторная №2")
    root.resizable(False,False)

    return root

def create_canvas(root):
    canvas = Canvas(root, width = 700, height = 700)
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(0, 0, 800, 800, outline = "", fill = "white")

    return canvas

def new_coord_scale(array, xm, ym, kx, ky):
    size = len(array)
        
    for i in range(0, size, 2):
        array[i] = kx * array[i] + (1 - kx) * xm
        array[i + 1] = ky * array[i + 1] + (1 - ky) * ym

    return array

def new_coord_turn(array, xt, yt, angle):
    __angle = angle * pi / 180
    size = len(array)
    
    for i in range(0, size, 2):
        x = array[i]
        y = array[i + 1]
        array[i] = xt + (x - xt) * cos(__angle) + (y - yt) * sin(__angle)
        array[i + 1] = yt - (x - xt) * sin(__angle) + (y - yt) * cos(__angle)

    return array

def new_coord_replace(array, x_offset, y_offset):
    size = len(array)

    for i in range(0, size, 2):
        array[i] += x_offset
        array[i + 1] += y_offset

    return array

def go_center(__array):
    array = __array.copy()
    size = len(array)

    for i in range(0, size, 2):
        array[i] += center
        array[i + 1] = center - array[i + 1]

    return array

def replace_picture(x_entry, y_entry):
    global x_offset
    global y_offset
    
    x = x_entry.get()
    y = y_entry.get()

    if len(x) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели dx")
        return

    if len(y) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели dy")
        return

    try:
        x_offset = float(x)
        y_offset = float(y)
    except:
        messagebox.showerror("Ошибка", "Введены некорректные данные для перемещения изображения")
        return

    draw(x_offset, y_offset, xm, ym, 1, 1, xt, yt, 0, 0, 0, 1, 0)

def scale_picture(x0_entry, y0_entry, kx_entry, ky_entry):
    global xm
    global ym
    global kx
    global ky
    
    __xm = x0_entry.get()
    __ym = y0_entry.get()
    __kx = kx_entry.get()
    __ky = ky_entry.get()

    if len(__xm) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели xm")
        return

    if len(__ym) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели ym")
        return

    if len(__kx) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели kx")
        return

    if len(__ky) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели ky")
        return

    try:
        xm = float(__xm)
        ym = float(__ym)

        kx = float(__kx)
        ky = float(__ky)
    except:
        messagebox.showerror("Ошибка",\
            "Введены некорректные данные для масштабирования изображения")
        return

    draw(0, 0, xm, ym, kx, ky, xt, yt, 0, 1, 0, 0, 0)

def turn_picture(x0_entry, y0_entry, angle_entry):
    global xt
    global yt
    global angle

    __xt = x0_entry.get()
    __yt = y0_entry.get()
    __angle = angle_entry.get()

    if len(__xt) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели xt")
        return

    if len(__yt) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели yt")
        return

    if len(__angle) == 0:
        messagebox.showerror("Ошибка", "Вы не ввели угол поворота")
        return

    try:
        xt = float(__xt)
        yt = float(__yt)
        angle = float(__angle)
    except:
        messagebox.showerror("Ошибка",\
            "Введены некорректные данные для поворота изображения")
        return

    draw(0, 0, xm, ym, 1, 1, xt, yt, angle, 0, 1, 0, 0)
    
def save_last():
    global ellipse, treangle, lines
    global actions
    
    el = dict()
    el["ellipse"] = ellipse.copy()
    el["treangle"] = treangle.copy()
    el["lines"] = lines.copy()
    
    actions.append(el)

def back_one():
    global ellipse, treangle, lines
    global actions
    
    if len(actions) == 0:
        messagebox.showerror("Ошибка",\
            "Изображения находится в исходном положении")
        return

    el = actions.pop()
    
    treangle = el["treangle"].copy()
    ellipse = el["ellipse"].copy()
    lines = el["lines"].copy()

    draw(0,0,0,0,1,1,0,0,0,0,0,0,1)
    
def draw(x_offset, y_offset, xm, ym, kx, ky, xt, yt, angle, _scale, _turn, _replace, _back):
    global canvas, ellipse
    global treangle, lines

    if not _back:
        save_last()
        
    canvas.delete("all")
    canvas = create_canvas(root)
    
    if _scale:
        treangle = new_coord_scale(treangle, xm, ym, kx, ky)
        lines = new_coord_scale(lines, xm, ym, kx, ky)
        ellipse = new_coord_scale(ellipse, xm, ym, kx, ky)

    if _turn:
        treangle = new_coord_turn(treangle, xt, yt, angle)
        lines = new_coord_turn(lines, xt, yt, angle)
        ellipse = new_coord_turn(ellipse, xt, yt, angle)

    if _replace:
        treangle = new_coord_replace(treangle, x_offset, y_offset)
        lines = new_coord_replace(lines, x_offset, y_offset)
        ellipse = new_coord_replace(ellipse, x_offset, y_offset)

    __treangle = go_center(treangle)
    __lines = go_center(lines)
    __ellipse = go_center(ellipse)
    
    canvas.create_polygon(__ellipse, fill = "white", \
        outline = "black", width = 2)
    canvas.create_polygon(__treangle, fill = "white",\
        outline = "black", width = 2)

    for i in range(0, len(__lines), 4):
        canvas.create_line(__lines[i], __lines[i + 1],\
            __lines[i + 2], __lines[i + 3], width = 2)

def key_input(var):
    new = var.get()
    check = False
    
    for i in range(len(new)):
        if (not (new[i] in "1234567890-+.")) or\
           (i > 0 and new[i] in "+-." and new[i-1] in "+-."):
            check = True
            break
        if len(new) == 1 and new[0] == '+':
            break
    if new == "" or new == "-" or\
       not check:
        key_input.old = new
    else:
        var.set(key_input.old)
        
key_input.old = ""
ellipse = new_coord_turn(ellipse, 0, 0, 90)
ellipse = new_coord_replace(ellipse, -1, 0)

def reset_picture():
    global xm, ym, xt, yt
    global x_offset, y_offset, angle
    global ellipse, treangle, lines
    global actions

    actions = list()
    xm = 0
    ym = 0
    kx = 1
    ky = 1

    x_offset = 0
    y_offset = 0

    xt = 0
    yt = 0
    angle = 0

    treangle = [-7, 0, 0, 3, 0, -3]
    for i in range(len(treangle)):
        treangle[i] *= first_scale
        
    lines = [-1.25, 2.5, 1.5, -2.6, -3.7, 1.4, -1.95,\
             -2.15, -5, 0.9, -4, -1.2, 0, -3, -2.5, 1.9,
            0, 3, 2.5, -1.7]
    for i in range(len(lines)):
        lines[i] *= first_scale
        
    ellipse = list()
    x = -rx + 0.001

    while x < rx:
        ellipse.append(x)
        ellipse.append(sqrt((1 - (x**2 / rx**2)) * ry**2))
        x+= 0.001
    ellipse = new_coord_turn(ellipse, 0, 0, 90)
    ellipse = new_coord_replace(ellipse, -1, 0)

    draw(0,0,0,0,1,1,0,0,0,0,0,0,1)

def create_widgets(root):
    s_replace_x = StringVar(root)
    s_replace_x.trace('w', lambda nm, idx, mode, var=s_replace_x: key_input(var))

    s_replace_y = StringVar(root)
    s_replace_y.trace('w', lambda nm, idx, mode, var=s_replace_y: key_input(var))

    s_scale_x0 = StringVar(root)
    s_scale_x0.trace('w', lambda nm, idx, mode, var=s_scale_x0: key_input(var))

    s_scale_y0 = StringVar(root)
    s_scale_y0.trace('w', lambda nm, idx, mode, var=s_scale_y0: key_input(var))
    
    s_turn_x0 = StringVar(root)
    s_turn_x0.trace('w', lambda nm, idx, mode, var=s_turn_x0: key_input(var))

    s_turn_y0 = StringVar(root)
    s_turn_y0.trace('w', lambda nm, idx, mode, var=s_turn_y0: key_input(var))

    s_scale_x = StringVar(root)
    s_scale_x.trace('w', lambda nm, idx, mode, var=s_scale_x: key_input(var))

    s_scale_y = StringVar(root)
    s_scale_y.trace('w', lambda nm, idx, mode, var=s_scale_y: key_input(var))

    s_angle = StringVar(root)
    s_angle.trace('w', lambda nm, idx, mode, var=s_angle: key_input(var))

    label_for_replace_x_y = Label(root, text = "    dx\
                                                                dy ")
    label_for_replace_x_y.place(x = 800, y = 20)
    
    label_div_1 = Label(root, text = 120 * "-")
    label_div_1.place(x = 701, y = 130)

    label_div_2 = Label(root, text = 120 * "-")
    label_div_2.place(x = 701, y = 382)

    label_div_3 = Label(root, text = 120 * "-")
    label_div_3.place(x = 701, y = 615)
    
    replace_x = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_replace_x)
    replace_x.place(x = 701, y = 40, width = 249, height = 50)

    replace_y = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_replace_y)
    replace_y.place(x = 950, y = 40, width = 249, height = 50)

    label_for_replace = Label(root, text = "Переместить рисунок")
    label_for_replace.place(x = 880, y = 0)
    
    replace = Button(root, text = "Переместить",\
        command = lambda: replace_picture(replace_x, replace_y))
    replace.place(x = 701, y = 92, width = 499, height = 40)

    label_for_scale = Label(root, text = "Масштабировать рисунок\nЦентр масштабирования:")
    label_for_scale.place(x = 860, y = 145)

    label_for_scale_x0_y0 = Label(root, text = "    xm\
                                                                ym ")
    label_for_scale_x0_y0.place(x = 800, y = 180)

    scale_x0 = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_scale_x0)
    scale_x0.place(x = 701, y = 200, width = 249, height = 50)

    scale_y0 = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_scale_y0)
    scale_y0.place(x = 950, y = 200, width = 249, height = 50)

    label_for_scale = Label(root, text = "Коэффициенты масштабирования:")
    label_for_scale.place(x = 840, y = 252)

    label_for_scale_x0_y0 = Label(root, text = "    kx\
                                                                ky ")
    label_for_scale_x0_y0.place(x = 800, y = 272)

    scale_kx = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_scale_x)
    scale_kx.place(x = 701, y = 292, width = 249, height = 50)

    scale_ky = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_scale_y)
    scale_ky.place(x = 950, y = 292, width = 249, height = 50)

    scale = Button(root, text = "Масштабировать", command = lambda: scale_picture(scale_x0,\
        scale_y0, scale_kx, scale_ky))
    scale.place(x = 701, y = 344, width = 499, height = 40)

    label_for_turn = Label(root, text = "Повернуть рисунок\nЦентр поворота:")
    label_for_turn.place(x = 880, y = 397)

    label_for_turn_x0_y0 = Label(root, text = "    xt\
                                                                yt ")
    label_for_turn_x0_y0.place(x = 800, y = 432)

    turn_x0 = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_turn_x0)
    turn_x0.place(x = 701, y = 452, width = 249, height = 50)

    turn_y0 = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_turn_y0)
    turn_y0.place(x = 950, y = 452, width = 249, height = 50)

    label_for_turn = Label(root, text = "Угол поворота:")
    label_for_turn.place(x = 890, y = 505)

    angle = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s_angle)
    angle.place(x = 701, y = 525, width = 499, height = 50)

    turn = Button(root, text = "Повернуть",\
        command = lambda: turn_picture(turn_x0, turn_y0, angle))
    turn.place(x = 701, y = 577, width = 499, height = 40)

    back = Button(root, text = "Отменить последнее действие", command = back_one)
    back.place(x = 701, y = 635, width = 249, height = 60)

    reset_all = Button(root, text = "Сбросить все", command = reset_picture)
    reset_all.place(x = 950, y = 635, width = 249, height = 60)

    replace_x.bind("<Return>", lambda x: replace_picture(replace_x, replace_y))
    replace_y.bind("<Return>", lambda x: replace_picture(replace_x, replace_y))
    
    scale_x0.bind("<Return>", lambda x: scale_picture(scale_x0, scale_y0, scale_kx, scale_ky))
    scale_y0.bind("<Return>", lambda x: scale_picture(scale_x0, scale_y0, scale_kx, scale_ky))
    scale_ky.bind("<Return>", lambda x: scale_picture(scale_x0, scale_y0, scale_kx, scale_ky))
    scale_kx.bind("<Return>", lambda x: scale_picture(scale_x0, scale_y0, scale_kx, scale_ky))
    
    turn_x0.bind("<Return>", lambda x: turn_picture(turn_x0, turn_y0, angle))
    turn_y0.bind("<Return>", lambda x: turn_picture(turn_x0, turn_y0, angle))
    angle.bind("<Return>", lambda x: turn_picture(turn_x0, turn_y0, angle))
    
    return  replace_x, replace_y, scale_x0,\
        scale_y0, scale_kx, scale_ky, turn_x0, turn_y0, angle
    
def main():
    global root
    global canvas
    
    root = create_root()
    canvas = create_canvas(root)
    create_widgets(root)
    draw(0,0,0,0,1,1,0,0,0,0,0,0,1)
    mainloop()
    
main()
