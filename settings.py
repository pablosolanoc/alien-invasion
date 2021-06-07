

class Settings():

    def __init__(self):

        #Screen Settings
        self.screen_width=1200
        self.screen_heigth=800
        self.bg_color=(0,1,4)

        #Ship Settings
        self.hero_limit=1

        #Rocket Settings
        self.bullet_width=5
        self.bullet_height=80
        self.bullet_color= 220,50,50
        self.bullets_allowed = 3


        #setting up the DeathStar on screen
        self.death_star_location_x=self.screen_width-100
        self.death_star_location_y=100


        self.fleet_drop_speed=10

        self.score_scale = 1.5

        self.speedup_scale = 1.2

        self.star_speed=1

        self.initialize_dynamic_settings()

    def initialize_dynamic_settings(self):
        self.hero_speed_factor = 1
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1

        self.tie_points = 50

    def increase_speed(self):
        self.hero_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.tie_points = int(self.tie_points * self.score_scale)
