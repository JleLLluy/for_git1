from screens import Button, Title
import pygame
import random


def level_up(screen, width, height, fps):
    class HealthUpButton(Button):
        def pressed(self):
            global running
            running = False
            return "health"

    class DamageUpButton(Button):
        def pressed(self):
            global running
            running = False
            return "damage"

    class SpeedUpButton(Button):
        def pressed(self):
            global running
            running = False
            return "speed"

    clock = pygame.time.Clock()
    running = True
    screen_main = screen
    result = ""

    buttons = pygame.sprite.Group()
    titles = pygame.sprite.Group()

    HealthUpButton(buttons, pos=(width // 4 * 3, height // 3), sprite="P/health_up_proj.png", size=(200, 200))
    DamageUpButton(buttons, pos=(width // 4 * 2, height // 3), sprite="P/damage_boost.png", size=(200, 200))
    SpeedUpButton(buttons, pos=(width // 4 * 1, height // 3), sprite="P/speed_up_proj.png", size=(200, 200))
    Title(titles, pos=(width // 4 * 3, height // 3 - 140), slides_and_sizes=[["P/health_t_proj.png", (155, 30)]])
    Title(titles, pos=(width // 4 * 2, height // 3 - 140), slides_and_sizes=[["P/damage_t_proj.png", (177, 30)]])
    Title(titles, pos=(width // 4 * 1, height // 3 - 140), slides_and_sizes=[["P/speed_up_t_proj.png", (126, 33)]])

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
                    result = button.pressed()
                    running = False
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

    return result
