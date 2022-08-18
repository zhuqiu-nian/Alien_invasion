import sys
import pygame
from time import sleep
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
from bullet import Bullet
from alien import Alien
from alien_boss import Alien_Boss
from boss_bullet import Boss_bullet


class AlienInvasion:
    def __init__(self):
        """"游戏初始化"""
        pygame.init()
        self.settings = Settings()
        self.screen = pygame.display.set_mode(
            (self.settings.screen_width, self.settings.screen_height))

        pygame.display.set_caption("Alien Invasion")

        # 储存统计信息
        self.stats = GameStats(self)

        # 载入飞船
        self.ship = Ship(self)

        # 储存子弹
        self.bullets = pygame.sprite.Group()
        self.boss_bullets = pygame.sprite.Group()

        # 储存外星人
        self.aliens = pygame.sprite.Group()
        self._create_fleet()

        self.aliens_boss = pygame.sprite.Group()

        # 创建开始按钮
        self.play_button = Button(self, "Play")

        # 创建计分牌
        self.sb = Scoreboard(self)

    def run_game(self):
        """开始游戏主循环"""
        while True:
            self._check_events()

            if self.stats.game_active:
                self.ship.update()
                self._update_bullets()
                self._update_boss_bullets()
                self._update_aliens()

            self._update_screen()

    def _create_fleet(self):
        """创建外星人群"""

        # 计算外星人数量
        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        available_space_x = self.settings.screen_width - 2 * alien_width
        number_alien_x = available_space_x // (2 * alien_width)
        ship_height = self.ship.rect.height
        available_space_y = (self.settings.screen_height -
                             (3 * alien_height) - ship_height)
        number_rows = available_space_y // (2 * alien_height) - 1

        # 生成外星人或boss
        if not self.stats.boos_set:
            for row_number in range(number_rows - 1):
                for alien_number in range(number_alien_x - 1):
                    self._create_alien(alien_number, row_number)
        else:
            self._create_boss_alien()

    def _create_alien(self, alien_number, row_number):
        """生成外星人"""

        alien = Alien(self)
        alien_width, alien_height = alien.rect.size
        alien.x = alien_width + 2 * alien_width * alien_number
        alien.rect.x = alien.x
        alien.rect.y = alien.rect.y + 2 * alien.rect.height * row_number + 50
        self.aliens.add(alien)

    def _create_boss_alien(self):
        """生成外星人boss"""
        self.alien_boss = Alien_Boss(self)
        self.alien_boss.rect.x = 100
        self.alien_boss.rect.y = 25
        self.aliens_boss.add(self.alien_boss)

    def _boss_fire(self):
        """boss发射子弹"""
        new_boss_bullet = Boss_bullet(self)
        self.boss_bullets.add(new_boss_bullet)

    def _update_boss_bullets(self):
        """更新boss子弹"""

        # boss开火,这个地方判定有点多，主要是想做出boos一次性发射部分子弹，并且发射期间有一定间隔的效果
        # 后续应该要优化
        if self.aliens_boss:
            if self.settings.boss_move % 2000 == 0:
                self.settings.boss_bullets += 1
                if self.settings.boss_fire:
                    self._boss_fire()
                if self.settings.boss_bullets % self.settings.boss_max_bullets == 0:
                    self.settings.boss_fire = False
                if self.settings.boss_bullets % 15 == 0:
                    self.settings.boss_fire = True

        # 子弹前进
        self.boss_bullets.update()

        # 检测有没有击中飞船
        self._check_bullet_ship_collisions()

    def _update_aliens(self):
        """鉴定要更新谁"""
        if not self.stats.boos_set:
            self._update_alien_mob()
        else:
            self._update_alien_boss()

    def _update_alien_mob(self):
        """检查边缘，更新小怪位置"""

        self._check_fleet_edges()
        self.aliens.update()

        # 检测外星人和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens):
            self._ship_hit()

        # 检测外星人和屏幕底端的碰撞
        self._check_aliens_bottom()

    def _update_alien_boss(self):
        """检查边缘，更新boss位置,控制开火"""

        # 检查边缘
        self._check_boss_edges()
        self.aliens_boss.update()

        # 检测boss和飞船的碰撞
        if pygame.sprite.spritecollideany(self.ship, self.aliens_boss):
            self._ship_hit()

    def _check_bullet_ship_collisions(self):
        """检测boss子弹和飞船的碰撞"""
        if pygame.sprite.spritecollideany(self.ship, self.boss_bullets):
            self._ship_hit()

    def _ship_hit(self):
        """飞船被外星人撞毁"""

        if self.stats.ship_left > 0:
            # 飞船生命值减一
            self.stats.ship_left -= 1
            self.sb.prep_ships()

            # 清空屏幕上的外星人和子弹
            self.aliens.empty()
            self.bullets.empty()
            self.aliens_boss.empty()
            self.boss_bullets.empty()

            # 重新生成外星人和飞船
            self._create_fleet()
            self.ship.center_ship()

            # 暂停
            sleep(0.5)
        else:
            self.stats.game_active = False
            pygame.mouse.set_visible(True)

    def _check_boss_edges(self):
        """boss边界检查"""
        for alien_boss in self.aliens_boss.sprites():
            if alien_boss.check_edges():
                self._change_fleet_direction()
                break

    def _check_fleet_edges(self):
        """外星人边界检查"""
        for alien in self.aliens.sprites():
            if alien.check_edges():
                # 位于边缘时下移并改变方向
                self._change_fleet_direction()
                break

    def _change_fleet_direction(self):
        """外星人下移"""
        for alien in self.aliens.sprites():
            alien.rect.y += self.settings.fleet_drop_speed
        self.settings.fleet_direction *= -1

    def _check_aliens_bottom(self):
        """检查外星人是否到达底端"""
        screen_rect = self.screen.get_rect()
        for alien in self.aliens.sprites():
            if alien.rect.bottom >= screen_rect.bottom:
                self._ship_hit()
                break

    def _check_events(self):
        """响应按键和鼠标"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                self._check_keydown_events(event)
            elif event.type == pygame.KEYUP:
                self._check_keyup_events(event)
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                self._check_play_button(mouse_pos)

    def _check_play_button(self, mouse_pos):
        """单击play时开始游戏"""
        if self.play_button.rect.collidepoint(mouse_pos) and not self.stats.game_active:
            # 重置游戏
            self.stats.game_active = True
            self.stats.reset_stats()
            self.sb.reset_score()
            self.aliens.empty()
            self.bullets.empty()
            self._create_fleet()
            self.ship.center_ship()
            self.settings.initialize_dynamic_settiings()
            # 隐藏鼠标光标
            pygame.mouse.set_visible(False)

    def _check_keydown_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = True
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = True
        elif event.key == pygame.K_UP:
            self.ship.moving_up = True
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = True
        elif event.key == pygame.K_ESCAPE:
            sys.exit()
        elif event.key == pygame.K_SPACE:
            self._fire_bullet()
        elif event.key == pygame.K_0:
            self.aliens.empty()

    def _check_keyup_events(self, event):
        if event.key == pygame.K_RIGHT:
            self.ship.moving_right = False
        elif event.key == pygame.K_LEFT:
            self.ship.moving_left = False
        elif event.key == pygame.K_UP:
            self.ship.moving_up = False
        elif event.key == pygame.K_DOWN:
            self.ship.moving_down = False

    def _fire_bullet(self):
        """发射子弹"""

        new_bullet = Bullet(self)
        self.bullets.add(new_bullet)

    def _update_bullets(self):
        """更新子弹"""

        # 子弹前进
        self.bullets.update()

        # 删除屏幕外子弹
        for bullet in self.bullets.copy():
            if bullet.rect.bottom <= 0:
                self.bullets.remove(bullet)

        self._check_bullet_alien_collisions()

    def _check_bullet_alien_collisions(self):
        """响应子弹和外星人碰撞"""

        # 删除碰撞的子弹和外星人
        collisions = pygame.sprite.groupcollide(
            self.bullets, self.aliens, True, True)
        if collisions:
            for aliens in collisions.values():
                self.stats.score += self.settings.alien_points * len(aliens)
                self.sb.prep_score()

        # boss击杀检测:
        collisions_boss = pygame.sprite.groupcollide(
            self.bullets, self.aliens_boss, True, False)
        if collisions_boss:
            self.settings.alien_boss_hp -= 1
        if self.settings.alien_boss_hp <= 0:
            self.aliens_boss.empty()
            self.settings.boss_move = 0
            self.alien_boss.recover()
            self.settings.boss_bullets = 0

        # 外星人被清空后，刷新一批外星人或boss,并提高游戏等级
        if not self.aliens and not self.aliens_boss:
            self.bullets.empty()
            self.stats.level += 1
            self.stats.check_level()
            self._create_fleet()
            self.settings.increase_speed()
            self.sb.prep_level()

    def _update_screen(self):
        """更新屏幕"""
        self.screen.fill(self.settings.bg_color)
        self.ship.blitme()
        for bullet in self.bullets.sprites():
            bullet.draw_bullet()
        for boss_bullet in self.boss_bullets.sprites():
            boss_bullet.draw_bullet()
        if not self.stats.boos_set:
            self.aliens.draw(self.screen)
        else:
            self.aliens_boss.draw(self.screen)

        # 显示积分牌
        self.sb.show_score()

        # 非活动时显示Play
        if not self.stats.game_active:
            self.play_button.draw_button()

        pygame.display.flip()


if __name__ == '__main__':
    ai = AlienInvasion()
    ai.run_game()
