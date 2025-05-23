import pygame
from ..constants import *


class GameOver:
    def __init__(self):
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.retry_button = pygame.Rect(
            RETRY_BUTTON_POS[0],
            RETRY_BUTTON_POS[1],
            RETRY_BUTTON_SIZE[0],
            RETRY_BUTTON_SIZE[1]
        )

    def draw(self, screen, score):
        """게임 오버 화면을 그립니다."""
        # 게임 오버 텍스트
        game_over_text = self.font.render('GAME OVER', True, RED)
        game_over_rect = game_over_text.get_rect(center=GAMEOVER_TEXT_POS)
        screen.blit(game_over_text, game_over_rect)

        # 최종 점수
        score_text = self.font.render(f'Score: {score}m', True, WHITE)
        score_rect = score_text.get_rect(
            center=(GAMEOVER_TEXT_POS[0], GAMEOVER_TEXT_POS[1] + 40)
        )
        screen.blit(score_text, score_rect)

        # Retry 버튼
        pygame.draw.rect(screen, WHITE, self.retry_button)
        retry_text = self.font.render('Retry', True, BLACK)
        retry_text_rect = retry_text.get_rect(center=self.retry_button.center)
        screen.blit(retry_text, retry_text_rect)

    def check_retry_click(self, pos):
        """Retry 버튼 클릭을 확인합니다."""
        return self.retry_button.collidepoint(pos)
