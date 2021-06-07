
import sys
import pygame
from bullets import Bullet
from empire import TieFighter
from widgets import Star
from time import sleep
from random import randint
from pygame_functions import *


def check_events(ai_settings,screen,stats,play_button,ship,bullets,ties,sb):

    for event in pygame.event.get():
        """Respond to keypresses and mouse events."""
        if event.type==pygame.QUIT:
            sys.exit()
        elif event.type==pygame.KEYDOWN:
            check_keydown_events(event,ai_settings,screen,ship, bullets)
        elif event.type==pygame.KEYUP:
            check_keyup_events(event,ship)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x,mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings,screen,stats,play_button,ship,ties,bullets,mouse_x,mouse_y,sb)

def check_play_button(ai_settings,screen,stats,play_button,ship,ties,bullets,mouse_x,mouse_y,sb):


    button_clicked=play_button.rect.collidepoint(mouse_x,mouse_y)

    if button_clicked and not stats.game_active:

        ai_settings.initialize_dynamic_settings()
        stats.reset_stats()
        stats.game_active = True

        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        ties.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,ties)
        ship.center_ship()

def check_keydown_events(event,ai_settings, screen ,ship,bullets):

    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key== pygame.K_UP:
        ship.moving_up=True
    if event.key== pygame.K_DOWN:
        ship.moving_down=True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings,screen,ship,bullets)
    if event.key==pygame.K_q:
        sys.exit()




def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False
    if event.key== pygame.K_UP:
        ship.moving_up=False
    if event.key== pygame.K_DOWN:
        ship.moving_down=False

def create_background():
    rand=randint(1,4)
    flag_star=True
    list_ships=list()
    for i in range(rand):
        rand2=randint(1,4)
        print(rand2)
        if rand2==1:
            if flag_star:
                back=pygame.image.load('images/deathstar1.png')
                flag_star = False
        elif rand2==2:
            back = pygame.image.load('images/destroyer1.png')
        elif rand2==3:
            back = pygame.image.load('images/imageturned1.png')
        elif rand2==4:
            back = pygame.image.load('images/destroyer2.png')

        list_ships.append(back)

    return list_ships

def get_background_rect(list_ships,ai_settings):
    information=dict()

    for ship in list_ships:
        rect = ship.get_rect()
        rect.x = randint(200,ai_settings.screen_width-200)
        rect.y = randint(100, ai_settings.screen_heigth-100)
        information[ship]=rect

    return information

def show_images(screen,dict_information):

    for i in dict_information:
        screen.blit(i,dict_information[i])


def update_screen(ai_settings,stats,screen,sb,ship,bullets,ties,play_button,information):

    """Update images on the screen and flip to the new screen."""
    # Redraw the screen during each pass through the loop.
    screen.fill(ai_settings.bg_color)
    show_images(screen, information)



    for bullet in bullets.sprites():
        bullet.draw_bullet()

    ship.blitme()
    ties.draw(screen)
    sb.show_score()



    if not stats.game_active:
        play_button.draw_button()

    # Make the most recently drawn screen visible.
    pygame.display.flip()

def update_bullets(ai_settings,screen,stats,sb,ship,ties,bullets):

    bullets.update()

    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)

    check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,ties,bullets)

def check_bullet_alien_collisions(ai_settings,screen,stats,sb,ship,ties,bullets):
    collisions = pygame.sprite.groupcollide(bullets, ties, True, True)
    
    if collisions:
        for aliens in collisions.values():
            for alien in aliens:
                # explode(alien.rect.x,alien.rect.y)
                print(alien.rect.x)
                print(alien.rect.y)
            stats.score += ai_settings.tie_points*len(aliens)
            sb.prep_score()

        check_high_score(stats,sb)

    if len(ties) == 0:
        bullets.empty()
        ai_settings.increase_speed()

        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, ties)



def fire_bullet(ai_settings,screen,ship,bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def get_number_ties_x(ai_settings,tie_width):
    available_space_x = ai_settings.screen_width - (tie_width)
    number_fighters_x = int(available_space_x / (2 * tie_width)) - 1
    return number_fighters_x

def create_alien(ai_settings,screen,ties,tie_number, row_number):
    newTie = TieFighter(ai_settings, screen)
    tie_width=newTie.rect.width
    newTie.x = tie_width + (2 * tie_width * tie_number)
    newTie.rect.x = newTie.x
    newTie.rect.y= 2*newTie.rect.height + (1.5*newTie.rect.height*row_number)
    ties.add(newTie)

def get_number_rows(ai_settings,ship_height,tie_height):
    available_space_y=ai_settings.screen_heigth-(3*tie_height)-ship_height
    number_rows=int(available_space_y/(2*tie_height))
    return number_rows

def create_fleet(ai_settings, screen, ship,ties):

    tie = TieFighter(ai_settings,screen)
    number_fighters_x=get_number_ties_x(ai_settings,tie.rect.width)
    number_rows=get_number_rows(ai_settings,ship.rect.height,tie.rect.height)+1

    for row_number in range(number_rows):
        for tie_number in range(number_fighters_x):
           create_alien(ai_settings,screen,ties,tie_number,row_number)

def update_ties(ai_settings,stats,screen,sb,ship,ties,bullets):

    check_fleet_edges(ai_settings,ties)
    ties.update()

    if pygame.sprite.spritecollideany(ship,ties):
        ship_hit(ai_settings,stats,screen,sb,ship,ties,bullets)

    check_ties_bottom(ai_settings,stats,screen,sb,ship,ties,bullets)

def check_fleet_edges(ai_settings,ties):

    for tie in ties.sprites():
        if tie.check_edges():
            change_fleet_direction(ai_settings,ties)
            break

def change_fleet_direction(ai_settings,ties):
    for tie in ties.sprites():
        tie.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1

def ship_hit(ai_settings,stats,screen,sb,ship,ties,bullets):

    if stats.ships_left>= 0:

        stats.ships_left-=1

        sb.prep_ships()

        ties.empty()
        bullets.empty()

        create_fleet(ai_settings,screen,ship,ties)
        ship.center_ship()

        sleep(0.5)

    else:
        stats.ships_left -= 1

        sb.prep_ships()
        stats.game_active= False


def check_ties_bottom(ai_settings,stats,screen,sb,ship,ties,bullets):

    screen_rect = screen.get_rect()
    for tie in ties.sprites():
        if tie.rect.bottom>= screen_rect.bottom:
            ship_hit(ai_settings,stats,screen,sb,ship,ties,bullets)
            break

def check_high_score(stats,sb):
    if stats.score>stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()
