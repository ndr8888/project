import pygame
import os
import sys
import random
import math

clock = pygame.time.Clock()
pygame.init()
size = WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode(size)
tile_width = tile_height = 40
inventory_slot_width = 60


class Timer:
    def __init__(self, time_max):
        self.time_max = time_max
        self.time = 0

    def start(self):
        self.time = self.time_max

    def tick(self, time=1):
        self.time -= time
        if self.time < 0:
            self.time = 0

    def stop(self):
        self.time = 0

    def __int__(self):
        return self.time


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()
    image = pygame.image.load(fullname)
    return image


images = {
    'wall': pygame.transform.scale(load_image('box.png'), (tile_width, tile_height)),
    'empty': pygame.transform.scale(load_image('grass.png'), (tile_width, tile_height)),
    'bullet': load_image('bullet.png'),
    'close_attack': load_image('attack.png'),
    'close_attack1': load_image('attack1.png'),
    'empty_image': load_image('empty_image.png'),
    'monster': pygame.transform.scale(load_image('enemy.png'), (tile_width, tile_height)),
    'monster1': pygame.transform.scale(load_image('enemy1.png'), (tile_width, tile_height)),
    'player': pygame.transform.scale(load_image('mar.png'), (tile_width, tile_height)),
    'game_over': pygame.transform.scale(load_image('gameover.png'), (WIDTH, HEIGHT)),
    'inventory_slot': pygame.transform.scale(load_image('inventory_slot.png'), (inventory_slot_width, inventory_slot_width)),
    'inventory_slot2': pygame.transform.scale(load_image('inventory_slot2.png'), (inventory_slot_width, inventory_slot_width)),
    'sword': load_image('sword.png'),
    'gun': load_image('gun.png'),
    'frame': pygame.transform.scale(load_image('frame.png'), (inventory_slot_width, inventory_slot_width)),
    'health_potion': pygame.transform.scale(load_image('health_potion.png'), (inventory_slot_width, inventory_slot_width)),
    'shield_potion': pygame.transform.scale(load_image('shield_potion.png'), (inventory_slot_width, inventory_slot_width)),
    'rage_potion': pygame.transform.scale(load_image('rage_potion.png'), (inventory_slot_width, inventory_slot_width)),
    'speed_potion': pygame.transform.scale(load_image('speed_potion.png'), (inventory_slot_width, inventory_slot_width)),
}
FPS = 60


def terminate():
    pygame.quit()
    sys.exit()


def start_screen():
    intro_text = ["ЗАСТАВКА", "",
                  "Правила игры",
                  "Если в правилах несколько строк,",
                  "приходится выводить их построчно"]

    fon = pygame.transform.scale(load_image('fon.jpg'), (WIDTH, HEIGHT))
    screen.blit(fon, (0, 0))
    font = pygame.font.Font(None, 30)
    text_coord = 50
    for line in intro_text:
        string_rendered = font.render(line, 1, pygame.Color('white'))
        intro_rect = string_rendered.get_rect()
        text_coord += 10
        intro_rect.top = text_coord
        intro_rect.x = 10
        text_coord += intro_rect.height
        screen.blit(string_rendered, intro_rect)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or \
                    event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        pygame.display.flip()
        clock.tick(FPS)


start_screen()


def load_level(filename):
    filename = "data/" + filename
    # читаем уровень, убирая символы перевода строки
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]

    # и подсчитываем максимальную длину
    max_width = max(map(len, level_map))

    # дополняем каждую строку пустыми клетками ('.')
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


class BackgroundTile(pygame.sprite.Sprite):  # класс фоновой картинки, пришлось разделить его и класс стены
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.image = images['empty']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Wall(pygame.sprite.Sprite):  # класс стены
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites, wall_group)
        self.image = images['wall']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)

    def type(self):  # возвращает строку типа спрайта, нужно для использования спрайтов в матрице
        return 'wall'


class Empty:  # класс пустоты для матрицы
    def __init__(self):
        pass

    def type(self):
        return 'empty'


class Blocked:  # класс пустоты для матрицы
    def __init__(self):
        pass

    def type(self):
        return 'blocked'


class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.speed = 8  # должен быть кратен tile_width
        self.timer_x = Timer(self.speed)
        self.timer_y = Timer(self.speed)
        super().__init__(player_group, all_sprites, entity_group)
        self.hp_max = 12
        self.hp = self.hp_max
        self.diagonal = False  # переменная, нужная для диагонального хода игроком
        self.pos_x, self.pos_y = pos_x, pos_y  # координаты игрока в клетках
        self.image = images['player']
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.x_move, self.y_move = 0, 0
        self.x, self.y = self.rect.topleft

    def set_at_position(self, pos_x, pos_y):
        print(1)
        self.timer_x = Timer(self.speed)
        self.timer_y = Timer(self.speed)
        self.diagonal = False  # переменная, нужная для диагонального хода игроком
        self.x_move, self.y_move = 0, 0
        self.pos_x, self.pos_y = pos_x, pos_y
        self.rect.x, self.rect.y = tile_width * pos_x, tile_height * pos_y
        self.x, self.y = self.rect.topleft

    def type(self):
        return 'player'

    def make_move(self, x_move, y_move):
        if self.diagonal:
            if self.x_move == 0 and x_move != 0 and int(self.timer_y) == 0 and board[self.pos_x + x_move][
                self.pos_y].type() not in ['wall', 'monster', 'blocked']:
                board[self.pos_x + x_move][self.pos_y] = Blocked()
                self.x_move = x_move
                self.timer_x.start()
                self.diagonal = not self.diagonal
            if self.y_move == 0 and y_move != 0 and int(self.timer_x) == 0 and board[self.pos_x][
                self.pos_y + y_move].type() not in ['wall', 'monster', 'blocked']:
                board[self.pos_x][self.pos_y + y_move] = Blocked()
                self.y_move = y_move
                self.timer_y.start()
                self.diagonal = not self.diagonal
        else:
            if self.y_move == 0 and y_move != 0 and int(self.timer_x) == 0 and board[self.pos_x][
                self.pos_y + y_move].type() not in ['wall', 'monster', 'blocked']:
                board[self.pos_x][self.pos_y + y_move] = Blocked()
                self.y_move = y_move
                self.timer_y.start()
                self.diagonal = not self.diagonal
            if self.x_move == 0 and x_move != 0 and int(self.timer_y) == 0 and board[self.pos_x + x_move][
                self.pos_y].type() not in ['wall', 'monster', 'blocked']:
                board[self.pos_x + x_move][self.pos_y] = Blocked()
                self.x_move = x_move
                self.timer_x.start()
                self.diagonal = not self.diagonal

    def update(self):
        if self.x_move != 0:
            self.timer_x.tick()
            x_old = self.x
            self.x += self.x_move * (tile_width / self.timer_x.time_max)
            self.rect.x -= x_old - self.x
            if int(self.timer_x) == 0:
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_x += self.x_move
                board[self.pos_x][self.pos_y] = player
                self.x_move = 0
        if self.y_move != 0:
            self.timer_y.tick()
            y_old = self.y
            self.y += self.y_move * (tile_width / self.timer_y.time_max)
            self.rect.y -= y_old - self.y
            if int(self.timer_y) == 0:
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_y += self.y_move
                board[self.pos_x][self.pos_y] = player
                self.y_move = 0

    def damage(self, n):
        if int(inventory.armor_timer):
            self.hp -= n * 0
        else:
            self.hp -= n * 1
        if self.hp <= 0:
            Gameover()
            self.kill()



class CloseMonster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.weapon = CloseWeapon('empty_image', 'close_attack', -50, -50, self, monster_group, 1, FPS // 2,
                                  rang=2.25)  #изменяемый
        # self.weapon = BulletWeapon(-50, -50, self, monster_group, 1, FPS, speed=10, rang=400)
        self.hp_max = 10  #
        self.hp = self.hp_max #
        self.rang_min = 2  #
        self.rang_max = 7  #
        self.image = images['monster']  #
        self.close_mode = True  #
        self.x_move, self.y_move = 0, 0
        self.speed = 10
        self.timer_x = Timer(self.speed)
        self.timer_y = Timer(self.speed)
        self.pos_x, self.pos_y = pos_x, pos_y
        super().__init__(monster_group, all_sprites, entity_group)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.next_cell = 0, 0

    def type(self):
        return 'monster'

    def update(self):
        if not self.close_mode:
            if abs(self.pos_x - player.pos_x) <= self.rang_max and abs(self.pos_y - player.pos_y) <= self.rang_max:
                self.weapon.use(player.rect.x, player.rect.y)
        else:
            if abs(self.pos_x - player.pos_x) <= self.rang_min and abs(self.pos_y - player.pos_y) <= self.rang_min:
                self.weapon.use(player.rect.x, player.rect.y)

        if int(self.timer_x) == 0 and int(self.timer_y) == 0:
            path = board.get_path(self.pos_x, self.pos_y, player.pos_x, player.pos_y)
            next_cell = path[1]
            if board[next_cell[0]][next_cell[1]].type() == 'empty' and abs(
                    self.pos_x - player.pos_x) <= self.rang_max and abs(
                self.pos_y - player.pos_y) <= self.rang_max:
                if self.rang_min <= abs(self.pos_x - player.pos_x) or self.rang_min <= abs(
                        self.pos_y - player.pos_y):
                    self.next_cell = next_cell
                    x_move, y_move = self.next_cell[0] - self.pos_x, self.next_cell[1] - self.pos_y
                elif board[self.pos_x - (next_cell[0] - self.pos_x)][
                    self.pos_y - (next_cell[1] - self.pos_y)].type() == 'empty' and not (abs(
                    self.pos_x - player.pos_x) == self.rang_min - 1 or abs(
                    self.pos_y - player.pos_y) == self.rang_min - 1):
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

        if self.x_move != 0:
            self.timer_x.tick()
            self.rect.x += self.x_move * (tile_width / self.timer_x.time_max)
            if int(self.timer_x) == 0:
                board[self.next_cell[0]][self.next_cell[1]] = self
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_x += self.x_move
                self.x_move = 0
        if self.y_move != 0:
            self.timer_y.tick()
            self.rect.y += self.y_move * (tile_width / self.timer_y.time_max)
            if int(self.timer_y) == 0:
                board[self.next_cell[0]][self.next_cell[1]] = self
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_y += self.y_move
                self.y_move = 0

    def damage(self, n):
        if int(inventory.rage_timer):  # если действует зелье увеличения урона
            self.hp -= n * 2  # то урон х2
        else:
            self.hp -= n * 1
        if self.hp <= 0:
            board[self.next_cell[0]][self.next_cell[1]] = Empty()
            board[self.pos_x][self.pos_y] = Empty()
            self.kill()

class RangedMonster(CloseMonster):
    def __init__(self, *args):
        super().__init__(*args)
        self.weapon = BulletWeapon('empty_image', 'bullet', -50, -50, self, monster_group, 1, FPS, speed=10, rang=400) #
        self.hp_max = 8  #
        self.hp = self.hp_max
        self.rang_min = 5  #
        self.rang_max = 9  #
        self.image = images['monster1']  #
        self.close_mode = False  #


class Bullet(pygame.sprite.Sprite):
    def __init__(self, picture, x1, y1, x2, y2, fraction, damage, speed, rang, bullet_size, go_through):
        super().__init__(all_sprites, attack_group)
        self.go_through = go_through
        self.image = images[picture]
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
                i.damage(self.dmg)
                if not self.go_through:
                    self.kill()
        for i in wall_group:  # проверка на столкновение со стенами
            if pygame.sprite.collide_mask(self, i):
                self.kill()
        self.live_timer.tick(self.vel)
        if int(self.live_timer) == 0:
            self.kill()


class CloseAttack(pygame.sprite.Sprite):
    def __init__(self, picture, x, y, rang, rotation, owner, fraction, damage):
        super().__init__(all_sprites, attack_group)
        self.image = images[picture]
        self.image = pygame.transform.scale(self.image, (tile_width * rang, tile_height * rang))
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect().move(
            x, y)
        self.rect.x, self.rect.y = x - self.rect.w // 2, y - self.rect.h // 2
        self.damaged_lst = list()
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = Timer(FPS // 4)
        self.timer.start()
        self.fraction = fraction
        self.dmg = damage
        self.owner = owner

    def update(self):
        self.rect.x, self.rect.y = self.owner.rect.x - self.rect.w // 2 + tile_width * 0.5, self.owner.rect.y - self.rect.h // 2 + tile_width * 0.5
        for i in entity_group:  # проверка на столкновение с монстрами
            if pygame.sprite.collide_mask(self, i) and i not in self.fraction and i not in self.damaged_lst and (
                    is_linear_path(*self.owner.rect.center, *i.rect.topleft, owner=self.owner, target=i,
                                   fraction=self.fraction) or is_linear_path(*self.owner.rect.center, *i.rect.topright,
                                                                             owner=self.owner, target=i,
                                                                             fraction=self.fraction) or is_linear_path(
                *self.owner.rect.center, *i.rect.bottomleft, owner=self.owner, target=i,
                fraction=self.fraction) or is_linear_path(*self.owner.rect.center, *i.rect.bottomright,
                                                          owner=self.owner, target=i, fraction=self.fraction)):
                i.damage(self.dmg)
                self.damaged_lst.append(i)
        self.timer.tick()
        if int(self.timer) == 0:
            self.kill()


class Weapon(pygame.sprite.Sprite):
    def __init__(self, icon, attack_picture, x, y, owner, fraction, damage, cooldown):
        super().__init__(all_sprites, static_sprites, weapon_group)
        self.owner, self.fraction, self.damage = owner, fraction, damage
        self.timer = Timer(cooldown)
        self.image = pygame.transform.scale(images[icon], (inventory_slot_width, inventory_slot_width))
        self.attack_picture = attack_picture
        self.rect = self.image.get_rect().move(
            x, y)

    def update(self):
        self.timer.tick()

    # def use(self):
    #     if int(self.timer) == 0:
    #         self.timer.start()


class BulletWeapon(Weapon):
    def __init__(self, *args, speed=10, rang=400, bullet_size=(25, 25), go_through_entities=False, name=''):
        self.name = name
        super().__init__(*args)
        self.bullet_size = bullet_size
        self.speed, self.rang = speed, rang
        self.go_through_entities = go_through_entities

    def use(self, x, y):
        if int(self.timer) == 0:
            self.timer.start()
            Bullet(self.attack_picture, self.owner.rect.x + tile_width * 0.5 - self.bullet_size[0] * 0.5, self.owner.rect.y + tile_width * 0.5 - self.bullet_size[1] * 0.5, x, y,
                   self.fraction, self.damage,
                   self.speed, self.rang, self.bullet_size, self.go_through_entities)


class CloseWeapon(Weapon):
    def __init__(self, *args, rang=2.15, name=''):
        self.name = name
        super().__init__(*args)
        self.rang = rang

    def use(self, x, y):
        if int(self.timer) == 0:
            self.timer.start()
            vector1 = (x - self.owner.rect.x), (y - self.owner.rect.y)
            vector2 = 1, 0
            ugol = math.acos((vector1[1]) / (math.sqrt(vector1[0] ** 2 + vector1[1] ** 2))) * 57.3
            ugol -= 45
            if vector1[0] < 0:
                ugol = -ugol - 90
            CloseAttack(self.attack_picture, self.owner.rect.x + tile_width * 0.5, self.owner.rect.y + tile_width * 0.5,
                        self.rang, ugol,
                        self.owner, self.fraction, self.damage)


def generate_level(level):
    x, y = None, None
    table = [[] for _ in range(len(level[0]))]
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                BackgroundTile(x,
                               y)  # фоновые спрайты не добавляются в матрицу, потому что они наслаивались бы друг на друга и засоряли экран
                table[x].append(Empty())
            elif level[y][x] == '#':
                table[x].append(Wall(x, y))
            elif level[y][x] == '@':
                BackgroundTile(x, y)
                player_coords = x, y
                table[x].append(player)
            elif level[y][x] == '1':  # монстер обозначается цифрой 1, при добавлнии новых монстров будет 2, 3 и тд
                BackgroundTile(x, y)
                table[x].append(CloseMonster(x, y))
            elif level[y][x] == '2':  # монстер обозначается цифрой 1, при добавлнии новых монстров будет 2, 3 и тд
                BackgroundTile(x, y)
                table[x].append(RangedMonster(x, y))
    # вернем игрока, а также размер поля в клетках
    return Board(table), *player_coords


class Camera:
    # зададим начальный сдвиг камеры
    def __init__(self):
        self.dx = 0
        self.dy = 0

    # сдвинуть объект obj на смещение камеры
    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    # позиционировать камеру на объекте target
    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - HEIGHT // 2)


def is_linear_path(x1, y1, x2, y2, owner=None, fraction=[], target=None, go_through_entities=False):
    a = math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
    vector = ((x2 - x1) / a, (y2 - y1) / a)
    while abs(int(x1) - int(x2)) > 3 or abs(int(y1) - int(y2)) > 3:
        for i in wall_group:
            if i.rect.collidepoint(x1, y1) and i != owner and i != target and i not in fraction:
                return False
        if not go_through_entities:
            for i in entity_group:
                if i.rect.collidepoint(x1, y1) and i != owner and i != target and i not in fraction:
                    return False
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
                    for x in range(self.width):
                        for y in range(self.height):
                            if matrix[x][y] == n:
                                if 0 <= x - 1 < self.width and 0 <= y < self.height and matrix[x - 1][y] == -1:
                                    matrix[x - 1][y] = n + 1
                                if 0 <= x + 1 < self.width and 0 <= y < self.height and matrix[x + 1][y] == -1:
                                    matrix[x + 1][y] = n + 1
                                if 0 <= x < self.width and 0 <= y - 1 < self.height and matrix[x][y - 1] == -1:
                                    matrix[x][y - 1] = n + 1
                                if 0 <= x < self.width and 0 <= y + 1 < self.height and matrix[x][y + 1] == -1:
                                    matrix[x][y + 1] = n + 1
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

class StaticSprite(pygame.sprite.Sprite):
    def __init__(self, x, y, img_name):
        super().__init__(all_sprites, inventar_group, static_sprites)
        self.image = images[img_name]
        self.rect = self.image.get_rect().move(
            x, y)
        self.mask = pygame.mask.from_surface(self.image)

class Inventory():   # класс иневентаря. В игре он снизу слева

    def __init__(self):
        self.items = [CloseWeapon('sword', 'close_attack1', -50, -50, player, player_group, 2, FPS // 2,
                                         rang=4.25, name='меч'), BulletWeapon('gun', 'bullet', -50, -50,
                                                               player,
                                                               player_group,
                                                               1.5, FPS // 2,
                                                               speed=12,
                                                               rang=300, name='пистолет', bullet_size=(25, 25))]
        self.current_slot = 0
        for i in range(len(self.items)):
            self.items[i].rect.x = inventory_slot_width * i
            self.items[i].rect.y = HEIGHT - inventory_slot_width
        self.hp_potions = 0  # кол-во зелий, которые лечат 5хп
        self.rage_potion = 0  # кол-во зелий, которые увеличивают урон в 2 раза на 10 сек
        self.armor_potion = 0  # кол-во зелий, которые уменьшают получаемый урон до 0 на 5 сек
        self.speed_potion = 0  # кол-во зелий, которые увеличивают скорость в 2 раза
        self.armor_timer = Timer(0)  # таймер для зелий неуязвимости
        self.rage_timer = Timer(0)  # таймер для зелий увелмчения урона
        self.speed_timer = Timer(0)  # таймер для зелий скорости
        StaticSprite(0, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width * 2, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width * 3, HEIGHT - inventory_slot_width, 'inventory_slot')
        StaticSprite(inventory_slot_width * 4, HEIGHT - inventory_slot_width, 'inventory_slot')

        StaticSprite(inventory_slot_width * 5 + 10, HEIGHT - inventory_slot_width, 'health_potion')
        StaticSprite(inventory_slot_width * 6 + 10, HEIGHT - inventory_slot_width, 'rage_potion')
        StaticSprite(inventory_slot_width * 7 + 10, HEIGHT - inventory_slot_width, 'shield_potion')
        StaticSprite(inventory_slot_width * 8 + 10, HEIGHT - inventory_slot_width, 'speed_potion')

        StaticSprite(inventory_slot_width * 5 + 10, HEIGHT - inventory_slot_width, 'inventory_slot2')
        StaticSprite(inventory_slot_width * 6 + 10, HEIGHT - inventory_slot_width, 'inventory_slot2')
        StaticSprite(inventory_slot_width * 7 + 10, HEIGHT - inventory_slot_width, 'inventory_slot2')
        StaticSprite(inventory_slot_width * 8 + 10, HEIGHT - inventory_slot_width, 'inventory_slot2')
        self.weapon_frame = StaticSprite(0, HEIGHT - inventory_slot_width, 'frame')

    def use_weapon(self):
        if self.current_slot < len(self.items):
            self.items[self.current_slot].use(*pos)

    def plus_hp_potion(self):  # +1 зелье, которое лечит 5хп
        self.hp_potions += 1

    def plus_rage_potion(self):  # +1 зелье, которое увеличивает урон в 2 раза на 10 сек
        self.rage_potion += 1

    def plus_armor_potion(self):  # +1 зелье, которое уменьшает получаемый урон до 0 на 5 сек
        self.armor_potion += 1

    def plus_speed_potion(self):  # +1 зелье, которое уменьшает получаемый урон до 0 на 5 сек
        self.speed_potion += 1

    def hp_plus(self):
        if self.hp_potions:  # если есть зелье хп
            if player.hp + 5 <= player.hp_max:  # добавляем 5хп, если не привысим максимальное кол-во хп
                player.hp += 5  # +5 хп
                self.hp_potions -= 1  # -1 зелье, которое лечит 5 хп
            elif player.hp < player.hp_max:  # если +5 превысит максимальное кол-во хп, то добавляем до максимального
                player.hp = player.hp_max  # теперь хп = максимальные хп
                self.hp_potions -= 1  # -1 зелье, которое лечит 5 хп

    def plus_damage(self):
        if self.rage_potion and int(self.rage_timer) == 0:  # если есть зелье ярости и оно неактивно
            self.rage_potion -= 1  # поглощаем 1 зелье
            self.rage_timer = Timer(600)  # заводим таймер на 10 сек (60 тиков в секунду)
            self.rage_timer.start()  # начинаем отсчёт

    def plus_armor(self):
        if self.armor_potion and int(self.armor_timer) == 0:  # если есть зелье неуязвимости и оно неактивно
            self.armor_potion -= 1  # поглощаем 1 зелье
            self.armor_timer = Timer(300)  # заводим таймер на 5 сек (60 тиков в секунду)
            self.armor_timer.start()  # начинаем отсчёт

    def plus_speed(self):
        if self.speed_potion and int(self.speed_timer) == 0:  # если есть зелья скорости
            self.speed_potion -= 1  # поглощаем 1 зелье
            self.speed_timer = Timer(1800)  # заводим таймер на 30 сек
            self.speed_timer.start()  # начинаем отсчёт

    def quantity_rendering(self):  # отображение всего инвентаря
        inventar_group.update()  # обновляем положение инвентаря
        inventar_group.draw(screen)  # выводим инвентарь на экран
        weapon_group.draw(screen)
        text = font_for_inventory.render(f"{inventory.hp_potions}", True, (255, 0, 0))  # кол-во зелий hp
        screen.blit(text, (inventory_slot_width * 6 + 5, HEIGHT - 10))  # выводим кол-во зелий хп около зелья хп
        text = font_for_inventory.render(f"{inventory.rage_potion}", True, (255, 0, 0))  # кол-во зелий ярости
        screen.blit(text, (inventory_slot_width * 7 + 5, HEIGHT - 10))  # выводим кол-во зелий ярости около зелья ярости
        text = font_for_inventory.render(f"{inventory.armor_potion}", True, (255, 0, 0))  # кол-во зелий неуязвимости
        screen.blit(text, (inventory_slot_width * 8 + 5, HEIGHT - 10))  # выводим кол-во зелий неуязвимости около зелья неуязвимости
        text = font_for_inventory.render(f"{inventory.speed_potion}", True, (255, 0, 0))  # кол-во зелий скорости
        screen.blit(text, (inventory_slot_width * 9 + 5, HEIGHT - 10))  # выводим кол-во зелий скорости около зелья скорости

        text = font_for_inventory.render(f"{6}", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (inventory_slot_width * 6 + 5, HEIGHT - inventory_slot_width - 10))  # выводим зеленым шрифтом цифру 1
        text = font_for_inventory.render(f"{7}", True, (0, 255, 0))  # зелье ярости активируется при нажатии на 2
        screen.blit(text, (inventory_slot_width * 7 + 5, HEIGHT - inventory_slot_width - 10))  # выводим зеленым шрифтом цифру 2
        text = font_for_inventory.render(f"{8}", True, (0, 255, 0))  # зелье неуязвимости активируется при нажатии на 3
        screen.blit(text, (inventory_slot_width * 8 + 5, HEIGHT - inventory_slot_width - 10))  # выводим зеленым шрифтом цифру 3
        text = font_for_inventory.render(f"{9}", True, (0, 255, 0))  # зелье скорости активируется при нажатии на 4
        screen.blit(text, (inventory_slot_width * 9 + 5, HEIGHT - inventory_slot_width - 10))  # выводим зеленым шрифтом цифру 4

        inventory.rage_timer.tick()  # если зелье активно, то уменьшаем время действия до 0. Иначе 0
        inventory.armor_timer.tick()  # если зелье активно, то уменьшаем время действия до 0. Иначе 0
        inventory.speed_timer.tick()

class Gameover(pygame.sprite.Sprite):
    def __init__(self):
        global is_game_over
        is_game_over = True
        super().__init__(all_sprites, game_over_group, static_sprites)
        self.image = images['game_over']
        self.rect = self.image.get_rect()
        self.state = True
        self.rect.x = -WIDTH
        self.rect.y = 0

    def update(self):
        if self.state and self.rect.x + self.rect.width < WIDTH:
            self.rect.x += 20
        else:
            self.rect.x = 0


def draw_hp(entity):
    pygame.draw.rect(screen, (255, 0, 0), (entity.rect.x, entity.rect.y - 20,
                                           int(tile_width * (entity.hp / entity.hp_max)), 15))
    pygame.draw.rect(screen, (0, 0, 0), (entity.rect.x, entity.rect.y - 20,
                                         tile_width, 15), 2)
    font = pygame.font.Font(None, 20)
    text = font.render(str(entity.hp), True, pygame.Color('white'))
    screen.blit(text, (entity.rect.x, entity.rect.y - text.get_height() - 20))


all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()
static_sprites = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
player = Player(0, 0)
weapon_lst = [CloseWeapon('sword', 'close_attack1', -50, -50, player, player_group, 2, FPS // 2,
                                         rang=4.25, name='меч'), BulletWeapon('gun', 'bullet', -50, -50,
                                                               player,
                                                               player_group,
                                                               1.5, FPS // 2,
                                                               speed=10,
                                                               rang=400, name='пистолет')]

for map_name in ['map.txt']:
    is_game_over = False
    tiles_group = pygame.sprite.Group()
    wall_group = pygame.sprite.Group()
    monster_group = pygame.sprite.Group()
    entity_group = pygame.sprite.Group()  # игроки и мобы
    attack_group = pygame.sprite.Group()
    static_sprites = pygame.sprite.Group()
    weapon_group = pygame.sprite.Group()
    inventar_group = pygame.sprite.Group()
    game_over_group = pygame.sprite.Group()
    entity_group.add(player)
    static_sprites.add(*weapon_lst)
    static_sprites.add(*weapon_lst)
    flag = 1
    running = True
    pos = 0, 0
    board, player_x, player_y = generate_level(load_level(map_name))
    player.set_at_position(player_x, player_y)
    camera = Camera()
    direction = [0, 0]
    is_clicked_r, is_clicked_l = False, False
    inventory = Inventory()
    font_for_inventory = pygame.font.Font(None, 20)
    while running:
        # изменяем ракурс камеры
        # внутри игрового цикла ещё один цикл
        # приёма и обработки сообщений
        for event in pygame.event.get():
            # при закрытии окна
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                is_clicked_l = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                is_clicked_l = False
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                is_clicked_r = True
            if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
                is_clicked_r = False

            if event.type == pygame.KEYDOWN and event.key == pygame.K_1:
                inventory.current_slot = 0
                inventory.weapon_frame.rect.x = 0
            if event.type == pygame.KEYDOWN and event.key == pygame.K_2:
                inventory.current_slot = 1
                inventory.weapon_frame.rect.x = inventory_slot_width
            if event.type == pygame.KEYDOWN and event.key == pygame.K_3:
                inventory.current_slot = 2
                inventory.weapon_frame.rect.x = inventory_slot_width * 2
            if event.type == pygame.KEYDOWN and event.key == pygame.K_4:
                inventory.current_slot = 3
                inventory.weapon_frame.rect.x = inventory_slot_width * 3
            if event.type == pygame.KEYDOWN and event.key == pygame.K_5:
                inventory.current_slot = 4
                inventory.weapon_frame.rect.x = inventory_slot_width * 4


            if event.type == pygame.MOUSEMOTION:
                pos = event.pos

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:  # нажатие на колесико мыши дает +1 зелье хп
                inventory.plus_hp_potion()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_6:  # восстанавливает до 5хп
                inventory.hp_plus()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # колесико мыши вверх дает +1 зелье урона
                if inventory.current_slot != len(inventory.items) - 1:
                    inventory.current_slot += 1
                    inventory.weapon_frame.rect.x += inventory_slot_width
                else:
                    inventory.current_slot = 0
                    inventory.weapon_frame.rect.x = 0

                inventory.plus_rage_potion()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_7:  # активирует зелье урона
                inventory.plus_damage()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # колесико мыши вниз дает +1 зелье неуязвимости
                if inventory.current_slot != 0:
                    inventory.current_slot -= 1
                    inventory.weapon_frame.rect.x -= inventory_slot_width
                else:
                    inventory.current_slot = len(inventory.items) - 1
                    inventory.weapon_frame.rect.x = inventory_slot_width * (len(inventory.items) - 1)

                inventory.plus_armor_potion()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_8:  # активирует зелье неуязвимости
                inventory.plus_armor()

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:  # колесико мыши вниз дает +1 зелье скорости
                inventory.plus_speed_potion()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_9:  # активирует зелье скорости
                inventory.plus_speed()
            if event.type == pygame.QUIT:
                if is_game_over:
                    exit(0)
                running = False
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
        if int(inventory.speed_timer) > 0 and flag:
            player.speed = 5
            player.timer_x = Timer(player.speed)
            player.timer_y = Timer(player.speed)
            flag = 0
        elif int(inventory.speed_timer) == 0 and not flag:
            player.speed = 8
            player.timer_x = Timer(player.speed)
            player.timer_y = Timer(player.speed)
            flag = 1
        if is_clicked_r:
            pass
        if is_clicked_l:
            inventory.use_weapon()
        player.make_move(*direction)
        monster_group.update()
        player_group.update()
        attack_group.update()
        weapon_group.update()
        game_over_group.update()
        camera.update(player)
        # обновляем положение всех спрайтов
        for sprite in all_sprites:
            if sprite not in static_sprites:
                camera.apply(sprite)
        screen.fill((255, 255, 255))
        tiles_group.draw(
            screen)  # спрайты клеток и сущности рисуются отдельно, чтобы спрайты клеток не наслаивались на сущностей
        entity_group.draw(screen)
        attack_group.draw(screen)
        for i in entity_group:  # всем сущностям и герою выводим полоску хп
            draw_hp(i)
        inventory.quantity_rendering()
        game_over_group.draw(screen)
        clock.tick(FPS)
        pygame.display.flip()
