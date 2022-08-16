import pygame
from pygame.sprite import Sprite


class Ship(Sprite):

    def __init__(self, ai_game):
        """初始化飞船"""
        super().__init__()
        self.screen = ai_game.screen
        self.settings = ai_game.settings
        self.screen_rect = ai_game.screen.get_rect()

        self.image = pygame.image.load('images/ship.png')
        self.rect = self.image.get_rect()

        # 把飞船置于屏幕中间底端
        self.rect.midbottom = self.screen_rect.midbottom

        # 在属性x里储存小数值
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)

        # 移动标志
        self.moving_right = False
        self.moving_left = False
        self.moving_up = False
        self.moving_down = False

    def update(self):
        """移动飞船"""
        # 计算飞船位置
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.x += self.settings.ship_speed
        if self.moving_left and self.rect.left > 0:
            self.x -= self.settings.ship_speed
        if self.moving_up and self.rect.top > 0:
            self.y -= self.settings.ship_speed
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.y += self.settings.ship_speed
        # 更新飞船位置
        self.rect.x = self.x
        self.rect.y = self.y

    def blitme(self):
        """绘制飞船"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """重生飞船"""
        self.rect.midbottom = self.screen_rect.midbottom
        # 重置坐标跟随
        self.x = float(self.rect.x)
        self.y = float(self.rect.y)
