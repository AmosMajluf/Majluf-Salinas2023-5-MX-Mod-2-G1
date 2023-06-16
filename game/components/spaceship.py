import pygame
from pygame.sprite import Sprite

from game.utils.constants import SPACESHIP, SCREEN_WIDTH, BULLET
from game.components.bullet import Bullet


class SpaceShip(Sprite):
    
    def __init__(self):
        self.image_size = (40, 60)
        self.image = pygame.transform.scale(SPACESHIP, self.image_size)
        self.image_rect = self.image.get_rect()
        self.image_rect.x = 300 # self.image_size[0]
        self.image_rect.y = 500 # self.image_size[1]

        self.speed_x = 5  
        self.bullet = None

    def update(self):
        self.image_rect.x += self.speed_x
        if self.image_rect.right > SCREEN_WIDTH:
            self.image_rect.left = 0
        elif self.image_rect.left < 0:
            self.image_rect.right = SCREEN_WIDTH

        if self.bullet is not None:
            self.bullet.update()

    def move_left(self):
        print("move_left", self.speed_x)
        self.speed_x = -5

    def move_right(self):
        self.speed_x = 5
        print("move_right", self.speed_x)

    def move_straight(self):
        self.speed_x = 0

    def shoot(self):
        self.bullet = Bullet(self.image_rect.center, BULLET)


    def draw(self, screen):
        screen.blit(self.image, self.image_rect)

        if self.bullet is not None:
            self.bullet.draw(screen) 
