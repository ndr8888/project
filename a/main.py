import pygame

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


tile_images = {
    'wall': pygame.transform.scale(load_image('box.png'), (tile_width, tile_height)),
    'empty': pygame.transform.scale(load_image('grass.png'), (tile_width, tile_height)),
    'bullet': pygame.transform.scale(load_image('bomb2.png'), (30, 30)),
    'close_attack': pygame.transform.scale(load_image('close_attack.png'), (tile_width * 1.5, tile_height * 1.5))
}
player_image = pygame.transform.scale(load_image('mar.png'), (tile_width, tile_height))
monster_image = pygame.transform.scale(load_image('hero.png'), (tile_width, tile_height))
FPS = 60


start_screen()


level_running = True
pos = 0, 0
board, player, level_x, level_y = generate_level(load_level(map_name))
camera = Camera()
direction = [0, 0]
is_clicked = False
close_weapon, range_weapon = CloseWeapon(-50, -50, player, player_group, 3, FPS // 3), BulletWeapon(-50, -50, player, player_group, 3, FPS // 3, speed=10, rang=400)
inventory = Inventory()
font_for_inventory = pygame.font.Font(None, 20)
while level_running:
    # изменяем ракурс камеры
    # внутри игрового цикла ещё один цикл
    # приёма и обработки сообщений
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            level_running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            is_clicked = True
        if event.type == pygame.MOUSEBUTTONUP:
            is_clicked = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
            inventory.update(1)
        if event.type == pygame.MOUSEMOTION:
            pos = event.pos
        if event.type == pygame.KEYDOWN:
            if event.key == 1073741906:
                direction[1] -= 1
            if event.key == 1073741903:
                direction[0] += 1
            if event.key == 1073741905:
                direction[1] += 1
            if event.key == 1073741904:
                direction[0] -= 1
        if event.type == pygame.KEYUP:
            if event.key == 1073741906:
                direction[1] += 1
            if event.key == 1073741903:
                direction[0] -= 1
            if event.key == 1073741905:
                direction[1] -= 1
            if event.key == 1073741904:
                direction[0] += 1
    if is_clicked:
        close_weapon.use(*pos)
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
    inventar_group.update()
    inventar_group.draw(screen)
    text = font_for_inventory.render(f"{inventory.hp_potions}", True, (0, 0, 0))
    screen.blit(text, (35, 740))
    clock.tick(FPS)
    pygame.display.flip()
# создадим группу, содержащую все спрайты
all_sprites = pygame.sprite.Group()
