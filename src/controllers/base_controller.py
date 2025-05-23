from abc import ABC, abstractmethod


class BaseController(ABC):
    @abstractmethod
    def get_movement(self):
        """
        Returns:
            tuple: (horizontal_movement(-1, 0, 1), is_jump_pressed(bool))
        """
        pass

    @abstractmethod
    def update(self, events):
        """이벤트를 처리하고 컨트롤러 상태를 업데이트합니다."""
        pass
