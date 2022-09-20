from pygame import mixer
import pygame as pg
import os

# create the screen at globals
width = 800
height = 600
screen = pg.display.set_mode((width, height))  # (width, height)

life = 3
game_over = 0
win = 0
shooting_time = 0

charge_for_beam = 0


# Sound Effect:
def explode_sound():
    explode = mixer.Sound(os.path.join("image_sounds", "explosion.wav"))
    explode.play()


def over_sound():
    over = mixer.Sound(os.path.join("image_sounds", "game_over.wav"))
    over.play()
