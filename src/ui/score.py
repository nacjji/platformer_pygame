import pygame
from ..constants import *


class ScoreUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)  # 기본 폰트, 크기 36
        self.pos = (10, 10)  # 좌측 상단 위치

    def draw(self, screen, score):
        """점수를 화면에 표시합니다."""
        score_text = f"Height: {score}m"
        text_surface = self.font.render(score_text, True, WHITE)
        screen.blit(text_surface, self.pos)
