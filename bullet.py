import pygame


class Bullet:
    def __init__(self, x, y):
        self.width = 6
        self.height = 12

        self.x = x - self.width // 2
        self.y = y

        self.speed = 8

    def update(self):
        self.y -= self.speed

    def is_out_of_screen(self):
        return self.y + self.height < 0

    def get_rect(self):
        return pygame.Rect(
            self.x,
            self.y,
            self.width,
            self.height
        )

    def draw(self, screen):
        pygame.draw.rect(
            screen,
            (255, 80, 80),
            self.get_rect()
        )