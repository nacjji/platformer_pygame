import pygame
from .base_controller import BaseController


class KeyboardController(BaseController):
    def __init__(self):
        self.left_pressed = False
        self.right_pressed = False
        self.jump_pressed = False

    def update(self, events):
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = True
                elif event.key == pygame.K_RIGHT:
                    self.right_pressed = True
                elif event.key == pygame.K_SPACE:
                    self.jump_pressed = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.left_pressed = False
                elif event.key == pygame.K_RIGHT:
                    self.right_pressed = False
                elif event.key == pygame.K_SPACE:
                    self.jump_pressed = False

    def get_movement(self):
        horizontal = 0
        if self.left_pressed:
            horizontal -= 1
        if self.right_pressed:
            horizontal += 1
        return horizontal, self.jump_pressed
