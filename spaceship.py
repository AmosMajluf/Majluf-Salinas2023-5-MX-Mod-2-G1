import pygame
from pygame.sprite import Sprite
import time
from game.utils.constants import SPACESHIP, SPACESHIP_SHIELD
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
        
        # Constantes del escudo
        self.DURACION_ESCUDO = 15
        self.TIEMPO_RECARGA = 5
        self.escudo_activo = False
        self.tiempo_ultimo_uso = 0

        # Sprite del escudo
        self.shield_sprite = pygame.transform.scale(SPACESHIP_SHIELD, (self.image_width, self.image_height))

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

        # Si se presiona la tecla F, activar el escudo
        if events[pygame.K_f]:
            self.activar_escudo()

        # Actualizar el estado del escudo
        self.actualizar_escudo()

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

        # Dibujar el escudo si está activo
        if self.escudo_activo:
            screen.blit(self.shield_sprite, (self.rect.x, self.rect.y))

        # Asegurarse de que la nave espacial permanezca dentro de los límites de la pantalla
        self.rect.clamp_ip(self.screen.get_rect())

        # Mostrar el tiempo restante del escudo debajo de la nave espacial
        if self.escudo_activo:
            tiempo_restante = max(0, self.DURACION_ESCUDO - (time.time() - self.tiempo_ultimo_uso))
            font = pygame.font.Font(None, 24)
            text = font.render(f"Escudo: {int(tiempo_restante)}s", True, (255, 255, 255))
            text_rect = text.get_rect()
            text_rect.centerx = self.rect.centerx
            text_rect.y = self.rect.bottom + 5
            screen.blit(text, text_rect)

    def activar_escudo(self):
        if time.time() - self.tiempo_ultimo_uso >= self.TIEMPO_RECARGA:
            self.escudo_activo = True
            self.tiempo_ultimo_uso = time.time()
            print("Escudo activado.")

    def desactivar_escudo(self):
        self.escudo_activo = False
        print("Escudo desactivado.")

    def colisionar(self):
        if self.escudo_activo:
            print("La nave ha colisionado, pero el escudo la protegió.")
        else:
            print("La nave ha colisionado y su escudo no estaba activado.")

    def recibir_disparo(self):
        if self.escudo_activo:
            print("La nave ha recibido un disparo, pero el escudo lo ha bloqueado.")
        else:
            print("La nave ha recibido un disparo y su escudo no estaba activado.")

    def actualizar_escudo(self):
        if self.escudo_activo:
            tiempo_transcurrido = time.time() - self.tiempo_ultimo_uso
            if tiempo_transcurrido >= self.DURACION_ESCUDO:
                self.desactivar_escudo()
