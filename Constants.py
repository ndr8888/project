import pygame

clock = pygame.time.Clock()
pygame.init()
size = WIDTH, HEIGHT = 750, 750  # размеры окна
screen = pygame.display.set_mode(size)
tile_width = tile_height = 50  # размеры кнопокa
inventory_slot_width = 60  # размеры слотов инвентаря
FPS = 60  # кол-во тиков в секунду
fons = [pygame.transform.scale(pygame.image.load('data/fon1.jpg'), (WIDTH, HEIGHT)),
        pygame.transform.scale(pygame.image.load('data/fon2.jpg'), (WIDTH, HEIGHT)),
        pygame.transform.scale(pygame.image.load('data/fon3.jpg'), (WIDTH, HEIGHT))]
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