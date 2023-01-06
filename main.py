import pygame
import os
import sys
import random
import math

clock = pygame.time.Clock()
pygame.init()
size = WIDTH, HEIGHT = 750, 750  # размеры окна
screen = pygame.display.set_mode(size)
tile_width = tile_height = 50  # размеры кнопокa
inventory_slot_width = 60  # размеры слотов инвентаря


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


def load_image(name, colorkey=None):  # функция для загрузки изображений для спрайтов
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


# словарь с изображениями
images = {
    'wall': pygame.transform.scale(load_image('box.png'), (tile_width, tile_height)),  # стена
    'grass': pygame.transform.scale(load_image('grass.png'), (tile_width, tile_height)),  # зеленый фон, трава
    'bullet': load_image('bullet.png'),  # пуля
    'close_attack': load_image('attack2.png'),  # ближняя атака монстра
    'close_attack1': load_image('attack3.png'),  # ближняя атака главного героя
    'close_attack2': load_image('attack4.png'),  # ближняя атака главного героя
    'empty_image': load_image('empty_image.png'),  # черная пустота
    'monster': pygame.transform.scale(load_image('enemy.png'), (tile_width, tile_height)),  # враг, воюет в ближнем бою
    'monster1': pygame.transform.scale(load_image('enemy1.png'), (tile_width, tile_height)),  # враг дальнего боя
    'monster2': pygame.transform.scale(load_image('enemy2.png'), (tile_width, tile_height)),
    # враг-страж. При его убийстве рушатся некоторые стенки
    'player': pygame.transform.scale(load_image('mar.png'), (tile_width, tile_height)),  # игрок
    'game_over': pygame.transform.scale(load_image('gameover.png'), (WIDTH, HEIGHT)),  # конец игры из урока
    'inventory_slot': pygame.transform.scale(load_image('inventory_slot.png'),  # слот для оружий
                                             (inventory_slot_width, inventory_slot_width)),
    'inventory_slot2': pygame.transform.scale(load_image('inventory_slot2.png'),  # слот для зелий
                                              (inventory_slot_width, inventory_slot_width)),
    'sword': load_image('sword.png'),  # меч, ближний бой
    'gun': load_image('gun.png'),  # пистолет, дальний бой
    'frame': pygame.transform.scale(load_image('frame.png'), (inventory_slot_width, inventory_slot_width)),
    # обводка слота инвентаря
    'health_potion': pygame.transform.scale(load_image('health_potion1.png'),  # зелье исцеления
                                            (inventory_slot_width, inventory_slot_width)),
    'rage_potion': pygame.transform.scale(load_image('rage_potion1.png'), (inventory_slot_width, inventory_slot_width)),
    # зелье урона. х2
    'teleport': pygame.transform.scale(load_image('teleport.png'), (tile_width, tile_height)),  # активный телепорт
    'teleport1': pygame.transform.scale(load_image('teleport1.png'), (tile_width, tile_height)),  # неактивный телепорт
    'teleport_win': pygame.transform.scale(load_image('teleport_win.png'), (tile_width, tile_height)),
    # телепорт при полном прохождении игры
    'key': pygame.transform.scale(load_image('key.png'), (tile_width, tile_height)),
    # ключик, в моем коде ключ не работает, картинку нужно заменить
    'Jevel': pygame.transform.scale(load_image('Jewel.png'), (tile_width, tile_height)),  # сокровище
    'blast': load_image('blast.png'),  # магический выстрел
    'staff': load_image('staff.png'),  # посох
    'bomb_launcher': load_image('grenade_launcher.png'),
    'spear': load_image('spear.png'),
    'cross': load_image('cross.png'),  # невозможность применения. красный крестик
    'boom': load_image('boom.png'),  # взрыв бомбы
    'bomb': load_image('bomb2.png'),  # бомба, оружие
    'pause': pygame.transform.scale(load_image('pause.png'), (inventory_slot_width, inventory_slot_width)),  # пауза
    'snare': load_image('snare.png'),  # ловушка,
    'heal_zone': pygame.transform.scale(load_image('cross_heal.png'), (tile_width, tile_height))  # ловушка,
}
FPS = 60  # кол-во тиков в секунду


def terminate():  # выход из игры
    pygame.quit()
    sys.exit()


def start_screen():  # начальное окно
    direction = [0, 0]
    # текст
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    # цикл работы
    while True:
        screen.fill((0, 0, 0))
        text_coords = [10, 50]  # положение строки
        font = pygame.font.Font(None, 25)  # размер шрифта
        for line in intro_text:  # выводим построчно
            string_rendered = font.render(line, 1, pygame.Color('green'))  # цвет шрифта
            intro_rect = string_rendered.get_rect()  # положение строки. Нужно для возможности нажимания на текст
            text_coords[1] += 10  # опускаемся ниже для следуюшей строчки
            intro_rect.top = text_coords[1]  # верхняя граница строчки
            intro_rect.x = text_coords[0]  # боковая граница строчки
            text_coords[1] += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        # описание и размеры квадрата, где будет работать "Начать игру"
        font = pygame.font.Font(None, 50)
        text = font.render("Начать игру", True, (100, 255, 100))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 3)
        # описание и размеры квадрата, где будет работать "Выйти из игры"
        font = pygame.font.Font(None, 50)
        text = font.render("Выйти из игры", True, (100, 255, 100))
        text_x2 = WIDTH // 2 - text.get_width() // 2
        text_y2 = HEIGHT // 2 - text.get_height() // 2 + 100
        text_w2 = text.get_width()
        text_h2 = text.get_height()
        screen.blit(text, (text_x2, text_y2))
        pygame.draw.rect(screen, (0, 255, 0), (text_x2 - 10, text_y2 - 10,
                                               text_w2 + 20, text_h2 + 20), 3)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # назначаем движение
                if event.key == pygame.K_w:  # вверх
                    direction[1] -= 1
                if event.key == pygame.K_d:  # вправо
                    direction[0] += 1
                if event.key == pygame.K_s:  # вниз
                    direction[1] += 1
                if event.key == pygame.K_a:  # влево
                    direction[0] -= 1
            if event.type == pygame.KEYUP:  # убираем движение по направлениям, если клавишу отпустили
                if event.key == pygame.K_w:
                    direction[1] += 1
                if event.key == pygame.K_d:
                    direction[0] -= 1
                if event.key == pygame.K_s:
                    direction[1] -= 1
                if event.key == pygame.K_a:
                    direction[0] += 1
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and text_x - 10 < event.pos[
                0] < text_x + 10 + text_w and text_y - 10 < event.pos[1] < text_y + 10 + text_h:
                return direction, 0
            elif event.type == pygame.MOUSEBUTTONDOWN and text_x2 - 10 < event.pos[
                0] < text_x2 + 10 + text_w2 and text_y2 - 10 < event.pos[1] < text_y2 + 10 + text_h2:
                return direction, 2
        pygame.display.flip()
        clock.tick(FPS)


# def end_screen():
#     direction = [0, 0]
#     intro_text = ["ИГРА ОКОНЧЕНА",
#                   f"Время: {time_counter // 3600} мин {time_counter % 3600 // 60} сек"]
#
#     # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
#     # screen.blit(fon, (0, 0))
#
#     while True:
#         screen.fill((0, 0, 0))
#         text_coords = [10, 100]
#         font = pygame.font.Font(None, 30)
#         for line in intro_text:
#             string_rendered = font.render(line, 1, pygame.Color('red'))
#             intro_rect = string_rendered.get_rect()
#             text_coords[1] += 10
#             intro_rect.top = text_coords[1]
#             # intro_rect.x = text_coords[0] - intro_rect.w // 2
#             intro_rect.x = text_coords[0]
#             text_coords[1] += intro_rect.height
#             screen.blit(string_rendered, intro_rect)
#         font = pygame.font.Font(None, 50)
#         text = font.render("Начать заново", True, (255, 100, 100))
#         text_x = WIDTH // 2 - text.get_width() // 2
#         text_y = HEIGHT // 2 - text.get_height() // 2
#         text_w = text.get_width()
#         text_h = text.get_height()
#         screen.blit(text, (text_x, text_y))
#         pygame.draw.rect(screen, (255, 0, 0), (text_x - 10, text_y - 10,
#                                                text_w + 20, text_h + 20), 3)
#
#         font = pygame.font.Font(None, 50)
#         text = font.render("Выйти из игры", True, (255, 100, 100))
#         text_x2 = WIDTH // 2 - text.get_width() // 2
#         text_y2 = HEIGHT // 2 - text.get_height() // 2 + 100
#         text_w2 = text.get_width()
#         text_h2 = text.get_height()
#         screen.blit(text, (text_x2, text_y2))
#         pygame.draw.rect(screen, (255, 0, 0), (text_x2 - 10, text_y2 - 10,
#                                                text_w2 + 20, text_h2 + 20), 3)
#         for event in pygame.event.get():
#             if event.type == pygame.KEYDOWN:  # назначаем движение, без этого появляются ошибки, если зажимать кнопки движения во время экрана поражения
#                 if event.key == pygame.K_w:  # вверх
#                     direction[1] -= 1
#                 if event.key == pygame.K_d:  # вправо
#                     direction[0] += 1
#                 if event.key == pygame.K_s:  # вниз
#                     direction[1] += 1
#                 if event.key == pygame.K_a:  # влево
#                     direction[0] -= 1
#             if event.type == pygame.KEYUP:  # убираем движение по направлениям, если клавишу отпустили
#                 if event.key == pygame.K_w:
#                     direction[1] += 1
#                 if event.key == pygame.K_d:
#                     direction[0] -= 1
#                 if event.key == pygame.K_s:
#                     direction[1] -= 1
#                 if event.key == pygame.K_a:
#                     direction[0] += 1
#             if event.type == pygame.QUIT:
#                 terminate()
#             elif event.type == pygame.MOUSEBUTTONDOWN and text_x - 10 < event.pos[
#                 0] < text_x + 10 + text_w and text_y - 10 < event.pos[1] < text_y + 10 + text_h:
#                 return direction, 0
#             elif event.type == pygame.MOUSEBUTTONDOWN and text_x2 - 10 < event.pos[
#                 0] < text_x2 + 10 + text_w2 and text_y2 - 10 < event.pos[1] < text_y2 + 10 + text_h2:
#                 return direction, 2
#         pygame.display.flip()
#         clock.tick(FPS)


def win_screen():  # окно победы, принцип тот же, что и в функции выше
    direction = [0, 0]
    intro_text = ["ИГРА ПРОЙДЕНА",
                  f"Время: {time_counter // 3600} мин {time_counter % 3600 // 60} сек"]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))

    while True:
        screen.fill((0, 0, 0))
        text_coords = [10, 100]
        font = pygame.font.Font(None, 30)
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('yellow'))
            intro_rect = string_rendered.get_rect()
            text_coords[1] += 10
            intro_rect.top = text_coords[1]
            # intro_rect.x = text_coords[0] - intro_rect.w // 2
            intro_rect.x = text_coords[0]
            text_coords[1] += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        font = pygame.font.Font(None, 50)
        text = font.render("Пройти заново", True, (255, 255, 100))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (255, 255, 0), (text_x - 10, text_y - 10,
                                                 text_w + 20, text_h + 20), 3)

        font = pygame.font.Font(None, 50)
        text = font.render("Выйти из игры", True, (255, 255, 100))
        text_x2 = WIDTH // 2 - text.get_width() // 2
        text_y2 = HEIGHT // 2 - text.get_height() // 2 + 100
        text_w2 = text.get_width()
        text_h2 = text.get_height()
        screen.blit(text, (text_x2, text_y2))
        pygame.draw.rect(screen, (255, 255, 0), (text_x2 - 10, text_y2 - 10,
                                                 text_w2 + 20, text_h2 + 20), 3)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # назначаем движение, без этого появляются ошибки, если зажимать кнопки движения во время экрана поражения
                if event.key == pygame.K_w:  # вверх
                    direction[1] -= 1
                if event.key == pygame.K_d:  # вправо
                    direction[0] += 1
                if event.key == pygame.K_s:  # вниз
                    direction[1] += 1
                if event.key == pygame.K_a:  # влево
                    direction[0] -= 1
            if event.type == pygame.KEYUP:  # убираем движение по направлениям, если клавишу отпустили
                if event.key == pygame.K_w:
                    direction[1] += 1
                if event.key == pygame.K_d:
                    direction[0] -= 1
                if event.key == pygame.K_s:
                    direction[1] -= 1
                if event.key == pygame.K_a:
                    direction[0] += 1
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and text_x - 10 < event.pos[
                0] < text_x + 10 + text_w and text_y - 10 < event.pos[1] < text_y + 10 + text_h:
                return direction, 0
            elif event.type == pygame.MOUSEBUTTONDOWN and text_x2 - 10 < event.pos[
                0] < text_x2 + 10 + text_w2 and text_y2 - 10 < event.pos[1] < text_y2 + 10 + text_h2:
                return direction, 2
        pygame.display.flip()
        clock.tick(FPS)


def pause_screen():  # окно паузы, принцип тот же, что и в функции выше
    direction = [0, 0]
    intro_text = ["ПАУЗА"]

    # fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    # screen.blit(fon, (0, 0))
    text_coord = 50

    while True:
        screen.fill((0, 0, 0))
        text_coords = [WIDTH // 2, HEIGHT // 2 - 150]
        font = pygame.font.Font(None, 50)
        for line in intro_text:
            string_rendered = font.render(line, 1, pygame.Color('green'))
            intro_rect = string_rendered.get_rect()
            text_coords[1] += 10
            intro_rect.top = text_coords[1]
            intro_rect.x = text_coords[0] - intro_rect.w // 2
            text_coords[1] += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        font = pygame.font.Font(None, 50)
        text = font.render("Продолжить игру", True, (100, 255, 100))
        text_x = WIDTH // 2 - text.get_width() // 2
        text_y = HEIGHT // 2 - text.get_height() // 2
        text_w = text.get_width()
        text_h = text.get_height()
        screen.blit(text, (text_x, text_y))
        pygame.draw.rect(screen, (0, 255, 0), (text_x - 10, text_y - 10,
                                               text_w + 20, text_h + 20), 3)

        text = font.render("Начать заново", True, (100, 255, 100))
        text_x1 = WIDTH // 2 - text.get_width() // 2
        text_y1 = HEIGHT // 2 - text.get_height() // 2 + 100
        text_w1 = text.get_width()
        text_h1 = text.get_height()
        screen.blit(text, (text_x1, text_y1))
        pygame.draw.rect(screen, (0, 255, 0), (text_x1 - 10, text_y1 - 10,
                                               text_w1 + 20, text_h1 + 20), 3)

        font = pygame.font.Font(None, 50)
        text = font.render("Выйти из игры", True, (100, 255, 100))
        text_x2 = WIDTH // 2 - text.get_width() // 2
        text_y2 = HEIGHT // 2 - text.get_height() // 2 + 200
        text_w2 = text.get_width()
        text_h2 = text.get_height()
        screen.blit(text, (text_x2, text_y2))
        pygame.draw.rect(screen, (0, 255, 0), (text_x2 - 10, text_y2 - 10,
                                               text_w2 + 20, text_h2 + 20), 3)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:  # назначаем движение
                if event.key == pygame.K_w:  # вверх
                    direction[1] -= 1
                if event.key == pygame.K_d:  # вправо
                    direction[0] += 1
                if event.key == pygame.K_s:  # вниз
                    direction[1] += 1
                if event.key == pygame.K_a:  # влево
                    direction[0] -= 1
            if event.type == pygame.KEYUP:  # убираем движение по направлениям, если клавишу отпустили
                if event.key == pygame.K_w:
                    direction[1] += 1
                if event.key == pygame.K_d:
                    direction[0] -= 1
                if event.key == pygame.K_s:
                    direction[1] -= 1
                if event.key == pygame.K_a:
                    direction[0] += 1
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.MOUSEBUTTONDOWN and text_x - 10 < event.pos[
                0] < text_x + 10 + text_w and text_y - 10 < event.pos[1] < text_y + 10 + text_h:
                return direction, 0
            elif event.type == pygame.MOUSEBUTTONDOWN and text_x1 - 10 < event.pos[
                0] < text_x1 + 10 + text_w1 and text_y1 - 10 < event.pos[1] < text_y1 + 10 + text_h1:
                return direction, 1
            elif event.type == pygame.MOUSEBUTTONDOWN and text_x2 - 10 < event.pos[
                0] < text_x2 + 10 + text_w2 and text_y2 - 10 < event.pos[1] < text_y2 + 10 + text_h2:
                return direction, 2
        pygame.display.flip()
        clock.tick(FPS)


def load_level(filename):  # чтение уровня
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip('\n') for line in mapFile]
    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('№')
    return list(map(lambda x: x.ljust(max_width, '-'), level_map))


class BackgroundTile(pygame.sprite.Sprite):  # класс фоновой картинки, пришлось разделить его и класс стены
    def __init__(self, pos_x, pos_y):  # положение
        super().__init__(tiles_group, all_sprites)  # добавляем в группы спрайтов
        self.image = images['grass']  # изображение фоновой картинки
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)  # передвигаем фоновую картинку на её место
        self.mask = pygame.mask.from_surface(self.image)


class Key(BackgroundTile):  # ключ для перехода на следующий уровень
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)  # положение
        self.image = images['key']  # изображение ключа
        global keys_not_collected
        keys_not_collected += 1
        self.pos_x, self.pos_y = pos_x, pos_y

    def update(self):
        # если взяли ключ, то портал срабатывает, а ключ удаляется
        if player.pos_x == self.pos_x and player.pos_y == self.pos_y:
            global keys_not_collected
            keys_not_collected -= 1
            self.kill()

    def type(self):  # можно пройти сквозь и подобрать
        return 'empty'


class Snare(BackgroundTile):  # ловушка, убивает персонажа
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)  # положение
        self.image = images['snare']  # изображение ловушки
        self.pos_x, self.pos_y = pos_x, pos_y
        snares_group.add(self)  # группа ловушек

    # def make_move(self):
    #     if (self.x_move == 0 ) and board[self.pos_x + self.x_move][self.pos_y + self.y_move].type() not in ['wall', 'blocked']:
    #         board[self.pos_x + self.x_move][self.pos_y + self.y_move] = Blocked()
    #

    def update(self):  # если попали в ловушку, то персонаж умирает
        if player.pos_x == self.pos_x and player.pos_y == self.pos_y:
            player.is_killed = True

    def type(self):
        return 'empty'


class Teleport(BackgroundTile):  # класс телепорта
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)  # положение
        self.image = images['teleport']
        self.pos_x, self.pos_y = pos_x, pos_y

    def update(self):
        if player.pos_x == self.pos_x and player.pos_y == self.pos_y:
            global level_running
            level_running = False

    def type(self):
        return 'empty'

class HealZone(BackgroundTile):  # класс телепорта
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)  # положение
        self.image = images['heal_zone']
        self.pos_x, self.pos_y = pos_x, pos_y

    def update(self):
        if player.pos_x == self.pos_x and player.pos_y == self.pos_y:
            player.hp = player.hp_max

    def type(self):
        return 'empty'


class WinTeleport(BackgroundTile):  # отдельный финишный телепорт, выполняет другие функции, поэтому отдельно
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        self.image = images['teleport_win']
        self.pos_x, self.pos_y = pos_x, pos_y

    def update(self):  # если активирован и персонаж в него зашел, то выводим окно победы и завершаем игру
        if player.pos_x == self.pos_x and player.pos_y == self.pos_y:
            global level_running, game_running, is_won
            level_running = False
            game_running = False
            is_won = True

    def type(self):
        return 'empty'


class Wall(pygame.sprite.Sprite):  # класс стены
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, wall_group)
        self.image = images['wall']
        self.rect = self.image.get_rect().move(  # положение на экране
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def type(self):  # возвращает строку типа спрайта, нужно для использования спрайтов в матрице
        return 'wall'


class WallTriggerable(Wall):  # разрушаемая стена. Разрушается при смерти monster2
    def __init__(self, pos_x, pos_y, key_trigger, monster_trigger):
        super().__init__(pos_x, pos_y)
        self.image = images['wall']
        self.pos_x, self.pos_y = pos_x, pos_y
        self.status = True  # для разрушения стен
        self.key_trigger, self.monster_trigger = key_trigger, monster_trigger

    def update(self):
        if (len(guard_monster_group) == 0 or not self.monster_trigger) and (keys_not_collected == 0 or not self.key_trigger):  # если все monster2 мертвы, то стены рушатся
            self.status = False
            self.image = images['grass']

    def type(self):
        if self.status:
            return 'wall'
        else:
            return 'empty'


class Jewel(BackgroundTile):  # класс сокровищ
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        img_name = ['gun', 'staff', 'spear', 'bomb_launcher'][map_num]
        self.image = pygame.transform.scale(images[img_name], (tile_width, tile_height))  # изображение сокровища
        self.pos_x, self.pos_y = pos_x, pos_y  # координаты
        self.rand_potion = ''

    def update(self):
        if player.pos_x == self.pos_x and player.pos_y == self.pos_y:  # проверяю координаты перса и сокровища
            if map_num == 0:
                weapon_lst.append(BulletWeapon('gun', 'bullet', -50, -50,
                                               player,
                                               player_group,
                                               10, FPS // 2,
                                               speed=13,
                                               rang=400, name='пистолет'))
            if map_num == 1:
                weapon_lst.append(MagicWeapon('staff', 'blast', -50, -50, player, player_group, 10, FPS // 1.5,
                                              area_width=1.25, name='меч', rang=300))
            if map_num == 2:
                weapon_lst.append(CloseWeapon('spear', 'close_attack', -50, -50, player, player_group, 13, FPS // 2,
                                              rang=4.8, name='копьё'))
            if map_num == 3:
                weapon_lst.append(
                    BombWeapon('bomb_launcher', 'bomb', -50, -50, player, player_group, 15, FPS, speed=12, rang=300))
            # weapon_lst.append(MagicWeapon('staff', 'blast', -50, -50, player, player_group, 1, FPS,
            #                               area_width=1, name='меч'))
            # добавляем зельку в инвентарь
            # inventory.hp_potions += 1
            # сокровище собрано, убираем его
            self.kill()

    def type(self):
        return 'empty'


class HealPotion(BackgroundTile):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        potion_group.add(self)
        self.image = pygame.transform.scale(images['health_potion'], (tile_width, tile_height))  # изображение сокровища
        self.pos_x, self.pos_y = pos_x, pos_y  # координаты

    def update(self):
        if player.pos_x == self.pos_x and player.pos_y == self.pos_y:  # проверяю координаты перса и сокровища
            global hp_potions, rage_potions
            hp_potions += 1
            self.kill()

    def type(self):
        return 'empty'


class RagePotion(BackgroundTile):
    def __init__(self, pos_x, pos_y):
        super().__init__(pos_x, pos_y)
        potion_group.add(self)
        self.image = pygame.transform.scale(images['rage_potion'], (tile_width, tile_height))  # изображение сокровища
        self.pos_x, self.pos_y = pos_x, pos_y  # координаты

    def update(self):
        if player.pos_x == self.pos_x and player.pos_y == self.pos_y:  # проверяю координаты перса и сокровища
            global hp_potions, rage_potions
            rage_potions += 1
            self.kill()

    def type(self):
        return 'empty'


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


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.speed = 8
        self.timer_x = Timer(self.speed)  # для анимации передвижения
        self.timer_y = Timer(self.speed)  # для анимации передвижения
        super().__init__(player_group, all_sprites, entity_group)
        self.hp_max = 100
        self.hp = self.hp_max
        self.diagonal = False  # переменная, нужная для диагонального хода игроком
        self.pos_x, self.pos_y = pos_x, pos_y  # координаты игрока в клетках
        self.image = images['player']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)  # положение игрока на поле
        self.mask = pygame.mask.from_surface(self.image)
        self.x_move, self.y_move = 0, 0
        self.x, self.y = self.rect.topleft
        self.is_killed = False  # живой

    def set_at_position(self, pos_x, pos_y):  # передвижение
        self.timer_x = Timer(self.speed)
        self.timer_y = Timer(self.speed)
        self.diagonal = False  # переменная, нужная для диагонального хода игроком
        self.x_move, self.y_move = 0, 0
        self.pos_x, self.pos_y = pos_x, pos_y
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y
        self.x, self.y = self.rect.topleft  # левый верхний угол

    def type(self):
        return 'player'

    def make_move(self, x_move, y_move):
        # ход по диагонали
        if self.diagonal:
            # если есть ход по x и анимация прошлого хода уже закончена и поле, в которое мы идем, не является стеной,
            # препятствием или монстром, то выполняем ход
            if self.x_move == 0 and x_move != 0 and self.timer_y.time == 0 and board[self.pos_x + x_move][
                self.pos_y].type() not in ['wall', 'monster', 'blocked']:
                board[self.pos_x + x_move][self.pos_y] = Blocked()
                self.x_move = x_move
                self.timer_x.start()
                self.diagonal = not self.diagonal
            # тоже самое с y
            if self.y_move == 0 and y_move != 0 and self.timer_x.time == 0 and board[self.pos_x][
                self.pos_y + y_move].type() not in ['wall', 'monster', 'blocked']:
                board[self.pos_x][self.pos_y + y_move] = Blocked()
                self.y_move = y_move
                self.timer_y.start()
                self.diagonal = not self.diagonal
        else:
            # принципе описан в верхнем if'е
            if self.y_move == 0 and y_move != 0 and self.timer_x.time == 0 and board[self.pos_x][
                self.pos_y + y_move].type() not in ['wall', 'monster', 'blocked']:
                board[self.pos_x][self.pos_y + y_move] = Blocked()
                self.y_move = y_move
                self.timer_y.start()
                self.diagonal = not self.diagonal
            if self.x_move == 0 and x_move != 0 and self.timer_y.time == 0 and board[self.pos_x + x_move][
                self.pos_y].type() not in ['wall', 'monster', 'blocked']:
                board[self.pos_x + x_move][self.pos_y] = Blocked()
                self.x_move = x_move
                self.timer_x.start()
                self.diagonal = not self.diagonal

    def update(self):
        if self.x_move != 0:
            self.timer_x.tick()
            # плавная анимация движения
            self.x += self.x_move * (tile_width / self.timer_x.time_max)
            self.rect.x = self.x + camera.dx_total
            # прежнее местоположение игрока делаем травой, позицию игрока переносим
            if self.timer_x.time == 0:
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_x += self.x_move
                board[self.pos_x][self.pos_y] = player
                self.x_move = 0
        if self.y_move != 0:
            self.timer_y.tick()
            # плавная анимация движения
            self.y += self.y_move * (tile_width / self.timer_y.time_max)
            self.rect.y = self.y + camera.dy_total
            # прежнее место игрока делаем травой, позицию игрока переносим
            if self.timer_y.time == 0:
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_y += self.y_move
                board[self.pos_x][self.pos_y] = player
                self.y_move = 0

    def damage(self, n):
        if not cheats:
            self.hp = round((self.hp - n))
            if self.hp <= 0:
                self.is_killed = True


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, weapon, hp_max, rang_min, rang_max, image_name, close_mode, speed, dop_groups=[],
                 clever_shoot=False, is_mage=False):
        # self.weapon = CloseWeapon('empty_image', 'close_attack', -50, -50, self, monster_group, 1, FPS // 2,
        #                           rang=2.25)  # изменяемый
        weapon.owner = self
        weapon.fraction = monster_group  # чтобы не бил своих и не получал урона от ловушек
        self.weapon = weapon
        self.hp_max = hp_max
        self.hp = self.hp_max
        self.rang_min = rang_min  # радиус, в котором монстр нападёт на тебя
        self.rang_max = rang_max
        self.image = images[image_name]
        self.close_mode = close_mode
        speed = speed
        self.timer_x = Timer(speed)
        self.timer_y = Timer(speed)

        self.x_move, self.y_move = 0, 0
        self.pos_x, self.pos_y = pos_x, pos_y
        super().__init__(monster_group, all_sprites, entity_group, *dop_groups)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.next_cell = 0, 0
        self.x, self.y = self.rect.topleft
        self.state = False
        self.state_new = False
        self.player_coords_old = player.pos_x, player.pos_y  # место, где был персонаж до анимации его движения
        self.coords_old = self.pos_x, self.pos_y
        self.clever_shoot = clever_shoot  # донаводка
        self.path = None
        self.is_mage = is_mage

    def type(self):
        return 'monster'

    def update(self):
        if self.path is None:
            self.path = board.get_path(self.pos_x, self.pos_y, player.pos_x, player.pos_y)
        if self.timer_x.time == 0 and self.timer_y.time == 0 and abs(
                self.pos_x - player.pos_x) <= self.rang_max and abs(
            self.pos_y - player.pos_y) <= self.rang_max:
            self.path = board.get_path(self.pos_x, self.pos_y, player.pos_x, player.pos_y)
            if not self.path:
                return None
            next_cell = self.path[1]
            cond = board[self.pos_x - (next_cell[0] - self.pos_x)][
                       self.pos_y - (next_cell[1] - self.pos_y)].type() == 'empty' and not (abs(
                self.pos_x - player.pos_x) == self.rang_min - 1 or abs(
                self.pos_y - player.pos_y) == self.rang_min - 1)
            if (self.player_coords_old != (player.pos_x, player.pos_y) or self.coords_old != (self.pos_x, self.pos_y)) and not (self.rang_min <= abs(
                    self.pos_x - player.pos_x) <= self.rang_max and self.rang_min <= abs(
                self.pos_y - player.pos_y) <= self.rang_max):
                self.state_new = is_linear_path(*self.rect.center, *player.rect.center, owner=self, target=player,
                                                fraction=monster_group,
                                                field=self.weapon.bullet_size[0] if type(self.weapon) in (
                                                BulletWeapon, BombWeapon) else 3, go_through_entities=True)
                self.coords_old = self.pos_x, self.pos_y
            elif not (not self.state and self.state_new and cond):
                self.state_new = self.state
            if self.is_mage:
                self.state = self.state_new = True
            if abs(
                    self.pos_x - player.pos_x) <= self.rang_max and abs(
                self.pos_y - player.pos_y) <= self.rang_max and len(self.path) < self.rang_max * 1.5:
                if ((self.rang_min <= abs(self.pos_x - player.pos_x) or self.rang_min <= abs(
                        self.pos_y - player.pos_y)) or (not self.state_new)) and board[next_cell[0]][
                    next_cell[1]].type() == 'empty':
                    self.next_cell = next_cell
                    x_move, y_move = self.next_cell[0] - self.pos_x, self.next_cell[1] - self.pos_y
                elif cond and self.state:
                    self.next_cell = [self.pos_x - (next_cell[0] - self.pos_x),
                                      self.pos_y - (next_cell[1] - self.pos_y)]
                    x_move, y_move = -(next_cell[0] - self.pos_x), -(next_cell[1] - self.pos_y)
                # elif (abs(self.pos_x - player.pos_x) == self.rang_min - 1 or abs(self.pos_y - player.pos_y) == self.rang_min - 1) and board[self.pos_x + (next_cell[1] - self.pos_y)][self.pos_y + (next_cell[0] - self.pos_x)].type() == 'empty':
                #     x_move, y_move = next_cell[1] - self.pos_y, next_cell[0] - self.pos_x
                #     self.next_cell = [self.pos_x + (next_cell[1] - self.pos_y), self.pos_y + (next_cell[0] - self.pos_x)]
                #     print(x_move, y_move)
                else:
                    x_move, y_move = 0, 0
                if self.x_move == 0 and x_move != 0:
                    self.x_move = x_move
                    self.timer_x.start()
                    board[self.pos_x + x_move][self.pos_y] = Blocked()
                if self.y_move == 0 and y_move != 0:
                    self.y_move = y_move
                    self.timer_y.start()
                    board[self.pos_x][self.pos_y + y_move] = Blocked()
            if not (not self.state and self.state_new and cond) or self.player_coords_old != (
            player.pos_x, player.pos_y):
                self.player_coords_old = player.pos_x, player.pos_y
                self.state = self.state_new

        if self.x_move != 0:
            self.timer_x.tick()
            x_old = self.x
            self.x += self.x_move * (tile_width / self.timer_x.time_max)
            self.rect.x = self.x + camera.dx_total
            if self.timer_x.time == 0:
                board[self.next_cell[0]][self.next_cell[1]] = self
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_x += self.x_move
                self.x_move = 0
        if self.y_move != 0:
            self.timer_y.tick()
            self.y += self.y_move * (tile_width / self.timer_y.time_max)
            self.rect.y = self.y + camera.dy_total
            if self.timer_y.time == 0:
                board[self.next_cell[0]][self.next_cell[1]] = self
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_y += self.y_move
                self.y_move = 0
        if abs(self.pos_x - player.pos_x) <= self.rang_max and abs(self.pos_y - player.pos_y) <= self.rang_max and len(
                self.path) < self.rang_max * 1.5 and (not self.close_mode or (abs(self.pos_x - player.pos_x) <= self.rang_min and abs(self.pos_y - player.pos_y) <= self.rang_min)):
            if not self.close_mode and (player.timer_x.time != 0 or player.timer_y.time != 0) and self.clever_shoot:
                self.weapon.use(player.rect.x + player.x_move * tile_width + tile_width * 0.5,
                                player.rect.y + player.y_move * tile_height + tile_width * 0.5)
            else:
                self.weapon.use(player.rect.x + tile_width * 0.5, player.rect.y + tile_width * 0.5)

    def damage(self, n):  # функция получения урона, не нанесения
        # if inventory.rage_timer.time:  # если действует зелье увеличения урона
        #     self.hp -= n * 2  # то урон х2
        # else:
        #     self.hp -= n * 1
        self.hp = round((self.hp - n))
        # клеточка становится травой, монстр умирает
        if self.hp <= 0 or cheats:
            board[self.next_cell[0]][self.next_cell[1]] = Empty()
            board[self.pos_x][self.pos_y] = Empty()
            # if True or random.random() > 0.1:
            #     if random.random() > 0.5:
            #         a = HealPotion(self.pos_x, self.pos_y)
            #         print(self.pos_x, self.pos_y, a.rect.x, a.rect.y)
            #     else:
            #         a = RagePotion(self.pos_x, self.pos_y)
            #         print(self.pos_x, self.pos_y, a.rect.x, a.rect.y)
            self.kill()


class Bullet(pygame.sprite.Sprite):  # дальняя атака
    def __init__(self, picture, x1, y1, x2, y2, fraction, damage, speed, rang, bullet_size, go_through):
        super().__init__(all_sprites, attack_group)
        self.go_through = go_through
        self.image = images[picture]
        self.image = pygame.transform.scale(self.image, bullet_size)
        self.rect = self.image.get_rect().move(x1, y1)
        self.mask = pygame.mask.from_surface(self.image)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.fraction = fraction  # чтобы монстры не били по своим
        self.vel = speed
        self.dmg = damage
        a = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)  # радиус полёта
        self.vector = ((x2 - x1) / a, (y2 - y1) / a)  # куда летит пуля
        self.live_timer = Timer(rang)
        self.live_timer.start()

    def update(self):
        old_x, old_y = self.x1, self.y1
        self.x1, self.y1 = self.x1 + self.vector[0] * self.vel, self.y1 + self.vector[1] * self.vel
        self.rect.x += self.x1 - old_x
        self.rect.y += self.y1 - old_y
        for i in entity_group:  # проверка на столкновение с монстрами
            if pygame.sprite.collide_mask(self, i) and i not in self.fraction:  # если не свои
                i.damage(self.dmg)
                if not self.go_through:  # если можем пролететь
                    self.kill()
        for i in wall_group:  # проверка на столкновение со стенами
            if pygame.sprite.collide_mask(self, i):
                self.kill()
        self.live_timer.tick(self.vel)
        if self.live_timer.time == 0:
            self.kill()


class CloseAttack(pygame.sprite.Sprite):  # ближняя атака
    def __init__(self, picture, x, y, rang, rotation, owner, fraction, damage):
        super().__init__(all_sprites, attack_group)
        self.image = images[picture]
        self.image = pygame.transform.scale(self.image, (int(tile_width * rang), int(tile_height * rang)))
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect().move(
            x, y)  # положение картинки на доске
        self.rect.x, self.rect.y = x - self.rect.w // 2, y - self.rect.h // 2
        self.damaged_lst = list()
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = Timer(FPS // 4)
        self.timer.start()
        self.fraction = fraction  # чтобы не бить по своим
        self.dmg = damage
        self.owner = owner

    def update(self):
        self.rect.x, self.rect.y = self.owner.rect.x - self.rect.w // 2 + tile_width * 0.5, self.owner.rect.y - self.rect.h // 2 + tile_width * 0.5
        for i in entity_group:  # проверка на столкновение с монстрами
            if pygame.sprite.collide_mask(self, i) and i not in self.fraction and i not in self.damaged_lst:
                n = len(list(filter(lambda x: x, [
                    is_linear_path(*self.owner.rect.center, *i.rect.topleft, owner=self.owner, target=i,
                                   fraction=self.fraction, go_through_entities=True),
                    is_linear_path(*self.owner.rect.center, *i.rect.topright,
                                   owner=self.owner, target=i,
                                   fraction=self.fraction, go_through_entities=True), is_linear_path(
                        *self.owner.rect.center, *i.rect.bottomleft, owner=self.owner, target=i,
                        fraction=self.fraction, go_through_entities=True),
                    is_linear_path(*self.owner.rect.center, *i.rect.bottomright,
                                   owner=self.owner, target=i, fraction=self.fraction, go_through_entities=True)])))
                if n > 0:
                    i.damage((self.dmg / 4) * n)
                    self.damaged_lst.append(i)
        self.timer.tick()
        if self.timer.time == 0:  # анимация атаки пропадает после атаки
            self.kill()


class MagicAttack(pygame.sprite.Sprite):  # магическая атака, бьёт сквозь стены
    def __init__(self, picture, x, y, rang, fraction, damage):
        super().__init__(all_sprites, attack_group)
        self.image = images[picture]
        self.image = pygame.transform.scale(self.image, (int(tile_width * rang), int(tile_height * rang)))
        self.rect = self.image.get_rect().move(
            x, y)
        self.rect.x, self.rect.y = x - self.rect.w // 2, y - self.rect.h // 2
        self.damaged_lst = list()
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = Timer(FPS // 4)
        self.timer.start()
        self.fraction = fraction
        self.dmg = damage

    def update(self):
        if self.timer.time == self.timer.time_max:
            for i in entity_group:  # проверка на столкновение с монстрами
                if pygame.sprite.collide_mask(self, i) and i not in self.fraction and i not in self.damaged_lst and (
                        is_linear_path(*self.rect.center, *i.rect.topleft, target=i,
                                       fraction=self.fraction, go_through_entities=True) or is_linear_path(
                    *self.rect.center,
                    *i.rect.topright,
                    target=i,
                    fraction=self.fraction, go_through_entities=True) or is_linear_path(
                    *self.rect.center, *i.rect.bottomleft, target=i,
                    fraction=self.fraction, go_through_entities=True) or is_linear_path(*self.rect.center,
                                                                                        *i.rect.bottomright,
                                                                                        target=i,
                                                                                        fraction=self.fraction,
                                                                                        go_through_entities=True)):
                    i.damage(self.dmg)
                    self.damaged_lst.append(i)
        self.timer.tick()
        if self.timer.time == 0:
            self.kill()


class Bomb(pygame.sprite.Sprite):  # бомба, бьёт по области
    def __init__(self, picture, x1, y1, x2, y2, fraction, damage, speed, rang, bullet_size, area_width, blast_image):
        super().__init__(all_sprites, attack_group)
        self.image = images[picture]
        self.blast_image = blast_image
        self.area_width = area_width
        self.image = pygame.transform.scale(self.image, bullet_size)
        self.rect = self.image.get_rect().move(x1, y1)
        self.mask = pygame.mask.from_surface(self.image)
        self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2
        self.fraction = fraction
        self.vel = speed
        self.dmg = damage
        a = math.sqrt((self.x2 - self.x1) ** 2 + (self.y2 - self.y1) ** 2)
        self.vector = ((x2 - x1) / a, (y2 - y1) / a)
        self.live_timer = Timer(rang)
        self.live_timer.start()

    def update(self):
        old_x, old_y = self.x1, self.y1
        self.x1, self.y1 = self.x1 + self.vector[0] * self.vel, self.y1 + self.vector[1] * self.vel
        self.rect.x += self.x1 - old_x
        self.rect.y += self.y1 - old_y
        for i in entity_group:  # проверка на столкновение с монстрами
            if pygame.sprite.collide_mask(self, i) and i not in self.fraction:
                MagicAttack(self.blast_image, self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2,
                            self.area_width, self.fraction, self.dmg)
                self.kill()
        for i in wall_group:  # проверка на столкновение со стенами
            if pygame.sprite.collide_mask(self, i):
                MagicAttack(self.blast_image, self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2,
                            self.area_width, self.fraction, self.dmg)
                self.kill()
        self.live_timer.tick(self.vel)
        if self.live_timer.time == 0:
            MagicAttack(self.blast_image, self.rect.x + self.rect.width / 2, self.rect.y + self.rect.height / 2,
                        self.area_width, self.fraction, self.dmg)
            self.kill()


class Weapon(pygame.sprite.Sprite):  # класс оружия
    def __init__(self, icon, attack_picture, x, y, owner, fraction, damage, cooldown):
        super().__init__(all_sprites, static_sprites, weapon_group)
        self.owner, self.fraction, self.damage = owner, fraction, damage
        self.timer = Timer(cooldown)  # чтобы нельзя было 10 раз кликать за секунду
        self.image = pygame.transform.scale(images[icon], (inventory_slot_width, inventory_slot_width))
        self.attack_picture = attack_picture
        self.rect = self.image.get_rect().move(
            x, y)

    def update(self):
        if self.owner != player or weapon_lst[inventory.current_slot] == self:
            self.timer.tick()
            if self.owner == player and inventory.rage_timer.time != 0:
                self.timer.tick()

    # def use(self):
    #     if int(self.timer) == 0:
    #         self.timer.start()


class BulletWeapon(Weapon):  # дальнее оружие
    def __init__(self, *args, speed=10, rang=tile_width * 8, bullet_size=(25, 25), go_through_entities=False, name=''):
        self.name = name
        super().__init__(*args)
        self.bullet_size = bullet_size
        self.speed, self.rang = speed, rang
        self.go_through_entities = go_through_entities

    def use(self, x, y):
        if self.timer.time == 0:
            self.timer.start()
            Bullet(self.attack_picture, self.owner.rect.x + tile_width * 0.5 - self.bullet_size[0] * 0.5,
                   self.owner.rect.y + tile_width * 0.5 - self.bullet_size[1] * 0.5, x, y,
                   self.fraction, self.damage,
                   self.speed, self.rang, self.bullet_size, self.go_through_entities)


class MagicWeapon(Weapon):  # магическое оружие
    def __init__(self, *args, rang=tile_width * 5, area_width=2.15, name=''):
        self.name = name
        super().__init__(*args)
        self.area_width = area_width
        self.rang = rang

    def use(self, x, y):
        if self.timer.time == 0:
            self.timer.start()
            if abs(x - self.owner.rect.x) <= self.rang and abs(y - self.owner.rect.y) <= self.rang:
                MagicAttack(self.attack_picture, x, y,
                            self.area_width, self.fraction, self.damage)
            else:
                MagicAttack('cross', x, y,
                            self.area_width, self.fraction, 0)


class CloseWeapon(Weapon):  # оружие ближнего боя
    def __init__(self, *args, rang=2.15, name=''):
        self.name = name
        super().__init__(*args)
        self.rang = rang

    def use(self, x, y):
        if self.timer.time == 0:
            self.timer.start()
            vector1 = (x - self.owner.rect.center[0]), (y - self.owner.rect.center[1])
            vector2 = 1, 0
            ugol = math.acos((vector1[1]) / (math.sqrt(vector1[0] ** 2 + vector1[1] ** 2))) * 57.3
            ugol -= 45
            if vector1[0] < 0:
                ugol = -ugol - 90
            CloseAttack(self.attack_picture, self.owner.rect.x + tile_width * 0.5, self.owner.rect.y + tile_width * 0.5,
                        self.rang, ugol,
                        self.owner, self.fraction, self.damage)


class BombWeapon(Weapon):  # оружие - бомбы
    def __init__(self, *args, speed=10, rang=tile_width * 8, bullet_size=(25, 25), area_width=4, name='',
                 blast_image='boom'):
        self.name = name
        self.area_width = area_width
        super().__init__(*args)
        self.bullet_size = bullet_size
        self.speed, self.rang = speed, rang
        self.blast_image = blast_image

    def use(self, x, y):
        if self.timer.time == 0:
            self.timer.start()
            Bomb(self.attack_picture, self.owner.rect.x + tile_width * 0.5 - self.bullet_size[0] * 0.5,
                 self.owner.rect.y + tile_width * 0.5 - self.bullet_size[1] * 0.5, x, y,
                 self.fraction, self.damage,
                 self.speed, self.rang, self.bullet_size, self.area_width, self.blast_image)


def generate_level(level):
    x, y = None, None
    table = [[] for _ in range(len(level[0]))]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':  # трава
                BackgroundTile(x, y)
                table[x].append(Empty())
            elif level[y][x] == '#':  # стена
                table[x].append(Wall(x, y))
            elif level[y][x] == ' ' or level[y][x] == '-':
                table[x].append(Empty())
            elif level[y][x] == 'T':  # телепорт на следующий уровень
                BackgroundTile(x, y)
                table[x].append(Teleport(x, y))
            elif level[y][x] == 'W':  # телепорт при прохождении всей игры
                BackgroundTile(x, y)
                table[x].append(WinTeleport(x, y))
            elif level[y][x] == 'K':  # ключ, чтобы открылся телепорт на следующий уровень
                BackgroundTile(x, y)
                table[x].append(Key(x, y))
            elif level[y][x] == '%':  # стена, которая разрушится, если умрёт страж
                table[x].append(WallTriggerable(x, y, True if map_num in [1, 2] else False, True if map_num in [0, 3, 3.2] else False))
            elif level[y][x] == '@':  # игрок
                BackgroundTile(x, y)
                player_coords = x, y
                table[x].append(player)
            elif level[y][x] == 'J':  # сокровище
                BackgroundTile(x, y)
                table[x].append(Jewel(x, y))
            elif level[y][x] == 'H':  # сокровище
                BackgroundTile(x, y)
                table[x].append(HealPotion(x, y))
            elif level[y][x] == 'R':  # сокровище
                BackgroundTile(x, y)
                table[x].append(RagePotion(x, y))
            elif level[y][x] == 'S':  # ловушка
                BackgroundTile(x, y)
                table[x].append(Snare(x, y))
            elif level[y][x] == 'Z':  # ловушка
                BackgroundTile(x, y)
                table[x].append(HealZone(x, y))
            elif level[y][x] == '1':  # монстр ближнего боя
                BackgroundTile(x, y)
                table[x].append(
                    Monster(x, y,
                            CloseWeapon('empty_image', 'close_attack1', -50, -50, None, monster_group, 15, FPS,
                                        rang=3), 80, 2, 7, 'monster', True, 11,
                            dop_groups=[] if map_num != 0 else [guard_monster_group]))
            elif level[y][x] == '2':  # монстр дальнего боя
                BackgroundTile(x, y)
                table[x].append(Monster(x, y,
                                        BulletWeapon('empty_image', 'bullet', -50, -50, None, monster_group, 10, FPS,
                                                     speed=10, rang=400), 60, 5, 9, 'monster1', False, 11, dop_groups=[] if map_num not in [0, 3.2] else [guard_monster_group]))
            elif level[y][x] == '3':  # монстр, при убийстве которого разрушается некоторая стена
                BackgroundTile(x, y)
                table[x].append(
                    Monster(x, y, BulletWeapon('empty_image', 'bullet', -50, -50, None, monster_group, 13, FPS, speed=15,
                                               rang=500), 150, 8, 8, 'monster2', False, 30,
                            dop_groups=[guard_monster_group], clever_shoot=True))
            elif level[y][x] == '4':  # монстр, который кидает бомбы
                BackgroundTile(x, y)
                table[x].append(Monster(x, y,
                                        BombWeapon('empty_image', 'bomb', -50, -50, None, monster_group, 10, FPS,
                                                   speed=8, rang=300, area_width=3.5), 80, 5, 9, 'monster1', False, 10, clever_shoot=True, dop_groups=[] if map_num not in [0, 3.2] else [guard_monster_group]))
            elif level[y][x] == '5':  # монстр ближнего боя
                BackgroundTile(x, y)
                table[x].append(
                    Monster(x, y,
                            CloseWeapon('empty_image', 'close_attack2', -50, -50, None, monster_group, 10, FPS // 1.5,
                                        rang=2.5), 60, 1, 9, 'monster', True, 8,
                            dop_groups=[] if map_num not in [0, 3.2] else [guard_monster_group]))
            elif level[y][x] == '':  # монстр дальнего боя
                BackgroundTile(x, y)
                table[x].append(Monster(x, y,
                                        MagicWeapon('empty_image', 'bullet', -50, -50, None, monster_group, 10, FPS,
                                                    rang=400, area_width=1.5, ), 60, 5, 9, 'monster1', False, 11, dop_groups=[] if map_num not in [0, 3.2] else [guard_monster_group]))
            elif level[y][x] == '7':  # монстр ближнего боя
                BackgroundTile(x, y)
                table[x].append(
                    Monster(x, y,
                            CloseWeapon('empty_image', 'close_attack', -50, -50, None, monster_group, 10, FPS,
                                        rang=3.5), 100, 3, 7, 'monster', True, 12,
                            dop_groups=[] if map_num not in [0, 3.2] else [guard_monster_group]))
            elif level[y][x] == '8':  # монстр, при убийстве которого разрушается некоторая стена
                BackgroundTile(x, y)
                table[x].append(
                    Monster(x, y, BulletWeapon('empty_image', 'bullet', -50, -50, None, monster_group, 13, FPS, speed=25,
                                               rang=tile_width * 30, bullet_size=(tile_width, tile_width)), 100, tile_width * 30, tile_width * 30, 'monster2', False, math.inf,
                            dop_groups=[] if map_num not in [0, 3.2] else [guard_monster_group], clever_shoot=False))
            elif level[y][x] == '9':  # монстр ближнего боя
                BackgroundTile(x, y)
                table[x].append(
                    Monster(x, y,
                            CloseWeapon('empty_image', 'close_attack1', -50, -50, None, monster_group, 15, FPS // 1.5,
                                        rang=4), 200, 2, 15, 'monster', True, 8,
                            dop_groups=[guard_monster_group]))
    # вернем игрока, а также координаты игрока
    return Board(table), player_coords[0], player_coords[1]


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


def is_linear_path(x1, y1, x2, y2, owner=None, fraction=None, target=None, go_through_entities=False, field=1):
    a = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    vector = ((x2 - x1) / a * 2, (y2 - y1) / a * 2)
    cond = field == 1
    cond1 = (vector[0] >= 0) == (vector[1] >= 0)
    field //= 2
    while abs(int(x1) - int(x2)) > 3 or abs(int(y1) - int(y2)) > 3:
        for i in wall_group:
            if cond:
                if i.rect.collidepoint(x1, y1):
                    return False
            elif cond1:
                if (i.rect.collidepoint(x1 + field, y1 - field) or i.rect.collidepoint(x1 - field, y1 + field)):
                    return False
            else:
                if (i.rect.collidepoint(x1 - field, y1 - field) or i.rect.collidepoint(x1 + field, y1 + field)):
                    return False
        # if not go_through_entities:
        #     for i in entity_group:
        #         if field == 1:
        #             if i.rect.collidepoint(x1, y1) and i != owner and i != target and i not in fraction:
        #                 return False
        #         else:
        #             if (vector[0] >= 0) == (vector[1] >= 0):
        #                 if (i.rect.collidepoint(x1 + field // 2, y1 - field // 2) or i.rect.collidepoint(
        #                         x1 - field // 2, y1 + field // 2)) and i != owner and i != target and i not in fraction:
        #                     return False
        #             else:
        #                 if (i.rect.collidepoint(x1 - field // 2, y1 - field // 2) or i.rect.collidepoint(
        #                         x1 + field // 2, y1 + field // 2)) and i != owner and i != target and i not in fraction:
        #                     return False
        x1 += vector[0]
        y1 += vector[1]
    return True


class Board:  # класс матрицы доски
    def __init__(self, table):
        self.table = table  # сама матрица
        self.width = len(table)
        self.height = len(table[0])

    def __getitem__(self, item):  # индексирование матрицы
        return self.table[item]

    def get_path(self, x1, y1, x2, y2):  # поиск пути
        n = 1
        matrix = [list(map(lambda x: False if x.type() in ['wall', 'monster', 'blocked'] else -1, i)) for i in
                  self.table]
        matrix[x1][y1] = 1
        while matrix[x2][y2] == -1:
            flag = False
            for x in range(self.width):
                for y in range(self.height):
                    if matrix[x][y] == n:
                        if 0 <= x - 1 < self.width and 0 <= y < self.height and matrix[x - 1][y] == -1:
                            matrix[x - 1][y] = n + 1
                            flag = True
                        if 0 <= x + 1 < self.width and 0 <= y < self.height and matrix[x + 1][y] == -1:
                            matrix[x + 1][y] = n + 1
                            flag = True
                        if 0 <= x < self.width and 0 <= y - 1 < self.height and matrix[x][y - 1] == -1:
                            matrix[x][y - 1] = n + 1
                            flag = True
                        if 0 <= x < self.width and 0 <= y + 1 < self.height and matrix[x][y + 1] == -1:
                            matrix[x][y + 1] = n + 1
                            flag = True
            n += 1
            if not flag:
                n = 1
                matrix = [list(map(lambda x: False if x.type() in ['wall'] else -1, i)) for i in self.table]
                matrix[x1][y1] = 1
                while matrix[x2][y2] == -1:
                    flag = False
                    for x in range(self.width):
                        for y in range(self.height):
                            if matrix[x][y] == n:
                                if 0 <= x - 1 < self.width and 0 <= y < self.height and matrix[x - 1][y] == -1:
                                    matrix[x - 1][y] = n + 1
                                    flag = True
                                if 0 <= x + 1 < self.width and 0 <= y < self.height and matrix[x + 1][y] == -1:
                                    matrix[x + 1][y] = n + 1
                                    flag = True
                                if 0 <= x < self.width and 0 <= y - 1 < self.height and matrix[x][y - 1] == -1:
                                    matrix[x][y - 1] = n + 1
                                    flag = True
                                if 0 <= x < self.width and 0 <= y + 1 < self.height and matrix[x][y + 1] == -1:
                                    matrix[x][y + 1] = n + 1
                                    flag = True
                    if not flag:
                        return False
                    n += 1
        # print(*matrix, sep='\n')
        x, y = x2, y2
        lst = [(x, y)]
        while x != x1 or y != y1:
            if player.x_move == 0:
                if 0 <= x - 1 < self.width and 0 <= y < self.height and matrix[x - 1][y] == n - 1:
                    x = x - 1
                if 0 <= x + 1 < self.width and 0 <= y < self.height and matrix[x + 1][y] == n - 1:
                    x = x + 1
                if 0 <= x < self.width and 0 <= y - 1 < self.height and matrix[x][y - 1] == n - 1:
                    y = y - 1
                if 0 <= x < self.width and 0 <= y + 1 < self.height and matrix[x][y + 1] == n - 1:
                    y = y + 1
            else:
                if 0 <= x < self.width and 0 <= y + 1 < self.height and matrix[x][y + 1] == n - 1:
                    y = y + 1
                if 0 <= x < self.width and 0 <= y - 1 < self.height and matrix[x][y - 1] == n - 1:
                    y = y - 1
                if 0 <= x + 1 < self.width and 0 <= y < self.height and matrix[x + 1][y] == n - 1:
                    x = x + 1
                if 0 <= x - 1 < self.width and 0 <= y < self.height and matrix[x - 1][y] == n - 1:
                    x = x - 1
            lst.append((x, y))
            n -= 1
        return lst[::-1]


class StaticSprite(pygame.sprite.Sprite):  # для слотов инвентаря
    def __init__(self, x, y, img_name):
        super().__init__(all_sprites, inventar_group, static_sprites)
        self.image = images[img_name]
        self.rect = self.image.get_rect().move(
            x, y)
        self.mask = pygame.mask.from_surface(self.image)


class Inventory:  # класс иневентаря. В игре он снизу слева

    def __init__(self):
        self.current_slot = 0
        self.rage_timer = Timer(0)  # таймер для зелий увелмчения урона
        # слоты инвентаря
        StaticSprite(0, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width * 2, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width * 3, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width * 4, HEIGHT - inventory_slot_width, 'inventory_slot')

        StaticSprite(inventory_slot_width * 5 + 10, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width * 6 + 10, HEIGHT - inventory_slot_width, 'inventory_slot')
        self.hp_potion_sprite = StaticSprite(inventory_slot_width * 5 + 10, HEIGHT - inventory_slot_width,
                                             'empty_image')
        self.rage_potion_sprite = StaticSprite(inventory_slot_width * 6 + 10, HEIGHT - inventory_slot_width,
                                               'empty_image')
        self.weapon_frame = StaticSprite(0, HEIGHT - inventory_slot_width, 'frame')

    def use_weapon(self):
        if self.current_slot < len(weapon_lst):
            weapon_lst[self.current_slot].use(*pos)

    def plus_hp_potion(self):  # +1 зелье, которое лечит 5хп
        global hp_potions, rage_potions
        hp_potions += 1

    def plus_rage_potion(self):  # +1 зелье, которое увеличивает урон в 2 раза на 10 сек
        global hp_potions, rage_potions
        rage_potions += 1

    def hp_plus(self):
        global hp_potions, rage_potions
        if hp_potions:  # если есть зелье хп
            if player.hp + 50 <= player.hp_max:  # добавляем 5хп, если не привысим максимальное кол-во хп
                player.hp += 50  # +5 хп
                hp_potions -= 1  # -1 зелье, которое лечит 5 хп
            elif player.hp < player.hp_max:  # если +5 превысит максимальное кол-во хп, то добавляем до максимального
                player.hp = player.hp_max  # теперь хп = максимальные хп
                hp_potions -= 1  # -1 зелье, которое лечит 5 хп

    def plus_damage(self):
        global hp_potions, rage_potions
        if rage_potions and self.rage_timer.time == 0:  # если есть зелье ярости и оно неактивно
            rage_potions -= 1  # поглощаем 1 зелье
            self.rage_timer = Timer(FPS * 5)  # заводим таймер на 10 сек (60 тиков в секунду)
            self.rage_timer.start()  # начинаем отсчёт

    def quantity_rendering(self):  # отображение всего инвентаря
        if hp_potions != 0:
            self.hp_potion_sprite.image = images['health_potion']
        else:
            self.hp_potion_sprite.image = images['empty_image']
        if rage_potions != 0:
            self.rage_potion_sprite.image = images['rage_potion']
        else:
            self.rage_potion_sprite.image = images['empty_image']
        inventar_group.update()  # обновляем положение инвентаря
        inventar_group.draw(screen)  # выводим инвентарь на экран
        weapon_group.draw(screen)
        text = font_for_inventory.render(f"{hp_potions}", True, (255, 0, 0))  # кол-во зелий hp
        screen.blit(text, (inventory_slot_width * 6 + 5, HEIGHT - 12))  # выводим кол-во зелий хп около зелья хп
        text = font_for_inventory.render(f"{rage_potions}", True, (255, 0, 0))  # кол-во зелий ярости
        screen.blit(text, (inventory_slot_width * 7 + 5, HEIGHT - 12))  # выводим кол-во зелий ярости около зелья ярости

        text = font_for_inventory.render(f"{1}", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (
            inventory_slot_width * 1 - 8, HEIGHT - inventory_slot_width - 14))  # выводим зеленым шрифтом цифру 1
        text = font_for_inventory.render(f"{2}", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (
            inventory_slot_width * 2 - 8, HEIGHT - inventory_slot_width - 14))  # выводим зеленым шрифтом цифру 1
        text = font_for_inventory.render(f"{3}", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (
            inventory_slot_width * 3 - 8, HEIGHT - inventory_slot_width - 14))  # выводим зеленым шрифтом цифру 1
        text = font_for_inventory.render(f"{4}", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (
            inventory_slot_width * 4 - 8, HEIGHT - inventory_slot_width - 14))  # выводим зеленым шрифтом цифру 1
        text = font_for_inventory.render(f"{5}", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (
            inventory_slot_width * 5 - 8, HEIGHT - inventory_slot_width - 14))  # выводим зеленым шрифтом цифру 1

        text = font_for_inventory.render(f"E", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (
            inventory_slot_width * 6 + 2, HEIGHT - inventory_slot_width - 14))  # выводим зеленым шрифтом цифру 1
        text = font_for_inventory.render(f"Q", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (
            inventory_slot_width * 7 + 2, HEIGHT - inventory_slot_width - 14))  # выводим зеленым шрифтом цифру 1

        inventory.rage_timer.tick()  # если зелье активно, то уменьшаем время действия до 0. Иначе 0


def draw_hp(entity):
    pygame.draw.rect(screen, (255, 0, 0), (entity.rect.x, entity.rect.y - 20,
                                           int(tile_width * (entity.hp / entity.hp_max)), 15))
    pygame.draw.rect(screen, (0, 0, 0), (entity.rect.x, entity.rect.y - 20,
                                         tile_width, 15), 2)
    font = pygame.font.Font(None, 20)
    text = font.render(str(entity.hp), True, pygame.Color('white'))
    screen.blit(text, (entity.rect.x, entity.rect.y - text.get_height() - 20))


direction, state = start_screen()  # стартовое окно
fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
if state == 2:  # 2я кнопка = выход из игры
    terminate()
is_start = True
while True:
    hp_potions = 0
    rage_potions = 0
    if not is_start:
        direction = [0, 0]
    is_start = False
    game_running = True
    all_sprites = pygame.sprite.Group()
    player_group = pygame.sprite.Group()
    entity_group = pygame.sprite.Group()
    static_sprites = pygame.sprite.Group()
    weapon_group = pygame.sprite.Group()
    player = Player(0, 0)
    time_counter = 0
    is_won = False
    weapon_lst = [CloseWeapon('sword', 'close_attack1', -50, -50, player, player_group, 20, FPS // 2,
                              rang=4, name='меч')]
    cheats = False

    for map_num, map_name in enumerate(['map.txt', 'map1.txt', 'map2.txt', 'map3', 'map4.txt']):
        level_running = True
        save_potions = [hp_potions, rage_potions]
        save_hp = player.hp
        save_weapons = weapon_lst.copy()
        map_num_save, map_name_save = map_num, map_name
        while level_running:
            map_num, map_name = map_num_save, map_name_save
            player.is_killed = False
            hp_potions, rage_potions = save_potions
            player.hp = save_hp
            weapon_lst = save_weapons.copy()
            for map_num, map_name in [(map_num, map_name)] if map_name != 'map3' else [(3.1, 'map3.1.txt'), (3.2, 'map3.2.txt'), (3, 'map3.txt')]:
                keys_not_collected = 0
                potion_group = pygame.sprite.Group()
                tiles_group = pygame.sprite.Group()  # всё, что не является сущностью и стеной
                snares_group = pygame.sprite.Group()  # ловушки
                wall_group = pygame.sprite.Group()  # стены
                monster_group = pygame.sprite.Group()
                guard_monster_group = pygame.sprite.Group()  # монстры, при смерти которых разрушаются стены
                entity_group = pygame.sprite.Group()  # сущности (игрок и монстры)
                attack_group = pygame.sprite.Group()  # ближняя, дальняя, магическая атаки и бомбы
                static_sprites = pygame.sprite.Group()  # для слотов инвентаря
                weapon_group = pygame.sprite.Group()  # для оружий
                inventar_group = pygame.sprite.Group()  # для инвентаря в целом
                entity_group.add(player)
                static_sprites.add(*weapon_lst)
                static_sprites.add(*weapon_lst)
                weapon_group.add(*weapon_lst)
                pos = 0, 0
                board, player_x, player_y = generate_level(load_level(map_name))
                player.set_at_position(player_x, player_y)
                camera = Camera()
                is_clicked_r, is_clicked_l = False, False
                level_running = True
                life_running = True
                inventory = Inventory()
                font_for_inventory = pygame.font.Font(None, 22)
                pause_btn = StaticSprite(WIDTH - inventory_slot_width, HEIGHT - inventory_slot_width,
                                         'pause')  # справа снизу
                while level_running and life_running:
                    time_counter += 1  # для вывода времени
                    # изменяем ракурс камеры
                    # внутри игрового цикла ещё один цикл
                    # приёма и обработки сообщений
                    for event in pygame.event.get():
                        # при закрытии окна
                        if event.type == pygame.QUIT:
                            terminate()
                        # атака при зажатой ЛКМ
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                            is_clicked_l = True
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                            is_clicked_l = False
                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                            is_clicked_r = True
                        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                            is_clicked_r = False
                        # выбор оружия клавишами 1 - 4, если такое оружия имеются у игрока
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                            inventory.current_slot = 0
                            inventory.weapon_frame.rect.x = 0
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_2 and len(weapon_lst) >= 2:
                            inventory.current_slot = 1
                            inventory.weapon_frame.rect.x = inventory_slot_width
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_3 and len(weapon_lst) >= 3:
                            inventory.current_slot = 2
                            inventory.weapon_frame.rect.x = inventory_slot_width * 2
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_4 and len(weapon_lst) >= 4:
                            inventory.current_slot = 3
                            inventory.weapon_frame.rect.x = inventory_slot_width * 3
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_5 and len(weapon_lst) >= 5:
                            inventory.current_slot = 4
                            inventory.weapon_frame.rect.x = inventory_slot_width * 4
                        # Esc = пауза
                        if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE) or (
                                event.type == pygame.MOUSEBUTTONDOWN and pause_btn.rect.x < event.pos[
                            0] < pause_btn.rect.x + pause_btn.rect.w and pause_btn.rect.y < event.pos[
                                    1] < pause_btn.rect.y + pause_btn.rect.h):
                            direction_new, state = pause_screen()
                            direction[0] += direction_new[0]
                            direction[1] += direction_new[1]
                            if state == 1:
                                player.is_killed = True
                            elif state == 2:
                                terminate()
                            is_clicked_r, is_clicked_l = False, False
                        # читы
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_0:
                            cheats = not cheats
                        # направление атаки
                        if event.type == pygame.MOUSEMOTION:
                            pos = event.pos

                        if event.type == pygame.KEYDOWN and event.key == pygame.K_e:  # восстанавливает до 5хп
                            inventory.hp_plus()

                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:
                            if inventory.current_slot != 0:
                                inventory.current_slot -= 1
                                inventory.weapon_frame.rect.x -= inventory_slot_width
                            else:
                                inventory.current_slot = len(weapon_lst) - 1
                                inventory.weapon_frame.rect.x = inventory_slot_width * (len(weapon_lst) - 1)
                        if event.type == pygame.KEYDOWN and event.key == pygame.K_q:  # активирует зелье урона
                            inventory.plus_damage()

                        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:
                            if inventory.current_slot != len(weapon_lst) - 1:
                                inventory.current_slot += 1
                                inventory.weapon_frame.rect.x += inventory_slot_width
                            else:
                                inventory.current_slot = 0
                                inventory.weapon_frame.rect.x = 0

                        if event.type == pygame.KEYDOWN:  # назначаем движение
                            if event.key == pygame.K_w:  # вверх
                                direction[1] -= 1
                            if event.key == pygame.K_d:  # вправо
                                direction[0] += 1
                            if event.key == pygame.K_s:  # вниз
                                direction[1] += 1
                            if event.key == pygame.K_a:  # влево
                                direction[0] -= 1
                        if event.type == pygame.KEYUP:  # убираем движение по направлениям, если клавишу отпустили
                            if event.key == pygame.K_w:
                                direction[1] += 1
                            if event.key == pygame.K_d:
                                direction[0] -= 1
                            if event.key == pygame.K_s:
                                direction[1] -= 1
                            if event.key == pygame.K_a:
                                direction[0] += 1
                    for i in range(len(weapon_lst)):
                        weapon_lst[i].rect.x = inventory_slot_width * i
                        weapon_lst[i].rect.y = HEIGHT - inventory_slot_width
                    if is_clicked_r:
                        pass
                    if is_clicked_l:
                        inventory.use_weapon()
                    # обновляем положение всех спрайтов
                    player.make_move(*direction)
                    monster_group.update()
                    player_group.update()
                    attack_group.update()
                    weapon_group.update()
                    tiles_group.update()
                    camera.update(player)
                    for sprite in all_sprites:
                        if sprite not in static_sprites:
                            camera.apply(sprite)
                    screen.fill((255, 255, 255))
                    # спрайты клеток и сущности рисуются отдельно, чтобы спрайты клеток не наслаивались на сущностей
                    # сначала фон, потом сущности, потом используемые атаки (пули, ближний бой и тд)
                    screen.blit(fon, (0, 0))

                    tiles_group.draw(
                        screen)
                    potion_group.draw(screen)
                    entity_group.draw(screen)
                    if inventory.rage_timer.time != 0:
                        pygame.draw.rect(screen, (255, 0, 255), (player.rect.x, player.rect.y,
                                                                 tile_width, tile_height), 3)
                    if cheats:
                        pygame.draw.rect(screen, (0, 0, 0), (player.rect.x - 3, player.rect.y - 3,
                                                                 tile_width + 6, tile_height + 6), 3)
                    attack_group.draw(screen)
                    for i in entity_group:  # всем сущностям и герою выводим полоску хп
                        draw_hp(i)
                    # обновляем инвентарь
                    static_sprites.draw(screen)
                    inventory.quantity_rendering()
                    clock.tick(FPS)
                    pygame.display.flip()
                    # при смерти экран поражения
                    if player.is_killed:
                        break
                        life_running = False
        if game_running == False:
            break
    # при победе экран победы
    if is_won:
        direction_new, state = win_screen()
        direction[0] += direction_new[0]
        direction[1] += direction_new[1]
        if state == 0:
            is_start = True
            game_running = False
        elif state == 2:
            terminate()
