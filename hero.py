import pygame
from pygame.sprite import Sprite

class Hero(Sprite):

    def __init__(self,screen, ai_settings):

        super(Hero, self).__init__()
        self.screen=screen
        self.ai_settings= ai_settings

        self.image=pygame.image.load('./images/milleium falcon.png')
        self.rect=self.image.get_rect()
        self.screen_rect=self.screen.get_rect()

        self.rect.centerx=self.screen_rect.centerx
        self.rect.bottom=self.screen_rect.bottom
        #self.rect.bottom=self.screen_rect.bottom

        self.centerx=float(self.rect.centerx)
        self.centery=float(self.rect.centery)

        self.moving_right=False
        self.moving_left=False
        self.moving_up=False
        self.moving_down=False

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def update(self):
        """Update the ship's position based on the movement flag."""
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.hero_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.centerx -= self.ai_settings.hero_speed_factor
        if self.moving_up and self.rect.top > 0:
            self.centery -= self.ai_settings.hero_speed_factor
        if self.moving_down and self.rect.bottom < self.screen_rect.bottom:
            self.centery += self.ai_settings.hero_speed_factor

        self.rect.centerx=self.centerx
        self.rect.centery=self.centery

    def center_ship(self):
        self.centerx = self.screen_rect.centerx
        self.centery = self.screen_rect.bottom