import pygame

from constants import PLAYFIELD_WIDTH, SCREEN_HEIGHT


class Player:
    def __init__(self):
        self.width = 40
        self.height = 16

        self.x = PLAYFIELD_WIDTH // 2 - self.width // 2
        self.y = SCREEN_HEIGHT - self.height - 20

        self.speed = 6

    def handle_input(self):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_LEFT]:
            self.x -= self.speed

        if keys[pygame.K_RIGHT]:
            self.x += self.speed

        self.x = max(0, self.x)
        self.x = min(
            PLAYFIELD_WIDTH - self.width,
            self.x
        )

    def get_shot_position(self):
        return (
            self.x + self.width // 2,
            self.y
        )

    def draw(self, screen):
        # Основание пушки
        pygame.draw.rect(
            screen,
            (220, 220, 220),
            (
                self.x,
                self.y,
                self.width,
                self.height
            )
        )

        # Ствол пушки
        pygame.draw.rect(
            screen,
            (150, 150, 150),
            (
                self.x + self.width // 2 - 4,
                self.y - 16,
                8,
                16
            )
        )