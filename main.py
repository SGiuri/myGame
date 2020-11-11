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


class Ship:
    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.ship_img, self.laser_img = None, None
        self.laser = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))

class Player(Ship):
    def __init__(self,x,y,health=100):
        super().__init__(x,y,health)
        self.ship_img = YELLOW_SHIP
        self.ship_laser = YELLOW_LASER



def main():
    run = True
    FPS = 60
    level = 1000
    lives = 5
    pygame.init()
    main_font = pygame.font.SysFont("comicsans", 50)

    clock = pygame.time.Clock()

    def redraw_window():
        WIN.blit(BG, (0, 0))
        level_label = main_font.render(f"Level = {level}", True, (255, 255, 255))
        lives_label = main_font.render(f"Lives = {lives}", True, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))

        player = Player(100, 100)
        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)
        redraw_window()



        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False





main()
