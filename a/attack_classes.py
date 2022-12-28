from main import all_sprites, attack_group, tile_images, wall_group, entity_group, FPS
from abstract_classes import Timer
import pygame
import math

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x1, y1, x2, y2, fraction, damage, speed, rang):
        super().__init__(all_sprites, attack_group)
        self.image = tile_images['bullet']
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
                self.kill()
        for i in wall_group:  # проверка на столкновение со стенами
            if pygame.sprite.collide_mask(self, i):
                self.kill()
        self.live_timer.tick(self.vel)
        if int(self.live_timer) == 0:
            self.kill()


class CloseAttack(pygame.sprite.Sprite):
    def __init__(self, x, y, rotation, fraction, damage):
        super().__init__(all_sprites, attack_group)
        self.image = tile_images['close_attack']
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect().move(
            x, y)
        self.damaged_lst = list()
        self.mask = pygame.mask.from_surface(self.image)
        self.timer = Timer(FPS // 4)
        self.timer.start()
        self.fraction = fraction
        self.dmg = damage

    def update(self):
        for i in entity_group:  # проверка на столкновение с монстрами
            if pygame.sprite.collide_mask(self, i) and i not in self.fraction and i not in self.damaged_lst:
                i.damage(self.dmg)
                self.damaged_lst.append(i)
        self.timer.tick()
        if int(self.timer) == 0:
            self.kill()