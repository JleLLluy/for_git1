import pygame
from screens import start_screen
from running_game import running_game


pygame.init()
fps = 180

infoObject = pygame.display.Info()
size = width, height = infoObject.current_w, infoObject.current_h
screen_main = pygame.display.set_mode(size)

difficulty = start_screen(width, height, fps)
while True:
    running_game(fps=fps, difficulty=difficulty, width=infoObject.current_w,
             height=infoObject.current_h, screen=screen_main)
