import pygame
from pygame.sprite import Sprite

from game.utils.constants import SCREEN_WIDTH


class Bullet(Sprite):
    def __init__(self, spaceship_center, image_object, speed = 20, direction = "vertical"):
        super().__init__()
        self.image = pygame.transform.scale(image_object, (10, 20))
        self.rect = self.image.get_rect()
        self.speed = speed
        self.rect.center = spaceship_center
        self.direction = direction

    def update(self):
        print("before self.rect.y", self.rect.y)
        if self.direction == "vertical":
            self.rect.y -= self.speed
        else:
            self.rect.x -= self.speed
        print("self.rect.y", self.rect.y)
        
        if self.rect.y < 0 or self.rect.y > SCREEN_WIDTH:
            print("kill")
            self.kill() 

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
