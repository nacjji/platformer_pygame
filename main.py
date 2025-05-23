import asyncio
import pygame
from src.game import Game


async def main():
    pygame.init()
    game = Game()

    while True:
        game.run()
        await asyncio.sleep(0)  # 웹 환경에서 필요한 비동기 처리

asyncio.run(main())
