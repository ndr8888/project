import sys
import os
import math
import random
from Constants import *


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


def load_image(name, colorkey=None):  # функция для загрузки изображений для спрайтов
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


def terminate():  # выход из игры
    pygame.quit()
    sys.exit()


def start_screen():  # начальное окно
    direction = [0, 0]
    # текст
    intro_text = ["Правила игры",
                  "Управление - WASD",
                  "Смена оружий - 12345, зелья - QE",
                  "0 - читы",
                  "Количество уровней - 5"]

    fon = random.choice(fons)
    screen.blit(fon, (0, 0))
    # цикл работы
    while True:
        screen.blit(fon, (0, 0))
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


def win_screen():  # окно победы, принцип тот же, что и в функции выше
    direction = [0, 0]
    a = [
        f'Уровень {i + 1}: {sum([j for j in level_counters[i]]) // 3600} мин ' +
        f'{sum([j for j in level_counters[i]]) % 3600 // 60} сек '
        for i in range(len(level_counters))]
    intro_text = ["ИГРА ПРОЙДЕНА",
                  f"Время: {time_counter // 3600} мин {time_counter % 3600 // 60} сек",
                  "Всего:"] + a

    fon = random.choice(fons)
    screen.blit(fon, (0, 0))

    while True:
        screen.blit(fon, (0, 0))
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

    fon = random.choice(fons)
    screen.blit(fon, (0, 0))
    text_coord = 50

    while True:
        screen.blit(fon, (0, 0))
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


def draw_hp(entity):
    pygame.draw.rect(screen, (255, 0, 0), (entity.rect.x, entity.rect.y - 20,
                                           int(tile_width * (entity.hp / entity.hp_max)), 15))
    pygame.draw.rect(screen, (0, 0, 0), (entity.rect.x, entity.rect.y - 20,
                                         tile_width, 15), 2)
    font = pygame.font.Font(None, 20)
    text = font.render(str(entity.hp), True, pygame.Color('white'))
    screen.blit(text, (entity.rect.x, entity.rect.y - text.get_height() - 20))