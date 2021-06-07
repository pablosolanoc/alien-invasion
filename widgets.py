import pygame
from random import randint


class Star():

    def __init__(self,screen,ai_settings):

        self.screen=screen
        self.ai_settings = ai_settings

        self.image=pygame.image.load('images/star.png')
        self.rect=self.image.get_rect()
        self.screen_rect=self.screen.get_rect()

        self.rect.bottom=self.screen_rect.top
        self.rect.centerx=randint(50,750)

        self.centery=float(self.rect.centery)

    def biltme(self):
        self.screen.blit(self.image,self.rect)

    def update(self):
        self.centery+=self.ai_settings.star_speed
        self.rect.bottom=self.centery

