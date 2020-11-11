import os

import pygame

WIDTH, HEIGHT = 750, 750
SCREEN_DIMENSION = (WIDTH, HEIGHT)

WIN = pygame.display.set_mode(SCREEN_DIMENSION)

assets_location = os.path

BG = pygame.transform.scale(
    pygame.image.load(
        assets_location.join("assets", 'background-black.png')), (WIDTH, HEIGHT))

BLU_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_green.png'))
RED_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_red.png'))
BLUE_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_blue_small.png'))
GREEN_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_green_small.png'))
RED_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_red_small.png'))

YELLOW_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_yellow.png'))
YELLOW_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_yellow.png'))


def main():
    run = True
    FPS = 60
    level = 1000
    lives = 5
    pygame.init()
    main_font = pygame.font.SysFont("comicsans", 50)

    clock = pygame.time.Clock()


    def redraw_window():
        WIN.blit(BG, (0,0))
        level_label = main_font.render(f"Level = {level}", 1, (255,255,255))
        lives_label = main_font.render(f"Lives = {lives}", 1, (255, 255, 255))

        WIN.blit(lives_label, (10,10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10,10))
        pygame.display.update()


    while run:
        clock.tick(FPS)
        redraw_window()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False


main()
