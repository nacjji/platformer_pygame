import pygame
import random
from ..constants import *


class Platform:
    def __init__(self, x, y, width=None, is_moving=False):
        """
        발판을 초기화합니다.
        Args:
            x (float): 발판의 x 좌표 (왼쪽 끝 기준)
            y (float): 발판의 y 좌표 (상단 기준)
            width (float, optional): 발판의 너비. None이면 랜덤한 너비로 생성
            is_moving (bool): 움직이는 플랫폼인지 여부
        """
        self.x = x
        self.initial_x = x  # 초기 x 위치 저장
        self.y = y
        self.width = width if width is not None else random.randint(
            PLATFORM_MIN_WIDTH, PLATFORM_MAX_WIDTH)
        self.height = PLATFORM_HEIGHT

        # 움직임 관련 속성
        self.is_moving = is_moving
        if is_moving:
            self.direction = 1  # 1: 오른쪽, -1: 왼쪽

            # 높이에 따른 속도 계산 (시작 높이에서 얼마나 올라갔는지)
            height_factor = abs(
                int((SCREEN_HEIGHT - self.y) / 400))  # 400픽셀당 1씩 증가
            self.speed = min(MOVING_PLATFORM_SPEED +
                             height_factor, MOVING_PLATFORM_MAX_SPEED)
            self.move_range = MOVING_PLATFORM_RANGE

    def update(self):
        """플랫폼의 상태를 업데이트합니다."""
        if self.is_moving:
            # 이동
            self.x += self.speed * self.direction

            # 화면 경계에서 방향 전환
            if self.x <= 0:
                self.x = 0
                self.direction = 1
            elif self.x + self.width >= SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.width
                self.direction = -1

    @property
    def right(self):
        """발판의 오른쪽 끝 x 좌표를 반환합니다."""
        return self.x + self.width

    @property
    def center_x(self):
        """발판의 중심 x 좌표를 반환합니다."""
        return self.x + self.width / 2

    @property
    def top(self):
        """발판의 상단 y 좌표를 반환합니다."""
        return self.y

    @property
    def bottom(self):
        """발판의 하단 y 좌표를 반환합니다."""
        return self.y + self.height

    def draw(self, screen, camera_y):
        """발판을 화면에 그립니다."""
        screen_y = self.y - camera_y  # 카메라 위치를 고려한 화면상의 y 위치

        # 화면에 보이는 발판만 그리기
        if screen_y + self.height > 0 and screen_y < SCREEN_HEIGHT:
            pygame.draw.rect(screen, GREEN, (
                int(self.x),
                int(screen_y),
                int(self.width),
                int(self.height)
            ))

    def is_point_above(self, x, y):
        """주어진 점이 발판 바로 위에 있는지 확인합니다."""
        return (self.x <= x <= self.right and
                self.y - 5 <= y <= self.y + 5)  # 약간의 여유 범위를 둠

    def is_within_reach(self, x, y, max_jump_height, max_jump_width):
        """현재 위치에서 이 발판에 도달할 수 있는지 확인합니다."""
        # 수직 거리 체크
        if y - max_jump_height > self.bottom:  # 발판이 너무 높음
            return False
        if y < self.y:  # 발판이 더 낮음
            return False

        # 수평 거리 체크
        horizontal_distance = min(abs(x - self.x), abs(x - self.right))
        return horizontal_distance <= max_jump_width

    @classmethod
    def create_initial_platforms(cls, count=5):
        """
        초기 발판들을 생성합니다.
        Args:
            count (int): 생성할 발판의 수
        Returns:
            list[Platform]: 생성된 발판들의 리스트
        """
        platforms = []

        # 첫 번째 발판은 화면 중앙 하단에 생성
        first_platform = cls(
            x=SCREEN_WIDTH//2 - PLATFORM_MAX_WIDTH//2,
            y=SCREEN_HEIGHT - 100,
            width=PLATFORM_MAX_WIDTH
        )
        platforms.append(first_platform)

        # 나머지 발판들은 이전 발판 기준으로 생성
        current_width = PLATFORM_MAX_WIDTH
        prev_platform = first_platform

        for _ in range(count - 1):
            new_platform = cls.create_random(
                prev_platform.x, prev_platform.y, current_width)
            current_width = new_platform.width
            platforms.append(new_platform)
            prev_platform = new_platform

        return platforms

    @classmethod
    def create_random(cls, prev_x, prev_y, current_width=None):
        """
        이전 발판에서 도달 가능한 범위 내에서 새로운 발판을 생성합니다.
        Args:
            prev_x (float): 이전 발판의 x 좌표
            prev_y (float): 이전 발판의 y 좌표
            current_width (int): 현재 생성할 발판의 너비. None이면 최대 너비로 시작
        Returns:
            Platform: 생성된 발판
        """
        # 현재 너비 결정
        if current_width is None:
            width = PLATFORM_MAX_WIDTH
        else:
            width = max(PLATFORM_MIN_WIDTH, current_width -
                        PLATFORM_WIDTH_DECREASE)

        # 최대 점프 거리 계산 (수평)
        max_jump_distance = PLAYER_SPEED * abs(2 * JUMP_POWER / GRAVITY)
        safe_jump_distance = max_jump_distance * 0.7

        # 이전 발판 위치 기준으로 도달 가능한 x 범위 계산
        min_x = max(0, prev_x - safe_jump_distance)
        max_x = min(SCREEN_WIDTH - width, prev_x + safe_jump_distance)

        # 범위 내에서 랜덤하게 x 위치 선택
        x = random.randint(int(min_x), int(max_x))

        # 수직 간격 결정
        max_jump_height = abs(JUMP_POWER * JUMP_POWER / (2 * GRAVITY))
        height_gap = random.uniform(
            max_jump_height * 0.6, max_jump_height * 0.8)
        y = prev_y - height_gap

        # 움직이는 플랫폼 결정 (30% 확률)
        is_moving = random.random() < MOVING_PLATFORM_CHANCE

        return cls(x, y, width, is_moving)
