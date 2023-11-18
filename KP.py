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
    :param point_3:
    :param point_4:
    :return:
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
                 radius_cable,
                 radius_rlsv,
                 radius_sc,
                 radius_eg):
        """
        инициализация параметров
        :param radius_cp: радиусы поражения командных пунктов
        :param radius_cable: радиусы поражения кабелей
        :param radius_rlsv: радиусы поражения РЛС и РЛВ
        :param radius_sc: радиусы поражения самоходных установок
        :param radius_eg: радиусы поражения энергогенераторов
        """

        self.radius_cp = radius_cp
        self.radius_cable = radius_cable
        self.radius_rlsv = radius_rlsv
        self.radius_sc = radius_sc
        self.radius_eg = radius_eg

        # расположение объектов
        self.objects = [Params(270, 280, 25, 25, 8, radius_cp[0]),
                        Params(420, 110, 25, 25, 15, radius_cp[1]),
                        Params(300, 280, 25, 25, 41, radius_cp[1]),
                        Params(170, 50, 25, 25, 35, radius_rlsv),
                        Params(130, 500, 25, 25, 81, radius_rlsv),
                        Params(480, 220, 25, 25, 0, radius_sc),
                        Params(440, 350, 25, 25, 0, radius_sc),
                        Params(550, 440, 25, 25, 130, radius_sc),
                        Params(90, 270, 25, 25, 0, radius_eg),
                        Params(540, 40, 25, 25, 32, radius_eg),
                        Params(490, 530, 25, 25, 13, radius_eg),
                        Params(0, 280, 200, 4, 0, radius_cable),
                        Params(135, 280, 181, 4, -2, radius_cable),
                        Params(200, 168, 231, 4, 70, radius_cable),
                        Params(120, 400, 243, 4, -80, radius_cable),
                        Params(220, 150, 254, 4, -66, radius_cable),
                        Params(210, 400, 235, 4, -120, radius_cable),
                        Params(355, 200, 219, 4, 45, radius_cable),
                        Params(290, 400, 235, 4, -80, radius_cable),
                        Params(480, 90, 135, 4, 26, radius_cable),
                        Params(410, 520, 195, 4, -13, radius_cable),
                        Params(460, 150, 127, 4, -62, radius_cable),
                        Params(460, 300, 131, 4, -110, radius_cable),
                        Params(500, 390, 150, 4, -42, radius_cable),
                        Params(420, 470, 254, 4, 11, radius_cable)]

        # повреждённые объекты
        self.damage_objects = []
        self.func_elem = [True for _ in range(25)]  # список состояний функциональных элементов

    def danger_area_explose_area(self):
        """
        метод для вычисления области опасных взрывов
        :return:
        """
        for obj in self.objects:
            fi_rad = radians(obj.angle)  # перевод угла из градусов в радианы
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

            if len(self.damage_objects) != 25:
                # заполнение списка поражённых объектов
                self.damage_objects.append(((x1, y1), (x2, y2), (x3, y3), (x4, y4)))
            else:
                self.damage_objects.clear()
                self.damage_objects.append(((x1, y1), (x2, y2), (x3, y3), (x4, y4)))

    def solve_fe(self):

        f_0 = self.func_elem[1] and self.func_elem[2] and self.func_elem[6] * self.func_elem[7] and self.func_elem[8] \
              and ((self.func_elem[18] and self.func_elem[22] and self.func_elem[23] and self.func_elem[24] and
                    self.func_elem[25] and (not self.func_elem[19])) or ())

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
        """

        aim_point = list()  # список точек прицеливания
        rbk_list = [[0, 0] for _ in range(num_ammunition)]

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
                    if weapon[1] != "ОФАБ":
                        for ammunition in range(num_ammunition):
                            rbk_list[ammunition][0] = x_zalp + np.random.uniform(-3 * ammunition_disp,
                                                                                 3 * ammunition_disp)
                            rbk_list[ammunition][1] = y_zalp + np.random.uniform(-ammunition_disp, ammunition_disp)

                            flag = True
                            # проход по каждому функциональному элементу ЗРК
                            for num_func_elem in range(len(self.func_elem)):
                                # если боеприпас нанёс урон, то есть попал в ФЭ
                                if destoy(rbk_list[ammunition], self.damage_objects[0], self.damage_objects[1],
                                          self.damage_objects[2], self.damage_objects[3]):
                                    self.func_elem[num_func_elem] = False
                                    flag = False

                            # для отрисовки только первой реализации
                            if num_bomb == 1:
                                pass
                    # если ОФАБ
                    else:
                        x_fab = random.gauss(x_zalp, technical_disp)
                        y_fab = random.gauss(y_zalp, technical_disp)

                        flag = True

                        for num_fe in range(len(self.func_elem)):
                            if destoy((x_fab, y_fab), self.damage_objects[0], self.damage_objects[1],
                                      self.damage_objects[2], self.damage_objects[3]):
                                self.func_elem[num_fe] = False
                                flag = False

                        # для отрисовки первой реализации
                        if num_bomb == 1:
                            pass


class Drawing(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Отрисовка решения")
        self.geometry("1000x1000")


class Widget:
    def __init__(self):
        """
        Инициализация виджета
        """

        self.window = tk.Tk()
        self.window.title("Моделирование бомбометания")

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

        # техническое прицеливание - текст
        lbl_tech = tk.Label(master=self.frm_chts, text="Техническое рассеивание, [м]")
        lbl_tech.place(x=2, y=50)

        # техническое прицеливание - ввод
        ent_aim = tk.Entry(master=self.frm_chts)
        ent_aim.place(x=220, y=50)

        # рассеивание суббоеприпасов - текст
        lbl_disp = tk.Label(master=self.frm_chts, text="Рассеивание суббоеприпасов, [м]")
        lbl_disp.place(x=2, y=80)

        # рассеивание суббоеприпасов - ввод
        ent_disp = tk.Entry(master=self.frm_chts)
        ent_disp.place(x=220, y=80)

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

        # дальность до траверза - текст
        lbl_dist = tk.Label(master=self.frm_chts, text="Дальность до траверза КП, [м]")
        lbl_dist.place(x=2, y=170)

        # дальность до траверза - ввод
        ent_dist = tk.Entry(master=self.frm_chts)
        ent_dist.place(x=220, y=170)

        # интервал строя - текст
        lbl_build = tk.Label(master=self.frm_chts, text="Интервал строя, [м]")
        lbl_build.place(x=2, y=200)

        # выпадающий список для интервала строя
        build = ["100", "200", "300", "400"]
        cbx_build = ttk.Combobox(master=self.frm_chts, values=build)
        cbx_build.place(x=220, y=200)

        # интерал серии - текст
        lbl_series = tk.Label(master=self.frm_chts, text="Интервал серии, [м]")
        lbl_series.place(x=2, y=230)

        # интервал серии - ввод
        ent_series = tk.Entry(master=self.frm_chts)
        ent_series.place(x=220, y=230)

        # высота бомбометания - текст
        lbl_height = tk.Label(master=self.frm_chts, text="Высота бомбометания, [м]")
        lbl_height.place(x=2, y=260)

        # выпадающий список для высоты бомбометания
        height = ["500", "1500", "3000"]
        cbx_height = ttk.Combobox(master=self.frm_chts, values=height)
        cbx_height.place(x=220, y=260)

        # количество АСП - текст
        lbl_count = tk.Label(master=self.frm_chts, text="Количество АСП, [шт]")
        lbl_count.place(x=2, y=290)

        # количество АСП - ввод
        ent_count = tk.Entry(master=self.frm_chts)
        ent_count.place(x=220, y=290)

        # кодичество суббоеприпасов СП - текст
        lbl_sp = tk.Label(master=self.frm_chts, text="Количество суббоеприпасов СП, [шт]")
        lbl_sp.place(x=2, y=320)

        # количество суббоеприпасов СП - ввод
        ent_sp = tk.Entry(master=self.frm_chts)
        ent_sp.place(x=220, y=320)

    def variants(self):
        """
        метод для отображения вариантов вооружения
        :return:
        """

        # заголовок вариантов вооружения
        lbl_opt = tk.Label(master=self.frm_opt_rad, text="Варианты вооружения")
        lbl_opt.place(x=90, y=0)

        # Создание переменной для отслеживания выбранного варианта
        selected_option = tk.StringVar(value="option1")  # Установка начального значения на "option1"

        # Создание радиокнопок для каждого варианта
        option1 = tk.Radiobutton(master=self.frm_opt_rad, text="ОФАБ-100-120", variable=selected_option,
                                 value="option1")
        option2 = tk.Radiobutton(master=self.frm_opt_rad, text="ОФАБ-250", variable=selected_option, value="option2")
        option3 = tk.Radiobutton(master=self.frm_opt_rad, text="РБС-Ф025-33", variable=selected_option, value="option3")
        option4 = tk.Radiobutton(master=self.frm_opt_rad, text="РБК-250-АО.25", variable=selected_option,
                                 value="option4")
        option5 = tk.Radiobutton(master=self.frm_opt_rad, text="РБК-500-АО.25", variable=selected_option,
                                 value="option5")

        option1.place(x=100, y=30)
        option2.place(x=100, y=50)
        option3.place(x=100, y=70)
        option4.place(x=100, y=90)
        option5.place(x=100, y=110)

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

        # радиусы - текст
        lbl_rad_kp12 = tk.Label(master=self.frm_opt_rad, text="Радиус КП1, КП2, [м]")
        lbl_rad_kp12.place(x=2, y=200)

        # радиусы - ввод
        ent_rad_kp12 = tk.Entry(master=self.frm_opt_rad)
        ent_rad_kp12.place(x=170, y=200)

        # радиусы СУ - текст
        lbl_rad_su = tk.Label(master=self.frm_opt_rad, text="Радиус СУ1, СУ2, СУ3, [м]")
        lbl_rad_su.place(x=2, y=230)

        # радиусы СУ - ввод
        ent_rad_su = tk.Entry(master=self.frm_opt_rad)
        ent_rad_su.place(x=170, y=230)

        # радиусы РЛ - текст
        lbl_rls_rlv = tk.Label(master=self.frm_opt_rad, text="Радиус РЛС, РЛВ, [м]")
        lbl_rls_rlv.place(x=2, y=260)

        # радиусы РЛ - ввод
        ent_rls_rlv = tk.Entry(master=self.frm_opt_rad)
        ent_rls_rlv.place(x=170, y=260)

        # радиусы ЭГ - текст
        lbl_eg = tk.Label(master=self.frm_opt_rad, text="Радиус ЭГ1, ЭГ2, [м]")
        lbl_eg.place(x=2, y=290)

        # радиусы ЭГ - ввод
        ent_eg = tk.Entry(master=self.frm_opt_rad)
        ent_eg.place(x=170, y=290)

        # радиусы кабелей - текст
        lbl_cabel = tk.Label(master=self.frm_opt_rad, text="Радиус кабелей, [м]")
        lbl_cabel.place(x=2, y=320)

        # радиусы кабелей - ввод
        ent_cabel = tk.Entry(master=self.frm_opt_rad)
        ent_cabel.place(x=170, y=320)

        # Количество реализаций - текст
        lbl_real = tk.Label(master=self.frm_opt_rad, text="Количество реализаций")
        lbl_real.place(x=2, y=350)

        # количество реализаций - ввод
        ent_real = tk.Entry(master=self.frm_opt_rad)
        ent_real.place(x=170, y=350)

    def frequency(self):
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

    def modeling(self):
        btn_model = tk.Button(master=self.frm_freq, text="Моделировать")
        btn_model.place(x=40, y=270)

    def open_window(self):
        # открываем виджет
        self.characteristics()
        self.mode_bomb()
        self.frequency()
        self.variants()
        self.modeling()
        self.radius()
        self.window.mainloop()


def widget():
    """
    функция, для вывод окна
    :return:
    """

    root = tk.Tk()

    # Создание списка для хранения значений из полей Entry
    entry_values = []

    # Функция для обработки нажатия кнопки
    def get_entry_values():
        for entry in entry_values:
            value = entry.get()
            print("Значение:", value)

    # Создание полей Entry
    entry1 = tk.Entry(root)
    entry1.pack()
    entry_values.append(entry1)

    entry2 = tk.Entry(root)
    entry2.pack()
    entry_values.append(entry2)

    # Создание кнопки для получения значений
    button = tk.Button(root, text="Получить значения", command=get_entry_values)
    button.pack()

    root.mainloop()

# window = Widget()
# window.open_window()
