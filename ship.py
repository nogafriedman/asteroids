###########################################
# FILE : ship.py
# WRITER : Noga_Friedman , nogafri
#          Nevo_Gat , nevo.gat
# Exercise: ex10
# DESCRIPTION: Class Ship of Asteroids game
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# WEB PAGES I USED: -
###########################################

from shape import Shape
import math


class Ship(Shape):
    """
    Class Ship: a ship object has a location on the screen (x,
    y coordinates), speed (on the x, y axis), heading (degrees),
    life points and a radius.
    """
    def __init__(self, loc_x, loc_y, speed_x, speed_y, heading, life=3):
        super().__init__(loc_x, loc_y, speed_x, speed_y, radius=1)
        self.__heading = heading  # degrees
        self.__life = life

    def get_heading(self):
        return self.__heading

    def turn_right(self):
        """
        Adjusts the ship's heading (called if is_right_pressed was True)
        :return: None
        """
        self.__heading -= 7

    def turn_left(self):
        """
        Adjusts the ship's heading (called if is_left_pressed was True)
        :return: None
        """
        self.__heading += 7

    def speed_up(self):
        """
        Speeds up the ship (called if is_up_pressed was True)
        :return:
        """
        new_speed_x = self.get_speed_x() + math.cos(math.radians(self.__heading))
        self.set_speed_x(new_speed_x)
        new_speed_y = self.get_speed_y() + math.sin(math.radians(self.__heading))
        self.set_speed_y(new_speed_y)

    def decrease_life(self):
        """
        Decreases the ship's life points by 1.
        :return: False if life points reached 0, True otherwise
        """
        self.__life -= 1
        if self.__life <= 0:
            return False
        else:
            return True
