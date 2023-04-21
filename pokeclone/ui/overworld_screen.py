import logging

import pygame
import pytmx

from pokeclone.world import MOVE_SPEED, World
from pokeclone.ui.battle_screen import BattleScreen
from pokeclone.ui.screen import Screen, ScreenManager
from pokeclone.ui.settings import WINDOW_SIZE

LOGGER = logging.getLogger(__name__)


class OverworldScreen(Screen):
    def __init__(self, screen_manager: ScreenManager):
        super().__init__()
        self.screen_manager = screen_manager
        self.world = World()
        self.player_image = pygame.image.load(
            "data/sprites/overworld/player_standing.png"
        ).convert()
        # self.tmxdata = pytmx.TiledMap("data/tiled/overworld.tmx")
        self.tmxdata = pytmx.load_pygame("data/tiled/overworld.tmx")

    def update(self, dt: float):
        if (
            pygame.key.get_pressed()[pygame.K_LEFT]
            or pygame.key.get_pressed()[pygame.K_a]
        ) and self.world.player.x > 0:
            self.world.move(dt * MOVE_SPEED, left=True)
        elif (
            pygame.key.get_pressed()[pygame.K_RIGHT]
            or pygame.key.get_pressed()[pygame.K_d]
        ) and self.world.player.x < WINDOW_SIZE[0]:
            self.world.move(dt * MOVE_SPEED, right=True)
        if (
            pygame.key.get_pressed()[pygame.K_UP]
            or pygame.key.get_pressed()[pygame.K_w]
        ) and self.world.player.y < WINDOW_SIZE[1]:
            self.world.move(dt * MOVE_SPEED, up=True)
        elif (
            pygame.key.get_pressed()[pygame.K_DOWN]
            or pygame.key.get_pressed()[pygame.K_s]
        ) and self.world.player.y > 0:
            self.world.move(dt * MOVE_SPEED, down=True)
        if self.world.enemy:
            # an encounter has been generated!
            self.screen_manager.push(BattleScreen(self.screen_manager, self.world))

    def draw(self, surface: pygame.Surface):
        surface.blit(self.background, (0, 0))
        for x in range(0, 10):
            for y in range(0, 10):
                image = self.tmxdata.get_tile_image(x, y, 0)
                if image:
                    surface.blit(image, (x * 32, y * 32))
        self.draw_overworld(
            surface, self.player_image, self.world.player.x, self.world.player.y
        )

    @classmethod
    def draw_overworld(cls, surface: pygame.Surface, image, x, y):
        """Converts world coordinates to screen coordinates"""
        if image is None:
            return
        screen_y = WINDOW_SIZE[1] - y - image.get_height() / 2
        surface.blit(image, (x + image.get_width() / 2, screen_y))
