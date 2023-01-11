from Constants import *


class Timer:  # класс для засекания времени
    def __init__(self, time_max):  # подаем время, на которое засекаем таймер
        self.time_max = time_max
        self.time = 0

    def start(self):  # начинаем отсчёт таймера. Обязательно, чтобы таймер начал работать
        self.time = self.time_max

    def tick(self, time=1):  # 60 раз в секунду убывает на 1
        self.time -= time  # вычитаем единичку
        if self.time < 0:  # считаем до 0
            self.time = 0

    def stop(self):
        self.time = 0


class Empty:  # класс травы для матрицы
    def __init__(self):
        pass

    def type(self):
        return 'empty'


class Blocked:  # класс стены для матрицы
    def __init__(self):
        pass

    def type(self):
        return 'blocked'