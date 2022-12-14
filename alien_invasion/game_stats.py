class GameStats:
    """统计信息"""

    def __init__(self, ai_game):
        """初始化游戏信息"""
        self.settings = ai_game.settings
        self.reset_stats()

        self.game_active = False

    def reset_stats(self):
        """初始化统计信息项"""
        self.ship_left = self.settings.ship_limit
        self.score = 0
        self.level = 1
        self.boos_set = False

    def check_level(self):
        """对游戏等级做出的响应"""
        if self.level % 3 == 0:
            self.boos_set = True
        else:
            self.boos_set = False
