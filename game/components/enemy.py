import pygame
import random
from pygame.sprite import Sprite

from game.utils.constants import ENEMY_1, SCREEN_HEIGHT, SCREEN_WIDTH, BULLET_ENEMY
from game.components.bullet import Bullet

class Enemy(Sprite):
    def __init__(self, y, width, height, speed):
        self.image = pygame.transform.scale(ENEMY_1, (width, height))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH/2 - width/2
        self.rect.y = y
        self.width = width
        self.height = height
        self.speed_y = speed
        self.bullet = None # no se ha disparado nada

    def update(self):
        self.move_vertical()
        self.shoot()
        if self.bullet is not None:
            self.bullet.update()

    def move_vertical(self):
        self.rect.y += self.speed_y
        if self.rect.y > SCREEN_HEIGHT:
            self.rect.x = random.randint(0, SCREEN_WIDTH - self.width)
            self.rect.y = random.randint(-300, -100)
    
    def shoot(self):
        self.bullet = Bullet(self.rect.center, BULLET_ENEMY, -30)

    def draw(self, screen):
        screen.blit(self.image, self.rect)
        if self.bullet is not None:
            self.bullet.draw(screen) 
