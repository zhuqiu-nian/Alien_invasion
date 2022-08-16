import pygame
from pygame.sprite import Sprite


class Buttle(Sprite):
    def __init__(self, ai_game):
        """生成子弹"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.color = self.settings.bullet_color

        # 先生成子弹
        self.rect = pygame.Rect(
            0, 0, self.settings.bullet_width, self.settings.bullet_height)
        self.rect.midtop = ai_game.ship.rect.midtop

        # 储存小数子弹位置
        self.y = float(self.rect.y)

    def update(self):
        """子弹运动"""
        self.y -= self.settings.bullet_speed
        self.rect.y = self.y

    def draw_bullet(self):
        # 绘制子弹
        pygame.draw.rect(self.screen, self.color, self.rect)
