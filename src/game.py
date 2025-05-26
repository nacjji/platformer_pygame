import pygame

from src.ui.score import ScoreUI
from src.ui.splash_screen import SplashScreen
from src.ui.nickname_screen import NicknameScreen
from src.ui.ranking_system import RankingSystem
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
        self.big_font = pygame.font.Font(None, FONT_SIZE + 20)  # 큰 폰트 추가

        # 버튼 위치 및 크기 조정
        button_width = 250
        button_height = 50
        button_gap = 20
        base_y = SCREEN_HEIGHT//2 + 30

        self.retry_button = pygame.Rect(
            SCREEN_WIDTH//2 - button_width//2,
            base_y,
            button_width, button_height)
        self.change_difficulty_button = pygame.Rect(
            SCREEN_WIDTH//2 - button_width//2,
            base_y + button_height + button_gap,
            button_width, button_height)

        # 게임 상태 추가
        self.ranking_system = RankingSystem()
        self.is_in_nickname = True  # 닉네임 입력 화면 상태
        self.is_in_splash = False  # 스플래시 화면 상태
        self.nickname_screen = NicknameScreen(self.ranking_system)
        self.splash_screen = SplashScreen()

        # 게임 객체 초기화
        self.platforms = []
        self.obstacles = []  # 장애물 리스트 추가
        self.last_obstacle_height = 0  # 마지막 장애물 생성 높이
        self.obstacle_interval = 300  # 10m (100픽셀 = 1m)
        self.player = None

    def reset_game(self):
        """게임을 초기 상태로 리셋합니다."""
        # 초기 발판들 생성 (더 많은 수의 초기 발판)
        self.platforms = Platform.create_initial_platforms(10)
        self.obstacles = []  # 장애물 리스트 초기화
        self.last_obstacle_height = 0

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

            # 닉네임 입력 화면일 때
            if self.is_in_nickname:
                if self.nickname_screen.handle_event(event):
                    self.is_in_nickname = False
                    self.is_in_splash = True

            # 스플래시 화면일 때
            elif self.is_in_splash:
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.splash_screen.handle_click(event.pos):
                        Platform.set_difficulty(
                            self.splash_screen.selected_difficulty)
                        self.is_in_splash = False
                        self.reset_game()

            # 게임 플레이 중일 때
            else:
                if self.player.is_dead:
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.retry_button.collidepoint(event.pos):
                            self.reset_game()
                        elif self.change_difficulty_button.collidepoint(event.pos):
                            self.is_in_splash = True
                else:
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_SPACE:
                            self.player.jump()
                        elif event.key == pygame.K_r:
                            self.reset_game()

        return True

    def update(self):
        """게임 상태를 업데이트합니다."""
        if self.is_in_nickname or self.is_in_splash:
            return

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

        # 장애물 업데이트 및 충돌 체크
        for obstacle in self.obstacles:
            obstacle.update()
            if obstacle.check_collision(self.player):
                # 충돌 효과는 check_collision 내에서 처리됨
                pass

        # 플레이어 업데이트
        self.player.update(self.platforms)

        # 점수 업데이트
        prev_score = self.player.score
        self.player.update_score()

        # 플레이어가 죽었을 때 랭킹 업데이트
        if self.player.is_dead and prev_score > 0:
            self.ranking_system.add_score(
                self.ranking_system.current_player,
                self.player.score)

        # 카메라 업데이트
        self.update_camera()

        # 플레이어의 화면상 위치 업데이트
        self.player.update_screen_position(self.camera_y)

        # 새로운 플랫폼 생성 로직
        self.generate_platforms()

    def draw(self):
        """게임을 화면에 그립니다."""
        if self.is_in_nickname:
            self.nickname_screen.draw(self.screen)
        elif self.is_in_splash:
            self.splash_screen.draw(self.screen)
        else:
            self.screen.fill(BLACK)

            # 발판 그리기
            for platform in self.platforms:
                platform.draw(self.screen, self.camera_y)

            # 플레이어 그리기
            self.player.draw(self.screen)

            # UI 그리기
            self.score_ui.draw(self.screen, self.player.score,
                               self.player.max_height)

            # 게임오버 화면
            if self.player.is_dead:
                # 반투명한 검은색 오버레이
                overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
                overlay.fill(BLACK)
                overlay.set_alpha(180)
                self.screen.blit(overlay, (0, 0))

                # 게임오버 텍스트
                game_over_text = self.big_font.render('GAME OVER', True, RED)
                game_over_rect = game_over_text.get_rect(
                    center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 150))
                self.screen.blit(game_over_text, game_over_rect)

                # 최종 점수와 순위
                rank = self.ranking_system.get_rank_for_score(
                    self.player.max_height)
                final_score_text = self.font.render(
                    f'Final Score: {self.player.max_height}m (Rank: {rank})', True, WHITE)
                final_score_rect = final_score_text.get_rect(
                    center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2 - 100))
                self.screen.blit(final_score_text, final_score_rect)

                # 랭킹 표시
                rankings = self.ranking_system.format_rankings()
                start_y = SCREEN_HEIGHT//2 - 50
                for i, rank_text in enumerate(rankings[:5]):
                    rank_surface = self.font.render(rank_text, True, WHITE)
                    rank_rect = rank_surface.get_rect(
                        center=(SCREEN_WIDTH//2, start_y + i * 30))
                    self.screen.blit(rank_surface, rank_rect)

                # Retry 버튼
                pygame.draw.rect(self.screen, (100, 100, 255),
                                 self.retry_button)
                pygame.draw.rect(self.screen, WHITE, self.retry_button, 2)
                retry_text = self.font.render("RETRY", True, WHITE)
                retry_rect = retry_text.get_rect(
                    center=self.retry_button.center)
                self.screen.blit(retry_text, retry_rect)

                # Change Difficulty 버튼
                pygame.draw.rect(self.screen, (100, 100, 255),
                                 self.change_difficulty_button)
                pygame.draw.rect(self.screen, WHITE,
                                 self.change_difficulty_button, 2)
                change_text = self.font.render(
                    "Change Difficulty", True, WHITE)
                change_rect = change_text.get_rect(
                    center=self.change_difficulty_button.center)
                self.screen.blit(change_text, change_rect)

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

    def run(self):
        """게임 메인 루프를 실행합니다."""
        running = True
        while running:
            running = self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
