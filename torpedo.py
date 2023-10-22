###########################################
# FILE : torpedo.py
# WRITER : Noga_Friedman , nogafri
#          Nevo_Gat , nevo.gat
# Exercise: ex10
# DESCRIPTION: Class Torpedo of Asteroids game
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# WEB PAGES I USED: -
###########################################

from shape import Shape
import math


class Torpedo(Shape):
    """
    Class Torpedo: a torpedo object has a location on the screen (x,
    y coordinates), speed (on the x, y axis), heading (degrees),
    life points and a radius.
    """
    def __init__(self, loc_x, loc_y, speed_x, speed_y, heading, life=200):
        # calculate torpedo's speed based on the shooting ship's speed:
        speed_x += 2 * math.cos(math.radians(heading))
        speed_y += 2 * math.sin(math.radians(heading))
        super().__init__(loc_x, loc_y, speed_x, speed_y, radius=4)
        self.__heading = heading  # degrees
        self.__life = life

    def get_heading(self):
        return self.__heading

    def decrease_life(self):
        """
        Decreases the torpedo's life points by 1.
        :return: False if life points reached 0, True otherwise
        """
        self.__life -= 1
        if self.__life <= 0:
            return False
        else:
            return True
