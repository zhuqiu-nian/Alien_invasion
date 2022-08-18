class Settings:
    """储存设置"""

    def __init__(self):
        # 屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (186, 205, 207)

        # 飞船设置
        self.ship_speed = 1.5
        self.ship_limit = 3

        # 子弹设置
        self.bullet_speed = 3.0
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (60, 60, 60)

        # 外星人设置
        self.alien_speed = 0.4
        self.fleet_drop_speed = 12
        self.fleet_direction = 1

        # boss设置
        self.alien_boss_hp = 25  # 修改hp还要在alien_boss的recover方法里修改
        self.boss_bullet_speed = 0.5
        self.boss_bullet_r = 2
        self.boss_bullet_color = (231, 66, 52)
        # boss是否开火的计数
        self.boss_move = 0
        # boss开火标志
        self.boss_fire = True
        # boss当前发射子弹计数
        self.boss_bullets = 0
        # 允许boss一次性最多发射的子弹数
        self.boss_max_bullets = 10

        # 加快游戏节奏
        self.speedup_scale = 1.3
        # 提高外星人分数
        self.score_scale = 1.5

        self.initialize_dynamic_settiings()

    def initialize_dynamic_settiings(self):
        """初始化游戏进行而变化的设置"""
        self.ship_speed = 1.5
        self.bullet_speed = 3.0
        self.alien_speed = 0.4
        self.fleet_direction = 1
        # 计分
        self.alien_points = 150

    def increase_speed(self):
        """提高速度设置，提高外星人分数设置"""
        self.ship_speed *= self.speedup_scale
        self.bullet_speed *= self.speedup_scale
        self.alien_speed *= self.speedup_scale
        self.alien_points = int(self.alien_points * self.score_scale)
