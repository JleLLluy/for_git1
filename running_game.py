import pygame
import math
import random
import sqlite3
import time
from level_up import level_up
from screens import Hud
from screens import Title
from screens import death_screen


def write_rec_to_db(result, time_elapsed):
    connection = sqlite3.connect('records.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS 
        Records (id INTEGER PRIMARY KEY,result TEXT NOT NULL,time TEXT NOT NULL)''')

    cursor.execute(f"""INSERT INTO Records (result, time) VALUES ({str(result)}, '{str(time_elapsed)}')""")
    connection.commit()
    connection.close()


def running_game(fps, difficulty, width, height, screen):
    if difficulty == "P/normal_menu_proj.png":
        difficulty = 1
    elif difficulty == "P/hard_menu_proj.png":
        difficulty = 2
    elif difficulty == "P/pain_menu_proj.png":
        difficulty = 3
    count = 0
    screen_count = 0
    health = 10
    damage_of_player = 1
    damage_of_enemies = 1 * difficulty
    hp_of_enemies = 2 * difficulty
    first_phase = True
    second_phase = False
    eternal_phase = False
    needed = 10

    class Player(pygame.sprite.Sprite):
        sprite = pygame.image.load("P/player_pyg.png")

        def __init__(self, *group, max_x, max_y):
            super().__init__(*group)
            self.time = time.thread_time()
            self.delay = 0.000000001
            self.total_speed = 3
            self.size = (48, 48)
            self.shooting = False

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

            if pygame.mouse.get_pressed()[0]:
                self.shooting = True
            else:
                self.shooting = False

            if self.shooting and time.thread_time() - self.time >= self.delay:
                self.time = time.thread_time()
                Bullet(bullets, pos_player=self.rect.center, pos_click=pygame.mouse.get_pos())

            if not (0 <= self.rect.x + self.speed[0] <= self.max_x - self.size[0]):
                self.speed[0] = 0
            if not (0 <= self.rect.y + self.speed[1] <= self.max_y - self.size[0]):
                self.speed[1] = 0

            self.rect = self.rect.move(self.speed)

        def position(self):
            return list(self.rect.center)

        def upgrade(self, upgrader):
            if upgrader == "health":
                pass                    #тут увелич хп героя
            elif upgrader == "damage":
                pass                  #тут увелич мощь выстрелов
            elif upgrader == "speed":
                pass                       #тут увелич

    class Bullet(pygame.sprite.Sprite):
        sprite = pygame.image.load("P/bullet_pyg.png")

        def __init__(self, *group, pos_player, pos_click):
            super().__init__(*group)

            self.total_speed = 7
            self.size = (32, 32)
            self.image = pygame.transform.scale(Bullet.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_player

            self.dir = (pos_click[0] - pos_player[0], pos_click[1] - pos_player[1])
            self.pos = pos_player

            dlen = math.hypot(*self.dir)
            if dlen == 0:
                self.dir = (0, -1)
            else:
                self.dir = (self.dir[0] / dlen, self.dir[1] / dlen)
            self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]

        def update(self, *args):

            self.rect.center = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
            self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]

    class Enemy_Bullet(pygame.sprite.Sprite):
        sprite = pygame.image.load("P/bullet_enemys.png")

        def __init__(self, *group, pos_enemy, pos_player):
            super().__init__(*group)

            self.total_speed = 4
            self.size = (32, 32)
            self.image = pygame.transform.scale(Enemy_Bullet.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_enemy

            self.dir = (pos_player[0] - pos_enemy[0], pos_player[1] - pos_enemy[1])
            self.pos = pos_enemy

            dlen = math.hypot(*self.dir)
            if dlen == 0:
                self.dir = (0, -1)
            else:
                self.dir = (self.dir[0] / dlen, self.dir[1] / dlen)
            self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]

        def update(self, *args):

            self.rect.center = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
            self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]

    class Enemy_one(pygame.sprite.Sprite):
        sprite = pygame.image.load("P/enemy_one_pygame_proj.png")

        def __init__(self, *group, pos_spawn, hp=hp_of_enemies):
            super().__init__(*group)

            self.total_speed = 1
            self.size = (32, 32)
            self.hp = hp
            self.image = pygame.transform.scale(Enemy_one.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_spawn
            self.pos = pos_spawn

            self.dir = [0, 0]
            self.speed = [0, 0]

        def update(self, pos_player):
            self.dir = (pos_player[0] - self.pos[0], pos_player[1] - self.pos[1])
            dlen = math.hypot(*self.dir)
            if dlen == 0:
                self.dir = (0, -1)
            else:
                self.dir = (self.dir[0] / dlen, self.dir[1] / dlen)
            self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]

            self.rect.center = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
            self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]

    class Enemy_Two_Shooter(pygame.sprite.Sprite):
        sprite = pygame.image.load("P/enemy_two_pygame_proj.png")
        sprite_1 = pygame.image.load('P/enemy_one_pygame_proj.png')
        size = (32, 32)

        def __init__(self, *group, pos_of_spawn, max_x, max_y, hp):
            super().__init__(*group)
            self.hp = hp
            self.max_y = max_y
            self.max_x = max_x
            self.total_speed = 2
            self.size = (32, 32)
            self.image = pygame.transform.scale(Enemy_Two_Shooter.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_of_spawn
            self.pos = pos_of_spawn

            self.dir = [0, 0]
            self.speed = [0, 0]

        def update(self, pos_of_player, *args):
            if args and args[0].type == Enemy_is_shooting:
                Enemy_Bullet(enemy_bullets, pos_enemy=self.rect.center, pos_player=pos_of_player)
            self.dir = (pos_of_player[0] - self.pos[0], pos_of_player[1] - self.pos[1])
            dlen = math.hypot(*self.dir)
            if dlen == 0:
                self.dir = (0, -1)
                self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]
            elif dlen <= 200:
                self.dir = (1 * self.dir[0], 1 * self.dir[1])
                self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]
            elif dlen >= 350:
                self.dir = (self.dir[0] / dlen, self.dir[1] / dlen)
                self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]
            else:
                self.speed = [self.total_speed * random.randint(-1, 1), self.total_speed * random.randint(-1, 1)]
            if not (0 <= self.rect.x + self.speed[0] <= self.max_x - self.size[0]):
                self.speed[0] = 0
            if not (0 <= self.rect.y + self.speed[1] <= self.max_y - self.size[0]):
                self.speed[1] = 0

            self.rect.center = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
            self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]

    class Enemy_Three_Dozer(pygame.sprite.Sprite):
        sprite = pygame.image.load("P/buldozer_full_armor.png")
        sprite_1 = pygame.image.load('P/buldozer_2.3_armor.png')
        sprite_2 = pygame.image.load('P/buldozer_1.3_armor.png')
        sprite_3 = pygame.image.load('P/buldozer_0.3_armor.png')
        size = (32, 32)

        def __init__(self, *group, pos_of_spawn, max_x, max_y, hp):
            super().__init__(*group)
            self.hp = hp
            self.max_y = max_y
            self.max_x = max_x
            self.total_speed = 1
            self.size = (128, 128)
            self.image = pygame.transform.scale(Enemy_Three_Dozer.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_of_spawn
            self.pos = pos_of_spawn

            self.dir = [0, 0]
            self.speed = [0, 0]

        def update(self, pos_of_player, *args):
            if args and args[0].type == Enemy_is_shooting:
                Enemy_Bullet(enemy_bullets, pos_enemy=self.rect.center, pos_player=pos_of_player)
            if args and args[0].type == Dozer_charges:
                self.speed = [self.total_speed * self.dir[0] * 10, self.total_speed * self.dir[1] * 10]
            self.dir = (pos_of_player[0] - self.pos[0], pos_of_player[1] - self.pos[1])
            dlen = math.hypot(*self.dir)
            if dlen == 0:
                self.dir = (0, -1)
                self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]
            elif dlen <= 200:
                self.dir = (1 * self.dir[0], 1 * self.dir[1])
                self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]
            elif dlen >= 350:
                self.dir = (self.dir[0] / dlen, self.dir[1] / dlen)
                self.speed = [self.total_speed * self.dir[0], self.total_speed * self.dir[1]]
            else:
                self.speed = [self.total_speed * random.randint(-1, 1), self.total_speed * random.randint(-1, 1)]

            if not (0 <= self.rect.x + self.speed[0] <= self.max_x - self.size[0]):
                self.speed[0] = 0
            if not (0 <= self.rect.y + self.speed[1] <= self.max_y - self.size[0]):
                self.speed[1] = 0

            self.rect.center = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]
            self.pos = [self.pos[0] + self.speed[0], self.pos[1] + self.speed[1]]

    class Kabachok(pygame.sprite.Sprite):
        sprite = pygame.image.load("P/secret_boss.png")

        def __init__(self, *group, pos_of_spawn, hp):
            super().__init__(*group)
            self.hp = hp
            self.total_speed = 1
            self.size = (128, 128)
            self.image = pygame.transform.scale(Enemy_Three_Dozer.sprite, self.size)

            self.rect = self.image.get_rect()
            self.rect.center = pos_of_spawn
            self.pos = pos_of_spawn

            self.dir = [0, 0]
            self.speed = [0, 0]

    clock = pygame.time.Clock()
    running = True
    screen_main = screen
    score = 0
    infoObject = pygame.display.Info()
    player = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    enemie_shooters = pygame.sprite.Group()
    enemie_dozers = pygame.sprite.Group()
    enemy_bullets = pygame.sprite.Group()
    kabachok = pygame.sprite.Group()
    Player(player, max_x=infoObject.current_w, max_y=infoObject.current_h)
    Enemy_is_shooting = pygame.USEREVENT + 1
    Dozer_charges = pygame.USEREVENT + 2
    Spawn_Enemy1_1 = pygame.USEREVENT + 3
    Spawn_Enemy2_1 = pygame.USEREVENT + 4
    Spawn_Dozer_1 = pygame.USEREVENT + 5
    Spawn_Enemy1_2 = pygame.USEREVENT + 6
    Spawn_Enemy2_2 = pygame.USEREVENT + 7
    Spawn_Dozer_2 = pygame.USEREVENT + 8
    Spawn_Enemy1_3 = pygame.USEREVENT + 9
    Spawn_Enemy2_3 = pygame.USEREVENT + 10
    kabachok_1 = pygame.USEREVENT + 11
    pygame.time.set_timer(Enemy_is_shooting, 1000)
    pygame.time.set_timer(Dozer_charges, 5000)
    pygame.time.set_timer(Spawn_Enemy1_1, 1000)
    pygame.time.set_timer(Spawn_Enemy1_2, 800)
    pygame.time.set_timer(Spawn_Enemy1_3, 500)
    pygame.time.set_timer(Spawn_Enemy2_1, 2000)
    pygame.time.set_timer(Spawn_Enemy2_2, 1500)
    pygame.time.set_timer(Spawn_Enemy2_3, 1000)
    pygame.time.set_timer(Spawn_Dozer_1, 10000)
    pygame.time.set_timer(Spawn_Dozer_2, 5000)
    pygame.time.set_timer(kabachok_1, 1000)
    titles = pygame.sprite.Group()

    Title(titles, pos=(width // 12 - 50, height // 12), slides_and_sizes=[["P/score_t_proj.png", (123, 30)]])

    temp_score_hud = Hud(text=score, size=45, color=(255, 255, 255), screen=screen, pos=(width // 12 + 30, height // 12 - 32))

    while running:
        clock.tick(fps)
        player.update()
        bullets.update()
        enemy_bullets.update()
        enemies.update(pos_player=player.sprites()[0].position())
        enemie_shooters.update(pos_of_player=player.sprites()[0].position())
        enemie_dozers.update(pos_of_player=player.sprites()[0].position())
        temp_score_hud.text = str(count)
        if count >= 100:
            eternal_phase = True
        elif 100 > count >= 30:
            second_phase = True

        if screen_count >= needed:
            upp = level_up(screen_main, infoObject.current_w, infoObject.current_h, fps)
            if upp == 'health':
                health += 10
            elif upp == 'speed':
                pass
            elif upp == 'damage':
                damage_of_player += 2
            screen_count -= needed
            needed *= 2
        for event in pygame.event.get():
            if eternal_phase:
                if event.type == Spawn_Dozer_2:
                    Enemy_Three_Dozer(enemie_dozers, pos_of_spawn=[random.randint(0, width), random.randint(0, height)],
                                      max_x=infoObject.current_w, max_y=infoObject.current_h, hp=hp_of_enemies * 10)
                if event.type == Spawn_Enemy2_3:
                    Enemy_Two_Shooter(enemie_shooters,
                                      pos_of_spawn=[random.randint(0, width), random.randint(0, height)],
                                      max_x=infoObject.current_w, max_y=infoObject.current_h, hp=hp_of_enemies * 2)
                if event.type == Spawn_Enemy1_3:
                    Enemy_one(enemies, pos_spawn=[random.randint(0, width), random.randint(0, height)])
                if event.type == kabachok:
                    Kabachok(kabachok, pos_of_spawn=[random.randint(0, width), random.randint(0, height)], hp=100 * hp_of_enemies)
            elif second_phase:
                if event.type == Spawn_Dozer_1:
                    Enemy_Three_Dozer(enemie_dozers, pos_of_spawn=[random.randint(0, width), random.randint(0, height)],
                                      max_x=infoObject.current_w, max_y=infoObject.current_h, hp=hp_of_enemies * 10)
                if event.type == Spawn_Enemy2_2:
                    Enemy_Two_Shooter(enemie_shooters,
                                      pos_of_spawn=[random.randint(0, width), random.randint(0, height)],
                                      max_x=infoObject.current_w, max_y=infoObject.current_h, hp=hp_of_enemies * 2)
                if event.type == Spawn_Enemy1_2:
                    Enemy_one(enemies, pos_spawn=[random.randint(0, width), random.randint(0, height)])
            elif first_phase:
                if event.type == Spawn_Enemy2_1:
                    Enemy_Two_Shooter(enemie_shooters,
                                      pos_of_spawn=[random.randint(0, width), random.randint(0, height)],
                                      max_x=infoObject.current_w, max_y=infoObject.current_h, hp=hp_of_enemies * 2)
                if event.type == Spawn_Enemy1_1:
                    Enemy_one(enemies, pos_spawn=[random.randint(0, width), random.randint(0, height)])
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                player.update(event)
            if event.type == pygame.KEYUP:
                player.update(event)
            if event.type == pygame.MOUSEBUTTONDOWN:
                player.update(event)
            if event.type == Enemy_is_shooting:
                enemie_shooters.update(player.sprites()[0].position(), event)
                enemie_dozers.update(player.sprites()[0].position(), event)
            if event.type == Dozer_charges:
                enemie_dozers.update(player.sprites()[0].position(), event)
        for bullet in bullets:
            if not screen_main.get_rect().collidepoint([bullet.rect.x, bullet.rect.y]):
                bullets.remove(bullet)
            for enemy in enemies:
                if bullet.rect.colliderect(enemy.rect):
                    enemy.hp -= damage_of_player
                    if enemy.hp <= 0:
                        enemy.kill()
                        count += 1
                        screen_count += 1
                    bullet.kill()
            for enemie_shooter in enemie_shooters:
                if bullet.rect.colliderect(enemie_shooter.rect):
                    enemie_shooter.hp -= damage_of_player
                    enemie_shooter.total_speed += 2
                    bullet.kill()
                    if 0 < enemie_shooter.hp <= hp_of_enemies:
                        enemie_shooter.image = pygame.transform.scale(Enemy_Two_Shooter.sprite_1, enemie_shooter.size)
                    if enemie_shooter.hp <= 0:
                        enemie_shooter.kill()
                        count += 3
                        screen_count += 3
            for enemie_dozer in enemie_dozers:
                if bullet.rect.colliderect(enemie_dozer.rect):
                    enemie_dozer.hp -= damage_of_player
                    enemie_dozer.total_speed += 0.1
                    bullet.kill()
                    if hp_of_enemies * 10 / 4 * 2 < enemie_dozer.hp <= hp_of_enemies * 10 / 4 * 3:
                        enemie_dozer.image = pygame.transform.scale(Enemy_Three_Dozer.sprite_1, enemie_dozer.size)
                    elif hp_of_enemies * 10 / 4 * 1 < enemie_dozer.hp <= hp_of_enemies * 10 / 4 * 2:
                        enemie_dozer.image = pygame.transform.scale(Enemy_Three_Dozer.sprite_2, enemie_dozer.size)
                    elif 0 < enemie_dozer.hp <= hp_of_enemies * 10 / 4 * 1:
                        enemie_dozer.image = pygame.transform.scale(Enemy_Three_Dozer.sprite_3, enemie_dozer.size)
                    if enemie_dozer.hp <= 0:
                        enemie_dozer.kill()
                        count += 100
                        screen_count += 100

        for enemy_bullet in enemy_bullets:
            if not screen_main.get_rect().collidepoint([enemy_bullet.rect.x, enemy_bullet.rect.y]):
                enemy_bullets.remove(enemy_bullet)
            for p in player:
                if p.rect.colliderect(enemy_bullet.rect):
                    enemy_bullet.kill()
                    health -= damage_of_enemies
                    if health <= 0:
                        running = False
                        write_rec_to_db(count, screen_count)
                        death_screen(infoObject.current_w, infoObject.current_h, fps, screen_main, count)

        screen_main.fill(pygame.Color("black"))
        temp_score_hud.update()
        player.draw(screen_main)
        bullets.draw(screen_main)
        enemies.draw(screen_main)
        titles.draw(screen_main)
        enemie_shooters.draw(screen_main)
        enemie_dozers.draw(screen_main)
        enemy_bullets.draw(screen_main)
        kabachok.draw(screen_main)
        pygame.display.flip()
