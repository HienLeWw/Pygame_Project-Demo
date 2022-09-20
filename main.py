import os
import random as rd
import pygame as pg
import object as o
import globals as g
from pygame import mixer


# Initialize the pygame
pg.mixer.pre_init()
pg.init()

pg.event.set_allowed([pg.QUIT, pg.KEYDOWN, pg.KEYUP])

# create the screen at globals


# Title and Icon
pg.display.set_caption("Space Invader")
icon = pg.image.load(os.path.join("image_sounds", "icon.png")).convert_alpha()
pg.display.set_icon(icon)

# Background
bg = pg.image.load(os.path.join("image_sounds", "background.jpg")).convert_alpha()
bg = pg.transform.scale(bg, (g.width, g.height))
i = 0


# display animation background
def display_background():
    global i
    if g.game_over == 0:
        g.screen.blit(bg, (0, i))
        g.screen.blit(bg, (0, -g.height + i))
        if i == g.height:
            i = 0
        i += 0.5
    else:
        g.screen.blit(bg, (0, 0))


# Background music
mixer.music.load(os.path.join("image_sounds", "background.wav"))
mixer.music.play(-1)

# Player
Player = o.Object(pg.image.load(os.path.join("image_sounds", "player_1.png")).convert_alpha(), 370, 480)

font = pg.font.Font("freesansbold.ttf", 16)

# Score
score_val = 0
scoreX = 10
scoreY = 10


def show_score(x, y):
    score = font.render("Score: " + str(score_val), True, (255, 255, 255))
    g.screen.blit(score, (x, y))


# Life
lifeX = 740
lifeY = 10


def show_life(x, y):
    life = font.render("Life: " + str(g.life), True, (255, 255, 255))
    g.screen.blit(life, (x, y))


# Game over
def show_game_over():
    game_over_font = pg.font.Font("freesansbold.ttf", 64)
    restart_font = pg.font.Font("freesansbold.ttf", 32)
    end = game_over_font.render("GAME OVER", True, (0, 255, 255))
    restart = restart_font.render("press 'ENTER' to restart game", True, (0, 255, 255))
    end_rect = end.get_rect(center=(g.width / 2, g.height / 2 - 50))
    restart_rect = restart.get_rect(center=(g.width / 2, g.height / 2))
    g.screen.blit(end, end_rect)
    g.screen.blit(restart, restart_rect)


# Win
def show_win():
    win_font = pg.font.Font("freesansbold.ttf", 64)
    win = win_font.render("YOU WIN!", True, (0, 255, 255))
    win_rect = win.get_rect(center=(g.width / 2, g.height / 2 - 50))
    g.screen.blit(win, win_rect)
    if g.win == 1:
        win_music = mixer.Sound(os.path.join("image_sounds", "win.wav"))
        win_music.play()


# Missile
Missile = o.Bullet(pg.image.load(os.path.join("image_sounds", "missile.png")).convert_alpha(), change_x=0, change_y=1)

# Enemy
asteroid_list = o.create_asteroid()
Ufo = o.create_ufo()


def asteroid(asteroid_list):
    for i in range(len(asteroid_list)):
        asteroid_list[i].draw()


def stop_running():
    Missile.state = "not ready"
    mixer.music.fadeout(1)
    Player.change_x = 0
    Ufo.x = 1000
    for i in range(len(asteroid_list)):
        asteroid_list[i].x += 1000


def restart_running():
    global score_val
    respawn_sound = mixer.Sound(os.path.join("image_sounds", "respawn.wav"))
    respawn_sound.play()
    mixer.music.play(-1)
    score_val = 0
    g.life = 3
    g.win = 0
    g.game_over = 0
    Missile.state = "ready"
    Player.x = 370
    Ufo.x = 370
    Ufo.y = 0
    for i in range(len(asteroid_list)):
        asteroid_list[i].x -= rd.randint(800, 1000)


if __name__ == "__main__":
    # Game Loop
    running = 1
    while running:
        # RGB
        g.screen.fill((0, 0, 50))

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False

            # if keystroke is pressed, check whether its right or left
            if event.type == pg.KEYDOWN:
                # print("A keystroke is pressed")
                move_left = event.key == pg.K_LEFT or event.key == pg.K_a
                move_right = event.key == pg.K_RIGHT or event.key == pg.K_d
                race = event.key == pg.K_s or event.key == pg.K_DOWN
                fire = event.key == pg.K_SPACE or event.key == pg.K_RCTRL or event.key == pg.K_LCTRL
                if move_left:
                    # print("Left arrow is pressed")
                    Player.change_x = -0.3
                if move_right:
                    # print("Right arrow is pressed")
                    Player.change_x = 0.3
                if fire:
                    if Missile.state == "ready":
                        missile_sound = mixer.Sound(os.path.join("image_sounds", "laser.wav"))
                        missile_sound.play()
                        Missile.x = Player.x + 16
                        Missile.draw()

                if g.life <= 0 and (event.key == pg.K_KP_ENTER or event.key == pg.K_RETURN):
                    restart_running()
            if event.type == pg.KEYUP:
                if move_left or move_right:
                    Player.change_x = 0

        if Player.x <= 0:
            Player.x = 0
        elif Player.x >= 736:
            Player.x = 736

        display_background()

        if Missile.y <= 0:
            Missile.y = 480
            Missile.state = "ready"

        Player.move()
        Player.draw()

        if Missile.state == "fire":
            Missile.draw()
            Missile.y -= Missile.change_y

        # Win
        if score_val >= 15:
            g.win += 1
            stop_running()
            show_win()

        if g.life > 0:
            score_val += o.asteroid_attack(asteroid_list, Player, Missile)
            asteroid(asteroid_list)
            # Ufo appears:
            if score_val >= 10:
                Ufo, ufo_score = o.ufo_attack(Ufo, Missile, Player)
                score_val += ufo_score
        else:
            g.game_over += 1
            stop_running()
            show_game_over()
            if g.game_over == 1:
                g.over_sound()

        show_score(scoreX, scoreY)
        show_life(lifeX, lifeY)

        pg.display.flip()
