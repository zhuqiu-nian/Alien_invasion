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
        self.y_1 = self.y
        self.y_2 = self.y
        self.y_3 = self.y

    def update(self):
        """子弹运动"""
        self.y_1 += self.settings.boss_bullet_speed
        self.x_1 = 720 - float(2 / 5) * self.y_1
        self.pos_1 = (self.x_1, self.y_1)
        self.y_2 += self.settings.boss_bullet_speed
        self.pos_2 = (self.x, self.y_2)
        self.y_3 += self.settings.boss_bullet_speed
        self.x_3 = 480 + float(2 / 5) * self.y_3
        self.pos_3 = (self.x_3, self.y_3)

    def draw_bullet(self):
        # 绘制子弹
        pygame.draw.circle(self.screen, self.settings.boss_bullet_color,
                           self.pos_1, self.settings.boss_bullet_r, width=0)
        pygame.draw.circle(self.screen, self.settings.boss_bullet_color,
                           self.pos_2, self.settings.boss_bullet_r, width=0)
        pygame.draw.circle(self.screen, self.settings.boss_bullet_color,
                           self.pos_3, self.settings.boss_bullet_r, width=0)
