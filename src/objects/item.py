import pygame
from ..constants import *


class Item:
    def __init__(self, x, y, item_type):
        """
        아이템을 초기화합니다.
        Args:
            x (float): 아이템의 x 좌표
            y (float): 아이템의 y 좌표
            item_type (str): 아이템의 종류 ('jump_boost', 'speed_reduce')
        """
        self.pos_x = x
        self.pos_y = y
        self.item_type = item_type
        self.is_collected = False
        self.animation_frame = 0
        self.animation_speed = 0.1
        self.float_offset = 0
        self.float_speed = 0.05
        self.float_direction = 1

        # 아이템 효과 정보 가져오기
        self.effect_info = ITEM_TYPES.get(item_type, {
            'color': (255, 255, 255),
            'duration': 10,
            'effect': None,
            'value': 1.0
        })

    @property
    def rect(self):
        """아이템의 충돌 박스를 반환합니다."""
        return pygame.Rect(
            self.pos_x - ITEM_SIZE/2,
            self.pos_y - ITEM_SIZE/2,
            ITEM_SIZE,
            ITEM_SIZE
        )

    def update(self):
        """아이템의 상태를 업데이트합니다."""
        if not self.is_collected:
            # 부드러운 상하 움직임
            self.float_offset += self.float_speed * self.float_direction
            if abs(self.float_offset) > 5:
                self.float_direction *= -1

            # 애니메이션 프레임 업데이트
            self.animation_frame += self.animation_speed
            if self.animation_frame >= 360:
                self.animation_frame = 0

    def draw(self, screen, camera_y):
        """아이템을 화면에 그립니다."""
        if not self.is_collected:
            screen_y = self.pos_y - camera_y
            # 부드러운 상하 움직임 적용
            screen_y += self.float_offset

            # 아이템 타입에 따른 색상 설정
            color = self.effect_info['color']

            # 아이템 그리기
            pygame.draw.circle(screen, color, (
                int(self.pos_x),
                int(screen_y)
            ), ITEM_SIZE/2)

            # 아이템 테두리
            pygame.draw.circle(screen, (0, 0, 0), (
                int(self.pos_x),
                int(screen_y)
            ), ITEM_SIZE/2, 1)

    def collect(self):
        """아이템을 수집합니다."""
        self.is_collected = True
        return {
            'type': self.item_type,
            'effect': self.effect_info['effect'],
            'value': self.effect_info['value'],
            'duration': self.effect_info['duration'],  # 지속 높이 (m)
            # 수집 시점의 높이 (m)
            'start_height': int((SCREEN_HEIGHT - 100 - self.pos_y) / 100)
        }
