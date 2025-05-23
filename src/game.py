import pygame
import sys

from src.ui.score import ScoreUI
from .constants import *
from .objects.player import Player
from .objects.platform import Platform


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.camera_y = 0  # 카메라의 y 위치
        self.score_ui = ScoreUI()  # 점수 UI 초기화
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.retry_button = pygame.Rect(
            BUTTON_POS[0], BUTTON_POS[1], BUTTON_SIZE[0], BUTTON_SIZE[1])
        self.reset_game()

    def reset_game(self):
        """게임을 초기 상태로 리셋합니다."""
        # 초기 발판들 생성 (더 많은 수의 초기 발판)
        self.platforms = Platform.create_initial_platforms(10)

        # 첫 번째 발판 위에 플레이어 생성
        first_platform = self.platforms[0]
        player_x = first_platform.center_x
        player_y = first_platform.y - PLAYER_HEIGHT/2
        self.player = Player(player_x, player_y)

        # 초기에 더 많은 플랫폼 미리 생성
        self.generate_platforms()

    def update_camera(self):
        """카메라 위치를 업데이트합니다."""
        # 플레이어가 화면의 40% 위치보다 위에 있을 때
        if self.player.pos_y < CAMERA_FOLLOW_THRESHOLD:
            # 카메라를 플레이어를 따라가도록 조정
            self.camera_y = self.player.pos_y - CAMERA_FOLLOW_THRESHOLD

    def draw_button(self, text, rect, color):
        """버튼을 그립니다."""
        pygame.draw.rect(self.screen, color, rect)
        pygame.draw.rect(self.screen, WHITE, rect, 2)  # 테두리
        text_surface = self.font.render(text, True, WHITE)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

    def handle_events(self):
        """이벤트를 처리합니다."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.player.is_dead:
                    self.player.jump()
                elif event.key == pygame.K_r and self.player.is_dead:
                    self.reset_game()

            # 마우스 클릭 처리
            if event.type == pygame.MOUSEBUTTONDOWN and self.player.is_dead:
                if self.retry_button.collidepoint(event.pos):
                    self.reset_game()

        return True

    def update(self):
        """게임 상태를 업데이트합니다."""
        # 게임오버 상태에서는 업데이트하지 않음
        if self.player.is_dead:
            return

        # 키보드 입력 처리
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            self.player.move(-1)
        if keys[pygame.K_RIGHT]:
            self.player.move(1)

        # 플랫폼 업데이트
        for platform in self.platforms:
            platform.update()

        # 플레이어 업데이트
        self.player.update(self.platforms)

        # 점수 업데이트
        self.player.update_score()

        # 카메라 업데이트
        self.update_camera()

        # 플레이어의 화면상 위치 업데이트
        self.player.update_screen_position(self.camera_y)

        # 새로운 플랫폼 생성 로직
        self.generate_platforms()

    def draw(self):
        """게임을 화면에 그립니다."""
        self.screen.fill(BLACK)

        # 발판 그리기
        for platform in self.platforms:
            platform.draw(self.screen, self.camera_y)

        # 플레이어 그리기
        self.player.draw(self.screen)

        # UI 그리기
        score_text = f"Height: {self.player.score}m"
        text_surface = self.font.render(score_text, True, WHITE)
        self.screen.blit(text_surface, (10, 10))

        # 게임오버 화면
        if self.player.is_dead:
            # 반투명한 검은색 오버레이
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
            overlay.fill(BLACK)
            overlay.set_alpha(128)
            self.screen.blit(overlay, (0, 0))

            # 게임오버 텍스트
            game_over_text = self.font.render('GAME OVER', True, RED)
            game_over_rect = game_over_text.get_rect(
                center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 50))
            self.screen.blit(game_over_text, game_over_rect)

            # 최종 점수
            final_score_text = self.font.render(
                f'Final Score: {self.player.score}m', True, WHITE)
            final_score_rect = final_score_text.get_rect(
                center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(final_score_text, final_score_rect)

            # Retry 버튼
            self.draw_button("RETRY", self.retry_button, BUTTON_COLOR)

        pygame.display.update()

    def generate_platforms(self):
        """필요한 경우 새로운 플랫폼을 생성합니다."""
        # 가장 높은 플랫폼 찾기
        highest_platform = min(self.platforms, key=lambda p: p.y)

        # 플레이어보다 화면 높이의 2배 위까지 미리 플랫폼 생성
        while highest_platform.y > self.player.pos_y - SCREEN_HEIGHT * 2:
            new_platform = Platform.create_random(
                highest_platform.x,  # 이전 플랫폼의 실제 x 좌표 전달
                highest_platform.y,
                highest_platform.width
            )
            self.platforms.append(new_platform)
            highest_platform = new_platform

        # 화면에서 너무 멀리 떨어진 플랫폼 제거 (메모리 관리)
        self.platforms = [p for p in self.platforms
                          if p.y - self.camera_y < SCREEN_HEIGHT * 3]

    def run(self):
        """게임 메인 루프를 실행합니다."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
