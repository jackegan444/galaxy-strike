import math
import random
import time
import pygame
from pygame import mixer


class Player:
    """""The player ship"""

    playerImg = pygame.image.load('sprites/playerShip.png')

    def __init__(self):
        self.xcoord = 370
        self.ycoord = 480
        self.xcoord_change = 0
        self.fire_speed = 0.75
        self.bullet_state = "ready"

    def blit(self):
        screen.blit(self.playerImg, (self.xcoord, self.ycoord))

    def move(self):
        self.xcoord += self.xcoord_change
        if self.xcoord < 0:
            self.xcoord = 0
        elif self.xcoord > 736:
            self.xcoord = 736


class Bullet:
    """""Basic projectile"""

    player_bulletImg = pygame.image.load('sprites/player_lasers.png')
    enemy_bulletImg = pygame.image.load('sprites/enemy_laser.png')

    def __init__(self, x, y, y_change, bullet_type):
        self.bulletX = x
        self.bulletY = y
        self.bulletX_change = 0
        self.bulletY_change = y_change
        self.went_offscreen = False
        self.img = None
        if bullet_type == "player":
            self.img = self.player_bulletImg
        elif bullet_type == "enemy":
            self.img = self.enemy_bulletImg
        bulletSound = mixer.Sound("audio/laser.wav")
        bulletSound.play()

    def blit(self):
        screen.blit(self.img, (self.bulletX, self.bulletY + 10))


class Enemy:
    """"Basic enemy class"""
    left_sprite = pygame.image.load('sprites/enemy1_left.png')
    right_sprite = pygame.image.load('sprites/enemy1_right.png')
    start_sprite = right_sprite
    starting_hp = 1
    point_value = 1
    starting_xcoord_change = 3
    starting_ycoord_change = 64

    def __init__(self):
        self.current_sprite = self.start_sprite
        self.hp = self.starting_hp
        self.xcoord = random.randint(0, 735)
        self.ycoord = random.randint(0, 2) * 64
        self.xcoord_change = self.starting_xcoord_change
        self.ycoord_change = self.starting_ycoord_change
        self.startingy_coord = self.ycoord
        self.last_fire = random.random() * -3
        self.fire_delay = 3

    def start_firing(self):
        self.last_fire += time.time()

    def blit(self):
        screen.blit(self.current_sprite, (self.xcoord, self.ycoord))

    def reset_hp(self):
        self.hp = self.starting_hp

    def move(self):
        self.xcoord += self.xcoord_change
        if self.xcoord < 0:
            self.xcoord_change = 4
            self.ycoord += self.ycoord_change
            self.current_sprite = self.right_sprite
        elif self.xcoord >= 736:
            self.xcoord_change = -4
            self.ycoord += self.ycoord_change
            self.current_sprite = self.left_sprite


class StrongEnemy(Enemy):
    """""Enemy that takes 3 hits to kill"""

    ne_sprite = pygame.image.load('sprites/enemy2_ne.png')
    nw_sprite = pygame.image.load('sprites/enemy2_nw.png')
    se_sprite = pygame.image.load('sprites/enemy2_se.png')
    sw_sprite = pygame.image.load('sprites/enemy2_sw.png')
    start_sprite = ne_sprite
    starting_hp = 3
    point_value = 5
    starting_xcoord_change = 3
    starting_ycoord_change = 3

    def __init__(self):
        super(StrongEnemy, self).__init__()
        self.going_down = True
        self.going_right = True

    def move(self):
        self.xcoord += self.xcoord_change
        self.ycoord += self.ycoord_change
        if self.ycoord < (self.startingy_coord - 100):
            self.ycoord_change = 3
            self.going_down = True

        elif self.ycoord >= (self.startingy_coord + 200):
            self.ycoord_change = -3
            self.going_down = False

        if self.xcoord < 0:
            self.xcoord_change = 3
            self.going_right = True
        elif self.xcoord >= 736:
            self.xcoord_change = -3
            self.going_right = False

        if self.going_down and self.going_right:
            self.current_sprite = self.se_sprite
        elif self.going_down and not self.going_right:
            self.current_sprite = self.sw_sprite
        elif not self.going_down and self.going_right:
            self.current_sprite = self.ne_sprite
        elif not self.going_down and not self.going_right:
            self.current_sprite = self.nw_sprite


class PowerUp:
    sprite = pygame.image.load('sprites/power_up.png')

    def __init__(self):
        self.xcoord = random.randint(32, 768)
        self.ycoord = random.randint(32, 400)

    def blit(self):
        screen.blit(self.sprite, (self.xcoord, self.ycoord))

    def isHit(self, player):
        player.fire_speed -= 0.25
        return player


class Background:
    """""Scrolling space background"""

    def __init__(self):
        self.bg_image = pygame.image.load('space_scrolling.png')
        self.bg_rect = self.bg_image.get_rect()
        self.ycoord = 3000

    def scroll(self):
        screen.blit(self.bg_image, self.bg_rect, (0, self.ycoord, 800, 600))
        if self.ycoord == 0:
            self.ycoord = 3000
        else:
            self.ycoord -= 1.5


class TitleScreen:
    def __init__(self):
        pass

    def display(self):
        screen.fill((0, 0, 0))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    return False

        background.scroll()
        title_text = large_font.render("GALAXY STRIKE", True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(SCREEN_LENGTH / 2, (SCREEN_WIDTH / 2) - 40))
        title_text2 = large_font.render("press spacebar to start", True, (255, 255, 255))
        title_rect2 = title_text.get_rect(center=((SCREEN_LENGTH / 2) - 100, (SCREEN_WIDTH / 2) + 40))

        screen.blit(title_text, title_rect)
        screen.blit(title_text2, title_rect2)

        pygame.display.update()
        clock.tick_busy_loop(100)
        return True


class GameInstance:
    display_scoreX = 10
    display_scoreY = 10

    def __init__(self):
        self.player = Player()
        self.enemies = []
        self.bullets = []
        self.enemy_bullets = []
        self.power_ups = []
        self.power_ups_spawned = 0
        self.display_power_up_msg = False
        self.power_up_message = small_font.render("POWER UP AQUIRED: INCREASED FIRE SPEED", True,
                                                  (255, 255, 255))
        self.power_up_msg_time_holder = 0
        self.score_value = 0
        self.game_over = False
        self.bullet_time_holder = time.time()
        self.game_start_time = time.time()
        self.enemy_spawn_time_holder = time.time()
        self.enemy_spawn_delay = 3
        self.enemies_spawned = 0
        self.initialize()

    def initialize(self):
        self.player = Player()
        self.bullets = []
        self.enemy_bullets = []
        for i in range(6):
            self.enemies.append(Enemy())
            self.enemies[i].start_firing()
        self.enemies.append(StrongEnemy())
        self.enemies_spawned = 7
        self.score_value = 0
        self.enemy_spawn_delay = 2
        self.power_ups = []
        self.power_ups_spawned = 0
        self.game_over = False

    def show_score(self, x, y):
        score = small_font.render("Score : " + str(self.score_value), True, (255, 255, 255))
        screen.blit(score, (x, y))

    def spawn_enemies(self):
        if time.time() > self.enemy_spawn_time_holder + self.enemy_spawn_delay:
            self.enemies.append(Enemy())
            self.enemies_spawned += 1
            self.enemy_spawn_time_holder = time.time()
        if self.enemies_spawned == 11:
            self.enemy_spawn_delay = 1.5
        elif self.enemies_spawned == 15:
            self.enemy_spawn_delay = 1
        elif self.enemies_spawned == 24:
            self.enemy_spawn_delay = 0.75
        elif self.enemies_spawned == 40:
            self.enemy_spawn_delay = 0.5

    def spawn_power_ups(self):
        if self.score_value == 0 and self.power_ups_spawned == 0:
            self.power_ups.append(PowerUp())
            self.power_ups_spawned += 1
        elif self.score_value == 12 and self.power_ups_spawned == 1:
            self.power_ups.append(PowerUp())
            self.power_ups_spawned += 1
        elif self.score_value == 18 and self.power_ups_spawned == 2:
            self.power_ups.append(PowerUp())
            self.power_ups_spawned += 1
        elif self.score_value == 24 and self.power_ups_spawned == 3:
            self.power_ups.append(PowerUp())
            self.power_ups_spawned += 1

    def game_loop(self):
        screen.fill((0, 0, 0))
        background.scroll()

        # event check
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.player.xcoord_change += -5
                if event.key == pygame.K_RIGHT:
                    self.player.xcoord_change += 5
                if event.key == pygame.K_SPACE:
                    if self.player.bullet_state == "ready" and not self.game_over:
                        self.bullets.append(Bullet(self.player.xcoord, self.player.ycoord, -10, "player"))
                        self.player.bullet_state = "fire"
                        self.bullet_time_holder = time.time()

                if event.key == pygame.K_r:
                    if self.game_over:
                        self.enemies = []
                        self.initialize()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    self.player.xcoord_change += 5
                if event.key == pygame.K_RIGHT:
                    self.player.xcoord_change += -5

        self.player.move()

        self.spawn_enemies()

        for i in reversed(range(len(self.enemies))):

            # Game Over
            if self.enemies[i].ycoord > 448:
                self.game_over = True
                game_over_text()
                break

            self.enemies[i].move()

            if time.time() - self.enemies[i].fire_delay > self.enemies[i].last_fire:
                self.enemy_bullets.append(Bullet(self.enemies[i].xcoord, self.enemies[i].ycoord, 5, "enemy"))
                self.enemies[i].last_fire = time.time()

            # enemy collision
            for j in reversed(range(len(self.bullets))):
                if isCollision(self.enemies[i].xcoord + 32, self.enemies[i].ycoord + 32,
                               self.bullets[j].bulletX + 32,
                               self.bullets[j].bulletY + 32, 32):
                    self.enemies[i].hp -= 1
                    if self.enemies[i].hp == 0:
                        self.score_value += self.enemies[i].point_value
                    explosionSound = mixer.Sound("audio/explosion.wav")
                    explosionSound.play()
                    self.bullets.pop(j)

            self.enemies[i].blit()

            if self.enemies[i].hp == 0:
                self.enemies.pop(i)

        for i in reversed(range(len(self.enemy_bullets))):
            if isCollision(self.player.xcoord + 32, self.player.ycoord + 32,
                           self.enemy_bullets[i].bulletX + 32,
                           self.enemy_bullets[i].bulletY + 32, 32) or self.game_over:
                self.game_over = True
                game_over_text()
                break

        for i in reversed(range(len(self.bullets))):

            self.bullets[i].bulletY += self.bullets[i].bulletY_change
            self.bullets[i].blit()

            if self.bullets[i].bulletY < -32:
                self.bullets.pop(i)

        for i in (range(len(self.enemy_bullets))):
            self.enemy_bullets[i].blit()
            self.enemy_bullets[i].bulletY += self.enemy_bullets[i].bulletY_change

        self.spawn_power_ups()
        for i in reversed(range(len(self.power_ups))):
            self.power_ups[i].blit()
            for j in reversed(range(len(self.bullets))):
                if isCollision(self.power_ups[i].xcoord + 64, self.power_ups[i].ycoord + 64,
                               self.bullets[j].bulletX + 32,
                               self.bullets[j].bulletY + 32, 48):
                    power_up_sound = mixer.Sound("audio/power_up.wav")
                    power_up_sound.play()
                    self.player = self.power_ups[i].isHit(self.player)
                    self.display_power_up_msg = True
                    self.power_up_msg_time_holder = time.time()
                    self.power_ups.pop(i)
                    self.bullets.pop(j)

        if time.time() < self.power_up_msg_time_holder + 3:
            screen.blit(self.power_up_message, (60, 100))

        self.player.blit()
        if self.player.bullet_state == "fire":

            if time.time() > (self.bullet_time_holder + self.player.fire_speed):
                self.player.bullet_state = "ready"

        self.show_score(self.display_scoreX, self.display_scoreY)
        pygame.display.update()
        clock.tick(100)


def game_over_text():
    screen.blit(over_text1, over_rect1)
    screen.blit(over_text2, over_rect2)


def isCollision(targetX, targetY, bulletX, bulletY, hitbox):
    isHit = False
    distance = math.sqrt(math.pow(targetX - bulletX, 2) + (math.pow(targetY - bulletY, 2)))
    if distance < hitbox:
        isHit = True
    return isHit


pygame.init()

# Clock for framerate limit
clock = pygame.time.Clock()

SCREEN_LENGTH = 800
SCREEN_WIDTH = 600
screen = pygame.display.set_mode((SCREEN_LENGTH, SCREEN_WIDTH))

background = Background()

mixer.music.load("audio/background_music.wav")
mixer.music.play(-1)

pygame.display.set_caption("Galaxy Strike")
icon = pygame.image.load('sprites/playerShip.png')
pygame.display.set_icon(icon)

small_font = pygame.font.Font('FORCED SQUARE.ttf', 32)
large_font = pygame.font.Font('FORCED SQUARE.ttf', 64)
over_text1 = large_font.render("GAME OVER", True, (255, 255, 255))
over_rect1 = over_text1.get_rect(center=(SCREEN_LENGTH / 2, (SCREEN_WIDTH / 2) - 40))
over_text2 = large_font.render("Press R to restart", True, (255, 255, 255))
over_rect2 = over_text2.get_rect(center=((SCREEN_LENGTH / 2), (SCREEN_WIDTH / 2) + 20))

title_screen = TitleScreen()
game_instance = None
running = True
display_title_screen = True
while running:

    while display_title_screen:
        if not title_screen.display():
            display_title_screen = False
            game_instance = GameInstance()
    if not display_title_screen:
        game_instance.game_loop()
