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
    rhomb.width = 5 #DINAMIC PROPERY

    image_filename = input("Enter filename to save the image (without ext): ")
    message = input("Enter the message for the image: ")
    print(utility.DELIMETER)

    draw_and_save_rhomb(rhomb, message, image_filename)
    print_shape_info(rhomb)

    print(f"The width is {rhomb.width}")
    del rhomb.width

    #USING SUPER
    rhomb.get_string_parameters()

    #USING MIXINS
    rect = Rectangle(30, 50, 30, 'green')


def get_rhomb_parameters() -> tuple:
    """ Get user input and return rhomb parameters as tuple (side, angle, color)
    """

    parameters = ()
    while True:
        print("Enter side:")
        size = utility.get_float()
        if size <= 0:
            print("The side must be positive!")
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

    width  = rhomb.side*math.cos(math.pi * rhomb.angle/180) + rhomb.side
    height = rhomb.side*math.sin(math.pi * rhomb.angle/180)
    window.setworldcoordinates(-1, -1, width * 1.5 - 1, height * 1.5 - 1)
    window.title("Rhomb")


    turtle.width(5)
    turtle.color(rhomb.color)
    turtle.setpos(0, 0)
    turtle.setpos(rhomb.side*math.cos(math.pi * rhomb.angle/180), rhomb.side*math.sin(math.pi * rhomb.angle/180))

    turtle.forward(rhomb.side/2)
    turtle.write(message, font=('Ubuntu', 17, 'normal'))

    turtle.setpos(rhomb.side*math.cos(math.pi * rhomb.angle/180) + rhomb.side, rhomb.side*math.sin(math.pi * rhomb.angle/180))
    turtle.setpos(rhomb.side, 0)
    turtle.setpos(0, 0)
    turtle.home()

    turtle.getscreen().getcanvas().postscript(file=filename)
    img = Image.open(filename)
    img.save(filename + '.png', 'png')


def print_shape_info(shape):
    """ Print info about shape (USING POLYMORPHISM)
    """
    print(f"Shape name: {shape.get_name()}.\n" \
          f"Shape perimeter: {shape.get_perimeter()}\n" \
          f"Shape area: {shape.get_area()}.\n")


class Shape(metaclass=abc.ABCMeta):
    """ Abstract class of the shape.
    """

    @staticmethod
    def get_base_name():
        print("I'm a shape!")

    @abc.abstractmethod
    def get_perimeter(self):
        pass

    @abc.abstractmethod
    def get_area(self):
        pass

    @abc.abstractmethod
    def get_name(self):
        pass


class Rhomb(Shape):
    """ Rhomb class (implements all the shape methods).
    """

    __name = "Rhomb"

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

    
    def __del__(self):
        print("Rhomb was deleted by garbage collector!")


    def __gt__(self, other):
        if (self.get_area() > other.get_area()):
            return True
        else:
            return False


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
        return Rhomb.__name


    def get_perimeter(self):
        return 4*self.__side


    def get_area(self):
        return math.sin(math.pi * self.__angle / 180) * self.__side**2


    def get_string_parameters(self):
        print(super().get_base_name())
        return "%s has the next parameters:\n" \
               "The perimeter is %f.\n" \
               "The area is %f.\n" \
               "The color is %f.\n".format(self.__name, 
                                           self.get_perimeter(),
                                           self.get_area(),
                                           self.__color)


class ResizeMixin:
    def resize(self, width, height):
        self.__width  = width
        self.__height = height


class Rectangle(Shape, ResizeMixin):
    __name = "Rectangle"

    def __init__(self, width: float, height: float, angle: float, color):
        self.resize(width, height)
        self.__angle = angle
        self.__color = color

    
    def get_name(self):
        return Rectangle.__name


    def get_perimeter(self):
        return 2*(self.__width + self.__height)


    def get_area(self):
        return self.__height * self.__width

    def get_string_parameters(self):
        print(super().get_base_name())
        return "%s has the next parameters:\n" \
               "The perimeter is %f.\n" \
               "The area is %f.\n" \
               "The color is %f.\n".format(self.__name, 
                                           self.get_perimeter(),
                                           self.get_area(),
                                           self.__color)