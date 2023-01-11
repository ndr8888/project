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


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0
        self.dx_total = 0
        self.dy_total = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)
        self.dx_total += self.dx
        self.dy_total += self.dy