import pygame
from pygame.locals import *
import sys
import random
from PIL import Image, ImageDraw

# create player and every other image
img = Image.new('RGB', (10,10), (255,0,0,255))
img.save('player-red.bmp')
img = Image.new('RGB', (10,10), (0,100,0,255))
img.save('player-green.bmp')
img = Image.new('RGB', (640, 480), (100,0,0,255))
img.save('background.bmp')

# import functions
from _cells_functions import *

pygame.init() #start pygame

for a in range(10): #spawn 10 reds
    spawn_red()
i = 0
while i < len(player_red): # place reds at random place
    player_red[i].place(random.randint(0,screen_x),random.randint(0, screen_y))
    i+=1
while True:
    for event in pygame.event.get(): # anything pressed = quit
        if event.type in (QUIT, KEYDOWN,):
            sys.exit()
    del_r = [] # queue red deletion
    del_g = [] # queue green deletion
    if random.randint(0, 100) >= red_spawn: # spawn by the odds
        spawn_red()
    if random.randint(0, 100) >= green_spawn: # same as above
        spawn_green()
    i = 0
    while i < len(player_red): # move every red by 1 px, reduce vitality by 0.05, dies if 0
        player_red[i].move(player_red_path_x[i],player_red_path_y[i])
        player_red[i].value -= 0.05
        if player_red[i].value < 0:
            del_r.append(i)
        if player_red[i].pos.x == player_red_path_x[i] and player_red[i].pos.y == player_red_path_y[i]:
            # is my position, my move target?
            player_red_path_x[i] = random.randint(0, screen_x)
            player_red_path_y[i] = random.randint(0, screen_y)
        i += 1
    i = 0
    while i < len(player_green): # set green place plus refresh and increase value by 0.000001
        player_green[i].value += 0.000001
        player_green[i].place(player_green_path_x[i], player_green_path_y[i])
        i += 1
    i = 0
    while i < len(player_red):
        pos = player_red[i].pos # get the position of red
        ib = 0
        while ib < len(player_red):# deathmatch!!!
            if i != ib:
                pos2 = player_red[ib].pos # second red position
                if close(pos.x, pos.y, pos2.x, pos2.y): # is close?, calculate vitality loss, until dead or flee
                    old = player_red[i].value
                    player_red[i].value -= player_red[ib].value
                    player_red[ib].value -= old
                    if old < 0: # dies on low vitality
                        del_r.append(i)
                    if player_red[ib].value < 0:
                        del_r.append(ib)
            ib += 1
        ib = 0
        while ib < len(player_green): # yummy
            pos2 = player_green[ib].pos
            if close(pos.x, pos.y, pos2.x, pos2.y): # is red close to food?, EAT!!!
                player_red[i].value += player_green[ib].value
                del_g.append(ib)
            ib += 1
        i += 1
    pygame.display.update()
    pygame.time.delay(100)
    screen.blit(background, (0, 0)) # update again

    for a in del_g: # set everything as dead, then delete
        player_green[a] = "dead"
        player_green_path_x[a] = "dead"
        player_green_path_y[a] = "dead"
    i = 0
    while i < len(player_green):
        if player_green[i] == "dead":
            del player_green[i]
            del player_green_path_x[i]
            del player_green_path_y[i]
            i -= 1
        i += 1
    del_g = []
    for a in del_r:
        player_red[a] = "dead"
        player_red_path_x[a] = "dead"
        player_red_path_y[a] = "dead"
    i = 0
    while i < len(player_red):
        if player_red[i] == "dead":
            del player_red[i]
            del player_red_path_x[i]
            del player_red_path_y[i]
            i -= 1
        i += 1
    del_r = []