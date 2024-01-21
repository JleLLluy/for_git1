import random
import pygame


class Button(pygame.sprite.Sprite):
    def __init__(self, *group, pos, sprite, size):
        super().__init__(*group)
        self.sprite = sprite
        self.size = size
        self.pushed = False
        self.img_unpressed = pygame.transform.scale(pygame.image.load(self.sprite), self.size)
        self.img_pressed = pygame.transform.scale(self.img_unpressed, tuple(i * 1.2 for i in self.size))
        self.image = self.img_unpressed

        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.pos = pos

    def update(self, *args):
        self.rect = self.image.get_rect()
        self.rect.center = self.pos


class Title(pygame.sprite.Sprite):
    def __init__(self, *group, pos, slides_and_sizes):
        super().__init__(*group)
        self.slides = []
        self.pos = pos
        self.slide_num = 0
        for slide in slides_and_sizes:
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


class Hud:
    def __init__(self, text, size, color, screen, pos):
        self.text = text
        self.size = size
        self.color = color
        self.screen = screen
        self.pos = pos
        pygame.font.init()

    def update(self):
        font = pygame.font.SysFont('Segoe UI Historic', self.size)
        text_surface = font.render(self.text, True, self.color)
        self.screen.blit(text_surface, self.pos)


def start_screen(width, height, fps):
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

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((width, height))
    size = width, height
    screen_main = pygame.display.set_mode(size)
    global running
    running = True

    buttons = pygame.sprite.Group()
    titles = pygame.sprite.Group()

    StartButton(buttons, pos=(width // 2, height // 4), sprite="P/start_b_proj.png", size=(256, 30))
    QuitButton(buttons, pos=(width // 2, height // 4 + 150), sprite="P/quit_b_proj.png", size=(83, 33))
    Title(titles, pos=(width // 2, height // 4 + 50), slides_and_sizes=[["P/difficulty_t_proj.png", (233, 30)]])
    Title(titles, pos=(width // 2, height // 4 + 100), slides_and_sizes=[["P/normal_menu_proj.png", (123, 30)],
                                                                         ["P/hard_menu_proj.png", (123, 30)],
                                                                         ["P/pain_menu_proj.png", (123, 30)]])

    LeftArrow(buttons, pos=(width // 2 - 100, height // 4 + 100),
              sprite="P/left_arrow_menu.png", size=(31, 30))
    RightArrow(buttons, pos=(width // 2 + 100, height // 4 + 100),
               sprite="P/right_arrow_menu.png", size=(31, 30))
    while running:
        clock.tick(fps)
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


def death_screen(width, height, fps, screen, score):
    class RetryButton(Button):
        def pressed(self):
            global running
            running = False

    class QuitButton(Button):
        def pressed(self):
            quit()

    clock = pygame.time.Clock()
    screen_main = screen
    global running
    running = True

    buttons = pygame.sprite.Group()
    titles = pygame.sprite.Group()

    RetryButton(buttons, pos=(width // 2, height // 4 + 150), sprite="P/retry_b_proj.png", size=(128, 30))
    QuitButton(buttons, pos=(width // 2, height // 4 + 200), sprite="P/quit_b_proj.png", size=(83, 33))
    Title(titles, pos=(width // 2, height // 4), slides_and_sizes=[["P/you_died_t_proj.png", (410, 60)]])
    Title(titles, pos=(width // 2 - 100, height // 4 + 100), slides_and_sizes=[["P/score_t_proj.png", (123, 30)]])
    score_hud = Hud(text=str(score), size=40, color=(255, 255, 255), screen=screen,
                    pos=(width // 2 - 20, height // 4 + 70))

    while running:
        clock.tick(fps)
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
        score_hud.update()
        buttons.update()
        buttons.draw(screen_main)
        titles.draw(screen_main)
        pygame.display.flip()



