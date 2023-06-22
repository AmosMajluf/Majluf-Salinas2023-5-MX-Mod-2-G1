import pygame
import random
from game.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS
from game.components.spaceship import Spaceship
from game.components.enemy import Enemy
from game.components.bullet import Bullet

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 10
        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.spaceship = Spaceship()
        self.enemies = []
        self.bullets = []
        self.score = 0
        self.max_score = 0
        self.enemies_destroyed = 0
        self.gameover = False

    def run(self):
        """
        Ejecuta el juego principal.
        """
        self.playing = True
        while self.playing:
            self.handle_events()
            self.update()
            self.draw()
        pygame.quit()

    def handle_events(self):
        """
        Maneja los eventos del juego, como la salida y la entrada del teclado.
        """
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.spaceship.shoot()
                elif event.key == pygame.K_r and self.gameover:
                    self.restart_game()

    def update(self):
        """
        Actualiza la lógica del juego en cada iteración del bucle principal.
        """
        events = pygame.key.get_pressed()
        self.spaceship.update(events)
        self.spaceship.update_bullets()

        if not self.gameover:
            self.handle_collisions()
            self.update_enemies()

    def handle_collisions(self):
        """
        Maneja las colisiones entre la nave espacial, los enemigos y las balas.
        """
        for enemy in self.enemies:
            enemy.update()

            if self.spaceship.rect.colliderect(enemy.rect):
                self.game_over()

            for bullet in self.spaceship.bullets:
                if bullet.rect.colliderect(enemy.rect):
                    self.enemies.remove(enemy)
                    self.spaceship.bullets.remove(bullet)
                    self.score += 15
                    self.enemies_destroyed += 1
                    if self.score > self.max_score:
                        self.max_score = self.score
                    break

            for enemy_bullet in enemy.bullets:
                if enemy_bullet.rect.colliderect(self.spaceship.rect):
                    self.game_over()
                    break

    def update_enemies(self):
        """
        Actualiza la posición y el comportamiento de los enemigos.
        """
        for enemy in self.enemies:
            enemy.update()

        if len(self.enemies) == 0:
            self.regenerate_enemies()

    def regenerate_enemies(self):
        """
        Genera una nueva oleada de enemigos.
        """
        for _ in range(10):
            enemy = Enemy()
            enemy.rect.x = random.randint(0, SCREEN_WIDTH - enemy.rect.width)
            enemy.rect.y = random.randint(-enemy.rect.height, -10)
            self.enemies.append(enemy)

    def draw(self):
        """
        Dibuja los elementos visuales en la pantalla.
        """
        self.clock.tick(FPS)
        self.screen.fill((0, 0, 0))  # Fondo negro

        if self.gameover:
            self.draw_gameover()
        else:
            self.draw_gameplay()

        pygame.display.update()

    def draw_gameplay(self):
        """
        Dibuja los elementos del juego durante el juego.
        """
        self.draw_background()
        self.spaceship.draw(self.screen)
        for enemy in self.enemies:
            enemy.draw(self.screen)

        for bullet in self.spaceship.bullets:
            bullet.draw(self.screen)

        self.draw_score()

    def draw_background(self):
        """
        Dibuja el fondo del juego.
        """
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT))
        image_height = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_height))
            self.y_pos_bg = 0
        self.y_pos_bg += self.game_speed

    def draw_score(self):
        """
        Dibuja la puntuación en la pantalla.
        """
        font = pygame.font.Font(pygame.font.get_default_font(), 18)
        score_text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        max_score_text = font.render(f"Max Score: {self.max_score}", True, (255, 255, 255))
        enemies_destroyed_text = font.render(f"Enemies Destroyed: {self.enemies_destroyed}", True, (255, 255, 255))
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(max_score_text, (10, 30))
        self.screen.blit(enemies_destroyed_text, (10, 50))

    def draw_gameover(self):
        """
        Dibuja la pantalla de Game Over.
        """
        font = pygame.font.Font(pygame.font.get_default_font(), 36)
        gameover_text = font.render("Game Over", True, (255, 0, 0))
        text_rect = gameover_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        self.screen.blit(gameover_text, text_rect)

        restart_text = font.render("Presiona 'R' para reiniciar", True, (255, 255, 255))
        restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))
        self.screen.blit(restart_text, restart_rect)

    def game_over(self):
        """
        Muestra la pantalla de Game Over y establece el estado del juego en Game Over.
        """
        self.gameover = True

    def restart_game(self):
        """
        Reinicia el juego y restablece todas las variables.
        """
        self.score = 0
        self.enemies_destroyed = 0
        self.spaceship = Spaceship()  # Reiniciar la nave espacial
        self.enemies.clear()
        self.regenerate_enemies()
        self.gameover = False
