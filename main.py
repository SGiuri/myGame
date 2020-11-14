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

BLUE_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_blue_small.png'))
GREEN_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_green_small.png'))
RED_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_red_small.png'))

BLU_LASER = pygame.transform.scale(
    pygame.image.load(assets_location.join("assets", 'pixel_laser_blue.png')),
    (BLUE_SHIP.get_width(), BLUE_SHIP.get_height()))

GREEN_LASER = pygame.transform.scale(
    pygame.image.load(assets_location.join("assets", 'pixel_laser_green.png')),
    (GREEN_SHIP.get_width(), GREEN_SHIP.get_height()))
RED_LASER = pygame.transform.scale(
    pygame.image.load(assets_location.join("assets", 'pixel_laser_red.png')),
    (RED_SHIP.get_width(), RED_SHIP.get_height()))

YELLOW_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_yellow.png'))
YELLOW_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_yellow.png'))


class Ship:
    COOL_DOWN = 30

    def __init__(self, x, y, health=100):
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.ship_img, self.laser_img = None, None
        self.lasers = []
        self.cool_down_counter = 0

    def draw(self, window):
        window.blit(self.ship_img, (self.x, self.y))
        for laser in self.lasers:
            laser.draw(window)
        

    def get_width(self):
        return self.ship_img.get_width()

    def get_height(self):
        return self.ship_img.get_height()

    def cooldown(self):
        if self.cool_down_counter >= self.COOL_DOWN:
            self.cool_down_counter = 0
        elif self.cool_down_counter > 0:
            self.cool_down_counter += 1

    def shoot_laser(self):
        if self.cool_down_counter == 0:
            laser = Laser(self.x, self.y, self.laser_img)
            self.lasers.append(laser)
            self.cool_down_counter = 1

    def move_lasers(self, vel, obj):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            elif laser.collision(obj):
                obj.health -= 10
                self.lasers.remove(laser)

    def health_bar(self, window):
        #pygame.draw.rect(screen, [red, blue, green], [left, top, width, height], filled)
        pygame.draw.rect(window,(255,0,0), [self.x, self.y +4 + self.get_height(), self.get_width(), 20])
        pygame.draw.rect(window, (0, 255, 0), [self.x + 2, self.y + 6 + self.get_height(),
                                               self.health/self.max_health * (self.get_width()-4), 16])


class Player(Ship):

    def __init__(self, x, y, health=100):
        super().__init__(x, y, health)
        self.ship_img = YELLOW_SHIP
        self.laser_img = YELLOW_LASER
        self.mask = pygame.mask.from_surface(self.ship_img)
        self.max_health = health

    def move_lasers(self, vel, objs):
        self.cooldown()
        for laser in self.lasers:
            laser.move(vel)
            if laser.off_screen(HEIGHT):
                self.lasers.remove(laser)
            else:
                for obj in objs:
                    if laser.collision(obj):
                        objs.remove(obj)
                        self.lasers.remove(laser)


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

    def shoot(self):
        if random.randrange(0, 120) == 1:
            self.shoot_laser()




class Laser():
    def __init__(self, x, y, img, ship_width=0):
        self.x = x - ship_width / 2
        self.y = y
        self.img = img
        self.mask = pygame.mask.from_surface(self.img)

    def move(self, vel):
        self.y += vel

    def draw(self, window):
        window.blit(self.img, (self.x, self.y))

    def off_screen(self, height):
        return not (self.y < height and self.y > 0)

    def collision(self, obj):
        return collide(self, obj)


def collide(obj1, obj2):
    offset_x = int(obj2.x - obj1.x)
    offset_y = int(obj2.y - obj1.y)
    return obj1.mask.overlap(obj2.mask, (offset_x, offset_y)) != None


def main():
    run = True
    FPS = 60
    level = 1
    lives = 5
    player_health = 100
    laser_vel = 4
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
        player.health_bar(WIN)

        pygame.display.update()

    while run:
        clock.tick(FPS)

        if lives <= 0:
            lost = True
            lost_count += 1

        if player.health <= 0:
            lives -= 1
            player.health = player.max_health

        if lost:
            if lost_count > FPS * 3:
                run = False
            else:
                continue

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        if len(enemies) == 0:
            level += 1
            wave_lenght += 1
            enemy_vel += 0
            for i in range(wave_lenght):
                enemy = Enemy(random.randrange(0, WIDTH - 40),
                              random.randrange(-600, -10),
                              random.choice(["red", "green", "blue"]))
                enemies.append(enemy)

        key = pygame.key.get_pressed()

        if key[pygame.K_LEFT] and player.x - player_vel + player.get_width()//2  > 0:
            player.x -= player_vel
        if key[pygame.K_RIGHT] and player.x + player_vel + player.get_width()//2 < WIDTH:
            player.x += player_vel
        if key[pygame.K_UP] and player.y - player_vel > 0:
            player.y -= player_vel
        if key[pygame.K_DOWN] and player.y + player_vel + player.get_height() < HEIGHT:
            player.y += player_vel
        if key[pygame.K_SPACE]:
            player.shoot_laser()

        for enemy in enemies:
            enemy.move(enemy_vel)
            enemy.move_lasers(laser_vel, player)
            enemy.shoot()
            if enemy.y > HEIGHT:
                enemies.remove(enemy)
                lives -= 1

            if collide(enemy, player):
                player.health -= 10
                enemies.remove(enemy)

        enemy.move_lasers(laser_vel, player)

        player.move_lasers(-laser_vel, enemies)

        redraw_window()


main()
