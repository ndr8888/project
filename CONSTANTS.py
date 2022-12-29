import pygame

size = WIDTH, HEIGHT = 750, 750
tile_width = tile_height = 50
inventory_slot_width = 60
FPS = 60

all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()
static_sprites = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
direction = [0, 0]

is_portal_activated = False
is_game_over = False
tiles_group = pygame.sprite.Group()
wall_group = pygame.sprite.Group()
monster_group = pygame.sprite.Group()
guard_monster_group = pygame.sprite.Group()
entity_group = pygame.sprite.Group()  # игроки и мобы
attack_group = pygame.sprite.Group()
static_sprites = pygame.sprite.Group()
weapon_group = pygame.sprite.Group()
inventar_group = pygame.sprite.Group()
game_over_group = pygame.sprite.Group()