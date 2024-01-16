import pygame
import math
import random
import sqlite3


def write_rec_to_db(result, time_elapsed):
    connection = sqlite3.connect('records.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS 
        Records (id INTEGER PRIMARY KEY,result TEXT NOT NULL,time TEXT NOT NULL)''')

    cursor.execute(f"""INSERT INTO Records (result, time) VALUES ({str(result)}, '{str(time_elapsed)}')""")
    connection.commit()
    connection.close()


def running_game(fps, difficulty, width, height, screen):
    class Player(pygame.sprite.Sprite):
        sprite = pygame.image.load("player_pyg.png")

        def __init__(self, *group, max_x, max_y):
            super().__init__(*group)

            self.total_speed = 3
            self.size = (48, 48)

            self.image = pygame.transform.scale(Player.sprite, self.size)
            self.speed = [0, 0]
            self.rect = self.image.get_rect()
            self.rect.center = [max_x // 2, max_y // 2]
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
                Bullet(bullets, pos_player=self.rect.center, pos_click=args[0].pos)
            if not (0 <= self.rect.x + self.speed[0] <= self.max_x - self.size[0]):
                self.speed[0] = 0
            if not (0 <= self.rect.y + self.speed[1] <= self.max_y - self.size[0]):
                self.speed[1] = 0

            self.rect = self.rect.move(self.speed)

        def position(self):
            return list(self.rect.center)

    class Bullet(pygame.sprite.Sprite):
        sprite = pygame.image.load("bullet_pyg.png")

        def __init__(self, *group, pos_player, pos_click):
            super().__init__(*group)

            self.total_speed = 7
            self.size = (32, 32)
            self.image = pygame.transform.scale(Bullet.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_player

            self.dir = (pos_click[0] - pos_player[0], pos_click[1] - pos_player[1])
            self.pos = pos_player

            len = math.hypot(*self.dir)
            if len == 0:
                self.dir = (0, -1)
            else:
                self.dir = (self.dir[0] / len, self.dir[1] / len)
            self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]

        def update(self, *args):

            self.rect.center = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
            self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]

    class Enemy_one(pygame.sprite.Sprite):
        sprite = pygame.image.load("enemy_one_pygame_proj.png")

        def __init__(self, *group, pos_spawn):
            super().__init__(*group)

            self.total_speed = 3
            self.size = (32, 32)
            self.image = pygame.transform.scale(Enemy_one.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_spawn
            self.pos = pos_spawn

            self.dir = [0, 0]
            self.speed = [0, 0]

        def update(self, pos_player):
            self.dir = (pos_player[0] - self.pos[0], pos_player[1] - self.pos[1])
            len = math.hypot(*self.dir)
            if len == 0:
                self.dir = (0, -1)
            else:
                self.dir = (self.dir[0] / len, self.dir[1] / len)
            self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]

            self.rect.center = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
            self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]

    class SharpshooterChangelingEnemyTwo(pygame.sprite.Sprite):
        sprite = pygame.image.load("enemy_one_pygame_proj.png")

        def __init__(self, *group, pos_spawn):
            super().__init__(*group)

            self.total_speed = 2
            self.size = (32, 32)
            self.image = pygame.transform.scale(Enemy_one.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_spawn
            self.pos = pos_spawn

            self.dir = [0, 0]
            self.speed = [0, 0]

        def update(self, pos_of_player, *args):
            if args and args[0].type == Sharpshooter_changeling_Enemy_Two_is_shooting:
                Bullet(bullets, pos_player=self.rect.center, pos_click=pos_of_player)
            self.dir = (pos_of_player[0] - self.pos[0], pos_of_player[1] - self.pos[1])
            len = math.hypot(*self.dir)
            if len == 0:
                self.dir = (0, -1)
            else:
                self.dir = (self.dir[0] / len, self.dir[1] / len)
            self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]

            self.rect.center = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
            self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]

    clock = pygame.time.Clock()
    running = True
    size = width, height
    screen_main = screen

    player = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemie_shooters = pygame.sprite.Group()
    Player(player, max_x=width, max_y=height)
    Enemy_one(enemies, pos_spawn=[random.randint(0, width), random.randint(0, height)])
    SharpshooterChangelingEnemyTwo(enemie_shooters, pos_spawn=[random.randint(0, width), random.randint(0, height)])
    Sharpshooter_changeling_Enemy_Two_is_shooting = pygame.USEREVENT + 1
    pygame.time.set_timer(Sharpshooter_changeling_Enemy_Two_is_shooting, 2000)

    while running:
        # Enemy_one(enemies, pos_spawn=[random.randint(0, width), random.randint(0, height)])
        clock.tick(fps)
        player.update()
        bullets.update()
        enemies.update(pos_player=player.sprites()[0].position())
        enemie_shooters.update(pos_of_player=player.sprites()[0].position())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.update(event)
            if event.type == pygame.KEYUP:
                player.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.update(event)
            if event.type == Sharpshooter_changeling_Enemy_Two_is_shooting:
                enemie_shooters.update(player.sprites()[0].position(), event)
        for bullet in bullets:
            if not screen_main.get_rect().collidepoint([bullet.rect.x, bullet.rect.y]):
                bullets.remove(bullet)

        screen_main.fill(pygame.Color("black"))
        player.draw(screen_main)
        bullets.draw(screen_main)
        enemies.draw(screen_main)
        enemie_shooters.draw(screen_main)
        pygame.display.flip()
