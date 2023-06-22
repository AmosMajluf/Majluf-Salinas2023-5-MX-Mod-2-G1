import pygame
from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP
from game.components.bullet import Bullet

class Spaceship(Sprite):
    def __init__(self):
        super().__init__()
        self.image_width = 40
        self.image_height = 60
        self.image = SPACESHIP
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
        self.rect = self.image.get_rect()
        self.screen = pygame.display.set_mode((1100, 600))
        self.rect.x = 300
        self.rect.y = 500
        self.speed_x = 5
        self.speed_y = 5
        self.shoot_delay = 500  # Tiempo de espera entre disparos
        self.last_shot = pygame.time.get_ticks()
        self.bullets = []

    def update(self, events):
        # Actualizar la posición de la nave espacial según los eventos de teclado recibidos
        if events[pygame.K_LEFT] and events[pygame.K_UP]:
            self.rect.x -= self.speed_x
            self.rect.y -= self.speed_y
        elif events[pygame.K_LEFT] and events[pygame.K_DOWN]:
            self.rect.x -= self.speed_x
            self.rect.y += self.speed_y
        elif events[pygame.K_RIGHT] and events[pygame.K_UP]:
            self.rect.x += self.speed_x
            self.rect.y -= self.speed_y
        elif events[pygame.K_RIGHT] and events[pygame.K_DOWN]:
            self.rect.x += self.speed_x
            self.rect.y += self.speed_y
        elif events[pygame.K_LEFT]:
            self.rect.x -= self.speed_x
        elif events[pygame.K_RIGHT]:
            self.rect.x += self.speed_x
        elif events[pygame.K_UP]:
            self.rect.y -= self.speed_y
        elif events[pygame.K_DOWN]:
            self.rect.y += self.speed_y

        # Si se presiona la tecla de espacio, disparar
        if events[pygame.K_SPACE]:
            self.shoot()

    def shoot(self):
        # Obtener el tiempo actual
        current_time = pygame.time.get_ticks()
        # Verificar si ha pasado suficiente tiempo desde el último disparo
        if current_time - self.last_shot > self.shoot_delay:
            # Crear una nueva bala y configurar su posición
            bullet = Bullet()
            bullet.rect.centerx = self.rect.centerx
            bullet.rect.y = self.rect.y
            self.bullets.append(bullet)
            # Actualizar el tiempo del último disparo al tiempo actual
            self.last_shot = current_time

    def update_bullets(self):
        # Actualizar todas las balas de la nave espacial
        for bullet in self.bullets:
            bullet.update()

    def draw(self, screen):
        # Dibujar la nave espacial en la pantalla
        screen.blit(self.image, (self.rect.x, self.rect.y))
        # Asegurarse de que la nave espacial permanezca dentro de los límites de la pantalla
        self.rect.clamp_ip(self.screen.get_rect())
