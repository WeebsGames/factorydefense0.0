import pygame
from pygame.locals import *
import math

import Player
import Bloons

pygame.init()
#initializes game

screen = pygame.display.set_mode((600, 600))
clock = pygame.time.Clock()

icon = pygame.image.load("retard.jpeg")
#loads image

pygame.display.set_icon(icon)
pygame.display.set_caption("Factory Defense")

#setup stuff

screen.fill([89, 128, 158])
#makes blue-gray backgrounds

#global variable definitions
WIDTH = 600
HEIGHT = 600
vec = pygame.math.Vector2

#function definitions

r = 0
g = 0
b = 0
up = True
def breatheRed(red, dir):
    if(red == 255):
        dir = False
    if(red == 0):
        dir = True
    if dir:
        red+=1
    else:
        red-=1
    return red
def breatheGreen(green, dir):
    if(green == 255):
        dir = False
    if(green == 0):
        dir = True
    if dir:
        green+=1
    else:
        green-=1
    return green
def breatheBlue(blue, dir):
    if(blue == 255):
        dir = False
    if(blue == 0):
        dir = True
    if dir:
        blue+=1
    else:
        blue-=1
    return blue, dir

def faceMouse(surf, rect, correction):
    mx, my = pygame.mouse.get_pos()
    angle  = math.degrees(math.atan2((mx-rect.centerx-10),(my-rect.centery-10)))
    return pygame.transform.rotozoom(surf, angle - correction, 1)

#class definitions
    #moved to separate files

#variable setup

fachp = 250

p1 = Player.Player()

e1 = Bloons.Enemy(1, 0)
e2 = Bloons.Enemy(1, 1)
e3 = Bloons.Enemy(1, 1)
e4 = Bloons.Enemy(1, 1)
e5 = Bloons.Enemy(2, 1)
e6 = Bloons.Enemy(1, 4)
e7 = Bloons.Enemy(1, 0.75)

spawnq = [e1, e2, e3, e4, e5, e6, e7]
enemies = []

object1 = pygame.Rect((20,60), (50,100))
object2 = pygame.Rect((20,50), (100,100))
print(object1.colliderect(object2))
print(object2.collidepoint(50, 75))

tester = pygame.Rect((0,0), (100,100))

track1 = pygame.Rect((0,290),(210,30))
track2 = pygame.Rect((200, 290), (30, 100))
track3 = pygame.Rect((130,390),(100, 30))
track4 = pygame.Rect((130,390),(30,100))
track5 = pygame.Rect((130,490), (300, 30))
track6 = pygame.Rect((400,95),(30,400))
track7 = pygame.Rect((70,95), (330,30))

tracks = [track1, track2, track3, track4, track5, track6, track7]

emptyhp = pygame.Rect((450,20),(100,30))
currhp = pygame.Rect((450,20),(100,30))
heartimg = pygame.image.load('pixel_heart.png')
heartimg = pygame.transform.rotozoom(heartimg, 0, 0.75)

emptyfhp = pygame.Rect((75,20),(100,30))
currfhp = pygame.Rect((75,20),(100,30))
facimg = pygame.image.load('factory.png')
facimg = pygame.transform.rotozoom(facimg, 0, 0.75)

all_sprites = pygame.sprite.Group()

now = pygame.time.get_ticks()
lastspawn = now
running = True
while running:
    #game stuff
    p1.move()
    events = pygame.event.get()
    #pygame.display.flip()
    screen.fill([89, 128, 158])
    pygame.draw.rect(screen, (r, g, b), object1)

    #spawn bloons
    now = pygame.time.get_ticks()
    if spawnq != [] and now - lastspawn > spawnq[0].stagger*500:
        spawnq[0].spawn()
        lastspawn = now
        enemies.append(spawnq[0])
        all_sprites.add(spawnq[0])
        spawnq.pop(0)

    #draw track
    for track in tracks:
        pygame.draw.rect(screen, (110, 72, 50), track)
    
    #blue breathing for factory
    b, up = breatheBlue(b, up)

    #draw entities 
    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)
    
    screen.blit(faceMouse(p1.surf, p1.rect, 180), p1.rect.topleft)

    #debug for attackbox
    screen.blit(faceMouse(p1.atkbox, p1.atkrect, 90), p1.atkrect.topleft)

    #draw bloon turn hitboxes (debug)
    # for turn in Bloons.turns:
    #     pygame.draw.rect(screen, (20,20,20), turn)
    for enemy in enemies:
        #damage factory
        if object1.colliderect(enemy):
            enemy.rect.center = (999,999)
            fachp -= enemy.hp
            enemy.kill()
        #player contact damage
        if p1.rect.colliderect(enemy):
            enemy.rect.center = (999,999)
            p1.damage(1/enemy.hp + 1)
            enemy.damage(1/enemy.hp + 1, True)
        #player weapon  
        if p1.atkrect.colliderect(enemy):
            p1.attack(enemy)

        #move enemy
        enemy.move()
        

    #draw hp bar
    pygame.draw.rect(screen, (0,0,0), emptyhp)
    pygame.draw.rect(screen, (200,0,0), currhp)
    currhp = pygame.Rect((450,20),(p1.hp/p1.maxhp * 100, 30))
    screen.blit(heartimg, (550,15))
    
    #draw fhp bar
    pygame.draw.rect(screen, (0,0,0), emptyfhp)
    pygame.draw.rect(screen, (0,0,200), currfhp)
    currfhp = pygame.Rect((75,20), (fachp/250 * 100, 30))
    screen.blit(facimg, (30, 15))
    
    pygame.display.update()
    clock.tick(60)
    #sets game to run at 60fps

    for event in events:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            running = False