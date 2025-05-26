import pygame
from ..constants import *
from ..objects.platform import Platform


class ScoreUI:
    def __init__(self):
        self.font = pygame.font.Font(None, 36)  # 기본 폰트, 크기 36
        self.small_font = pygame.font.Font(None, 24)  # 작은 폰트
        self.pos = (10, 10)  # 좌측 상단 위치

    def draw(self, screen, score, max_height):
        """현재 높이와 최고 높이를 화면에 표시합니다."""
        # 현재 난이도의 점수 배율
        multiplier = Platform.current_difficulty.score_multiplier

        # 실제 높이 계산 (배율 제외)
        raw_height = int(score / multiplier)
        raw_max_height = int(max_height / multiplier)

        # 메인 점수 텍스트 (배율 적용된 점수)
        height_text = f"Score: {score}m / {max_height}m"
        text_surface = self.font.render(height_text, True, EXCEL_FONT_COLOR)
        screen.blit(text_surface, self.pos)

        # 실제 높이 텍스트
        actual_height_text = f"Actual Height: {raw_height}m (x{multiplier} bonus)"
        bonus_surface = self.small_font.render(
            actual_height_text, True, EXCEL_FONT_COLOR)
        screen.blit(bonus_surface, (self.pos[0], self.pos[1] + 30))
