import pygame
from ..constants import *


class SplashScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, FONT_SIZE * 2)

        # 버튼 크기와 위치 설정
        self.start_button = pygame.Rect(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT//2 + 100,
            200, 50
        )

        # 난이도 버튼들
        button_y = SCREEN_HEIGHT//2
        self.easy_button = pygame.Rect(SCREEN_WIDTH//4 - 60, button_y, 120, 40)
        self.normal_button = pygame.Rect(
            SCREEN_WIDTH//2 - 60, button_y, 120, 40)
        self.hard_button = pygame.Rect(
            SCREEN_WIDTH * 3//4 - 60, button_y, 120, 40)

        # 선택된 난이도 (기본값: Normal)
        self.selected_difficulty = "Normal"

    def draw(self, screen):
        screen.fill(BLACK)

        # 타이틀 그리기
        title = self.title_font.render("Platform Jumper", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        screen.blit(title, title_rect)

        # 난이도 선택 텍스트
        difficulty_text = self.font.render("Select Difficulty:", True, WHITE)
        difficulty_rect = difficulty_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
        screen.blit(difficulty_text, difficulty_rect)

        # 난이도 버튼 그리기
        difficulties = [
            (self.easy_button, "Easy"),
            (self.normal_button, "Normal"),
            (self.hard_button, "Hard")
        ]

        for button, text in difficulties:
            color = WHITE if text == self.selected_difficulty else BLACK
            pygame.draw.rect(screen, color, button)
            pygame.draw.rect(screen, WHITE, button, 2)

            text_surface = self.font.render(text, True,
                                            BLACK if text == self.selected_difficulty else WHITE)
            text_rect = text_surface.get_rect(center=button.center)
            screen.blit(text_surface, text_rect)

        # Start Game 버튼 그리기
        pygame.draw.rect(screen, BLACK, self.start_button)
        pygame.draw.rect(screen, WHITE, self.start_button, 2)

        start_text = self.font.render("Start Game", True, WHITE)
        start_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_rect)

    def handle_click(self, pos):
        # 난이도 버튼 클릭 처리
        if self.easy_button.collidepoint(pos):
            self.selected_difficulty = "Easy"
        elif self.normal_button.collidepoint(pos):
            self.selected_difficulty = "Normal"
        elif self.hard_button.collidepoint(pos):
            self.selected_difficulty = "Hard"
        elif self.start_button.collidepoint(pos):
            return True  # 게임 시작 신호
        return False  # 게임 시작하지 않음
