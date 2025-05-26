import pygame

# 게임 설정
SCREEN_WIDTH = 450
SCREEN_HEIGHT = 800
FPS = 60

# 엑셀 스타일 설정
EXCEL_CELL_WIDTH = 60
EXCEL_CELL_HEIGHT = 25
EXCEL_HEADER_HEIGHT = 30
EXCEL_COLUMN_HEADER_COLOR = (240, 240, 240)
EXCEL_GRID_COLOR = (220, 220, 220)
EXCEL_SELECTED_CELL_COLOR = (217, 226, 243)
EXCEL_FONT_COLOR = (60, 60, 60)
EXCEL_HEADER_FONT_COLOR = (80, 80, 80)

# 카메라 설정
CAMERA_FOLLOW_THRESHOLD = SCREEN_HEIGHT * 0.4  # 화면 40% 지점부터 카메라가 따라감

# 색상
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (200, 200, 200)  # 발판 색상을 엑셀 스타일로 변경
RED = (192, 0, 0)  # 엑셀 스타일의 빨간색

# 플레이어 설정
PLAYER_WIDTH = 20  # 플레이어 너비
PLAYER_HEIGHT = 40  # 플레이어 높이
PLAYER_SPEED = 4
JUMP_POWER = -15
GRAVITY = 0.8

# 점프 관련 물리 계산
# 최대 점프 시간 (초) = 상승시간 + 하강시간
# 상승시간 = -JUMP_POWER / GRAVITY
# 최대 높이 = JUMP_POWER^2 / (2 * GRAVITY)
MAX_JUMP_TIME = abs(2 * JUMP_POWER / GRAVITY)  # 점프 후 착지까지 걸리는 시간
MAX_JUMP_HEIGHT = abs(JUMP_POWER * JUMP_POWER / (2 * GRAVITY))  # 최대 점프 높이
MAX_JUMP_DISTANCE = PLAYER_SPEED * MAX_JUMP_TIME  # 최대 수평 이동 거리

# 카메라 설정
CAMERA_MARGIN = SCREEN_HEIGHT * 0.4  # 화면 40% 지점을 기준으로 카메라 이동 시작

# 발판 설정
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 20
PLATFORM_MIN_WIDTH = 1   # 최소 발판 너비를 1px로 설정
PLATFORM_MAX_WIDTH = 60  # 최대 발판 너비
PLATFORM_WIDTH_DECREASE = 1  # 발판 생성마다 줄어드는 너비


# 점프 최대 거리 계산
MAX_VERTICAL_DISTANCE = abs(
    JUMP_POWER * MAX_JUMP_TIME / 2 + 0.5 * GRAVITY * (MAX_JUMP_TIME / 2) ** 2)


# UI 설정
FONT_SIZE = 36
SCORE_POS = (10, 10)
GAMEOVER_TEXT_POS = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
RETRY_BUTTON_SIZE = (120, 40)
RETRY_BUTTON_POS = (SCREEN_WIDTH // 2 - 60, SCREEN_HEIGHT // 2 + 50)
BUTTON_COLOR = (100, 100, 255)  # 버튼 색상
BUTTON_SIZE = (200, 50)  # 버튼 크기
BUTTON_POS = (SCREEN_WIDTH//2 - 100, SCREEN_HEIGHT//2 + 50)  # 버튼 위치

# 움직이는 플랫폼 설정
MOVING_PLATFORM_RANGE = 100  # 움직이는 거리


# 아이템 설정
ITEM_SIZE = 15  # 아이템의 크기
ITEM_SPAWN_CHANCE = 0.014  # 아이템 생성 확률 (0.4%)

# 아이템 종류
ITEM_TYPES = {
    'jump_boost': {
        'color': (0, 255, 0),  # 초록색
        'duration': 5,  # 사용 가능 횟수
        'effect': 'jump_power_multiplier',
        'value': 1.5  # 점프력 1.5배
    },
    'speed_reduce': {
        'color': (255, 0, 0),  # 빨간색
        'duration': 10,  # 지속 높이 (m)
        'effect': 'speed_multiplier',
        'value': 0.2  # 이동속도 절반
    },
    'double_jump': {
        'color': (255, 255, 0),  # 노란색
        'duration': 5,  # 사용 가능 횟수
        'effect': 'double_jump',
        'value': 1.0  # 이동속도 그대로
    }
}
