import pygame
import random
import time
from ..constants import *
from ..config.difficulty_settings import DIFFICULTY_SETTINGS


class Platform:
    # 현재 난이도 설정 (기본값: Normal)
    current_difficulty = DIFFICULTY_SETTINGS["Normal"]

    @classmethod
    def set_difficulty(cls, difficulty_name):
        """난이도 설정을 변경합니다."""
        cls.current_difficulty = DIFFICULTY_SETTINGS[difficulty_name]

    def __init__(self, x, y, width=None, is_moving=False, is_transforming=False, is_vanish=False):
        """
        발판을 초기화합니다.
        Args:
            x (float): 발판의 x 좌표 (왼쪽 끝 기준)
            y (float): 발판의 y 좌표 (상단 기준)
            width (float, optional): 발판의 너비. None이면 최대 너비로 설정
            is_moving (bool): 움직이는 플랫폼인지 여부
            is_transforming (bool): 크기가 변하는 플랫폼인지 여부
            is_vanish (bool): 사라졌다 나타나는 플랫폼인지 여부
        """
        self.x = x
        self.initial_x = x  # 초기 x 위치 저장
        self.y = y
        self.initial_width = width if width is not None else PLATFORM_MAX_WIDTH  # 랜덤 제거
        self.width = self.initial_width
        self.height = PLATFORM_HEIGHT
        self.min_width = max(PLATFORM_MIN_WIDTH, int(
            self.initial_width * self.current_difficulty.transform_min_width_ratio))

        # 움직임 관련 속성
        self.is_moving = is_moving
        if is_moving:
            self.direction = 1  # 1: 오른쪽, -1: 왼쪽
            height_factor = abs(
                int((SCREEN_HEIGHT - self.y) / 400))  # 400픽셀당 1씩 증가
            self.speed = min(self.current_difficulty.moving_platform_speed +
                             height_factor, self.current_difficulty.moving_platform_max_speed)
            self.move_range = MOVING_PLATFORM_RANGE

        # 변형 관련 속성
        self.is_transforming = is_transforming
        if is_transforming:
            self.transform_speed = random.uniform(
                self.current_difficulty.transform_min_speed,
                self.current_difficulty.transform_max_speed)
            self.transform_direction = -1  # -1: 줄어듦, 1: 늘어남
            self.center = self.x + self.width / 2  # 중심점 저장

        # 사라지는 속성
        self.is_vanish = is_vanish
        if is_vanish:
            self.is_visible = True
            self.last_vanish_time = time.time() * 1000
            self.vanish_start_time = 0

    def update(self):
        """플랫폼의 상태를 업데이트합니다."""
        current_time = time.time() * 1000

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

        if self.is_transforming:
            # 크기 변화
            self.width += self.transform_speed * self.transform_direction

            # 최소/최대 크기에서 방향 전환
            if self.width <= self.min_width:
                self.width = self.min_width
                self.transform_direction = 1
            elif self.width >= self.initial_width:
                self.width = self.initial_width
                self.transform_direction = -1

            # 중심점 기준으로 x 위치 조정
            self.x = self.center - self.width / 2

            # 화면 경계 처리
            if self.x < 0:
                self.x = 0
            elif self.x + self.width > SCREEN_WIDTH:
                self.x = SCREEN_WIDTH - self.width

        if self.is_vanish:
            if self.is_visible:
                # 보이는 상태에서 VANISH_INTERVAL 시간이 지나면 사라짐
                if current_time - self.last_vanish_time >= self.current_difficulty.vanish_interval:
                    self.is_visible = False
                    self.vanish_start_time = current_time
            else:
                # 사라진 상태에서 VANISH_DURATION 시간이 지나면 다시 나타남
                if current_time - self.vanish_start_time >= self.current_difficulty.vanish_duration:
                    self.is_visible = True
                    self.last_vanish_time = current_time

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
        # 사라지는 플랫폼이고 현재 보이지 않는 상태면 그리지 않음
        if self.is_vanish and not self.is_visible:
            return

        screen_y = self.y - camera_y  # 카메라 위치를 고려한 화면상의 y 위치

        # 화면에 보이는 발판만 그리기
        if screen_y + self.height > 0 and screen_y < SCREEN_HEIGHT:
            # 엑셀 스타일의 선택된 셀처럼 보이게 그리기
            pygame.draw.rect(screen, EXCEL_SELECTED_CELL_COLOR, (
                int(self.x),
                int(screen_y),
                int(self.width),
                int(self.height)
            ))
            # 엑셀 스타일의 테두리
            pygame.draw.rect(screen, EXCEL_GRID_COLOR, (
                int(self.x),
                int(screen_y),
                int(self.width),
                int(self.height)
            ), 1)  # 1픽셀 두께의 테두리

    def is_point_above(self, x, y):
        """주어진 점이 발판 바로 위에 있는지 확인합니다."""
        # 사라진 상태의 플랫폼은 밟을 수 없음
        if self.is_vanish and not self.is_visible:
            return False

        # x 좌표가 발판 범위 내에 있는지 확인 (약간의 여유 추가)
        x_margin = 2  # x축 여유 범위
        is_within_x = self.x - x_margin <= x <= self.right + x_margin

        # y 좌표가 발판 상단 근처에 있는지 확인 (더 넓은 범위)
        y_margin = 10  # y축 여유 범위
        is_within_y = self.y - y_margin <= y <= self.y + y_margin

        return is_within_x and is_within_y

    def is_within_reach(self, x, y, max_jump_height, max_jump_width):
        """현재 위치에서 이 발판에 도달할 수 있는지 확인합니다."""
        # 사라진 상태의 플랫폼은 도달할 수 없음
        if self.is_vanish and not self.is_visible:
            return False

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

        # 첫 번째 발판은 화면 중앙 하단에 생성 (일반 플랫폼으로 고정)
        first_platform = cls(
            x=SCREEN_WIDTH//2 - PLATFORM_MAX_WIDTH//2,
            y=SCREEN_HEIGHT - 50,  # 화면 하단에 더 가깝게 배치
            width=PLATFORM_MAX_WIDTH
        )
        platforms.append(first_platform)

        # 나머지 발판들은 이전 발판 기준으로 생성
        current_width = PLATFORM_MAX_WIDTH
        prev_platform = first_platform

        for _ in range(count - 1):
            new_platform = cls.create_random(
                prev_platform.x, prev_platform.y, current_width, prev_platform)
            current_width = new_platform.width
            platforms.append(new_platform)
            prev_platform = new_platform

        return platforms

    @classmethod
    def create_random(cls, prev_x, prev_y, current_width=None, prev_platform=None):
        """
        이전 발판에서 도달 가능한 범위 내에서 새로운 발판을 생성합니다.
        Args:
            prev_x (float): 이전 발판의 x 좌표
            prev_y (float): 이전 발판의 y 좌표
            current_width (int): 현재 생성할 발판의 너비. None이면 최대 너비로 시작
            prev_platform (Platform): 이전 플랫폼 객체
        Returns:
            Platform: 생성된 발판
        """

        # 현재 너비 결정 (Easy 모드에서는 항상 최대 너비 사용)
        if current_width is None or cls.current_difficulty.platform_width_decrease == 0:
            width = PLATFORM_MAX_WIDTH
        else:
            width = max(PLATFORM_MIN_WIDTH, current_width -
                        cls.current_difficulty.platform_width_decrease)
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

        # 플랫폼 타입 결정
        platform_type = random.random()

        # 이전 플랫폼이 사라지는 플랫폼이었다면 일반 또는 움직이는 플랫폼만 생성 가능
        if prev_platform and hasattr(prev_platform, 'is_vanish') and prev_platform.is_vanish:
            if platform_type < cls.current_difficulty.moving_platform_chance:
                return cls(x, y, width, is_moving=True)
            else:
                return cls(x, y, width)

        # 움직이는 플랫폼
        if platform_type < cls.current_difficulty.moving_platform_chance:
            return cls(x, y, width, is_moving=True)
        # 변형되는 플랫폼 (20% 확률)
        elif platform_type < cls.current_difficulty.moving_platform_chance + 0.2:
            return cls(x, y, width, is_transforming=True)
        # 사라지는 플랫폼
        elif platform_type < cls.current_difficulty.moving_platform_chance + 0.2 + cls.current_difficulty.vanish_platform_chance:
            return cls(x, y, width, is_vanish=True)
        # 일반 플랫폼
        else:
            return cls(x, y, width)
