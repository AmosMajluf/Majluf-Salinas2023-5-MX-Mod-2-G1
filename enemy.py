import pygame
import random
from game.utils.constants import ENEMY_1, SCREEN_WIDTH, SCREEN_HEIGHT
from game.components.bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image_width = 50
        self.image_height = 50
        self.image = ENEMY_1
        self.image = pygame.transform.scale(self.image, (self.image_width, self.image_height))
        self.rect = self.image.get_rect()
        self.rect.y = random.randint(-100, -40)  # Posición inicial en el eje Y (arriba de la pantalla)
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.image_width)  # Posición inicial en el eje X
        self.speedy = random.randint(1, 3)  # Velocidad vertical
        self.shoot_delay = 1500  # Tiempo de espera entre disparos
        self.last_shot = pygame.time.get_ticks()  # Tiempo del último disparo
        self.bullets = pygame.sprite.Group()  # Grupo de balas para gestionar múltiples balas

    def update(self):
        """
        Actualiza la posición del enemigo y dispara balas.
        """
        self.rect.y += self.speedy  # Mueve al enemigo hacia abajo en el eje Y

        # Comprueba si el enemigo ha salido de la pantalla y lo reinicia en una nueva posición
        if self.rect.top > SCREEN_HEIGHT or self.rect.right < 0 or self.rect.left > SCREEN_WIDTH:
            self.reset()

        self.shoot()  # Dispara balas

        self.bullets.update()  # Actualiza todas las balas

    def reset(self):
        """
        Reinicia la posición del enemigo.
        """
        self.rect.y = random.randint(-100, -40)  # Posición inicial en el eje Y
        self.rect.x = random.randint(0, SCREEN_WIDTH - self.image_width)  # Posición inicial en el eje X
        self.speedy = random.randint(1, 3)  # Velocidad vertical

    def shoot(self):
        """
        Dispara un proyectil hacia abajo.
        """
        current_time = pygame.time.get_ticks()  # Tiempo actual del juego
        if current_time - self.last_shot > self.shoot_delay:
            bullet = Bullet()  # Crea una nueva bala
            bullet.rect.centerx = self.rect.centerx  # Establece la posición horizontal de la bala al centro del enemigo
            bullet.rect.top = self.rect.bottom  # Establece la posición vertical de la bala en la parte inferior del enemigo
            bullet.speedy = random.randint(1, 3)  # Establece la velocidad vertical de la bala de forma aleatoria
            self.bullets.add(bullet)  # Añade la bala al grupo de balas
            self.last_shot = current_time  # Actualiza el tiempo del último disparo

    def draw(self, screen):
        """
        Dibuja el enemigo y las balas en la pantalla.
        """
        screen.blit(self.image, self.rect)  # Dibuja al enemigo en la pantalla
        self.bullets.draw(screen)  # Dibuja todas las balas en la pantalla
