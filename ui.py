import pygame

from constants import SCREEN_WIDTH, SCREEN_HEIGHT, PLAYFIELD_WIDTH


class GameUI:
    def __init__(self):
        self.font_title = pygame.font.Font(None, 42)
        self.font_large = pygame.font.Font(None, 36)
        self.font_medium = pygame.font.Font(None, 28)
        self.font_small = pygame.font.Font(None, 24)

        self.panel_x = PLAYFIELD_WIDTH + 30
        self.panel_width = SCREEN_WIDTH - self.panel_x - 30

    def draw_panel(self, screen):
        panel_rect = pygame.Rect(
            PLAYFIELD_WIDTH + 10,
            10,
            SCREEN_WIDTH - PLAYFIELD_WIDTH - 20,
            SCREEN_HEIGHT - 20
        )

        pygame.draw.rect(
            screen,
            (35, 35, 50),
            panel_rect,
            border_radius=12
        )

        pygame.draw.rect(
            screen,
            (80, 80, 100),
            panel_rect,
            2,
            border_radius=12
        )

    def draw_text_center(self, screen, text, font, y, color):
        text_surface = font.render(text, True, color)

        text_rect = text_surface.get_rect(
            center=(
                self.panel_x + self.panel_width // 2,
                y
            )
        )

        screen.blit(text_surface, text_rect)

    def draw_game_info(self, screen, score, cleared_lines):
        self.draw_panel(screen)

        self.draw_text_center(
            screen,
            "TETRIS-DEFENSE",
            self.font_title,
            60,
            (255, 220, 80)
        )

        self.draw_text_center(
            screen,
            f"Score: {score}",
            self.font_large,
            130,
            (255, 255, 255)
        )

        self.draw_text_center(
            screen,
            f"Lines: {cleared_lines}",
            self.font_medium,
            175,
            (180, 220, 255)
        )

        self.draw_text_center(
            screen,
            "Controls",
            self.font_medium,
            260,
            (255, 220, 80)
        )

        self.draw_text_center(
            screen,
            "←  →   Move",
            self.font_small,
            305,
            (220, 220, 220)
        )

        self.draw_text_center(
            screen,
            "SPACE   Shoot",
            self.font_small,
            340,
            (220, 220, 220)
        )

        self.draw_text_center(
            screen,
            "Destroy blocks",
            self.font_small,
            400,
            (170, 170, 180)
        )

        self.draw_text_center(
            screen,
            "before they fill",
            self.font_small,
            430,
            (170, 170, 180)
        )

        self.draw_text_center(
            screen,
            "the field!",
            self.font_small,
            460,
            (170, 170, 180)
        )

    def draw_game_over(self, screen, score, cleared_lines):
        overlay = pygame.Surface(
            (SCREEN_WIDTH, SCREEN_HEIGHT),
            pygame.SRCALPHA
        )

        overlay.fill((0, 0, 0, 170))
        screen.blit(overlay, (0, 0))

        center_x = SCREEN_WIDTH // 2
        center_y = SCREEN_HEIGHT // 2

        title = self.font_title.render(
            "GAME OVER",
            True,
            (255, 80, 80)
        )

        title_rect = title.get_rect(
            center=(center_x, center_y - 80)
        )

        screen.blit(title, title_rect)

        score_text = self.font_medium.render(
            f"Score: {score}",
            True,
            (255, 255, 255)
        )

        score_rect = score_text.get_rect(
            center=(center_x, center_y - 25)
        )

        screen.blit(score_text, score_rect)

        lines_text = self.font_medium.render(
            f"Lines: {cleared_lines}",
            True,
            (180, 220, 255)
        )

        lines_rect = lines_text.get_rect(
            center=(center_x, center_y + 15)
        )

        screen.blit(lines_text, lines_rect)

        restart_text = self.font_medium.render(
            "Press R to restart",
            True,
            (255, 220, 80)
        )

        restart_rect = restart_text.get_rect(
            center=(center_x, center_y + 75)
        )

        screen.blit(restart_text, restart_rect)