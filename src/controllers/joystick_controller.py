import pygame
import math
from .base_controller import BaseController


class JoystickController(BaseController):
    def __init__(self):
        # 조이스틱 위치 및 크기 설정
        self.joystick_pos = (100, 400)  # 화면 왼쪽 아래
        self.joystick_radius = 50
        self.handle_radius = 20
        self.handle_pos = self.joystick_pos
        self.is_active = False

        # 점프 버튼 설정
        self.jump_button_pos = (700, 400)  # 화면 오른쪽 아래
        self.jump_button_radius = 30
        self.jump_pressed = False

    def update(self, events):
        for event in events:
            if event.type == pygame.MOUSEBUTTONDOWN or (
                    event.type == pygame.FINGERDOWN and hasattr(event, 'x')):
                # 터치/마우스 위치 계산
                pos = pygame.mouse.get_pos() if event.type == pygame.MOUSEBUTTONDOWN else (
                    event.x * pygame.display.get_surface().get_width(),
                    event.y * pygame.display.get_surface().get_height()
                )

                # 조이스틱 영역 확인
                if self._distance(pos, self.joystick_pos) <= self.joystick_radius:
                    self.is_active = True
                    self.handle_pos = pos

                # 점프 버튼 영역 확인
                if self._distance(pos, self.jump_button_pos) <= self.jump_button_radius:
                    self.jump_pressed = True

            elif event.type == pygame.MOUSEBUTTONUP or (
                    event.type == pygame.FINGERUP and hasattr(event, 'x')):
                self.is_active = False
                self.handle_pos = self.joystick_pos
                self.jump_pressed = False

            elif (event.type == pygame.MOUSEMOTION or
                  (event.type == pygame.FINGERMOTION and hasattr(event, 'x'))) and self.is_active:
                # 터치/마우스 드래그 처리
                pos = pygame.mouse.get_pos() if event.type == pygame.MOUSEMOTION else (
                    event.x * pygame.display.get_surface().get_width(),
                    event.y * pygame.display.get_surface().get_height()
                )

                # 조이스틱 제한 범위 계산
                distance = self._distance(pos, self.joystick_pos)
                if distance <= self.joystick_radius:
                    self.handle_pos = pos
                else:
                    # 최대 범위로 제한
                    angle = math.atan2(
                        pos[1] - self.joystick_pos[1],
                        pos[0] - self.joystick_pos[0]
                    )
                    self.handle_pos = (
                        self.joystick_pos[0] +
                        math.cos(angle) * self.joystick_radius,
                        self.joystick_pos[1] +
                        math.sin(angle) * self.joystick_radius
                    )

    def get_movement(self):
        if not self.is_active:
            return 0, self.jump_pressed

        # 조이스틱 방향 계산
        dx = self.handle_pos[0] - self.joystick_pos[0]
        threshold = self.joystick_radius * 0.3

        if abs(dx) < threshold:
            return 0, self.jump_pressed
        return 1 if dx > 0 else -1, self.jump_pressed

    def draw(self, screen):
        # 조이스틱 베이스 그리기
        pygame.draw.circle(screen, (100, 100, 100),
                           self.joystick_pos, self.joystick_radius)
        # 조이스틱 핸들 그리기
        pygame.draw.circle(screen, (150, 150, 150),
                           self.handle_pos, self.handle_radius)
        # 점프 버튼 그리기
        color = (200, 100, 100) if self.jump_pressed else (150, 150, 150)
        pygame.draw.circle(screen, color, self.jump_button_pos,
                           self.jump_button_radius)

    @staticmethod
    def _distance(pos1, pos2):
        return math.sqrt((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)
