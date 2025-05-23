import platform
import pygame
from .keyboard_controller import KeyboardController
from .joystick_controller import JoystickController


class ControllerFactory:
    @staticmethod
    def create_controller():
        """
        플랫폼에 따라 적절한 컨트롤러를 생성합니다.
        Returns:
            BaseController: 키보드 또는 조이스틱 컨트롤러
        """
        # 모바일 플랫폼 확인
        system = platform.system().lower()
        is_mobile = system in ['ios', 'android'] or (
            system == 'darwin' and platform.machine().startswith('iP'))

        # 터치스크린 지원 확인
        has_touch = False
        if pygame.display.get_init():
            try:
                has_touch = pygame.display.get_surface().get_flags() & pygame.FINGERDOWN
            except:
                pass

        return JoystickController() if (is_mobile or has_touch) else KeyboardController()
