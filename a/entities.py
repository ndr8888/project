from main import all_sprites, player_group, player_image, tile_width, tile_height, entity_group, FPS, board, player, monster_group, monster_image
from abstract_classes import Timer, Empty, Blocked
import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.speed = 8  # должен быть кратен tile_width
        self.timer_x = Timer(self.speed)
        self.timer_y = Timer(self.speed)
        super().__init__(player_group, all_sprites, entity_group)
        self.hp = 10
        self.hp_max = 10
        self.diagonal = False  # переменная, нужная для диагонального хода игроком
        self.pos_x, self.pos_y = pos_x, pos_y  # координаты игрока в клетках
        self.image = player_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
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
            self.rect.x += self.x_move * (tile_width / self.timer_x.time_max)
            if int(self.timer_x) == 0:
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_x += self.x_move
                board[self.pos_x][self.pos_y] = player
                self.x_move = 0
        if self.y_move != 0:
            self.timer_y.tick()
            self.rect.y += self.y_move * (tile_width / self.timer_y.time_max)
            if int(self.timer_y) == 0:
                board[self.pos_x][self.pos_y] = Empty()
                self.pos_y += self.y_move
                board[self.pos_x][self.pos_y] = player
                self.y_move = 0

    def damage(self, n):
        self.hp -= n
        if self.hp <= 0:
            self.kill()


class Monster(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        self.x_move, self.y_move = 0, 0
        self.speed = 10
        self.timer_x = Timer(self.speed)
        self.timer_y = Timer(self.speed)
        self.hp = 10
        self.hp_max = 10
        self.pos_x, self.pos_y = pos_x, pos_y
        super().__init__(monster_group, all_sprites, entity_group)
        self.image = monster_image
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)
        self.rang_min = 3
        self.rang_max = 7
        self.next_cell = 0, 0
        self.weapon = BulletWeapon(-50, -50, self, monster_group, 1, FPS, speed=10, rang=400)

    def type(self):
        return 'monster'

    def update(self):
        if abs(self.pos_x - player.pos_x) <= self.rang_max and abs(self.pos_y - player.pos_y) <= self.rang_max:
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
        self.hp -= n
        if self.hp <= 0:
            board[self.next_cell[0]][self.next_cell[1]] = Empty()
            board[self.pos_x][self.pos_y] = Empty()
            self.kill()