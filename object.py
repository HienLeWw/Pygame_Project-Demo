import pygame as pg
import random as rd
import math
import globals as g
import os

color_list = (os.path.join("image_sounds", "asteroid1.png"),
              os.path.join("image_sounds", "asteroid2.png"),
              os.path.join("image_sounds", "asteroid3.png"))
s_color_list = (os.path.join("image_sounds", "diamond.png"),
                os.path.join("image_sounds", "meteor.png"))
ufo_list = (os.path.join("image_sounds", "ufo_1.png"),
        os.path.join("image_sounds", "ufo_2.png"),
        os.path.join("image_sounds", "ufo_3.png"))


# Collision
def is_collision(A_x, A_y, B_x, B_y, is_special_skill):
    if not is_special_skill:
        distance = math.sqrt(math.pow(A_x - B_x, 2) + math.pow(A_y - B_y, 2))
        if distance <= 32.0:
            return True
        return False
    else:
        if A_x == B_x:
            return True
        return False


class Object:
    def __init__(self, img=pg.image.load(os.path.join("image_sounds", "pic.png")).convert_alpha(), x=0, y=0, change_x=0.0, change_y=0.0):
        self.img = img
        self.x = x
        self.y = y
        self.change_y = change_y
        self.change_x = change_x

    def move(self):
        self.y += self.change_y
        self.x += self.change_x

    def draw(self):
        g.screen.blit(self.img, (self.x, self.y))


class Enemy(Object):
    def __init__(self, img=pg.image.load(os.path.join("image_sounds", "pic.png")).convert_alpha(), x=0, y=0, change_x=0, change_y=0, s=False):
        super().__init__(img, x, y, change_x, change_y)
        self.s = s


class Bullet(Object):
    def __init__(self, img=pg.image.load(os.path.join("image_sounds", "pic.png")).convert_alpha(), x=0, y=0, change_x=0, change_y=0, state="ready", skill=False):
        super().__init__(img, x, y, change_x, change_y)
        self.state = state
        self.skill = skill

    def draw(self):
        self.state = "fire"
        if not self.skill:
            g.screen.blit(self.img, (self.x, self.y))
        else:
            g.screen.blit(self.img)


def asteroid_attack(asteroid_list, Player, Missile):
    score_val = 0
    for i in range(len(asteroid_list)):
        if asteroid_list[i].s:
            asteroid_list[i].change_y = 0.4
            asteroid_list[i].move()
        else:
            asteroid_list[i].change_y = rd.uniform(0.1, 0.3)
            asteroid_list[i].move()

    for i in range(len(asteroid_list)):
        got = is_collision(asteroid_list[i].x, asteroid_list[i].y, Missile.x, Missile.y, False) and (Missile.state == "fire")
        hit = is_collision(asteroid_list[i].x, asteroid_list[i].y, Player.x+16, Player.y, False)
        if got:
            g.explode_sound()
            Missile.y = 480
            Missile.state = "ready"
        if hit:
            g.life -= 1
        if got and asteroid_list[i].s:
            score_val += 1
        if asteroid_list[i].y >= 600 or got or hit:
            asteroid_list[i].y = 0
            asteroid_list[i].x = rd.randint(50, 730)
            asteroid_list[i].s = rd.getrandbits(1)
            if not asteroid_list[i].s:
                asteroid_list[i].img = pg.image.load(rd.choice(color_list)).convert_alpha()
            else:
                asteroid_list[i].img = pg.image.load(rd.choice(s_color_list)).convert_alpha()
    return score_val


asteroid = Enemy()


def create_asteroid():
    global asteroid
    n = 5
    asteroid_list = []
    count_s = rd.randint(1, 3)
    for i in range(n):
        s = False
        count = 0
        if count >= count_s:
            img = rd.choice(color_list)
            asteroid = Enemy(pg.image.load(img).convert_alpha(), rd.randint(50, 730), y=0, s=s)
        else:
            s = True
            count += 1
            img = rd.choice(s_color_list)
            asteroid = Enemy(pg.image.load(img).convert_alpha(), rd.randint(50, 730), y=0, s=s)
        asteroid_list.append(asteroid)
    return asteroid_list


def create_ufo():
    Ufo = Enemy(pg.image.load(rd.choice(ufo_list)).convert_alpha(), rd.randint(50, 730), change_x=0.3)
    return Ufo


# Laser
Laser = Bullet(pg.image.load(os.path.join("image_sounds", "laser.png")).convert_alpha(), change_x=0, change_y=1)


def ufo_attack(Ufo, Missile, Player):
    # Laser
    score_val = 0
    if is_collision(Ufo.x, Ufo.y, Missile.x, Missile.y, False):
        g.explode_sound()
        Missile.state = "ready"
        Missile.y = 480
        Ufo = create_ufo()
        Ufo.change_x = rd.choice((0.3, -0.3))
        score_val += 1

    Ufo.move()
    if Ufo.x <= 0:
        Ufo.change_x = 0.3
        Ufo.change_y = 30
        Ufo.move()
    elif Ufo.x >= 730:
        Ufo.change_x = -0.3
        Ufo.change_y = 30
        Ufo.move()
    Ufo.change_y = 0

    Ufo.draw()
    g.shooting_time += 0.5
    wait_time = rd.choice((700, 500))
    if Laser.state == "ready" and g.shooting_time >= wait_time:
        Laser.x = Ufo.x
        Laser.draw()
        g.shooting_time = 0
    if Laser.state == "fire":
        Laser.y += Laser.change_y
        Laser.draw()
    collision = is_collision(Laser.x, Laser.y, Player.x, Player.y, False)
    if collision:
        g.life -= 1
    if Laser.y >= 600 or collision:
        Laser.y = Ufo.y
        Laser.state = "ready"

    return Ufo, score_val




