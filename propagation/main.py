"""
le fichier main sert a lancer le programme
mais le fichier game peut aussi le lancer
le code dois etre mis dans le fichier game
"""

import game
import pygame
from pygame.locals import *
import pickle, os

class Box:
    def __init__(self):
        self.AUTO_SIZE = None
        self.size = self.AUTO_SIZE
        self.flags = FULLSCREEN
        self.title = "The Game"
        self.fps = 60

    def __str__(self):
        return str(self.__dict__)


if __name__ != "__main__":
    param = Box()


def save(file, var):
    try:
        f = open(file, "wb")
        pickle.Pickler(f).dump(var)
        f.close()
    except IOError as e:
        print("Impossible d'ouvrir", file, ":", e)


def load(file, destroy = False):
    try:
        f = open(file, "rb")
        lecture = pickle.Unpickler(f).load()
        f.close()

        if destroy:
            try:
                os.remove(file)
            except OSError as e:
                print("Impossible de supprimer", file, ":", e)

        return lecture
    except IOError as e:
        print("Impossible d'ouvrir", file, ":", e)
        return None


def newGame():
    global screen
    pygame.init()
    pygame.font.init()
    save("game_var", param)

    if param.size == param.AUTO_SIZE:
        param.size = pygame.display.Info()
        param.size = param.size.current_w, param.size.current_h

    screen = pygame.display.set_mode(param.size, param.flags)
    pygame.display.set_caption(param.title)

    return screen

def loop():
    continuer = True
    ecart = 1000 / param.fps
    last_time = pygame.time.get_ticks() - ecart

    while continuer:
        if pygame.time.get_ticks() - last_time >= ecart:
            last_time += ecart
            events = pygame.event.get()

            for event in events:
                if event.type == QUIT or event.type == KEYDOWN and event.key == K_ESCAPE:
                    continuer = False

            game.draw(events)
            pygame.display.flip()

def stop():
    game.stop()
    pygame.font.quit()
    pygame.quit()

def main():
    global param, screen
    screen = game.setup()
    param = load("game_var", destroy = True)
    loop()
    stop()

if __name__ == "__main__":
    main()
