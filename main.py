import os
import pygame
import time
import random

assets_location = os.path

BG = pygame.image.load(assets_location.join("assets", 'background-black.png'))

BLU_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_blue.png'))
GREEN_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_green.png'))
RED_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_red.png'))
BLUE_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_blue_small.png'))
GREEN_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_green_small.png'))
RED_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_red_small.png'))

YELLOW_LASER = pygame.image.load(assets_location.join("assets", 'pixel_laser_yellow.png'))
YELLOW_SHIP = pygame.image.load(assets_location.join("assets", 'pixel_ship_yellow.png'))
