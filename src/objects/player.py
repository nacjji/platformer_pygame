import pygame
from ..constants import *
from ..actions.movement import Movement
from ..objects.platform import Platform  # Platform 클래스 임포트 추가


class Player:
    def __init__(self, x, y):
        self.pos_x = x
        self.pos_y = y  # 실제 게임 월드에서의 y 위치
        self.screen_y = y  # 화면상의 y 위치
        self.velocity_y = 0
        self.is_jumping = False
        self.score = 0  # 현재 점수 (높이)
        self.max_height = 0  # 도달한 최대 높이
        self.is_dead = False

    @property
    def rect(self):
        """플레이어의 충돌 박스를 반환합니다."""
        return pygame.Rect(
            self.pos_x - PLAYER_WIDTH/2,  # 중심점 기준으로 좌우 위치 계산
            self.pos_y - PLAYER_HEIGHT/2,  # 중심점 기준으로 상하 위치 계산
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        )

    @property
    def bottom(self):
        """플레이어의 바닥 y좌표를 반환합니다."""
        return self.pos_y + PLAYER_HEIGHT/2

    @property
    def top(self):
        """플레이어의 상단 y좌표를 반환합니다."""
        return self.pos_y - PLAYER_HEIGHT/2

    def move(self, direction):
        """플레이어를 좌우로 이동시킵니다."""
        Movement.move_horizontal(self, direction)

    def jump(self):
        """플레이어가 점프합니다."""
        Movement.jump(self)

    def update(self, platforms):
        """플레이어의 상태를 업데이트합니다."""
        Movement.apply_gravity(self, platforms)

        # 화면 아래로 떨어졌는지 확인
        if self.screen_y > SCREEN_HEIGHT + PLAYER_HEIGHT:
            self.is_dead = True

    def draw(self, screen):
        """플레이어를 화면에 그립니다."""
        # 엑셀 스타일의 선택된 셀처럼 보이게 그리기
        pygame.draw.rect(screen, BLACK, (
            int(self.pos_x - PLAYER_WIDTH/2),
            int(self.screen_y - PLAYER_HEIGHT/2),
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        ))
        # 엑셀 스타일의 테두리
        pygame.draw.rect(screen, EXCEL_GRID_COLOR, (
            int(self.pos_x - PLAYER_WIDTH/2),
            int(self.screen_y - PLAYER_HEIGHT/2),
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        ), 1)  # 1픽셀 두께의 테두리

    def update_screen_position(self, camera_y):
        """화면상의 위치를 업데이트합니다."""
        self.screen_y = self.pos_y - camera_y

    def update_score(self):
        """점수(높이)를 업데이트합니다."""
        # 시작 위치로부터의 현재 높이를 계산 (위로 갈수록 y값이 작아짐)
        current_height = abs(
            int((SCREEN_HEIGHT - self.pos_y) / 100))  # 100픽셀당 1m

        # 현재 높이를 score에 반영
        self.score = current_height

        # 최고 높이 업데이트
        if current_height > self.max_height:
            self.max_height = current_height
