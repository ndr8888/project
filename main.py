import pygame
import os
import sys
import random
import math

map_name = 'map.txt'
clock = pygame.time.Clock()
pygame.init()
size = WIDTH, HEIGHT = 750, 750
screen = pygame.display.set_mode(size)
tile_width = tile_height = 40
all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()  # игроки и мобы
attack_group = pygame.sprite.Group()
static_sprites = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
inventar_group = pygame.sprite.Group()


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
    'bullet': load_image('bomb2.png'),
    'close_attack': load_image('attack.png'),
    'close_attack1': load_image('attack1.png'),
    'inventory_slot': load_image('inventory_slot.png'),
    'empty_image': load_image('empty_image.png'),
    'monster': pygame.transform.scale(load_image('enemy.png'), (tile_width, tile_height)),
    'monster1': pygame.transform.scale(load_image('enemy1.png'), (tile_width, tile_height)),
    'player': pygame.transform.scale(load_image('mar.png'), (tile_width, tile_height))
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
        self.x, self.y = tile_width * pos_x, tile_height * pos_y
        self.mask = pygame.mask.from_surface(self.image)
        self.x_move, self.y_move = 0, 0

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
        self.hp -= n
        if self.hp <= 0:
            self.kill()


class CloseMonster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.weapon = CloseWeapon('empty_image', 'close_attack1', -50, -50, self, monster_group, 1, FPS // 2,
                                  rang=2.5)  #изменяемый
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
        if int(inventory.rage_timer) != 0:  # если действует зелье увеличения урона
            print(1)
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
        self.description = ''''''
        self.owner, self.fraction, self.damage = owner, fraction, damage
        self.timer = Timer(cooldown)
        self.image = images[icon]
        self.attack_picture = attack_picture
        self.rect = self.image.get_rect().move(
            x, y)

    def update(self):
        self.timer.tick()

    # def use(self):
    #     if int(self.timer) == 0:
    #         self.timer.start()


class BulletWeapon(Weapon):
    def __init__(self, *args, speed=10, rang=400, bullet_size=(30, 30), go_through_entities=False):
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
    def __init__(self, *args, rang=2.15):
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
    new_player, x, y = None, None, None
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
                new_player = Player(x, y)
                table[x].append(new_player)
            elif level[y][x] == '1':  # монстер обозначается цифрой 1, при добавлнии новых монстров будет 2, 3 и тд
                BackgroundTile(x, y)
                table[x].append(CloseMonster(x, y))
            elif level[y][x] == '2':  # монстер обозначается цифрой 1, при добавлнии новых монстров будет 2, 3 и тд
                BackgroundTile(x, y)
                table[x].append(RangedMonster(x, y))
    # вернем игрока, а также размер поля в клетках
    return Board(table), new_player, x, y


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


class Inventory(pygame.sprite.Sprite):   # класс иневентаря. В игре он снизу слева
    image = load_image('инвентарь.png')

    def __init__(self):
        super().__init__(all_sprites, inventar_group)  # добавляем в группы спрайтов

        self.hp_potions = 0  # кол-во зелий, которые лечат 5хп
        self.rage_potion = 0  # кол-во зелий, которые увеличивают урон в 2 раза на 10 сек
        self.armor_potion = 0  # кол-во зелий, которые уменьшают получаемый урон до 0 на 5 сек

        self.armor_timer = Timer(0)  # таймер для зелий неуязвимости
        self.rage_timer = Timer(0)  # таймер для зелий увелмчения урона

        self.image = Inventory.image
        self.rect = self.image.get_rect()
        self.rect.x = 0  # положение
        self.rect.y = 700

    def update(self):
        self.rect.x = 0  # чтобы передвигался вместе с камерой
        self.rect.y = 700

    def plus_hp_potion(self):  # +1 зелье, которое лечит 5хп
        self.hp_potions += 1

    def plus_rage_potion(self):  # +1 зелье, которое увеличивает урон в 2 раза на 10 сек
        self.rage_potion += 1

    def plus_armor_potion(self):  # +1 зелье, которое уменьшает получаемый урон до 0 на 5 сек
        self.armor_potion += 1

    def hp_plus(self):
        if self.hp_potions:  # если есть зелье хп
            if player.hp + 5 <= player.hp_max:  # добавляем 5хп, если не привысим максимальное кол-во хп
                player.hp += 5  # +5 хп
                self.hp_potions -= 1  # -1 зелье, которое лечит 5 хп
            elif player.hp < player.hp_max:  # если +5 преdвысит максимальное кол-во хп, то добавляем до максимального
                player.hp = player.hp_max  # теперь хп = максимальные хп
                self.hp_potions -= 1  # -1 зелье, которое лечит 5 хп

    def plus_damage(self):
        if self.rage_potion and int(self.rage_timer) == 0:  # если есть зелье ярости и оно неактивно
            print(3)
            self.rage_potion -= 1  # поглощаем 1 зелье
            self.rage_timer = Timer(FPS * 10)  # заводим таймер на 10 сек (60 тиков в секунду)
            self.rage_timer.start()  # начинаем отсчёт

    def plus_armor(self):
        if self.armor_potion and int(self.armor_timer) == 0:  # если есть зелье неуязвимости и оно неактивно
            self.armor_potion -= 1  # поглощаем 1 зелье
            self.armor_timer = Timer(FPS * 5)  # заводим таймер на 5 сек (60 тиков в секунду)
            self.armor_timer.start()  # начинаем отсчёт

    def quantity_rendering(self):  # отображение всего инвентаря
        inventar_group.update()  # обновляем положение инвентаря
        inventar_group.draw(screen)  # выводим инвентарь на экран
        text = font_for_inventory.render(f"{inventory.hp_potions}", True, (255, 0, 0))  # кол-во зелий hp
        screen.blit(text, (35, 740))  # выводим кол-во зелий хп около зелья хп
        text = font_for_inventory.render(f"{inventory.rage_potion}", True, (255, 0, 0))  # кол-во зелий ярости
        screen.blit(text, (105, 740))  # выводим кол-во зелий ярости около зелья ярости
        text = font_for_inventory.render(f"{inventory.armor_potion}", True, (255, 0, 0))  # кол-во зелий неуязвимости
        screen.blit(text, (155, 740))  # выводим кол-во зелий неуязвимости около зелья неуязвимости

        text = font_for_inventory.render(f"{1}", True, (0, 255, 0))  # зелье хп активируется при нажатии на 1
        screen.blit(text, (10, 700))  # выводим зеленым шрифтом цифру 1
        text = font_for_inventory.render(f"{2}", True, (0, 255, 0))  # зелье ярости активируется при нажатии на 2
        screen.blit(text, (80, 700))  # выводим зеленым шрифтом цифру 2
        text = font_for_inventory.render(f"{3}", True, (0, 255, 0))  # зелье неуязвимости активируется при нажатии на 3
        screen.blit(text, (130, 700))  # выводим зеленым шрифтом цифру 3

        inventory.rage_timer.tick()  # если зелье активно, то уменьшаем время действия до 0. Иначе 0
        inventory.armor_timer.tick()  # если зелье активно, то уменьшаем время действия до 0. Иначе 0


def draw_hp(entity):
    pygame.draw.rect(screen, (255, 0, 0), (entity.rect.x, entity.rect.y - 20,
                                           int(tile_width * (entity.hp / entity.hp_max)), 15))
    pygame.draw.rect(screen, (0, 0, 0), (entity.rect.x, entity.rect.y - 20,
                                         tile_width, 15), 2)
    font = pygame.font.Font(None, 20)
    text = font.render(str(entity.hp), True, pygame.Color('white'))
    screen.blit(text, (entity.rect.x, entity.rect.y - text.get_height() - 20))


running = True
pos = 0, 0
board, player, level_x, level_y = generate_level(load_level(map_name))
camera = Camera()
direction = [0, 0]
is_clicked_r, is_clicked_l = False, False
close_weapon, range_weapon = CloseWeapon('close_attack1', 'close_attack1', -50, -50, player, player_group, 2, FPS // 2,
                                         rang=4), BulletWeapon('bullet', 'bullet', -50, -50,
                                                               player,
                                                               player_group,
                                                               1.5, FPS // 3,
                                                               speed=10,
                                                               rang=400)
inventory = Inventory()
font_for_inventory = pygame.font.Font(None, 20)
player.speed = 5
while running:
    # изменяем ракурс камеры
    # внутри игрового цикла ещё один цикл
    # приёма и обработки сообщений
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            is_clicked_l = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            is_clicked_l = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            is_clicked_r = True
        if event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            is_clicked_r = False

        if event.type == pygame.MOUSEMOTION:
            pos = event.pos

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:  # нажатие на колесико мыши дает +1 зелье хп
            inventory.plus_hp_potion()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_1:  # восстанавливает до 5хп
            inventory.hp_plus()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 4:  # колесико мыши вверх дает +1 зелье урона
            inventory.plus_rage_potion()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_2:  # активирует зелье урона
            inventory.plus_damage()

        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 5:  # колесико мыши вниз дает +1 зелье неуязвимости
            inventory.plus_armor_potion()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_3:  # активирует зелье неуязвимости
            inventory.plus_armor()

        if event.type == pygame.KEYDOWN:  # назначаем движение
            if event.key == pygame.K_w or event.key == pygame.K_UP:  # вверх
                direction[1] -= 1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:  # вправо
                direction[0] += 1
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:  # вниз
                direction[1] += 1
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:  # влево
                direction[0] -= 1
        if event.type == pygame.KEYUP:  # убираем движение по направлениям, если клавишу отпустили
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                direction[1] += 1
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                direction[0] -= 1
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                direction[1] -= 1
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                direction[0] += 1
    if is_clicked_r:
        close_weapon.use(*pos)
    if is_clicked_l:
        range_weapon.use(*pos)
    player.make_move(*direction)
    monster_group.update()
    player_group.update()
    attack_group.update()
    weapon_group.update()
    camera.update(player)
    # обновляем положение всех спрайтов
    for sprite in all_sprites:
        camera.apply(sprite)
    screen.fill((255, 255, 255))
    tiles_group.draw(
        screen)  # спрайты клеток и сущности рисуются отдельно, чтобы спрайты клеток не наслаивались на сущностей
    entity_group.draw(screen)
    attack_group.draw(screen)
    for i in entity_group:
        draw_hp(i)
    inventar_group.update()  # обновляем положение инвентаря
    inventar_group.draw(screen)  # выводим его на экран
    text = font_for_inventory.render(f"{inventory.hp_potions}", True, (255, 0, 0))  # кол-во зелий
    screen.blit(text, (35, 740))  # выводим кол-во зелий около зелья
    clock.tick(FPS)
    pygame.display.flip()
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
