import pygame
import time
from pygame.locals import *

#turn hitboxes for enemies
turn0 = pygame.Rect((-10,300), (5,5))
turn1 = pygame.Rect((225,290),(5,30))
turn2 = pygame.Rect((200,415), (30,5))
turn3 = pygame.Rect((130,390), (5,30))
turn4 = pygame.Rect((130,515), (30,5))
turn5 = pygame.Rect((425,490), (5,30))
turn6 = pygame.Rect((400,95), (30,5))

turns = [turn1, turn2, turn3, turn4, turn5, turn6, turn0]

class Enemy(pygame.sprite.Sprite):
    #class definition for the enemies

    def __init__(self, tier, stagger):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((15,15))
        self.stagger = stagger
        self.velx = 0
        self.vely = 0
        if tier == 1:
            self.hp = 1
            self.speed = 1
            self.armor = 0
            self.surf.fill((44, 91, 24))
        if tier == 2:
            self.hp = 2
            self.speed = 1
            self.armor = 0
            self.surf.fill((116, 88, 193))
        if tier == 3:
            self.hp = 2
            self.speed = 2
            self.armor = 0
            self.surf.fill((51, 255, 0))
        if tier == 4:
            self.hp = 4
            self.speed = 2
            self.armor = 0.1
            self.surf.fill((19, 69, 183))
        if tier == 5:
            self.hp = 2
            self.speed = 5
            self.armor = 0
            self.surf.fill((0, 255, 255))
        if tier == 6:
            self.hp = 10
            self.speed = 2
            self.armor = 0.5
            self.surf.fill((55, 66, 73))
        
    def damage(self, power, ignore):
        if not ignore:
            self.hp -= power*(1-self.armor)
        else:
            self.hp -= power
        if self.hp <= 0:
           self.kill()
         
    def spawn(self):
        self.rect = self.surf.get_rect(center = (turn0.center))

    def move(self):
        self.rect.centerx = self.rect.centerx + self.velx
        self.rect.centery = self.rect.centery + self.vely
        if self.rect.colliderect(turn0):
            self.velx = self.speed
        if self.rect.colliderect(turn1):
            self.vely = self.speed
            self.velx = 0
        if self.rect.colliderect(turn2):
            self.velx = self.speed * -1
            self.vely = 0
        if self.rect.colliderect(turn3):
            self.vely = self.speed
            self.velx = 0
        if self.rect.colliderect(turn4):
            self.velx = self.speed
            self.vely = 0
        if self.rect.colliderect(turn5):
            self.vely = self.speed * -1
            self.velx = 0
        if self.rect.colliderect(turn6):
            self.vely = 0
            self.velx = self.speed * -1
