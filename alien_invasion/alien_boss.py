import pygame
from pygame.sprite import Sprite


class Alien_Boss(Sprite):
    """表示外星人boss的类"""

    def __init__(self, ai_game):
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        # 载入boss图像
        self.image = pygame.image.load('images/alien_boss.png')
        self.rect = self.image.get_rect()

        # 每个外星人初始在左上角
        self.rect.x = self.rect.width
        self.rect.y = self.rect.height

        self.x = float(self.rect.x)

    def check_edges(self):
        """位于屏幕边缘时返回True"""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right or self.rect.left <= 0:
            return True

    def update(self):
        """移动外星人"""
        self.x += (self.settings.alien_speed * self.settings.fleet_direction)
        self.rect.x = self.x
        self.settings.boss_move += 10

    def recover(self):
        """boss回复生命值"""
        self.settings.alien_boss_hp = 25
