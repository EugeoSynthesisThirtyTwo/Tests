import pygame
from pygame.locals import *
import main
import random
import math

from propagation import *

def setup():
    global screen, size, screenRect, width, height

    main.param.fps = 60  # facultatif, c'est la valeur par défaut
    main.param.size = main.param.AUTO_SIZE  # facultatif, c'est la valeur par défaut
    # main.param.size = 1920, 1080
    main.param.flags = FULLSCREEN  # facultatif, c'est la valeur par défaut
    main.param.title = "The Game"  # facultatif, c'est la valeur par défaut

    screen = main.newGame()
    size = screen.get_size()
    width, height = size
    screenRect = Rect(0, 0, width, height)

    global font, cloud, pressed
    font = pygame.font.Font("courbd.ttf", 100)
    cloud = Cloud(screenRect)
    pressed = False

    return screen  # important !

def updateEvents(events):
    global pressed

    for e in events:
        if e.type == pygame.MOUSEBUTTONDOWN and e.button == 1:
            pressed = True
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 2:
            cloud.add(Point(e.pos[0], e.pos[1], (255, 64, 0)))
        elif e.type == pygame.MOUSEBUTTONDOWN and e.button == 3:
            cloud.add(Point(e.pos[0], e.pos[1], (0, 255, 64)))
        elif e.type == pygame.KEYDOWN and e.key == pygame.K_RETURN:
            if not cloud.propagation_en_cours:
                cloud.propagate_setup()
        elif e.type == pygame.MOUSEBUTTONUP and e.button == 1:
            pressed = False


def draw(events):
    updateEvents(events)
    cloud.propagate_update()

    if pressed:
        pos = pygame.mouse.get_pos()
        a = random.random() * math.pi * 2
        r = random.random() * 50
        p = Point(pos[0] + r * math.cos(a), pos[1] + r * math.sin(a))
        if p.x > 0 and p.x < width and p.y > 0 and p.y < height:
        	cloud.add(p)

    screen.fill((255, 255, 255))
    cloud.draw(screen)


def stop():
    # au cas ou vous voudriez réaliser quelques dernières actions
    # si l'utilisateur demande à quitter la fenêtre
    pass

if __name__ == "__main__":
    main.main()
