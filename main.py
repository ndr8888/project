# import pygame
#
# # ДО ОСНОВНОГО ЦИКЛА while running
# # inventory = Inventory()
# # font_for_inventory = pygame.font.Font(None, 20)
#
# # ВНУТРИ ЦИКЛА while вначале со всеми if
# # if event.type == pygame.MOUSEBUTTONDOWN and event.button == 2:
# #     inventory.update(1)
#
# # в самый конец цикла while перед clock.tick(FPS)
# # inventar_group.update()
# # inventar_group.draw(screen)
# # text = font_for_inventory.render(f"{inventory.hp_potions}", True, (0, 0, 0))
# # screen.blit(text, (35, 740))
#
#
# class Inventory(pygame.sprite.Sprite):
#     image = load_image('инвентарь.png')
#
#     def __init__(self):
#         super().__init__(all_sprites, inventar_group)
#         self.hp_potions = 0  # кол-во зелий, которые лечат хп
#         self.image = Inventory.image
#         self.rect = self.image.get_rect()
#         self.rect.x = 0  # положение
#         self.rect.y = 700
#
#     def update(self, plus=0, minus=0):
#         if plus:  # если получаем, то кол-во += 1
#             self.hp_potions += 1
#         if minus:  # если тратим, то кол-во -= 1
#             self.hp_potions -= 1
#         self.rect.x = 0
#         self.rect.y = 700