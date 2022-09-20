import os
import pygame as pg

pg.init()

width = 800
height = 600
screen = pg.display.set_mode((width, height))

pg.display.set_caption("Demo")
icon = pg.image.load(os.path.join("image_sounds", "pic.png"))
pg.display.set_icon(icon)

bg = pg.image.load((os.path.join("D:\Download\mycollection\png", "beam_4.png")))

running = True
while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    screen.fill((0, 0, 50))
    screen.blit(bg, (370, 0))
    pg.display.update()
