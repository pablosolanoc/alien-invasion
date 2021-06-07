import pygame
from settings import Settings
from hero import Hero
import game_functions as gf
from pygame.sprite import Group
from gamestats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():

    pygame.init()
    ai_settings=Settings()
    screen=pygame.display.set_mode((ai_settings.screen_width,ai_settings.screen_heigth))
    pygame.display.set_caption("Alien Invasion")

    play_button = Button(ai_settings,screen,"Play")
    stats=GameStats(ai_settings)
    sb = Scoreboard(ai_settings,screen,stats)

    ship=Hero(screen,ai_settings)
    bullets=Group()
    ties = Group()
    gf.create_fleet(ai_settings,screen,ship,ties)

    listships = gf.create_background()
    information=gf.get_background_rect(listships,ai_settings)

    print(pygame.font.get_fonts())


    # Start the main loop for the game.
    while True:

            gf.check_events(ai_settings, screen, stats, play_button, ship, bullets, ties, sb)


            if stats.game_active:

                ship.update()
                gf.update_bullets(ai_settings,screen,stats,sb,ship,ties,bullets)
                gf.update_ties(ai_settings,stats,screen,sb,ship,ties,bullets)

            gf.update_screen(ai_settings, stats, screen, sb, ship, bullets, ties, play_button, information)


run_game()
