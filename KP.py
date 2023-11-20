import tkinter as tk
from tkinter import ttk
from math import radians, cos, sin, pi
import random
import numpy as np


def sign(value):
    """
    функция, возрващающая:
     -1, если выражение меньше 0
     0, если выражение равно 0
     1, если выражение больше 0

    :param value: выражение
    :return:
    """
    if value < 0:
        return -1
    elif value == 0:
        return 0
    else:
        return 1


def destoy(coord,
           point_1,
           point_2,
           point_3,
           point_4):
    """
    метод для вычисления координат поражения элемента
    :param coord: коордианты ребра квадрата
    :param point_1: первая точка опасной области поражения
    :param point_2: вторая точка опасной области поражения
    :param point_3: третья точка опасной области поражения
    :param point_4: четвёртая точка опасной области поражения
    :return: True - произошло попадание, False - не попали
    """

    i = 0
    x, y = coord
    x1, y1 = point_1
    x2, y2 = point_2
    x3, y3 = point_3
    x4, y4 = point_4

    if sign((x - x2) / (x2 - x1) - (y - y2) / (y2 - y1)) == sign((x3 - x2) / (x2 - x1) - (y3 - y2) / (y2 - y1)):
        i += 1
    if sign((x - x3) / (x3 - x2) - (y - y3) / (y3 - y2)) == sign((x4 - x3) / (x3 - x2) - (y4 - y3) / (y3 - y2)):
        i += 1
    if sign((x - x4) / (x4 - x3) - (y - y4) / (y4 - y3)) == sign((x1 - x4) / (x4 - x3) - (y1 - y4) / (y4 - y3)):
        i += 1
    if sign((x - x1) / (x1 - x4) - (y - y1) / (y1 - y4)) == sign((x2 - x1) / (x1 - x4) - (y2 - y1) / (y1 - y4)):
        i += 1

    if i == 4:
        return True
    else:
        return False


# класс параметров каждого объекта
class Params:
    def __init__(self, x, y, a, b, fi, r):
        """
        инициализация каждого объекта
        :param x: координата x на карте
        :param y: коорданат y на карте
        :param a: длина побъекта
        :param b: ширина объекта
        :param fi: угол поворота объекта
        :param r: радиус поражения
        """

        self.x = x
        self.y = y
        self.length = a
        self.width = b
        self.angle = fi
        self.radius = r


# класс логики
class Logic:
    def __init__(self,
                 radius_cp,
                 radius_cp12,
                 radius_cable,
                 radius_rlsv,
                 radius_sc,
                 radius_eg):
        """
        инициализация параметров
        :param radius_cp: радиус поражения командного пункта
        :param radius_cp12: радиус поражения комнадного пункта 1 и 2
        :param radius_cable: радиусы поражения кабелей
        :param radius_rlsv: радиусы поражения РЛС и РЛВ
        :param radius_sc: радиусы поражения самоходных установок
        :param radius_eg: радиусы поражения энергогенераторов
        """

        radius_cp = int(radius_cp)
        radius_cp12 = int(radius_cp12)
        radius_cable = float(radius_cable)
        radius_rlsv = int(radius_rlsv)
        radius_sc = int(radius_sc)
        radius_eg = int(radius_eg)

        # расположение объектов
        self.objects = [Params(270, 280, 25, 25, 8, radius_cp),
                        Params(420, 110, 25, 25, 15, radius_cp12),
                        Params(300, 480, 25, 25, 41, radius_cp12),
                        Params(170, 50, 25, 25, 35, radius_rlsv),
                        Params(130, 500, 25, 25, 81, radius_rlsv),
                        Params(480, 220, 25, 25, 1, radius_sc),
                        Params(440, 350, 25, 25, 1, radius_sc),
                        Params(550, 440, 25, 25, 13, radius_sc),
                        Params(90, 270, 25, 25, 1, radius_eg),
                        Params(540, 40, 25, 25, 32, radius_eg),
                        Params(490, 530, 25, 25, 13, radius_eg),
                        Params(45, 270, 90, 4, 1, radius_cable),
                        Params(180, 275, 180.2, 4, 3.1, radius_cable),
                        Params(130, 160, 234, 4, -70, radius_cable),
                        Params(110, 385, 233.4, 4, 80.1, radius_cable),
                        Params(220, 165, 250.79, 4, 66.5, radius_cable),
                        Params(200, 390, 260.7, 4, -57.52, radius_cable),
                        Params(345, 195, 226.7, 4, -48.57, radius_cable),
                        Params(285, 380, 202.2, 4, 81.46, radius_cable),
                        Params(480, 75, 138.9, 4, -30.2, radius_cable),
                        Params(395, 505, 196.46, 4, 14.74, radius_cable),
                        Params(450, 165, 125.29, 4, 61.3, radius_cable),
                        Params(460, 285, 136, 4, -72.89, radius_cable),
                        Params(490, 395, 142.12, 4, 39.28, radius_cable),
                        Params(425, 460, 253.17, 4, -9, radius_cable)]

        # повреждённые объекты
        self.damage_objects = []
        self.func_elem = [True for _ in range(25)]  # список состояний функциональных элементов

    def return_objects(self):
        return self.objects

    def danger_area_explose_area(self):
        """
        метод для вычисления области опасных взрывов
        :return:
        """
        for obj in self.objects:
            fi_rad = radians(-obj.angle)  # перевод угла из градусов в радианы
            d_x1 = (obj.length / 2 + obj.radius) * cos(fi_rad)
            d_x2 = (obj.width / 2 + obj.radius) * cos(pi / 2 - fi_rad)
            d_y1 = (obj.length / 2 + obj.radius) * sin(fi_rad)
            d_y2 = (obj.width / 2 + obj.radius) * sin(pi / 2 - fi_rad)

            # координаты вершин области опасных разрывов
            x1 = obj.x - d_x1 - d_x2
            y1 = obj.y + d_y1 - d_y2

            x2 = obj.x + d_x1 - d_x2
            y2 = obj.y - d_y1 - d_y2

            x3 = obj.x + d_x1 + d_x2
            y3 = obj.y - d_y1 + d_y2

            x4 = obj.x - d_x1 + d_x2
            y4 = obj.y + d_y1 + d_y2
            self.damage_objects.append(((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

    def solve_fe(self):
        """
        метод для расчёта ДУКР
        :return: dukr - дискретный уровень качества решения
        """

        dukr = [0 for _ in range(7)]  # частота попаданий

        f_0 = self.func_elem[1] and self.func_elem[2] and self.func_elem[5] * self.func_elem[6] and self.func_elem[7] \
              and ((self.func_elem[17] and self.func_elem[21] and self.func_elem[22] and self.func_elem[23] and
                    self.func_elem[24] and (not self.func_elem[18]))
                   or (self.func_elem[17] and self.func_elem[21] and self.func_elem[22] and self.func_elem[23]
                       and (not self.func_elem[24]) and self.func_elem[18])
                   or (self.func_elem[17] and self.func_elem[21] and self.func_elem[22] and (not self.func_elem[23])
                       and self.func_elem[24] and self.func_elem[18])
                   or (self.func_elem[17] and self.func_elem[21] and (not self.func_elem[22]) and self.func_elem[23]
                       and self.func_elem[24] and self.func_elem[18])
                   or (self.func_elem[17] and (not self.func_elem[21]) and self.func_elem[22] and self.func_elem[23]
                       and self.func_elem[24] and self.func_elem[18])
                   or ((not self.func_elem[17]) and self.func_elem[21] and self.func_elem[22] and self.func_elem[23]
                       and self.func_elem[24] and self.func_elem[18]))

        f_1 = self.func_elem[1] and self.func_elem[2] and self.func_elem[17] and self.func_elem[18] and (
                (self.func_elem[5] and self.func_elem[6] and self.func_elem[21] and self.func_elem[22] and
                 ((not self.func_elem[7]) or ((self.func_elem[7]) and (not self.func_elem[23]) and (
                     not self.func_elem[24])))) or (
                        self.func_elem[5] and self.func_elem[7] and self.func_elem[21] and self.func_elem[24] and
                        ((not self.func_elem[6]) or (self.func_elem[6] and (not self.func_elem[22]) and
                                                     (not self.func_elem[23])))) or (
                        self.func_elem[6] and self.func_elem[7] and self.func_elem[23] and self.func_elem[24] and
                        ((not self.func_elem[5]) or (
                                self.func_elem[5] and (not self.func_elem[21]) and (not self.func_elem[22])))))

        f_2 = self.func_elem[5] and self.func_elem[22] and self.func_elem[6] and self.func_elem[23] and self.func_elem[
            7] and ((self.func_elem[1] and self.func_elem[17] and self.func_elem[21] and (
                (not self.func_elem[2]) or (self.func_elem[2] and
                                            (not self.func_elem[18]) and (not self.func_elem[24])))) or (
                            self.func_elem[2] and self.func_elem[18] and self.func_elem[24] and
                            ((not self.func_elem[1]) or (
                                    self.func_elem[1] and (not self.func_elem[17]) and (not self.func_elem[21])))))

        f_3 = self.func_elem[1] and self.func_elem[2] and self.func_elem[17] and (
                (self.func_elem[5] and self.func_elem[21] and (
                        (not self.func_elem[6]) and (self.func_elem[6] and (not self.func_elem[22]))) and (
                         (not self.func_elem[7]) or (self.func_elem[7] and (not self.func_elem[24])))) or (
                    ((self.func_elem[7] and self.func_elem[24]) and (
                            (not self.func_elem[5]) or (self.func_elem[5] and (not self.func_elem[21]))) and (
                             (not self.func_elem[6]) or (self.func_elem[6] and (not self.func_elem[23]))))))

        f_4 = self.func_elem[6] and (
                (self.func_elem[1] and self.func_elem[5] and self.func_elem[17] and self.func_elem[21] and
                 self.func_elem[22] and (
                         (not self.func_elem[2]) or (self.func_elem[2] and (not self.func_elem[18]))) and (
                         (not self.func_elem[7]) or (self.func_elem[7] and (not self.func_elem[23])))) or (
                    (self.func_elem[2] and self.func_elem[7] and self.func_elem[18] and self.func_elem[23] and
                     self.func_elem[24] and (
                             (not self.func_elem[1]) or (self.func_elem[1] and (not self.func_elem[17]))) and (
                             (not self.func_elem[5]) or (self.func_elem[5] and (not self.func_elem[22]))))))

        f_5 = (self.func_elem[1] and self.func_elem[5] and self.func_elem[17] and self.func_elem[21] and (
                (not self.func_elem[2]) or (self.func_elem[2] and (not self.func_elem[18]))) and (
                       (not self.func_elem[6]) or (self.func_elem[6] and (not self.func_elem[22])))) or (
                      self.func_elem[2] and self.func_elem[7] and self.func_elem[18] and self.func_elem[24] and (
                      (not self.func_elem[1]) or (self.func_elem[1] and (not self.func_elem[17]))) and (
                              (not self.func_elem[6]) or (self.func_elem[6] and (not self.func_elem[23]))))

        f_6 = ((not self.func_elem[1]) or (self.func_elem[1] and (not self.func_elem[5])) or (
                self.func_elem[1] and self.func_elem[5] and (not self.func_elem[17])) or (
                       self.func_elem[1] and self.func_elem[5] and self.func_elem[17] and (
                   not self.func_elem[21]))) and (
                      (not self.func_elem[2]) or (self.func_elem[2] and (not self.func_elem[7])) or (
                      self.func_elem[2] and self.func_elem[7] and (not self.func_elem[18])) or (
                              self.func_elem[2] and self.func_elem[7] and self.func_elem[18] and (
                          not self.func_elem[24])))

        kp = self.func_elem[0] and self.func_elem[4] and self.func_elem[16] and (
                (self.func_elem[11] and self.func_elem[12]) or (self.func_elem[3] and self.func_elem[15] and (
                self.func_elem[12] or self.func_elem[13] or self.func_elem[14])))

        if kp and f_0:
            dukr[0] += 1
        elif kp and f_1:
            dukr[1] += 1
        elif kp and f_2:
            dukr[2] += 1
        elif kp and f_3:
            dukr[3] += 1
        elif kp and f_4:
            dukr[4] += 1
        elif kp and f_5:
            dukr[5] += 1
        elif f_6 or (not kp):
            dukr[6] += 1

        return dukr

    def calculate_figures(self, ellipse, defeat, colors):
        """
        метод для преобразования координат фигур для построения
        :param ellipse: параметры элипсов рассеивания
        :param defeat: координаты точек попадания
        :param colors: цвета наполнения фигур
        :return: figures - словарь фигур
        """

        rectangle = []
        line = []
        circle = []
        hit = []

        figures = {"line": line,
                   "rectangle": rectangle,
                   "circle": circle,
                   "point": hit}

        for index, info in enumerate(self.objects):
            if index < 11:
                x = info.x
                y = info.y
                width = info.width
                length = info.length
                angle = info.angle

                # Находим координаты вершин прямоугольника относительно его центра
                half_length = length / 2
                half_width = width / 2
                vertices = [
                    (-half_length, -half_width),  # Левая нижняя вершина
                    (half_length, -half_width),  # Правая нижняя вершина
                    (half_length, half_width),  # Правая верхняя вершина
                    (-half_length, half_width)  # Левая верхняя вершина
                ]

                # Применяем матрицу поворота к каждой вершине прямоугольника
                rotated_vertices = []
                for vertex in vertices:
                    x_new = vertex[0] * cos(angle) - vertex[1] * sin(angle)
                    y_new = vertex[0] * sin(angle) + vertex[1] * cos(angle)
                    rotated_vertices.append((x + x_new, y + y_new))

                rectangle.append((rotated_vertices, colors[index]))

            # расчёт линий
            else:
                x_center = info.x
                y_center = info.y
                length = info.length
                angle = info.angle

                x_delta = length * cos(radians(angle))
                y_delta = length * sin(radians(angle))

                start_x = x_center - x_delta / 2
                start_y = y_center - y_delta / 2
                end_x = x_center + x_delta / 2
                end_y = y_center + y_delta / 2

                line.append(((end_x, end_y, start_x, start_y), colors[index]))

        for values in ellipse:
            x, y = values[0]  # координаты центра эллипса
            a, b = values[1]  # ширина и высота эллипса

            circle.append(((x - a / 2, y - b / 2,
                            x + a / 2, y + b / 2)))

        for point in defeat:
            x, y = point
            point_size = 2
            hit.append((x - point_size, y - point_size, x + point_size, y + point_size))

        return figures

    def damage_calculation(self,
                           range_to_traverse,
                           combat_route,
                           interval_form,
                           interval_series,
                           num_implement,
                           num_acp,
                           target_disp,
                           weapon,
                           num_ammunition,
                           ammunition_disp,
                           technical_disp):

        """
        метод вычислений урона
        :param range_to_traverse: дальность до траверза
        :param combat_route: боевой маршрут центра пары
        :param interval_form: интервал строя
        :param interval_series: интервал серии
        :param num_implement: количество реализаций
        :param num_acp: количество АСП
        :param target_disp: прицельное рассеивание
        :param weapon: вариант вооружения
        :param num_ammunition: количество суббоеприпасов
        :param ammunition_disp: рассеивание суббоеприпасов СП
        :param technical_disp: техническое рассеивание
        :return:
        scat_ellipse - список координат для 4-ч эллипсов
        boom_list - список координат точек попадания
        color - список цветов наполнения фигур
        discret_level - ДУКР
        """
        range_to_traverse = int(range_to_traverse)
        combat_route = int(combat_route)
        interval_form = int(interval_form)
        interval_series = int(interval_series)
        num_implement = int(num_implement)
        num_acp = int(num_acp)
        target_disp = int(target_disp)
        weapon = weapon
        num_ammunition = int(num_ammunition)
        ammunition_disp = int(ammunition_disp)
        technical_disp = int(technical_disp)

        aim_point = list()  # список точек прицеливания
        boom_list = []  # список координат точек взрывов
        scat_ellipse = []  # список параметров элипса рассеивания
        color = ["green" for _ in range(25)]  # список цветов (зелёный - функционирует, красный - поразили)
        discret_level = 0  # дукр

        aim_point.append((350 - range_to_traverse, 300 - combat_route + interval_form))
        aim_point.append((350 - range_to_traverse + interval_series, 300 - combat_route + interval_form))
        aim_point.append((350 - range_to_traverse, 300 - combat_route - interval_form))
        aim_point.append((350 - range_to_traverse + interval_series, 300 - combat_route - interval_form))

        # перебор всех заходов на бомбометание по ЗРК
        for num_bomb in range(num_implement):
            # формируем список состояний элементов ЗРК
            for elem in range(25):
                self.func_elem[elem] = True

            # перебор 4-х залпов
            for num_area in range(4):
                # реализация координат центров залпов
                x_zalp = random.gauss(aim_point[num_area][0], target_disp)
                y_zalp = random.gauss(aim_point[num_area][1], target_disp)

                # идём по АСП
                for acp in range(round(num_acp / 2)):
                    # если не ОФАБ
                    if "ОФАБ" not in weapon:
                        for ammunition in range(num_ammunition):
                            x_boom = x_zalp + np.random.uniform(-3 * ammunition_disp, 3 * ammunition_disp)
                            y_boom = y_zalp + np.random.uniform(-ammunition_disp, ammunition_disp)

                            # проход по каждому функциональному элементу ЗРК
                            for num_func_elem in range(len(self.func_elem)):
                                # если боеприпас нанёс урон, то есть попал в ФЭ
                                if destoy((x_boom, y_boom), self.damage_objects[num_func_elem][0],
                                          self.damage_objects[num_func_elem][1],
                                          self.damage_objects[num_func_elem][2], self.damage_objects[num_func_elem][3]):
                                    self.func_elem[num_func_elem] = False
                                    color[num_func_elem] = "red"

                            # для отрисовки только первой реализации
                            if num_bomb == 0:
                                boom_list.append((x_boom, y_boom))

                                if (ammunition == 0) and (acp == 0):
                                    scat_ellipse.append(
                                        ((x_zalp, y_zalp), (ammunition_disp * 7, ammunition_disp * 2.5)))

                    # если ОФАБ
                    else:
                        x_fab = random.gauss(x_zalp, technical_disp)
                        y_fab = random.gauss(y_zalp, technical_disp)
                        boom_list.append((x_fab, y_fab))

                        for num_fe in range(len(self.func_elem)):
                            if destoy((x_fab, y_fab), self.damage_objects[num_fe][0], self.damage_objects[num_fe][1],
                                      self.damage_objects[num_fe][2], self.damage_objects[num_fe][3]):
                                self.func_elem[num_fe] = False
                                color[num_fe] = "red"

                        # для отрисовки первой реализации
                        if num_bomb == 0:

                            if acp == 0:
                                scat_ellipse.append(((x_zalp, y_zalp), (technical_disp * 6, technical_disp * 6)))

            discret_level = self.solve_fe()

        return scat_ellipse, boom_list, color, discret_level


class Draw(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Решение")
        self.canvas = tk.Canvas(self, width=600, height=600)
        self.canvas.pack()

        self.texts = {"КП": [310, 280],
                      "КП-1": [450, 110],
                      "КП-2": [330, 480],
                      "РЛС": [210, 50],
                      "РЛВ": [170, 500],
                      "СУ-1": [510, 220],
                      "СУ-2": [470, 350],
                      "СУ-3": [580, 440],
                      "ЭГ": [120, 270],
                      "ЭГ-1": [570, 40],
                      "ЭГ-2": [520, 530],
                      }

    def draw_figures(self, figures):
        """
        метод для отрисовки фигур
        :param figures: словарь параметров фигур
        :return:
        """

        for key, parameters in figures.items():

            # если у нас линия
            if key == "line":
                for data in parameters:
                    self.canvas.create_line(data[0], width=4, fill=data[1])

            # если у нас прямоугольник
            elif key == "rectangle":
                for param in parameters:
                    self.canvas.create_polygon(param[0], fill=param[1])
                    self.canvas.update()

            # если у нас эллипс
            elif key == "circle":
                for points in parameters:
                    self.canvas.create_oval(points, outline="blue")

            # если у нас точка взрыва
            elif key == "point":
                for coordinates in parameters:
                    self.canvas.create_oval(coordinates, fill="red")

        for text, point in self.texts.items():
            self.canvas.create_text(point[0], point[1], text=text, font=("Arial", 11))

    def drawing(self):
        self.mainloop()


class Widget:
    def __init__(self):
        """
        Инициализация виджета
        """

        self.window = tk.Tk()
        self.window.title("Моделирование бомбометания")
        self.input_data = dict()  # словарь входных данных
        self.output = []  # список окон, куда выводится информация
        self.draw = Draw()
        self.ent_weapon = dict()

        # список форматов окон
        self.border_effects = {
            "flat": tk.FLAT,
            "sunken": tk.SUNKEN,
            "raised": tk.RAISED,
            "groove": tk.GROOVE,
            "ridge": tk.RIDGE,
        }

        # виджет для характеристик рассеивания и режима бомбометания
        self.frm_chts = tk.Frame(master=self.window, width=380, height=400, relief=self.border_effects["raised"],
                                 borderwidth=5)
        self.frm_chts.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        # виждет для вариантов вооружения и радиуса поражения
        self.frm_opt_rad = tk.Frame(master=self.window, width=310, height=100, relief=self.border_effects["raised"],
                                    borderwidth=5)
        self.frm_opt_rad.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        # виджет для частоты попадания в ФЭ
        self.frm_freq = tk.Frame(master=self.window, width=180, height=100, relief=self.border_effects["raised"],
                                 borderwidth=5)
        self.frm_freq.pack(fill=tk.BOTH, side=tk.LEFT, expand=True)

        btn_model = tk.Button(master=self.frm_freq, text="Моделирование", command=self.update_data)
        btn_model.place(x=40, y=270)

    def characteristics(self):
        """
        метод для отображения характеристик рассеивания
        :return:
        """
        # заголовок раздела характеристик
        lbl_chrs = tk.Label(master=self.frm_chts, text="Характеристики рассеивания")
        lbl_chrs.place(x=100, y=0)

        # прицельное рассеивание - текст
        lbl_aim = tk.Label(master=self.frm_chts, text="Прицельное рассеивание, [м]")
        lbl_aim.place(x=2, y=20)

        # прицельное рассеивание - ввод
        ent_aim = tk.Entry(master=self.frm_chts)
        ent_aim.place(x=220, y=20)
        ent_aim.insert(0, "35")
        self.input_data["прицельное рассеивание"] = ent_aim

        # техническое прицеливание - текст
        lbl_tech = tk.Label(master=self.frm_chts, text="Техническое рассеивание, [м]")
        lbl_tech.place(x=2, y=50)

        # техническое прицеливание - ввод
        ent_tech = tk.Entry(master=self.frm_chts)
        ent_tech.place(x=220, y=50)
        ent_tech.insert(0, "10")
        self.input_data["техническое рассеивание"] = ent_tech

        # рассеивание суббоеприпасов - текст
        lbl_disp = tk.Label(master=self.frm_chts, text="Рассеивание суббоеприпасов, [м]")
        lbl_disp.place(x=2, y=80)

        # рассеивание суббоеприпасов - ввод
        ent_disp = tk.Entry(master=self.frm_chts)
        ent_disp.place(x=220, y=80)
        ent_disp.insert(0, "40")
        self.input_data["рассеивание суббоеприпасов"] = ent_disp

    def mode_bomb(self):
        """
        метод для отображения режима бомбометания
        :return:
        """

        # заголовок режимов бомбометания
        lbl_mode = tk.Label(master=self.frm_chts, text="Режим бомбометания")
        lbl_mode.place(x=120, y=110)

        # боевой маршрут центра пары - текст
        lbl_route = tk.Label(master=self.frm_chts, text="Боевой маршрут центра пары")
        lbl_route.place(x=2, y=140)

        # боевой маршрут центра пары - ввод
        ent_route = tk.Entry(master=self.frm_chts)
        ent_route.place(x=220, y=140)
        ent_route.insert(0, "100")
        self.input_data["боевой маршрут"] = ent_route

        # дальность до траверза - текст
        lbl_dist = tk.Label(master=self.frm_chts, text="Дальность до траверза КП, [м]")
        lbl_dist.place(x=2, y=170)

        # дальность до траверза - ввод
        ent_dist = tk.Entry(master=self.frm_chts)
        ent_dist.place(x=220, y=170)
        ent_dist.insert(0, "50")
        self.input_data["дальность до траверза"] = ent_dist

        # интервал строя - текст
        lbl_build = tk.Label(master=self.frm_chts, text="Интервал строя, [м]")
        lbl_build.place(x=2, y=200)

        # выпадающий список для интервала строя
        build = ["100", "200", "300", "400"]
        cbx_build = ttk.Combobox(master=self.frm_chts, values=build)
        cbx_build.place(x=220, y=200)
        cbx_build.set("100")
        self.input_data["интервал строя"] = cbx_build

        # интерал серии - текст
        lbl_series = tk.Label(master=self.frm_chts, text="Интервал серии, [м]")
        lbl_series.place(x=2, y=230)

        # интервал серии - ввод
        ent_series = tk.Entry(master=self.frm_chts)
        ent_series.place(x=220, y=230)
        ent_series.insert(0, "150")
        self.input_data["интервал серии"] = ent_series

        # высота бомбометания - текст
        lbl_height = tk.Label(master=self.frm_chts, text="Высота бомбометания, [м]")
        lbl_height.place(x=2, y=260)

        # выпадающий список для высоты бомбометания
        height = ["500", "1500", "3000"]
        cbx_height = ttk.Combobox(master=self.frm_chts, values=height)
        cbx_height.place(x=220, y=260)
        cbx_height.set("1500")
        self.input_data["высота бомбометания"] = cbx_height

        # количество АСП - текст
        lbl_count = tk.Label(master=self.frm_chts, text="Количество АСП, [шт]")
        lbl_count.place(x=2, y=290)

        # количество АСП - ввод
        ent_count = tk.Entry(master=self.frm_chts)
        ent_count.place(x=220, y=290)
        ent_count.insert(0, "38")
        self.input_data["количество АСП"] = ent_count

        # кодичество суббоеприпасов СП - текст
        lbl_sp = tk.Label(master=self.frm_chts, text="Количество суббоеприпасов СП, [шт]")
        lbl_sp.place(x=2, y=320)

        # количество суббоеприпасов СП - ввод
        ent_sp = tk.Entry(master=self.frm_chts)
        ent_sp.place(x=220, y=320)
        ent_sp.insert(0, "0")
        self.input_data["количество суббоеприпасов"] = ent_sp
        self.ent_weapon["количество суббоеприпасов"] = ent_sp

    def insert_param(self, weapon):
        """
        метод добавления информации при выборе варианта вооружения
        :param entry: переменная текстового поля, куда введётся новая информация
        :param weapon: какой вид вооружения выбран
        :return:
        """

        match weapon:
            case "ОФАБ-100-120":
                self.ent_weapon["радиус КП"].delete(0, tk.END)
                self.ent_weapon["радиус КП"].insert(0, str(23))
                self.ent_weapon["радиус КП 1 и 2"].delete(0, tk.END)
                self.ent_weapon["радиус КП 1 и 2"].insert(0, str(23))
                self.ent_weapon["радиус СУ"].delete(0, tk.END)
                self.ent_weapon["радиус СУ"].insert(0, str(23))
                self.ent_weapon["радиус РЛС, РЛВ"].delete(0, tk.END)
                self.ent_weapon["радиус РЛС, РЛВ"].insert(0, str(24))
                self.ent_weapon["радиус ЭГ"].delete(0, tk.END)
                self.ent_weapon["радиус ЭГ"].insert(0, str(20))
                self.ent_weapon["радиус кабелей"].delete(0, tk.END)
                self.ent_weapon["радиус кабелей"].insert(0, str(3.4))

            case "ОФАБ-250":
                self.ent_weapon["радиус КП"].delete(0, tk.END)
                self.ent_weapon["радиус КП"].insert(0, str(26))
                self.ent_weapon["радиус КП 1 и 2"].delete(0, tk.END)
                self.ent_weapon["радиус КП 1 и 2"].insert(0, str(26))
                self.ent_weapon["радиус СУ"].delete(0, tk.END)
                self.ent_weapon["радиус СУ"].insert(0, str(26))
                self.ent_weapon["радиус РЛС, РЛВ"].delete(0, tk.END)
                self.ent_weapon["радиус РЛС, РЛВ"].insert(0, str(27))
                self.ent_weapon["радиус ЭГ"].delete(0, tk.END)
                self.ent_weapon["радиус ЭГ"].insert(0, str(22))
                self.ent_weapon["радиус кабелей"].delete(0, tk.END)
                self.ent_weapon["радиус кабелей"].insert(0, str(4.6))
            case "РБС-Ф025-33":
                self.ent_weapon["радиус КП"].delete(0, tk.END)
                self.ent_weapon["радиус КП"].insert(0, str(13))
                self.ent_weapon["радиус КП 1 и 2"].delete(0, tk.END)
                self.ent_weapon["радиус КП 1 и 2"].insert(0, str(13))
                self.ent_weapon["радиус СУ"].delete(0, tk.END)
                self.ent_weapon["радиус СУ"].insert(0, str(13))
                self.ent_weapon["радиус РЛС, РЛВ"].delete(0, tk.END)
                self.ent_weapon["радиус РЛС, РЛВ"].insert(0, str(14))
                self.ent_weapon["радиус ЭГ"].delete(0, tk.END)
                self.ent_weapon["радиус ЭГ"].insert(0, str(12))
                self.ent_weapon["радиус кабелей"].delete(0, tk.END)
                self.ent_weapon["радиус кабелей"].insert(0, str(2.4))
                self.ent_weapon["количество суббоеприпасов"].delete(0, tk.END)
                self.ent_weapon["количество суббоеприпасов"].insert(0, str(48))
            case "РБК-250-АО.25":
                self.ent_weapon["радиус КП"].delete(0, tk.END)
                self.ent_weapon["радиус КП"].insert(0, str(0))
                self.ent_weapon["радиус КП 1 и 2"].delete(0, tk.END)
                self.ent_weapon["радиус КП 1 и 2"].insert(0, str(0))
                self.ent_weapon["радиус СУ"].delete(0, tk.END)
                self.ent_weapon["радиус СУ"].insert(0, str(0))
                self.ent_weapon["радиус РЛС, РЛВ"].delete(0, tk.END)
                self.ent_weapon["радиус РЛС, РЛВ"].insert(0, str(0))
                self.ent_weapon["радиус ЭГ"].delete(0, tk.END)
                self.ent_weapon["радиус ЭГ"].insert(0, str(0))
                self.ent_weapon["радиус кабелей"].delete(0, tk.END)
                self.ent_weapon["радиус кабелей"].insert(0, str(0.6))
                self.ent_weapon["количество суббоеприпасов"].delete(0, tk.END)
                self.ent_weapon["количество суббоеприпасов"].insert(0, str(52))
            case "РБК-500-АО.25":
                self.ent_weapon["радиус КП"].delete(0, tk.END)
                self.ent_weapon["радиус КП"].insert(0, str(0))
                self.ent_weapon["радиус КП 1 и 2"].delete(0, tk.END)
                self.ent_weapon["радиус КП 1 и 2"].insert(0, str(0))
                self.ent_weapon["радиус СУ"].delete(0, tk.END)
                self.ent_weapon["радиус СУ"].insert(0, str(0))
                self.ent_weapon["радиус РЛС, РЛВ"].delete(0, tk.END)
                self.ent_weapon["радиус РЛС, РЛВ"].insert(0, str(0))
                self.ent_weapon["радиус ЭГ"].delete(0, tk.END)
                self.ent_weapon["радиус ЭГ"].insert(0, str(0))
                self.ent_weapon["радиус кабелей"].delete(0, tk.END)
                self.ent_weapon["радиус кабелей"].insert(0, str(0.6))
                self.ent_weapon["количество суббоеприпасов"].delete(0, tk.END)
                self.ent_weapon["количество суббоеприпасов"].insert(0, str(70))

        return "good"

    def variants(self):
        """
        метод для отображения вариантов вооружения
        :return:
        """

        # заголовок вариантов вооружения
        lbl_opt = tk.Label(master=self.frm_opt_rad, text="Варианты вооружения")
        lbl_opt.place(x=90, y=0)

        # Создание переменной для отслеживания выбранного варианта
        selected_option = tk.StringVar(value="ОФАБ-100-120")  # Установка начального значения

        # Создание радиокнопок для каждого варианта
        option1 = tk.Radiobutton(master=self.frm_opt_rad, text="ОФАБ-100-120", variable=selected_option,
                                 value="ОФАБ-100-120", command=lambda: self.insert_param("ОФАБ-100-120"))
        option2 = tk.Radiobutton(master=self.frm_opt_rad, text="ОФАБ-250", variable=selected_option,
                                 value="ОФАБ-250", command=lambda: self.insert_param("ОФАБ-250"))
        option3 = tk.Radiobutton(master=self.frm_opt_rad, text="РБС-Ф025-33", variable=selected_option,
                                 value="РБС-Ф025-33", command=lambda: self.insert_param("РБС-Ф025-33"))
        option4 = tk.Radiobutton(master=self.frm_opt_rad, text="РБК-250-АО.25", variable=selected_option,
                                 value="РБК-250-АО.25", command=lambda: self.insert_param("РБК-250-АО.25"))
        option5 = tk.Radiobutton(master=self.frm_opt_rad, text="РБК-500-АО.25", variable=selected_option,
                                 value="РБК-500-АО.25", command=lambda: self.insert_param("РБК-500-АО.25"))

        option1.place(x=100, y=30)
        option2.place(x=100, y=50)
        option3.place(x=100, y=70)
        option4.place(x=100, y=90)
        option5.place(x=100, y=110)

        self.input_data["варианты вооружения"] = selected_option

    def radius(self):
        """
        метод для отображения радиусов поражения ФЭ
        :return:
        """

        # заголов раздела радиусов поражения ФЭ
        lbl_rads = tk.Label(master=self.frm_opt_rad, text="Радиусы поражения ФЭ")
        lbl_rads.place(x=88, y=140)

        # радиус КП - текст
        lbl_rad_kp = tk.Label(master=self.frm_opt_rad, text="Радиус КП, [м]")
        lbl_rad_kp.place(x=2, y=170)

        # радиус КП - ввод
        ent_rad_kp = tk.Entry(master=self.frm_opt_rad)
        ent_rad_kp.place(x=170, y=170)
        ent_rad_kp.insert(0, "23")
        self.input_data["радиус КП"] = ent_rad_kp
        self.ent_weapon["радиус КП"] = ent_rad_kp

        # радиусы - текст
        lbl_rad_kp12 = tk.Label(master=self.frm_opt_rad, text="Радиус КП1, КП2, [м]")
        lbl_rad_kp12.place(x=2, y=200)

        # радиусы - ввод
        ent_rad_kp12 = tk.Entry(master=self.frm_opt_rad)
        ent_rad_kp12.place(x=170, y=200)
        ent_rad_kp12.insert(0, "23")
        self.input_data["радиус КП 1 и 2"] = ent_rad_kp12
        self.ent_weapon["радиус КП 1 и 2"] = ent_rad_kp12

        # радиусы СУ - текст
        lbl_rad_su = tk.Label(master=self.frm_opt_rad, text="Радиус СУ1, СУ2, СУ3, [м]")
        lbl_rad_su.place(x=2, y=230)

        # радиусы СУ - ввод
        ent_rad_su = tk.Entry(master=self.frm_opt_rad)
        ent_rad_su.place(x=170, y=230)
        ent_rad_su.insert(0, "23")
        self.input_data["радиус СУ"] = ent_rad_su
        self.ent_weapon["радиус СУ"] = ent_rad_su

        # радиусы РЛ - текст
        lbl_rls_rlv = tk.Label(master=self.frm_opt_rad, text="Радиус РЛС, РЛВ, [м]")
        lbl_rls_rlv.place(x=2, y=260)

        # радиусы РЛ - ввод
        ent_rls_rlv = tk.Entry(master=self.frm_opt_rad)
        ent_rls_rlv.place(x=170, y=260)
        ent_rls_rlv.insert(0, "24")
        self.input_data["радиус РЛС, РЛВ"] = ent_rls_rlv
        self.ent_weapon["радиус РЛС, РЛВ"] = ent_rls_rlv

        # радиусы ЭГ - текст
        lbl_eg = tk.Label(master=self.frm_opt_rad, text="Радиус ЭГ1, ЭГ2, [м]")
        lbl_eg.place(x=2, y=290)

        # радиусы ЭГ - ввод
        ent_eg = tk.Entry(master=self.frm_opt_rad)
        ent_eg.place(x=170, y=290)
        ent_eg.insert(0, "20")
        self.input_data["радиус ЭГ"] = ent_eg
        self.ent_weapon["радиус ЭГ"] = ent_eg

        # радиусы кабелей - текст
        lbl_cabel = tk.Label(master=self.frm_opt_rad, text="Радиус кабелей, [м]")
        lbl_cabel.place(x=2, y=320)

        # радиусы кабелей - ввод
        ent_cabel = tk.Entry(master=self.frm_opt_rad)
        ent_cabel.place(x=170, y=320)
        ent_cabel.insert(0, "3.4")
        self.input_data["радиус кабелей"] = ent_cabel
        self.ent_weapon["радиус кабелей"] = ent_cabel

        # Количество реализаций - текст
        lbl_real = tk.Label(master=self.frm_opt_rad, text="Количество реализаций")
        lbl_real.place(x=2, y=350)

        # количество реализаций - ввод
        ent_real = tk.Entry(master=self.frm_opt_rad)
        ent_real.place(x=170, y=350)
        ent_real.insert(0, "1")
        self.input_data["количество реализаций"] = ent_real

    def frequency(self):
        """
        метод для отображения рамки частоты попадания по ФЭ
        :return:
        """

        # частота попадания по ФЭ
        lbl_freq = tk.Label(master=self.frm_freq, text="Частота попадания по ФЭ")
        lbl_freq.place(x=10, y=0)

        lbl_w0 = tk.Label(master=self.frm_freq, text="W0")
        lbl_w0.place(x=2, y=30)

        ent_w0 = tk.Entry(master=self.frm_freq)
        ent_w0.place(x=30, y=30)

        lbl_w1 = tk.Label(master=self.frm_freq, text="W1")
        lbl_w1.place(x=2, y=60)

        ent_w1 = tk.Entry(master=self.frm_freq)
        ent_w1.place(x=30, y=60)

        lbl_w2 = tk.Label(master=self.frm_freq, text="W2")
        lbl_w2.place(x=2, y=90)

        ent_w2 = tk.Entry(master=self.frm_freq)
        ent_w2.place(x=30, y=90)

        lbl_w3 = tk.Label(master=self.frm_freq, text="W3")
        lbl_w3.place(x=2, y=120)

        ent_w3 = tk.Entry(master=self.frm_freq)
        ent_w3.place(x=30, y=120)

        lbl_w4 = tk.Label(master=self.frm_freq, text="W4")
        lbl_w4.place(x=2, y=150)

        ent_w4 = tk.Entry(master=self.frm_freq)
        ent_w4.place(x=30, y=150)

        lbl_w5 = tk.Label(master=self.frm_freq, text="W5")
        lbl_w5.place(x=2, y=180)

        ent_w5 = tk.Entry(master=self.frm_freq)
        ent_w5.place(x=30, y=180)

        lbl_w6 = tk.Label(master=self.frm_freq, text="W6")
        lbl_w6.place(x=2, y=210)

        ent_w6 = tk.Entry(master=self.frm_freq)
        ent_w6.place(x=30, y=210)

        self.output = [ent_w0, ent_w1, ent_w2, ent_w3, ent_w4, ent_w5, ent_w6]

    def update_data(self):
        """
        метод для считывания, вычисления и вывода параметров
        :return:
        """

        # инициализация логики
        logic = Logic(self.input_data["радиус КП"].get(),
                      self.input_data["радиус КП 1 и 2"].get(),
                      self.input_data["радиус кабелей"].get(),
                      self.input_data["радиус РЛС, РЛВ"].get(),
                      self.input_data["радиус СУ"].get(),
                      self.input_data["радиус ЭГ"].get())

        # расчёт координат области опасных взрывов
        logic.danger_area_explose_area()
        ellipse, hit_points, colors, discret_levels = logic.damage_calculation(
            self.input_data["дальность до траверза"].get(),
            self.input_data["боевой маршрут"].get(),
            self.input_data["интервал строя"].get(),
            self.input_data["интервал серии"].get(),
            self.input_data["количество реализаций"].get(),
            self.input_data["количество АСП"].get(),
            self.input_data[
                "прицельное рассеивание"].get(),
            self.input_data["варианты вооружения"].get(),
            self.input_data[
                "количество суббоеприпасов"].get(),
            self.input_data[
                "рассеивание суббоеприпасов"].get(),
            self.input_data[
                "техническое рассеивание"].get())

        new_figures = logic.calculate_figures(ellipse, hit_points, colors)

        # вывод информации
        for index, ent in enumerate(self.output):
            ent.delete(0, tk.END)
            ent.insert(0, f"{discret_levels[index] * 100}%")

        draw = Draw()

        draw.draw_figures(new_figures)
        draw.drawing()

        return "super"

    def open_window(self):
        # открываем виджет
        self.characteristics()
        self.mode_bomb()
        self.variants()
        self.radius()
        self.frequency()
        self.window.mainloop()


widget = Widget()

widget.open_window()
