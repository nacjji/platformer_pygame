import asyncio
import pygame

from src.game import Game


async def main():
    game = Game()
    while True:
        game.run()
        await asyncio.sleep(0)  # 브라우저가 응답할 수 있도록 제어권을 양보

asyncio.run(main())
