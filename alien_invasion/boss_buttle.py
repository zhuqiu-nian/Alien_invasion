import pygame
from pygame.sprite import Sprite


class Boss_buttle(Sprite):
    """管理boss射出子弹的类"""

    def __init__(self, ai_game):
        """生成子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.boss_bullet_color

        # 先生成子弹
        self.x_1 = float(ai_game.alien_boss.rect.midbottom)
        self.y_1 = float(-2.5 * self.x_1 + 1800)
        self.pos_1 = (self.x_1, self.y_1)

        self.x_2 = float(ai_game.alien_boss.rect.midbottom)
        self.y_2 = float(0)
        self.pos_2 = (self.x_2, self.y_2)

        self.x_3 = float(ai_game.alien_boss.rect.midbottom)
        self.y_3 = float(2.5 * self.x_3 - 1200)
        self.pos_3 = (self.x_3, self.y_3)

    def update(self):
        """子弹运动"""
        self.y_1 += self.settings.boss_buttle_speed
        self.x_1 = 720 - float(2 / 5) * self.y_1
        self.y_2 += self.settings.boss_buttle_speed
        self.y_3 += self.settings.boss_buttle_speed
        self.x_3 = 480 + float(2 / 5) * self.y_3

    def draw_bullet(self):
        # 绘制子弹
        pygame.draw.circle(screen, self.settings.boss_bullet_color,
                           self.pos_1, self.settings.boss_buttle_r, width=0)
        pygame.draw.circle(screen, self.settings.boss_bullet_color,
                           self.pos_2, self.settings.boss_buttle_r, width=0)
        pygame.draw.circle(screen, self.settings.boss_bullet_color,
                           self.pos_3, self.settings.boss_buttle_r, width=0)
