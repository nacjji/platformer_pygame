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
        self.raw_height = 0  # 실제 높이 (배율 적용 전)

        # 버프 효과를 위한 속성
        self.jump_power_multiplier = 1.0  # 점프력 배율
        self.speed_multiplier = 1.0  # 이동속도 배율
        self.active_buff_type = None  # 현재 활성화된 버프 타입

    def set_buff(self, buff_type):
        """현재 활성화된 버프 타입을 설정합니다."""
        self.active_buff_type = buff_type

    def remove_buff(self):
        """버프를 제거합니다."""
        self.active_buff_type = None

    @property
    def border_color(self):
        """현재 버프에 따른 테두리 색상을 반환합니다."""
        if self.active_buff_type:
            return ITEM_TYPES[self.active_buff_type]['color']
        return EXCEL_GRID_COLOR

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
        Movement.move_horizontal(self, direction * self.speed_multiplier)

    def jump(self):
        """플레이어가 점프합니다."""
        if not self.is_jumping:
            self.velocity_y = JUMP_POWER * self.jump_power_multiplier
            self.is_jumping = True
            return True
        return False

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
        # 버프에 따른 테두리 색상 적용
        pygame.draw.rect(screen, self.border_color, (
            int(self.pos_x - PLAYER_WIDTH/2),
            int(self.screen_y - PLAYER_HEIGHT/2),
            PLAYER_WIDTH,
            PLAYER_HEIGHT
        ), 2)  # 2픽셀 두께의 테두리

    def update_screen_position(self, camera_y):
        """화면상의 위치를 업데이트합니다."""
        self.screen_y = self.pos_y - camera_y

    def update_score(self):
        """점수(높이)를 업데이트합니다."""
        # 시작 위치로부터의 현재 높이를 계산 (위로 갈수록 y값이 작아짐)
        # SCREEN_HEIGHT - 100 이 시작 위치이므로, 이를 기준으로 계산
        self.raw_height = max(0, abs(
            int((SCREEN_HEIGHT - 100 - self.pos_y) / 100)))  # 100픽셀당 1m

        # 난이도 배율 적용
        current_height = int(
            self.raw_height * Platform.current_difficulty.score_multiplier)

        # 현재 높이를 score에 반영
        self.score = current_height

        # 최고 높이 업데이트 (배율 적용된 값으로)
        if current_height > self.max_height:
            self.max_height = current_height
