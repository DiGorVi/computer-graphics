from tkinter import *
from tkinter import messagebox
from math import atan, degrees, fabs, sqrt

coords_1 = list()
coords_2 = list()
result = dict()

## Проверка существование треугольника
def treangle_exist(coor_treangle):
    x1 = coor_treangle[0]
    y1 = coor_treangle[1]
    x2 = coor_treangle[2]
    y2 = coor_treangle[3]
    x3 = coor_treangle[4]
    y3 = coor_treangle[5]
    
    A = sqrt((x2-x1)**2+(y2-y1)**2)
    B = sqrt((x3-x1)**2+(y3-y1)**2)
    C = sqrt((x3-x2)**2+(y3-y2)**2)

    if not (A + B > C and A + C > B and B + C > A):
        return False
    return True

## Поиск пересечения высот треугольника        
def heights_point(coor_treangle):
    x1 = coor_treangle[0]
    y1 = coor_treangle[1]
    x2 = coor_treangle[2]
    y2 = coor_treangle[3]
    x3 = coor_treangle[4]
    y3 = coor_treangle[5]
    
    A = sqrt((x2-x1)**2+(y2-y1)**2)
    B = sqrt((x3-x1)**2+(y3-y1)**2)
    C = sqrt((x3-x2)**2+(y3-y2)**2)
    
    if C > B and C > A:
        if fabs(C**2 - (B**2 + A**2)) <= 0.000001:
            return x1, y1, x1, y1, x1, y1
    elif B > C and B > A:
        if fabs(B**2 - (C**2 + A**2)) <= 0.000001:
            return x2, y2, x2, y2, x2, y2
    elif A > C and A > B:
        if fabs(A**2 - (C**2 + B**2)) <= 0.000001:
            return x3, y3, x3, y3, x3, y3
        
    if x1 == x2 or y1 == y2:
        k1 = -1 / ((y1 - y3) / (x1 - x3))
        b1 = -k1 * x2 + y2

        x_return_1 = x2
        y_return_1 = y2

        k2 = -1 / ((y3 - y2) / (x3 - x2))
        b2 = -k2 * x1 + y1
        
        x_return_2 = x1
        y_return_2 = y1
        
    elif x2 == x3 or y2 == y3:
        k1 = -1 / ((y2 - y1) / (x2 - x1))
        b1 = -k1 * x3 + y3

        x_return_1 = x3
        y_return_1 = y3

        k2 = -1 / ((y1 - y3) / (x1 - x3))
        b2 = -k2 * x2 + y2

        x_return_2 = x2
        y_return_2 = y2
    else:
        k1 = -1 / ((y2 - y1) / (x2 - x1))
        b1 = -k1 * x3 + y3

        x_return_1 = x3
        y_return_1 = y3

        k2 = -1 / ((y3 - y2) / (x3 - x2))
        b2 = -k2 * x1 + y1

        x_return_2 = x1
        y_return_2 = y1

    heig_point_x = (b2 - b1) / (k1 - k2)
    heig_point_y = k1 * heig_point_x + b1

    return heig_point_x, heig_point_y, x_return_1, y_return_1, x_return_2, y_return_2

## Нахождение минимального угла между осью оХ и прямой
def angle_between_0x_line(coor_line):
    x1 = coor_line[0]
    y1 = coor_line[1]
    x2 = coor_line[2]
    y2 = coor_line[3]
    
    m = x2 - x1
    
    if m == 0:
        return 90
    
    k = (y2 - y1) / m

    return fabs(degrees(atan(k)))

def create_root():
    root = Tk()
    root.geometry("1200x705")
    root.title("Лабораторная №1")
    root.resizable(False,False)

    return root
    
def create_canvas(root):
    canvas = Canvas(root, width = 700, height = 700)
    canvas.place(x = 0, y = 0)
    canvas.create_rectangle(0, 0, 800, 800, outline = "", fill = "white")
    
##    for i in range(70):
##        m = i * 25
##        canvas.create_line(m, 0, m, 700, fill = 'grey')
##        canvas.create_line(0, m , 700, m, fill = 'grey')
        
    canvas.create_line(349, 700, 349, 3, width = "3", arrow = LAST)
    canvas.create_line(0, 349, 700, 349, width = "3", arrow = LAST)

    canvas.create_line(690, 360, 700, 370, width = "3")
    canvas.create_line(690, 370, 700, 360, width = "3")

    canvas.create_line(328, 10, 335, 17, width = "3")
    canvas.create_line(339, 10, 328, 25, width = "3")
    
    return canvas

def key_input(var):
    new = var.get()
    check = False
    
    for i in range(len(new)):
        if (not (new[i] in "1234567890-+. ")) or\
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

def create_widgets(root):
    s = StringVar()
    s.trace('w', lambda nm, idx, mode, var=s: key_input(var))
    
    input_points = Entry(root, width = 50, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s)
    input_points.place(x = 701, y = 25, width = 499, height = 50)

    label_for_add_points = Label(root, text = "Введите координаты точки(-ек) \
через пробел (x1 y1 x2 y2...):")
    label_for_add_points.place(x = 750, y = 0)
 
    label_for_added_points = Label(root, text = "Ваши добавленные точки:")
    label_for_added_points.place(x = 860, y = 145)

    label_for_answer = Label(root, text = "Ваш ответ:")
    label_for_answer.place(x = 0, y = 710)

    all_points_1 = Listbox(root)
    all_points_1.place(x = 710, y = 165, width = 240, height = 200)

    all_points_2 = Listbox(root)
    all_points_2.place(x = 951, y = 165, width = 240, height = 200)
    
    add_points_1 = Button(root, text = "Добавить введенную(-ые) точку(-и)\n\
в первое множество",\
        command = lambda: command_add(input_points,\
        all_points_1, root, 1))
    add_points_1.place(x = 701, y = 78, width = 240, height = 60)

    add_points_2 = Button(root, text = "Добавить введенную(-ые) точку(-и)\n\
во второе множество",\
        command = lambda: command_add(input_points,\
        all_points_2, root, 2))
    add_points_2.place(x = 952, y = 78, width = 240, height = 60)
    
    delete_one_point = Button(root, text = "Удалить выбранную точку",\
        command = lambda: command_delete_one(all_points_1, all_points_2, root))
    delete_one_point.place(x = 701, y = 370, width = 499, height = 50)

    change_one_point = Button(root, text = "Изменить выбранную точку",\
        command = lambda: command_change_one(all_points_1, all_points_2, root))
    change_one_point.place(x = 701, y = 420, width = 499, height = 50)

    delete_all_points = Button(root, text = "Удалить все введенные точки",\
        command = lambda: command_delete_all(all_points_1, all_points_2, root))
    delete_all_points.place(x = 701, y = 470, width = 499, height = 50)

    calculate = Button(root, text ="Изобразить два треугольника и прямую, проходящую\n\
через точки пересечения высот этих треугольников и\n образующую минимальный угол\
 с осью Х.\nНайти угол.",\
        command = lambda: find_angle(root))
    calculate.place(x = 701, y = 520, width = 499, height = 182)

    return input_points, add_points_1, all_points_1, delete_one_point, change_one_point,\
        calculate, label_for_answer

def new_input_x_y(var):
    new = var.get()
    check = False
    FindDot = False
    for i in range(len(new)):
        if (not (new[i] in "1234567890-+.")) or\
           (i > 0 and new[i] in "+-." and new[i-1] in "+-.") or\
           (FindDot and new[i] == '.'):
            check = True
            break
        if len(new) == 1 and new[0] == '+':
            break
        if new[i] == '.':
            FindDot = True
        if new[i] in '+-':
            FindDot = False
    if new == "" or new == "-" or\
       not check:
        key_input.old = new
    else:
        var.set(key_input.old)

def command_delete_one(listbox_1, listbox_2, root):
    cur_el = listbox_1.curselection()
    
    if len(cur_el) != 0:
        listbox_1.delete(cur_el[0])
        coords_1.pop(cur_el[0] * 2)
        coords_1.pop(cur_el[0] * 2)
        add_in_listbox_canvas(listbox_1, root, 1)
        return

    cur_el = listbox_2.curselection()
    
    if len(cur_el) != 0:
        listbox_2.delete(cur_el[0])
        coords_2.pop(cur_el[0] * 2)
        coords_2.pop(cur_el[0] * 2)
        add_in_listbox_canvas(listbox_2, root, 2)
        return

    messagebox.showerror("Ошибка", "Вы ничего не выбрали")

def command_change_one(listbox_1, listbox_2, root):
    global coords_2
    global coords_1
    
    cur_el = listbox_1.curselection()
    listbox = listbox_1
    h = 1
    coords = coords_1
    
    if len(cur_el) == 0:
        cur_el = listbox_2.curselection()
        listbox = listbox_2
        coords = coords_2
        h = 2
        
        if len(cur_el) == 0:
            messagebox.showerror("Ошибка", "Вы ничего не выбрали")
            return
        
    old_x = coords[cur_el[0] * 2]
    old_y = coords[cur_el[0] * 2 + 1]
    
    new_root = Tk()
    new_root.geometry("270x150")
    title = "Изменение точки № " + str(cur_el[0] + 1)
    new_root.title(title)
    new_root.resizable(False,False)

    s1 = StringVar(new_root)
    s2 = StringVar(new_root)
    s1.trace('w', lambda nm, idx, mode, var=s1: new_input_x_y(var))
    s2.trace('w', lambda nm, idx, mode, var=s2: new_input_x_y(var))
    
    info_label = Label(new_root, text = "           Новый x        \
              Новый y")
    info_label.place(x = 0, y = 0)
    
    new_x = Entry(new_root, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s1)
    new_x.place(x = 10, y = 25, width = 120, height = 50)

    new_y = Entry(new_root, justify = CENTER,
        font = ("Calibri", 20), fg = "green", bd = 4, textvariable = s2)
    new_y.place(x = 140, y = 25, width = 120, height = 50)

    change_coords = Button(new_root, text = "Изменить координаты",\
        command = lambda: command_add_new_coords(new_x, new_y, listbox, root,\
        cur_el[0] * 2, new_root, old_x, old_y, h))
    change_coords.place(x = 10, y = 90, width = 250, height = 50)

def command_add_new_coords(x, y, listbox, root, ind, new_root, old_x, old_y, h):
    global coords_1
    global coords_2
    
    new_x = x.get().strip().split()
    new_y = y.get().strip().split()
    text = ""
    
    if len(new_x) == 0:
        text += "Не введен новый x!\n"

    if len(new_y) == 0:
        text += "Не введен новый y!"

    if text != "":
        messagebox.showerror("Ошибка", text)
        return
    
    try:
        new_x = float(new_x[0])
    except:
        text += "Некорректный новый x!\n"

    try:
        new_y = float(new_y[0])
    except:
        text += "Некорректный новый y!\n"

    if text != "":
        messagebox.showerror("Ошибка", text)
        return
    coords = list()

    if h == 1:
        coords = coords_1
    else:
        coords = coords_2
        
    size = len(coords)
    if len(coords) <= ind:
        messagebox.showerror("Ошибка", "Изменено количество точек")
        new_root.destroy()
        return

    if coords[ind] != old_x or coords[ind + 1] != old_y:
        messagebox.showerror("Ошибка", "Выбранная точка уже была изменена")
        new_root.destroy()
        return
            
    for i in range(0, size, 2):
        if new_x == coords[i] and new_y == coords[i + 1]:
            messagebox.showerror("Ошибка", "Уже есть такая точка!")
            return
    coords[ind] = new_x
    coords[ind + 1] = new_y

    if h == 1:
        coords_1 = coords
    else:
        coords_2 = coords
        
    new_root.destroy()
    add_in_listbox_canvas(listbox, root, h)
    
def command_add(entry, listbox, root, h):
    global coords_1
    global coords_2
    
    coord = entry.get().strip().split()
    size = len(coord)
    coords = list()
    
    if size == 0:
        messagebox.showerror("Ошибка", "Вы ничего не ввели!")
        return

    for i in range(size):
        try:
            coord[i] = float(coord[i])
        except:
            messagebox.showerror("Ошибка", "Координаты введены с ошибкой!")
            return
        
    if size % 2 != 0:
        messagebox.showerror("Ошибка", "Вы ввели нечетное количество координат!")
        return

    if h == 1:
        coords = coords_1
    else:
        coords = coords_2
    size_coords = len(coords)
    size_coord = len(coord)
    
    for j in range(0, size_coord, 2):
        check = True
        for i in range(0, len(coords), 2):
            if coords[i] == coord[j] and coords[i + 1] == coord[j + 1]:
                text = "Точка x = " + str(coords[i]) + " y = " + str(coords[i + 1])\
                       + " уже есть в списке"
                messagebox.showwarning("Предупреждение", text)
                check = False
                break;

        if check:
            coords.append(coord[j])
            coords.append(coord[j + 1])

    if (len(coords) > size_coords):
        if h == 1:
            coords_1 = coords
        else:
            coords_2 = coords
        entry.delete(0, END)
        add_in_listbox_canvas(listbox, root, h)
        
def add_in_listbox_canvas(listbox, root, h):
    global canvas
    global result

    scale = 1
    last_scale = 1
    
    canvas.delete("all")
    canvas = create_canvas(root)
    result = dict()
    
    listbox.delete(0, END)

    if h == 1:
        coords = coords_1
    else:
        coords = coords_2
        
    size = len(coords)
    k = 1
    
    if size == 0:
        return

    all_coords = coords_1 + coords_2
    size_coords = len(all_coords)
    max_coord = all_coords[0]

    for i in range(size_coords):
        if fabs(all_coords[i]) > fabs(max_coord):
            max_coord = all_coords[i]

    if max_coord != 0:
        scale = 320 / fabs(max_coord)
    size_1 = len(coords_1)
    size_2 = len(coords_2)

    for i in range(0, size_1, 2):
        canvas.create_oval(349 + scale * coords_1[i] - 3, 349 - scale * coords_1[i + 1] - 3,\
            349 + scale * coords_1[i] + 3, (349 - scale * coords_1[i + 1] + 3), fill = "orange")

    for i in range(0, size_2, 2):
        canvas.create_oval(349 + scale * coords_2[i] - 3, 349 - scale * coords_2[i + 1] - 3,\
            349 + scale * coords_2[i] + 3, (349 - scale * coords_2[i + 1] + 3), fill = "yellow")
        
    for i in range(0, size, 2):
        listbox.insert(END, "№ " + str(k) + " x = " + '{:.5g}'.format(coords[i]) +\
            " y = " + '{:.5g}'.format(coords[i + 1]))
        k += 1
        
        
def command_delete_all(listbox_1, listbox_2, root):
    global canvas
    global coords_1
    global coords_2
    global result
    
    if len(coords_1) == 0 and len(coords_2) == 0:
        messagebox.showerror("Ошибка", "Нет введенных точек!")
        return
    
    canvas.delete("all")
    canvas = create_canvas(root)
    listbox_1.delete(0, END)
    listbox_2.delete(0, END)
    
    coords_1 = list()
    coords_2 = list()
    result = dict()

def find_angle(root):
    global canvas
    
    size_1 = len(coords_1)
    size_2 = len(coords_2)
    
    treangle_1 = list()
    treangle_2 = list()
    cur_treangle = list()

    if size_1 == 0:
        messagebox.showerror("Ошибка", "Вы не ввели координаты в первое множество!")
        return
    if size_2 == 0:
        messagebox.showerror("Ошибка", "Вы не ввели координаты во второе множество!")
        return
    
    for i in range(0, size_1, 2):
        for j in range(i + 2, size_1, 2):
            for k in range(j + 2, size_1, 2):
                cur_treangle.append(coords_1[i])
                cur_treangle.append(coords_1[i + 1])
                cur_treangle.append(coords_1[j])
                cur_treangle.append(coords_1[j + 1])
                cur_treangle.append(coords_1[k])
                cur_treangle.append(coords_1[k + 1])
                
                if treangle_exist(cur_treangle):
                    treangle_1.append(cur_treangle)
                cur_treangle = list()

    for i in range(0, size_2, 2):
        for j in range(i + 2, size_2, 2):
            for k in range(j + 2, size_2, 2):
                cur_treangle.append(coords_2[i])
                cur_treangle.append(coords_2[i + 1])
                cur_treangle.append(coords_2[j])
                cur_treangle.append(coords_2[j + 1])
                cur_treangle.append(coords_2[k])
                cur_treangle.append(coords_2[k + 1])
                
                if treangle_exist(cur_treangle):
                    treangle_2.append(cur_treangle)
                cur_treangle = list()

    len_treangle_1 = len(treangle_1)
    len_treangle_2 = len(treangle_2)

    if len_treangle_1 < 1:
        messagebox.showerror("Ошибка",\
        "Из введенных коррдинат не получвется один и более существующих\
треугольников в первом множестве!")
        return
        
    if len_treangle_2 < 1:
        messagebox.showerror("Ошибка",\
        "Из введенных коррдинат не получвется один и более существующих\
треугольников во втором множестве!")
        return

    angle = 360
    
    for i in range(len_treangle_1):
        x1, y1, x_r_11, y_r_11, x_r_12, y_r_12 = heights_point(treangle_1[i])
        for j in range(len_treangle_2):
            x2, y2, x_r_21, y_r_21, x_r_22, y_r_22 = heights_point(treangle_2[j])
            line = list()
            pick = list()
            
            line.append(x1)
            line.append(y1)
            line.append(x2)
            line.append(y2)

            pick.append(x_r_11)
            pick.append(y_r_11)
            pick.append(x_r_12)
            pick.append(y_r_12)
            pick.append(x_r_21)
            pick.append(y_r_21)
            pick.append(x_r_22)
            pick.append(y_r_22)

            cur_angle = angle_between_0x_line(line)

            if cur_angle < angle:
                result["1"] = treangle_1[i]
                result["2"] = treangle_2[j]
                result["angle"] = cur_angle
                result["line"] = line
                result["pick"] = pick
                angle = cur_angle

    all_coords = result["1"] + result["2"] + result["line"]
    max_coord = all_coords[0]
    size = len(all_coords)
    scale = 1
    last_scale = 1
    
    for i in range(size):
        if fabs(all_coords[i]) > fabs(max_coord):
            max_coord = all_coords[i]

    if max_coord != 0:
        scale = 320 / fabs(max_coord)
    
    canvas.delete("all")
    canvas = create_canvas(root)
    color = "orange"
    
    for i in range(0, size, 2):
        if i == 6:
            color = "yellow"
        if i == 12:
            color = "pink"
        canvas.create_oval(349 + scale * all_coords[i] - 3, 349 - scale * all_coords[i + 1] - 3,\
            349 + scale * all_coords[i] + 3, (349 - scale * all_coords[i + 1] + 3), fill = color)
        
    canvas.create_line(scale * result["1"][0] + 349, 349 - scale * result["1"][1],\
            scale * result["1"][2] + 349, 349 - scale * result["1"][3], fill='red', width = 2)
    canvas.create_line(scale * result["1"][2] + 349, 349 - scale * result["1"][3],\
            scale * result["1"][4] + 349, 349 - scale * result["1"][5], fill='red', width = 2)
    canvas.create_line(scale * result["1"][4] + 349, 349 - scale * result["1"][5],\
            scale * result["1"][0] + 349, 349 - scale * result["1"][1], fill='red', width = 2)
    
    canvas.create_line(scale * result["2"][0] + 349, 349 - scale * result["2"][1],\
            scale * result["2"][2] + 349, 349 - scale * result["2"][3], fill='Fuchsia', width = 2)
    canvas.create_line(scale * result["2"][2] + 349, 349 - scale * result["2"][3],\
            scale * result["2"][4] + 349, 349 - scale * result["2"][5], fill='Fuchsia', width = 2)
    canvas.create_line(scale * result["2"][4] + 349, 349 - scale * result["2"][5],\
            scale * result["2"][0] + 349, 349 - scale * result["2"][1], fill='Fuchsia', width = 2)

    canvas.create_line(scale * result["line"][0] + 349, 349 - scale * result["line"][1],\
            scale * result["line"][2] + 349, 349 - scale * result["line"][3], fill = "green", width = 3)

    canvas.create_line(scale * result["pick"][2] + 349, 349 - scale * result["pick"][3],\
            scale * result["line"][0] + 349, 349 - scale * result["line"][1], fill = "pink", width = 2)

    canvas.create_line(scale * result["pick"][0] + 349, 349 - scale * result["pick"][1],\
            scale * result["line"][0] + 349, 349 - scale * result["line"][1], fill = "pink", width = 2)

    canvas.create_line(scale * result["pick"][4] + 349, 349 - scale * result["pick"][5],\
            scale * result["line"][2] + 349, 349 - scale * result["line"][3], fill = "black", width = 2)
    
    canvas.create_line(scale * result["pick"][6] + 349, 349 - scale * result["pick"][7],\
            scale * result["line"][2] + 349, 349 - scale * result["line"][3], fill = "black", width = 2)

    color = "orange"
    for i in range(0, size, 2):
        if i == 6:
            color = "yellow"
        if i == 12:
            color = "pink"
        text = "({:.3g};{:.3g})".format(all_coords[i], all_coords[i + 1])
        canvas.create_text(349 + scale * all_coords[i] - 5, 349 - scale * all_coords[i + 1] - 5,\
            text = text, fill = "darkblue", font = ("Calibri", 10))
    show_result()

def show_result():
    global result_root
    
    result_root = Tk()
    result_root.geometry("400x300")
    result_root.title("Ответ")
    result_root.resizable(False,False)

    listbox_result = Listbox(result_root)
    listbox_result.place(x = 0, y = 0, width = 400, height = 300)
    
    listbox_result.insert(END, "Координаты точек красного треугольника:\n")
    k = 1
    
    for i in range(0, 6, 2):
        listbox_result.insert(END, "x" + str(k) +\
        ": " + '{:.5g}'.format(result["1"][i]) + " y"\
            + str(k) + ": " + '{:.5g}'.format(result["1"][i+1]) + "\n")
        k += 1

    listbox_result.insert(END, "\n")
    listbox_result.insert(END, "Координаты точек розового треугольника:\n")
    k = 1
    
    for i in range(0, 6, 2):
        listbox_result.insert(END, "x" + str(k) + ": " + '{:.5g}'.format(result["2"][i]) + " y"\
            + str(k) + ": " + '{:.5g}'.format(result["2"][i+1]) + "\n")
        k += 1

    listbox_result.insert(END, "\n")
    listbox_result.insert(END, "Координаты точек пересечения высот в каждом треугольнике:\n")
    k = 1
    text = "В красном: "

    for i in range(0, 4, 2):
        listbox_result.insert(END, text +"x" + str(k) + ": " + '{:.5g}'.format(result["line"][i]) + " y"\
            + str(k) + ": " + '{:.5g}'.format(result["line"][i+1]) + "\n")
        text = "В розовом: "
        k += 1
    listbox_result.insert(END, "\n")
    listbox_result.insert(END, "Минимальный угол между зеленой линией,")
    listbox_result.insert(END, "проходящей через пересечения высот, и осью абсцисс:\n")
    listbox_result.insert(END, '{:.3g}'.format(result["angle"]) + "°")         

def main():
    root = create_root()
    
    global canvas
    canvas = create_canvas(root)
    create_widgets(root)
    root.bind('<Escape>', lambda x: root.destroy())
    
    mainloop();

main();
