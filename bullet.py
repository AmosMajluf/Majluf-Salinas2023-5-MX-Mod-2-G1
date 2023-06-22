import pygame
from game.utils.constants import BULLET

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_width = 30
        self.image_height = 30
        self.image = BULLET
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
        self.rect = self.image.get_rect()
        self.rect.y = self.rect.top
        self.rect.x = self.rect.centerx
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

    def draw(self, screen):
        screen.blit(self.image, self.rect)
