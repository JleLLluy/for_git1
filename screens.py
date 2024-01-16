import random

import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, sprite, size):
        super().__init__(*group)
        self.sprite = sprite
        self.size = size
        self.pushed = False
        self.img_unpressed = pygame.transform.scale(pygame.image.load(self.sprite), self.size)
        self.img_pressed = pygame.transform.scale(self.img_unpressed, tuple(i * 1.2 for i in self.size))
        self.image = self.img_unpressed

        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.pos = (x, y)

    def update(self, *args):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Title(pygame.sprite.Sprite):
    def __init__(self, *group, x, y, slides):
        super().__init__(*group)
        self.slides = []
        self.pos = (x, y)
        self.slide_num = 0
        for slide in slides:
            self.slides.append(pygame.transform.scale(pygame.image.load(slide[0]), slide[1]))

        self.total_slides = len(self.slides)

        self.image = self.slides[self.slide_num]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def previous(self):
        self.slide_num = (self.slide_num - 1) % self.total_slides
        self.image = self.slides[self.slide_num]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos

    def next(self):
        self.slide_num = (self.slide_num + 1) % self.total_slides
        self.image = self.slides[self.slide_num]
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


def start_screen(width, height):
    class StartButton(Button):
        def pressed(self):
            global running
            running = False

    class QuitButton(Button):
        def pressed(self):
            quit()

    class LeftArrow(Button):
        def pressed(self):
            if not self.pushed:
                self.pushed = True
                titles.sprites()[1].previous()

    class RightArrow(Button):
        def pressed(self):
            if not self.pushed:
                self.pushed = True
                titles.sprites()[1].next()

    screen = pygame.display.set_mode((width, height))
    size = width, height
    screen_main = pygame.display.set_mode(size)
    global running
    running = True

    buttons = pygame.sprite.Group()
    titles = pygame.sprite.Group()

    StartButton(buttons, x=width // 2, y=height // 4, sprite="start_b_proj.png", size=(256, 30))
    QuitButton(buttons, x=width // 2, y=height // 4 + 150, sprite="quit_b_proj.png", size=(83, 33))
    Title(titles, x=width // 2, y=height // 4 + 50, slides=[["difficulty_t_proj.png", (233, 30)]])
    Title(titles, x=width // 2, y=height // 4 + 100, slides=[["normal_menu_proj.png", (123, 30)],
                                                             ["hard_menu_proj.png", (123, 30)],
                                                             ["pain_menu_proj.png", (123, 30)]])

    LeftArrow(buttons, x=width // 2 - 100, y=height // 4 + 100, sprite="left_arrow_menu.png", size=(31, 30))
    RightArrow(buttons, x=width // 2 + 100, y=height // 4 + 100, sprite="right_arrow_menu.png", size=(31, 30))
    while running:
        screen_main.fill("Black")
        mouse_coord = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for button in buttons:
            if button.rect.collidepoint(mouse_coord):
                button.image = button.img_pressed
                if pygame.mouse.get_pressed()[0]:
                    button.pressed()
                else:
                    button.pushed = False
            else:
                button.image = button.img_unpressed

        for i in range(80):
            screen.fill(pygame.Color('white'),
                        (random.random() * width,
                         random.random() * height, 2, 2))
        buttons.update()
        buttons.draw(screen_main)
        titles.draw(screen_main)
        pygame.display.flip()
    return titles.sprites()[1].slide_num


def death_screen(width, height):
    class RetryButton(Button):
        def pressed(self):
            global running
            running = False

    class QuitButton(Button):
        def pressed(self):
            quit()

    screen = pygame.display.set_mode((width, height))
    size = width, height
    screen_main = pygame.display.set_mode(size)
    global running
    running = True

    buttons = pygame.sprite.Group()
    titles = pygame.sprite.Group()

    RetryButton(buttons, x=width // 2, y=height // 4 + 150, sprite="retry_b_proj.png", size=(128, 30))
    QuitButton(buttons, x=width // 2, y=height // 4 + 200, sprite="quit_b_proj.png", size=(83, 33))
    Title(titles, x=width // 2, y=height // 4, slides=[["you_died_t_proj.png", (410, 60)]])
    Title(titles, x=width // 2 - 100, y=height // 4 + 100, slides=[["score_t_proj.png", (123, 30)]])
    while running:
        screen_main.fill("black")
        mouse_coord = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for button in buttons:
            if button.rect.collidepoint(mouse_coord):
                button.image = button.img_pressed
                if pygame.mouse.get_pressed()[0]:
                    button.pressed()
                else:
                    button.pushed = False
            else:
                button.image = button.img_unpressed

        for i in range(1000):
            screen.fill(pygame.Color('red'),
                        (random.random() * width,
                         random.random() * height, 2, 2))
        buttons.update()
        buttons.draw(screen_main)
        titles.draw(screen_main)
        pygame.display.flip()


