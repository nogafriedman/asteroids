###########################################
# FILE : shape.py
# WRITER : Noga_Friedman , nogafri
#          Nevo_Gat , nevo.gat
# Exercise: ex10
# DESCRIPTION: Class Shape of Asteroids game
# STUDENTS I DISCUSSED THE EXERCISE WITH: -
# WEB PAGES I USED: -
###########################################

class Shape:
    """
    A class of objects that are shapes in space, that share traits like
    having a location, speed and radius.
    """
    def __init__(self, loc_x, loc_y, speed_x, speed_y, radius):
        self.__loc_x = loc_x
        self.__loc_y = loc_y
        self.__speed_x = speed_x
        self.__speed_y = speed_y
        self.__radius = radius

    # setters:
    def set_loc_x(self, new_location):
        self.__loc_x = new_location

    def set_loc_y(self, new_location):
        self.__loc_y = new_location

    def set_speed_x(self, new_speed):
        self.__speed_x = new_speed

    def set_speed_y(self, new_speed):
        self.__speed_y = new_speed

    # getters:
    def get_loc_x(self):
        return self.__loc_x

    def get_loc_y(self):
        return self.__loc_y

    def get_speed_x(self):
        return self.__speed_x

    def get_speed_y(self):
        return self.__speed_y

    def get_radius(self):
        return self.__radius

    def move(self, screen_min_x , screen_max_x, screen_min_y, screen_max_y):
        """
        Calculates the new location of the object according to the formula:
        NewSpot_i = ScreenMin_i +
        (OldSpot_i + Speed_i - ScreenMin_i) % (ScreenMax_i - ScreenMin_i)
        with 'i' being either x or y.
        :return: None
        """
        # change location on the x axis:
        new_x_location = screen_min_x + \
                       (self.__loc_x + self.__speed_x - screen_min_x) % \
                       (screen_max_x - screen_min_x)
        self.set_loc_x(new_x_location)

        # change location on the y axis:
        new_y_location = screen_min_y + \
                       (self.__loc_y + self.__speed_y - screen_min_y) % \
                       (screen_max_y - screen_min_y)
        self.set_loc_y(new_y_location)
