###########################################
# FILE : asteroids_main.py
# WRITER : Noga_Friedman , nogafri
#          Nevo_Gat , nevo.gat
# Exercise: ex10
# DESCRIPTION: Class GameRunner of Asteroids game
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# WEB PAGES I USED: -
###########################################

from screen import Screen
import sys
import random
from ship import *
from asteroid import *
from torpedo import *
import math

DEFAULT_ASTEROIDS_NUM = 5
# added:
ASTEROIDS_SCORE = {3: 20, 2: 50, 1: 100}
SPEED_OPTIONS = [1, 2, 3, 4, -1, -2, -3, -4]


class GameRunner:

    def __init__(self, asteroids_amount):
        self.__screen = Screen()
        self.__screen_max_x = Screen.SCREEN_MAX_X
        self.__screen_max_y = Screen.SCREEN_MAX_Y
        self.__screen_min_x = Screen.SCREEN_MIN_X
        self.__screen_min_y = Screen.SCREEN_MIN_Y
        # added:
        self.__ship = self.create_ship()  # creates a new ship
        self.__asteroids = self.create_asteroids(asteroids_amount)
        self.__torpedoes = []
        self.draw_objects()  # draws a ship, asteroids and torpedoes
        self.__score = 0  # initializes user score at 0

    def run(self):
        self._do_loop()
        self.__screen.start_screen()

    def _do_loop(self):
        # You should not to change this method!
        self._game_loop()
        # Set the timer to go off again
        self.__screen.update()
        self.__screen.ontimer(self._do_loop, 5)

    def _game_loop(self):
        self.user_win()
        self.check_pressed_keys()
        self.move_objects()
        self.torpedo_lifetime()
        for asteroid in self.__asteroids:
            if self.asteroid_torpedo_impact(asteroid):
                continue  # asteroid has been destroyed - skip to the next one
            self.asteroid_ship_impact(asteroid)  # check impact with ship
        self.draw_objects()

    #################################
    # ADDED FUNCTIONS - NOT IN API: #

    def get_random_loc(self):
        """
        Randomizes a location on the x, y axis within screen boundaries.
        :return: list - [x coordinate, y coordinate]
        """
        loc_x = random.randint(self.__screen_min_x, self.__screen_max_x)
        loc_y = random.randint(self.__screen_min_y, self.__screen_max_y)
        return [loc_x, loc_y]

    def create_ship(self):
        """
        Creates a ship object with location chosen randomly within screen
        boundaries, starting speed at 0, and heading degree at 0.
        :return: ship object
        """
        loc_x = random.randint(self.__screen_min_x, self.__screen_max_x)
        loc_y = random.randint(self.__screen_min_y, self.__screen_max_y)
        ship = Ship(loc_x, loc_y, 0, 0, 0)
        return ship

    def create_asteroids(self, asteroids_amount):
        """
        Creates asteroids for the game based on the requested amount and adds
        them to a list.
        :param asteroids_amount: int - number of asteroids to create
        :return: list of asteroid objects
        """
        asteroids = []
        for i in range(asteroids_amount):
            # randomize coordinates for the asteroid's location:
            speed_x = random.choice(SPEED_OPTIONS)
            speed_y = random.choice(SPEED_OPTIONS)
            # check if asteroid's location intersects with the ship, and if
            # so, randomize different coordinates for it's location:
            while True:
                loc_x = self.get_random_loc()[0]
                loc_y = self.get_random_loc()[1]
                asteroid = Asteroid(loc_x, loc_y, speed_x, speed_y, 3)
                if not asteroid.has_intersection(self.__ship):
                    break
            # after asteroid was created successfully, add to asteroids list:
            asteroids.append(asteroid)
            self.__screen.register_asteroid(asteroid, 3)
        return asteroids

    def draw_objects(self):
        """
        Draws an object by using the drawing function from Screen and
        updates it's visuals on screen.
        :return: None
        """
        # draw ship:
        self.__screen.draw_ship(self.__ship.get_loc_x(),
                                self.__ship.get_loc_y(),
                                self.__ship.get_heading())
        # draw asteroid:
        for asteroid in self.__asteroids:
            self.__screen.draw_asteroid(asteroid, asteroid.get_loc_x(),
                                        asteroid.get_loc_y())

        # draw torpedoes:
        for torpedo in self.__torpedoes:
            self.__screen.draw_torpedo(torpedo, torpedo.get_loc_x(),
                                       torpedo.get_loc_y(),
                                       torpedo.get_heading())

    def move_objects(self):
        """
        Moves objects according to the given formula.
        :return: None
        """
        # ship:
        self.__ship.move(self.__screen_min_x, self.__screen_max_x,
                         self.__screen_min_y, self.__screen_max_y)
        # asteroids:
        for asteroid in self.__asteroids:
            asteroid.move(self.__screen_min_x, self.__screen_max_x,
                          self.__screen_min_y, self.__screen_max_y)

        # torpedoes:
        for torpedo in self.__torpedoes:
            torpedo.move(self.__screen_min_x, self.__screen_max_x,
                         self.__screen_min_y, self.__screen_max_y)

    def check_pressed_keys(self):
        """
        Checks if user pressed any key (by using functions from Screen) and
        executes the desired action.
        :return: None
        """
        if self.__screen.is_left_pressed():
            self.__ship.turn_left()  # turns the ship left
        if self.__screen.is_right_pressed():
            self.__ship.turn_right()  # turns the ship right
        if self.__screen.is_up_pressed():
            self.__ship.speed_up()  # speeds the ship up
        if self.__screen.is_space_pressed() and len(self.__torpedoes) < 10:
            self.fire_torpedo()  # fires one torpedo
        if self.__screen.should_end():  # ends the game if user pressed 'q'
            self.__screen.show_message("Quit Game", "You have quit the "
                                                    "game, goodbye!")
            self.__screen.end_game()
            sys.exit()

    def asteroid_torpedo_impact(self, asteroid):
        """
        Checks if the asteroid has been hit by a torpedo, and if so -
        splits it into two smaller asteroids.
        :param asteroid: asteroid object
        :return: True if asteroid has been hit by a torpedo, otherwise False
        """
        for torpedo in self.__torpedoes:
            if asteroid.has_intersection(torpedo):
                # remove the torpedo from the game:
                self.__torpedoes.remove(torpedo)
                self.__screen.unregister_torpedo(torpedo)
                # split the asteroid:
                self.split_asteroid(asteroid, torpedo)
                return True
        return False

    def asteroid_ship_impact(self, asteroid):
        """
        Checks if the asteroid has collided with the ship, and if so -
        removes it from the game, decreases the ship's life points by 1,
        and adds points to user score based on the asteroid's size.
        :param asteroid: asteroid object
        :return: None
        """
        # check if collided:
        if asteroid.has_intersection(self.__ship):
            # remove destroyed asteroid:
            self.__asteroids.remove(asteroid)
            self.__screen.unregister_asteroid(asteroid)

            # decrease a life point from the ship:
            has_life = self.__ship.decrease_life()
            self.__screen.remove_life()

            # check if ship has reached 0 life points and is dead:
            if not has_life:
                self.__screen.show_message("Game Over",
                                           "You have lost all your lives! "
                                           "Final score: " + str(self.__score))
                self.__screen.end_game()
                sys.exit()
            else:
                self.__screen.show_message("Warning",
                                           "You have just hit an asteroid!")

    def fire_torpedo(self):
        """
        Creates a torpedo for the ship to fire.
        :return: None
        """
        # create a torpedo object with the ship's data:
        torpedo = Torpedo(self.__ship.get_loc_x(), self.__ship.get_loc_y(),
                          self.__ship.get_speed_x(), self.__ship.get_speed_y(),
                          self.__ship.get_heading())
        self.__torpedoes.append(torpedo)
        self.__screen.register_torpedo(torpedo)

    def split_asteroid(self, asteroid, torpedo):
        """
        "Splits" the hit asteroid to two new created asteroids and removes
        the hit asteroid from the game.
        :param asteroid: asteroid object
        :param torpedo: torpedo object
        :return: None
        """
        # if asteroid's size is 1, skip to the end of the function to just 
        # remove it from the game without splitting it:
        if asteroid.get_size() > 1:
            # calculate the speed of the new asteroid:
            distance = math.hypot(asteroid.get_speed_x(),
                                  asteroid.get_speed_y())
            asteroid_new_speed_x = \
                (torpedo.get_speed_x() + asteroid.get_speed_x()) / distance
            asteroid_new_speed_y = \
                (torpedo.get_speed_y() + asteroid.get_speed_y()) / distance

            # create two new asteroids instead of the previous one:
            for i in -1, 1:
                # gives the asteroid a negative speed if i = -1,
                # and gives it a positive speed if i = 1:
                new_asteroid = Asteroid(asteroid.get_loc_x(),
                                        asteroid.get_loc_y(),
                                        i * asteroid_new_speed_x,
                                        i * asteroid_new_speed_y,
                                        asteroid.get_size() - 1)

                self.__screen.register_asteroid(new_asteroid,
                                                asteroid.get_size() - 1)
                self.__asteroids.append(new_asteroid)
        # increase user score:
        self.__score += ASTEROIDS_SCORE[asteroid.get_size()]
        self.__screen.set_score(self.__score)
        # remove impacted asteroid from the game:
        self.__screen.unregister_asteroid(asteroid)
        self.__asteroids.remove(asteroid)

    def torpedo_lifetime(self):
        """
        Decreases the torpedoes' life points by 1 with each loop of the
        game, and removes a torpedo when it reaches 0.
        :return: None
        """
        for torpedo in self.__torpedoes:
            has_life = torpedo.decrease_life()
            if not has_life:
                self.__screen.unregister_torpedo(torpedo)
                self.__torpedoes.remove(torpedo)

    def user_win(self):
        """
        Checks if usr has destroyed all the asteroids, if so - prints a
        winning message and ends the game.
        :return: None
        """
        if self.__asteroids == []:
            self.__screen.show_message("YOU WIN!", "You have destroyed "
                                       "all the asteroids! Final score: "
                                       + str(self.__score))
            self.__screen.end_game()
            sys.exit()

    #################################


def main(amount):
    runner = GameRunner(amount)
    runner.run()


if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
