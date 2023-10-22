###########################################
# FILE : asteroid.py
# WRITER : Noga_Friedman , nogafri
#          Nevo_Gat , nevo.gat
# Exercise: ex10
# DESCRIPTION: Class Asteroid of Asteroids game
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# WEB PAGES I USED: -
###########################################

from shape import Shape
import math


class Asteroid(Shape):
    """
    Class Asteroid: an asteroid object has a location on the screen (x,
    y coordinates), speed (on the x, y axis), a size and a radius.
    """
    def __init__(self, loc_x, loc_y, speed_x, speed_y, size):
        super().__init__(loc_x, loc_y, speed_x, speed_y, size * 10 - 5)
        self.__size = size

    def get_size(self):
        return self.__size

    def has_intersection(self, obj):
        """
        Checks if an object has intersected with an asteroid.
        :param obj: a ship or a torpedo object
        :return: True if the objects have intersected, False if they have not.
        """
        distance = math.hypot(obj.get_loc_x() - self.get_loc_x(),
                              obj.get_loc_y() - self.get_loc_y())
        if distance <= self.get_radius() + obj.get_radius():
            return True
        else:
            return False
