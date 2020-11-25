import pygame
from pygame.locals import *
import random
import math
class GameObject:
    def __init__(self, image, screen, value):
        self.image = image # oject image
        self.pos = image.get_rect() # object position
        self.screen = screen # screen being used
        self.value = value # vitality
    def move(self, _tox, _toy): # move towards position
        if self.pos.x > _tox:
            self.pos.x -= 1
        if self.pos.x < _tox:
            self.pos.x += 1
        if self.pos.y > _toy:
            self.pos.y -= 1
        if self.pos.y < _toy:
            self.pos.y += 1
        self.screen.blit(self.image, self.pos)
    def place(self, _tox, _toy): # teleports to position
        self.pos.x = _tox
        self.pos.y = _toy
        self.screen.blit(self.image, self.pos)

def close(x,y, tx, ty, dist=10):# is me (x,y) close to him (tx, ty) with a distance of X pixels?
    if abs(x-tx) <= dist and abs(y-ty) <= dist:
        return True
    else:
        return False

player_red = [] # red thingis
player_red_path_x = [] # red go position
player_red_path_y = [] # red go position
red_value = 50 # vitality
red_spawn = 99 # chance to spawn (100-x = chance)

# same as red, but green
player_green = []
player_green_path_x = []
player_green_path_y = []
green_value = 10
green_spawn = 99

# screen x and y
screen_x = 640
screen_y = 480

grid = 10 # grid to spawn greens

#set everything up
screen = pygame.display.set_mode((screen_x, screen_y))
player = pygame.image.load('player-red.bmp').convert() # red people
greens = pygame.image.load('player-green.bmp').convert() # food
background = pygame.image.load('background.bmp').convert()
screen.blit(background, (0, 0))

def spawn_red():# place new red at a given position
    o = GameObject(player,screen, red_value)
    player_red.append(o)
    player_red_path_x.append(random.randint(0,screen_x))
    player_red_path_y.append(random.randint(0, screen_y))
    o.place(random.randint(0, screen_x), random.randint(0, screen_y))

def spawn_green(): # place new green at a given position, if already in use, try other place in radius
    o = GameObject(greens,screen, green_value)
    x = random.randint(0,screen_x)
    y = random.randint(0, screen_y)
    x = round(x/grid)*grid
    y = round(y/grid)*grid

    size = grid * 5 # circle radius
    points = size * 4 # joints in the circle (the bigger the more precise)
    count = points
    radius = size
    center = [x,y] # center, duh
    angle_step = 2.0 * math.pi / count # math to 360 formula
    angle = 0 # initial angle
    steps = [] # joints
    for i in range(0, count):# create joints and angle
        direction = [math.cos(angle), math.sin(angle)]
        pos = [center[0] + direction[0] * radius,center[1] + direction[1] * radius]
        steps.insert(0, pos)
        angle += angle_step

    for s in steps:
        for ss in steps:
            if ss[1] == s[1] or ss[1] - s[1] > 0 and ss[1] - s[1] < grid - 1: # check if loop variable is equal or inside grid
                last = [0,0] # create last position
                while True:
                    if last[1] > s[1] and last[1] > ss[1]: # if last outside circle (y bigger than biggest circle joint y value)
                        break
                    if last[0] >= ss[0] and last[0] <= s[0] and last[1] > s[1] - grid and last[1] > ss[1] - grid: # is last inside?
                        if last[0] != player_green_path_x and last[1] != player_green_path_y: # not occupied by green? so add a green!
                            player_green.append(o)
                            player_green_path_x.append(last[0])
                            player_green_path_y.append(last[1])
                            o.place(last[0], last[1])
                            return
                    last[0] += grid # add a grid to the right
                    if last[0] > screen_x: # is too much to the right? go back and a little down!
                        last[0] = 0
                        last[1] += grid