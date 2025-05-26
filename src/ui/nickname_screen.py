import pygame
from ..constants import *


class NicknameScreen:
    def __init__(self, ranking_system):
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.nickname = ""
        self.max_length = 10
        self.error_message = ""
        self.error_timer = 0
        self.ranking_system = ranking_system

        # 입력 박스 설정
        self.input_box = pygame.Rect(
            SCREEN_WIDTH//2 - 100,
            SCREEN_HEIGHT//2 - 20,
            200, 40
        )

        # 시작 버튼
        self.start_button = pygame.Rect(
            SCREEN_WIDTH//2 - 60,
            SCREEN_HEIGHT//2 + 40,
            120, 40
        )

        self.active = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                return self.try_submit()
            elif event.key == pygame.K_BACKSPACE:
                self.nickname = self.nickname[:-1]
            else:
                # 영문, 숫자만 허용
                if len(self.nickname) < self.max_length and event.unicode.isalnum():
                    self.nickname += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.start_button.collidepoint(event.pos):
                return self.try_submit()

        return False

    def try_submit(self):
        """닉네임 제출을 시도합니다."""
        if len(self.nickname) < 2:
            self.error_message = "Nickname must be at least 2 characters"
            self.error_timer = 60
            return False

        if self.ranking_system.is_nickname_taken(self.nickname):
            self.error_message = "Nickname already taken"
            self.error_timer = 60
            return False

        self.ranking_system.current_player = self.nickname
        return True

    def draw(self, screen):
        screen.fill(BLACK)

        # 제목 텍스트
        title = self.font.render("Enter Your Nickname:", True, WHITE)
        title_rect = title.get_rect(
            center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 60))
        screen.blit(title, title_rect)

        # 입력 박스
        pygame.draw.rect(screen, WHITE, self.input_box, 2)

        # 닉네임 텍스트
        text_surface = self.font.render(self.nickname, True, WHITE)
        text_rect = text_surface.get_rect(center=self.input_box.center)
        screen.blit(text_surface, text_rect)

        # 시작 버튼
        pygame.draw.rect(screen, (100, 100, 255), self.start_button)
        pygame.draw.rect(screen, WHITE, self.start_button, 2)
        start_text = self.font.render("Start", True, WHITE)
        start_rect = start_text.get_rect(center=self.start_button.center)
        screen.blit(start_text, start_rect)

        # 에러 메시지
        if self.error_timer > 0:
            error_surface = self.font.render(self.error_message, True, RED)
            error_rect = error_surface.get_rect(
                center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 + 100))
            screen.blit(error_surface, error_rect)
            self.error_timer -= 1

        # 랭킹 표시
        rankings = self.ranking_system.format_rankings()
        start_y = SCREEN_HEIGHT//2 - 200
        for i, rank_text in enumerate(rankings[:5]):  # 상위 5개만 표시
            rank_surface = self.font.render(rank_text, True, WHITE)
            rank_rect = rank_surface.get_rect(
                center=(SCREEN_WIDTH//2, start_y + i * 30))
            screen.blit(rank_surface, rank_rect)
