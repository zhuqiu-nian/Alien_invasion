import pygame.font
from pygame.sprite import Group
from ship import Ship


class Scoreboard:
    """显示得分信息"""

    def __init__(self, ai_game):
        """初始化各项属性"""
        self.ai_game = ai_game
        self.screen = ai_game.screen
        self.screen_rect = self.screen.get_rect()
        self.settings = ai_game.settings
        self.stats = ai_game.stats

        # 得分信息字体设置
        self.text_color = (30, 30, 30)
        self.font = pygame.font.SysFont(None, 48)
        # 初始化得分图像
        self.prep_score()
        # 初始化当前游戏等级图像
        self.prep_level()
        # 初始化剩余飞船显示图像
        self.prep_ships()

    def prep_score(self):
        """渲染为图像"""
        rounded_score = round(self.stats.score, -1)
        score_str = "{:,}".format(rounded_score)
        self.score_image = self.font.render(
            score_str, True, self.text_color, self.settings.bg_color)

        # 在右上角设置得分
        self.score_rect = self.score_image.get_rect()
        self.score_rect.right = self.screen_rect.right - 20
        self.score_rect.top = 20

    def show_score(self):
        """显示得分,等级,剩余飞船数"""
        self.screen.blit(self.score_image, self.score_rect)
        self.screen.blit(self.level_font_image, self.level_font_rect)
        self.screen.blit(self.level_image, self.level_rect)
        self.ships.draw(self.screen)

    def reset_score(self):
        """重置得分和等级和生命值"""
        self.stats.score = 0
        self.prep_score()
        self.stats.level = 1
        self.prep_level()
        self.prep_ships()

    def prep_level(self):
        """渲染游戏等级为图像"""
        level_str = str(self.stats.level)
        self.level_image = self.font.render(
            level_str, True, self.text_color, self.settings.bg_color)

        # 放置位置
        self.level_rect = self.level_image.get_rect()
        self.level_rect.right = self.score_rect.right
        self.level_rect.top = self.score_rect.bottom + 10

        # 显示level字样
        level_font = str('level:')
        self.level_font_image = self.font.render(
            level_font, True, self.text_color, self.settings.bg_color)
        self.level_font_rect = self.level_font_image.get_rect()
        self.level_font_rect.right = self.level_rect.left - 10
        self.level_font_rect.top = self.level_rect.top

    def prep_ships(self):
        """显示剩余生命（飞船）"""
        self.ships = Group()
        for ship_number in range(self.stats.ship_left):
            ship_live = Ship(self.ai_game)
            ship_live.rect.x = 10 + ship_number * ship_live.rect.width
            ship_live.rect.y = 10
            self.ships.add(ship_live)
