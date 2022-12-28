from functions import load_image, inventar_group, static_sprites, weapon_group, tile_width
from abstract_classes import Timer
from attack_classes import *

class Inventory(pygame.sprite.Sprite):
    image = load_image('инвентарь.png')

    def __init__(self):
        super().__init__(all_sprites, inventar_group)
        self.hp_potions = 0  # кол-во зелий, которые лечат хп
        self.image = Inventory.image
        self.rect = self.image.get_rect()
        self.rect.x = 0  # положение
        self.rect.y = 700

    def update(self, plus=0, minus=0):
        if plus:  # если получаем, то кол-во += 1
            self.hp_potions += 1
        if minus:  # если тратим, то кол-во -= 1
            self.hp_potions -= 1
        if self.hp_potions == 0:  # если 0 штук, то серое неактивное
            self.image = load_image('инвентарь2.png')
        else:  # если зелья есть, то картинка зелья
            self.image = load_image('инвентарь.png')
        self.rect.x = 0
        self.rect.y = 700


class Weapon(pygame.sprite.Sprite):
    def __init__(self, x, y, owner, fraction, damage, cooldown):
        super().__init__(all_sprites, static_sprites, weapon_group)
        self.description = ''''''
        self.owner, self.fraction, self.damage = owner, fraction, damage
        self.timer = Timer(cooldown)
        self.image = tile_images['bullet']
        self.rect = self.image.get_rect().move(
            x, y)

    def update(self):
        self.timer.tick()

    # def use(self):
    #     if int(self.timer) == 0:
    #         self.timer.start()


class BulletWeapon(Weapon):
    def __init__(self, *args, speed=10, rang=400):
        super().__init__(*args)
        self.speed, self.rang = speed, rang
        self.image = tile_images['bullet']

    def use(self, x, y):
        if int(self.timer) == 0:
            self.timer.start()
            Bullet(self.owner.rect.x, self.owner.rect.y, x, y, self.fraction, self.damage, self.speed, self.rang)


class CloseWeapon(Weapon):
    def __init__(self, *args):
        super().__init__(*args)
        self.image = tile_images['close_attack']

    def use(self, x, y):
        if int(self.timer) == 0:
            self.timer.start()
            CloseAttack(self.owner.rect.x + tile_width * 0.5, self.owner.rect.y + tile_width * 0.5, 45, self.fraction, self.damage)