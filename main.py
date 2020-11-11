import os
import random
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

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()


class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.ship_laser = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health


class Enemy(Ship):
    COLOR_MAP = {
        "red": (RED_SHIP, RED_LASER),
        "green": (GREEN_SHIP, GREEN_LASER),
        "blue": (BLUE_SHIP, BLU_LASER)
    }

    def __init__(self, x, y, color, health=100):
        super().__init__(x, y, health)
        self.ship_img, self.laser_img = self.COLOR_MAP[color]
        self.mask = pygame.mask.from_surface(self.ship_img)

    def move(self, vel):
        self.y += vel


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    player_health = 100
    pygame.init()
    main_font = pygame.font.SysFont("comicsans", 50)

    enemies = []
    wave_lenght = 0
    enemy_vel = 1
    
    
    clock = pygame.time.Clock()
    player = Player(300, 600)
    player.x = WIDTH / 2 - player.get_width() / 2

    player_vel = 5

    lost = False
    lost_count = 0

    def redraw_window():
        WIN.blit(BG, (0, 0))
        level_label = main_font.render(f"Level = {level}", True, (255, 255, 255))
        lives_label = main_font.render(f"Lives = {lives}", True, (255, 255, 255))

        WIN.blit(lives_label, (10, 10))
        WIN.blit(level_label, (WIDTH - level_label.get_width() - 10, 10))



        for enemy in enemies:
            enemy.draw(WIN)

        player.draw(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if lives <= 0 or player_health <= 0:
            lost = True
            lost_count += 1

        if lost:
            if lost_count > FPS * 5:
                run = False
            else:
                continue


        if len(enemies) == 0:
            level += 1
            wave_lenght += 5
            enemy_vel += 1
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(5,WIDTH - 5),
                              random.randrange(0, 100),
                              random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and player.x - player_vel > 0:
            player.x -= player_vel
        if key[pygame.K_RIGHT] and player.x + player_vel + player.get_width() < WIDTH:
            player.x += player_vel
        if key[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if key[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel

        for enemy in enemies:
            enemy.move(enemy_vel)

            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                lives -= 1

        redraw_window()
main()
