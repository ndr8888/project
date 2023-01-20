import pygame

clock = pygame.time.Clock()
pygame.init()
size = WIDTH, HEIGHT = 750, 750  # размеры окна
screen = pygame.display.set_mode(size)
tile_width = tile_height = 50  # размеры кнопки
inventory_slot_width = 60  # размеры слотов инвентаря
sc = 0  # счёт
keybord = {pygame.K_q: 'q', pygame.K_w: 'w', pygame.K_e: 'e', pygame.K_r: 'r', pygame.K_t: 't', pygame.K_y: 'y',
           pygame.K_u: 'u', pygame.K_i: 'i', pygame.K_o: 'o', pygame.K_p: 'p', pygame.K_a: 'a', pygame.K_s: 's',
           pygame.K_d: 'd', pygame.K_f: 'f', pygame.K_g: 'g', pygame.K_h: 'h', pygame.K_j: 'j', pygame.K_k: 'k',
           pygame.K_l: 'l', pygame.K_z: 'z', pygame.K_x: 'x', pygame.K_c: 'c', pygame.K_v: 'v', pygame.K_b: 'b',
           pygame.K_n: 'n', pygame.K_m: 'm', pygame.K_0: '0', pygame.K_1: '1', pygame.K_2: '2', pygame.K_3: '3',
           pygame.K_4: '4', pygame.K_5: '5', pygame.K_6: '6', pygame.K_7: '7', pygame.K_8: '8', pygame.K_9: '9', }
# Перевод сигнала с клавиатуры
FPS = 60  # кол-во тиков в секунду
fons = [pygame.transform.scale(pygame.image.load('data/fon1.jpg'), (WIDTH, HEIGHT)),
        pygame.transform.scale(pygame.image.load('data/fon2.jpg'), (WIDTH, HEIGHT)),
        pygame.transform.scale(pygame.image.load('data/fon3.jpg'), (WIDTH, HEIGHT))]
hp_potions = 0
rage_potions = 0
time_counter = 0
level_counters = [[0 for _ in range(i)] for i in [1, 1, 1, 3, 3]]

animation_group = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()
static_sprites = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
potion_group = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()  # всё, что не является сущностью и стеной
snares_group = pygame.sprite.Group()  # ловушки
wall_group = pygame.sprite.Group()  # стены
monster_group = pygame.sprite.Group()
spawned_monsters = pygame.sprite.Group()
guard_monster_group = pygame.sprite.Group()  # монстры, при смерти которых разрушаются стены
attack_group = pygame.sprite.Group()  # ближняя, дальняя, магическая атаки и бомбы
inventar_group = pygame.sprite.Group()  # для инвентаря в целом