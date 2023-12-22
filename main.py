import pygame
import time
import math

pygame.init()
difficulty = []
#тут должны быть кортежи, в котором в зависимости от сложности хранят определенное количество кортежей с информацией о противнике


class Player(pygame.sprite.Sprite):
    sprite = pygame.image.load("player_pyg.png")

    def __init__(self, *group, posx, posy, max_x, max_y):
        super().__init__(*group)

        self.total_speed = 3
        self.size = (48, 48)

        self.image = pygame.transform.scale(Player.sprite, self.size)
        self.speed = [0, 0]
        self.rect = self.image.get_rect()
        self.rect.x = posx
        self.rect.y = posy
        self.max_x = max_x
        self.max_y = max_y

    def update(self, *args):
        if args and args[0].type == pygame.KEYDOWN:
            self.speed = [pygame.key.get_pressed()[pygame.K_d] * self.total_speed +
                          pygame.key.get_pressed()[pygame.K_a] * -self.total_speed,
                          pygame.key.get_pressed()[pygame.K_s] * self.total_speed +
                          pygame.key.get_pressed()[pygame.K_w] * -self.total_speed]

        if args and args[0].type == pygame.KEYUP:
            self.speed = [pygame.key.get_pressed()[pygame.K_d] * self.total_speed +
                          pygame.key.get_pressed()[pygame.K_a] * -self.total_speed,
                          pygame.key.get_pressed()[pygame.K_s] * self.total_speed +
                          pygame.key.get_pressed()[pygame.K_w] * -self.total_speed]

        if args and args[0].type == pygame.MOUSEBUTTONDOWN:
            Bullet(bullets, pos_player=[self.rect.x, self.rect.y], pos_click=args[0].pos)
        if not (0 <= self.rect.x + self.speed[0] <= self.max_x - self.size[0]):
            self.speed[0] = 0
        if not (0 <= self.rect.y + self.speed[1] <= self.max_y - self.size[0]):
            self.speed[1] = 0

        self.rect = self.rect.move(self.speed)

    def position(self):
        return self.rect


class Bullet(pygame.sprite.Sprite):
    sprite = pygame.image.load("bullet_pyg.png")

    def __init__(self, *group, pos_player, pos_click):
        super().__init__(*group)

        self.total_speed = 4
        self.image = pygame.transform.scale(Bullet.sprite, (32, 32))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_player

        self.dir = (pos_click[0] - pos_player[0], pos_click[1] - pos_player[1])
        self.pos = pos_player

        len = math.hypot(*self.dir)
        if len == 0:
            self.dir = (0, -1)
        else:
            self.dir = (self.dir[0] / len, self.dir[1] / len)
        self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]

    def update(self, *args):

        self.rect.x = self.pos[0] + self.speed[0]
        self.rect.y = self.pos[1] + self.speed[1]
        self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]


class Enemies(pygame.sprite.Sprite):
    sprite = pygame.image.load("KNGHT_ONE.png")

    def __init__(self, *group, pos_spawn):
        super().__init__(*group)

        self.image = pygame.transform.scale(Enemies.sprite, (32, 32))

        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos_spawn
        self.pos = pos_spawn
        self.speed = 3

    def update(self, *args, pos_player):

        if self.pos[0] >= pos_player[0]:
            self.pos[0] += self.speed * abs(self.pos[0] - pos_player[0])\
                           / ((self.pos[0] - pos_player[0]) ** 2 + (self.pos[1] - pos_player[1]) ** 2) ** 0.5
        else:
            self.pos[0] += self.speed * abs(self.pos[0] - pos_player[0]) \
                           / ((self.pos[0] - pos_player[0]) ** 2 + (self.pos[1] - pos_player[1]) ** 2) ** 0.5
        if self.pos[1] >= pos_player[1]:
            self.pos[1] += self.speed * abs(self.pos[1] - pos_player[1])\
                           / ((self.pos[0] - pos_player[0]) ** 2 + (self.pos[1] - pos_player[1]) ** 2) ** 0.5
        else:
            self.pos[1] += self.speed * abs(self.pos[1] - pos_player[1]) \
                           / ((self.pos[0] - pos_player[0]) ** 2 + (self.pos[1] - pos_player[1]) ** 2) ** 0.5


fps = 180
clock = pygame.time.Clock()
running = True
infoObject = pygame.display.Info()
pygame.display.set_mode((infoObject.current_w, infoObject.current_h))
size = width, height = infoObject.current_w, infoObject.current_h
screen_main = pygame.display.set_mode(size)

player = pygame.sprite.Group()
bullets = pygame.sprite.Group()
enemies = pygame.sprite.Group()
Player(player, posx=infoObject.current_w // 2, posy=infoObject.current_h // 2,
       max_x=infoObject.current_w, max_y=infoObject.current_h)


while running:
    clock.tick(fps)
    player.update()
    bullets.update()
    enemies.update(player.sprites()[0].position())
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            player.update(event)
            enemies.update(event)
        if event.type == pygame.KEYUP:
            player.update(event)
        if event.type == pygame.MOUSEBUTTONDOWN:
            player.update(event)
    for bullet in bullets:
        if not screen_main.get_rect().collidepoint([bullet.rect.x, bullet.rect.y]):
            bullets.remove(bullet)
    for enemy in enemies:
        if not screen_main.get_rect().collidepoint([enemy.rect.x, enemy.rect.y]):
            pass

    screen_main.fill(pygame.Color("black"))
    player.draw(screen_main)
    bullets.draw(screen_main)
    pygame.display.flip()
