import os
import sys

# 웹 캔버스 설정
CANVAS_WIDTH = 450
CANVAS_HEIGHT = 800

# 웹 배포 설정
__EMSCRIPTEN__ = True
PYGAME_FULL_SCREEN = False

# 키보드 이벤트 매핑
KEY_MAP = {
    "ArrowLeft": "LEFT",
    "ArrowRight": "RIGHT",
    "Space": "SPACE",
    "KeyR": "r"
}

# 터치 스크린 지원 설정
TOUCH_ENABLED = True
TOUCH_CONTROL_SIZE = 50  # 터치 컨트롤 버튼 크기
