import utility
import math
import abc
import turtle
from PIL import Image

def solve_task4():
    """ Solve the fourth task of the 4-th laboratory work.
    """
    print("You have a rhomb with side, sharp angle and color. Enter their values. ")
    rhomb_parameters = get_rhomb_parameters()
    rhomb = Rhomb(rhomb_parameters[0], rhomb_parameters[1], rhomb_parameters[2])

    image_filename = input("Enter filename to save the image (without ext): ")
    message = input("Enter the message for the image: ")

    draw_and_save_rhomb(rhomb, message, image_filename)


def get_rhomb_parameters() -> tuple:
    """ Get user input and return rhomb parameters as tuple (side, angle, color)
    """

    parameters = ()
    while True:
        print("Enter angle:")
        size = utility.get_float()
        if size <= 0:
            print("The size must be positive!")
            continue
        else:
            parameters += (size,)
            break

    while True:
        print("Enter angle:")
        angle = utility.get_float()
        if 0 < angle <= 90:
            parameters += (angle,)
            break
        else:
            print("The angle must be in range (0, 90]!")
            continue

    colors = ["blue", "red", "green", "orange", "yellow", "black", "brown", "pink", "gray", "purple"]
    while True:
        color = input("Enter color: ")
        if color not in colors:
            print("No such color! Try again.")
        else:
            parameters += (color,)
            break

    return parameters


def draw_and_save_rhomb(rhomb, message, filename):
    """ Draw the rhomb and save image to file with filename.
    """
    window = turtle.Screen()
    window.bgcolor('white')

    width  = 1200
    height = 900
    window.setup(width, 
                 height)
    window.title("Rhomb")


    turtle.width(5)
    turtle.color(rhomb.color)
    turtle.setpos(0, 0)
    turtle.setpos(rhomb.side*math.cos(180 * rhomb.angle/ math.pi), rhomb.side*math.sin(180 * rhomb.angle / math.pi))

    turtle.forward(rhomb.side/2)
    turtle.write(message, font=('Ubuntu', 17, 'normal'))

    turtle.setpos(rhomb.side*math.cos(180 * rhomb.angle / math.pi) + rhomb.side, rhomb.side*math.sin(180 * rhomb.angle / math.pi))
    turtle.setpos(rhomb.side, 0)
    turtle.setpos(0, 0)
    turtle.home()

    turtle.getscreen().getcanvas().postscript(file=filename)
    img = Image.open(filename)
    img.save(filename + '.png', 'png')

class Shape(metaclass=abc.ABCMeta):
    """ Abstract class of the shape.
    """

    @abc.abstractmethod
    def get_perimeter(self):
        pass

    @abc.abstractmethod
    def get_area():
        pass

    @abc.abstractmethod
    def get_name():
        pass


class Rhomb(Shape):
    """ Rhomb class (implements all the shape methods).
    """

    def __init__(self, side: float, angle: float, color):
        """ The constructor the class.
            Parameters:
            side - the side of the rhomb
            angle - the sharp angle
            color - the shape color
        """
        self.__side  = side
        self.__angle = angle
        self.__color = color
        self.__name  = "Rhomb"


    @property
    def side(self):
        return self.__side

    @side.setter
    def side(self, value):
        if (side <= 0):
            raise ValueError(f"The {self.__name}'s side must be positive!")

    @property
    def angle(self):
        return self.__angle

    @angle.setter
    def angle(self, value):
        if ((0 < value <= 90) is False):
            raise ValueError(f"The {self.__name}'s angle must be in range (0, 90]!")

    @property
    def color(self):
        return self.__color

    @color.setter
    def color(self, value):
        self.__color = value

 
    def get_name(self):
        return self.__name


    def get_perimeter(self):
        return 4*side


    def get_area(self):
        return math.sin(angle) * side**2


    def get_string_parameters(self):
        return "%s has the next parameters:\n" \
               "The perimeter is %f.\n" \
               "The area is %f.\n" \
               "The color is %f.\n".format(self.__name, 
                                           self.get_perimeter(),
                                           self.get_area(),
                                           self.__color)