import pygame
from pygame.locals import *
import math

class Player(pygame.sprite.Sprite):
    #Class for the player and stuff

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.surf = pygame.Surface((25,25), pygame.SRCALPHA)
        self.surf.fill((0,0,0))
        self.rect = self.surf.get_rect(center = (300,300))
        self.img = pygame.image.load('pilot.png').convert_alpha()
        self.atkbox = pygame.Surface((20,40), pygame.SRCALPHA)
        self.atkbox.fill((255,0,0))
        self.atkrect = self.atkbox.get_rect(center = (300,300))
        self.atkimg_orig = pygame.image.load('sword.png').convert()

        self.pivot = pygame.math.Vector2(self.rect.center)
        self.atkpos = self.pivot

        self.now = pygame.time.get_ticks()
        self.lastatk = 0

        self.x = 300
        self.y = 300
        self.hp = 10
        self.maxhp = 10
        self.armor = 0
        self.str = 1
        self.dex = 2
    
    def rotate_on_pivot(self, image, angle, pivot, origin):

        surf = pygame.transform.rotate(image, angle)

        offset = pivot + (origin - pivot).rotate(-angle)
        rect = surf.get_rect(center = offset)

        return surf, rect

    def move(self):
        pressed_keys = pygame.key.get_pressed()
        velx = 0
        vely = 0

        #basic movement
        if pressed_keys[pygame.K_LEFT] or pressed_keys[pygame.K_a]:
            velx = -2
        if pressed_keys[pygame.K_RIGHT] or pressed_keys[pygame.K_d]:
            velx = 2
        if pressed_keys[pygame.K_UP] or pressed_keys[pygame.K_w]:
            vely = -2
        if pressed_keys[pygame.K_DOWN] or pressed_keys[pygame.K_s]:
            vely = 2

        #sprint
        if(pressed_keys[pygame.K_LSHIFT]):
            velx *= 2.5
            vely *= 2.5

        #update player pos
        self.rect.centerx = self.rect.centerx + velx
        self.rect.centery = self.rect.centery + vely

        #keeps player on screen
        if self.rect.centerx > 600:
            self.rect.centerx = 600
        if self.rect.centerx < 0:
            self.rect.centerx = 0
        if self.rect.centery > 600:
            self.rect.centery = 600
        if self.rect.centery < 0:
            self.rect.centery = 0
        
        self.pivot = pygame.math.Vector2(self.rect.center)
        self.atkpos = self.pivot + (00,25)

        mouse_pos = pygame.math.Vector2(pygame.mouse.get_pos())
        mouse_offset = mouse_pos - self.pivot
        mouse_angle = math.degrees(math.atan2(mouse_offset.x, mouse_offset.y))

        self.atkimg, self.atkrect = self.rotate_on_pivot(self.atkimg_orig, mouse_angle, self.pivot, self.atkpos)


    
    def damage(self, power):
        self.hp -= power*(1-self.armor)
        if self.hp <= 0:
           self.kill()

    def attack(self, enemy):
        self.now = pygame.time.get_ticks()
        pressed_keys = pygame.mouse.get_pressed()
        if pressed_keys[0] and self.now - self.lastatk > 1000/self.dex:
            self.lastatk = self.now
            print("DIE!")
            enemy.damage(self.str, False)

