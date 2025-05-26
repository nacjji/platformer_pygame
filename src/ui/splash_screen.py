import pygame
from ..constants import *
from ..config.difficulty_settings import DIFFICULTY_SETTINGS


class SplashScreen:
    def __init__(self):
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.title_font = pygame.font.Font(None, FONT_SIZE * 2)
        self.small_font = pygame.font.Font(None, FONT_SIZE - 8)  # 작은 폰트 크기 조정

        # 난이도 버튼들 크기와 위치 설정
        button_width = 120  # 버튼 너비
        button_height = 60  # 버튼 높이
        gap = 30  # 버튼 사이 간격

        total_width = (button_width * 3) + (gap * 2)
        start_x = (SCREEN_WIDTH - total_width) // 2
        button_y = SCREEN_HEIGHT - 200  # 화면 하단에서 200픽셀 위

        # 난이도 버튼 위치 설정
        self.easy_button = pygame.Rect(
            start_x, button_y, button_width, button_height)
        self.normal_button = pygame.Rect(
            start_x + button_width + gap, button_y, button_width, button_height)
        self.hard_button = pygame.Rect(
            start_x + (button_width + gap) * 2, button_y, button_width, button_height)

        # Start Game 버튼 위치 설정
        self.start_button = pygame.Rect(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT - 100,  # 화면 하단에서 100픽셀 위
            200, 50
        )

        # 선택된 난이도 (기본값: Normal)
        self.selected_difficulty = "Normal"

    def draw(self, screen):
        screen.fill(BLACK)

        # 타이틀 그리기
        title = self.title_font.render("Platform Jumper", True, WHITE)
        title_rect = title.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//4))
        screen.blit(title, title_rect)

        # 조작법 가이드 추가
        guide_texts = [
            "How to Play",
            "<- -> : Move Left/Right",
            "SPACE : Jump"
        ]

        guide_y = SCREEN_HEIGHT//4 + 60
        for text in guide_texts:
            guide_surface = self.font.render(text, True, WHITE)
            guide_rect = guide_surface.get_rect(
                center=(SCREEN_WIDTH//2, guide_y))
            screen.blit(guide_surface, guide_rect)
            guide_y += 30

        # 난이도 선택 텍스트
        difficulty_text = self.font.render("Select Difficulty:", True, WHITE)
        difficulty_rect = difficulty_text.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT - 250))  # 난이도 버튼 위에 표시
        screen.blit(difficulty_text, difficulty_rect)

        # 난이도 버튼 그리기
        difficulties = [
            (self.easy_button, "Easy",
             DIFFICULTY_SETTINGS["Easy"].score_multiplier),
            (self.normal_button, "Normal",
             DIFFICULTY_SETTINGS["Normal"].score_multiplier),
            (self.hard_button, "Hard",
             DIFFICULTY_SETTINGS["Hard"].score_multiplier)
        ]

        for button, text, multiplier in difficulties:
            color = WHITE if text == self.selected_difficulty else BLACK
            pygame.draw.rect(screen, color, button)
            pygame.draw.rect(screen, WHITE, button, 2)

            # 난이도 텍스트
            text_surface = self.font.render(text, True,
                                            BLACK if text == self.selected_difficulty else WHITE)
            text_rect = text_surface.get_rect(
                center=(button.centerx, button.centery - 10))
            screen.blit(text_surface, text_rect)

            # 점수 배율 텍스트
            multiplier_text = self.small_font.render(f"x{multiplier:.1f}", True,
                                                     BLACK if text == self.selected_difficulty else WHITE)
            multiplier_rect = multiplier_text.get_rect(
                center=(button.centerx, button.centery + 10))
            screen.blit(multiplier_text, multiplier_rect)

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
