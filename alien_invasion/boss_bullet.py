import sys
import pygame
from pygame.sprite import Sprite
from time import sleep


class Boss_bullet(Sprite):
    """管理boss射出子弹的类"""

    def __init__(self, ai_game):
        """生成子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.boss_bullet_color

        (self.x, self.y) = ai_game.alien_boss.rect.midbottom
        self.y_2 = self.y

        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)

    def update(self):
        """子弹运动"""

        self.y_2 += self.settings.boss_bullet_speed
        self.pos_2 = (self.x, self.y_2)

    def draw_bullet(self):
        # 绘制子弹

        pygame.draw.circle(self.screen, self.settings.boss_bullet_color,
                           self.pos_2, self.settings.boss_bullet_r, width=0)
