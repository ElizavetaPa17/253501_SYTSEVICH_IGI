import math
import utility
import statistics
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def solve_task3():
    """ Solve the third task of the 4-th laboratory work.
    """

    task3_sequence = MathSequence(lambda x, n: (-1)**(n-1) * (x**n)/n, (-1, 1), 1)

    filename_dst = input("Enter the destination filename (for answer): ")
    filename_img = input("Enter the image filename (for graphics): ")
    print("Enter x (-1, 1) to calculate the value of log:")
    while True:
        x = utility.get_float()
        if ((-1 < x < 1) is False):
            continue
        else:
            break

    print("Enter n to calculate the value of log:")
    while True:
        n = utility.get_integer()
        if n < 1:
            continue
        else:
            break

    try:
        with open(filename_dst, "a") as file:
            write_all_text_data(task3_sequence, file, x, n)

            solutions = []
            start = -0.9
            while start < 1:
                solutions.append(decompose_log(start, 1e-2))
                start += 0.1

            file.write(get_task3_text_solution(solutions))
            make_plots(solutions, filename_img)
    except OSError as err:
        print("File error:" + err)


def write_all_text_data(math_sequence, file, x, n):
    """ Write all text information of the math sequence in the file (opened for writing).
    """

    value = math_sequence.calculate_value(x, n)
    average_value = math_sequence.calculate_average_value(x, n)
    median = math_sequence.calculate_median(x, n)
    mode = math_sequence.calculate_mode(x, n)
    variant = math_sequence.calculate_variant(x, n)
    st_dev = math_sequence.calculate_standard_deviation(x, n)

    file.write("The sequence is sum((-1)**(n-1) * (x**n)/n, |x|<1, n=0..inf).\n" \
               f"The value is {value}.\n"
               f"The average value is {average_value}.\n"
               f"The median is: {median}.\n"
               f"The mode is: {mode}.\n"
               f"The variant is: {variant}.\n"
               f"The standard deviation is {st_dev}.\n")


def make_plots(solutions: list, image_filename):
    """ Make all plots and save it into files.
    """

    x = []
    y_app = []
    y_bld = []

    for solution in solutions:
        x.append(solution[0])
        y_app.append(solution[2])
        y_bld.append(solution[3])

    plt.plot(x, y_app, 'r', label='approximation')
    plt.plot(x, y_bld, 'g', label='build-in')

    plt.xlabel('X')
    plt.ylabel('Y')

    plt.legend()
    plt.savefig(image_filename)


def decompose_log(x: tuple, eps: float = 1e-3) -> tuple:
    """ Calculate decompose of the ln(x+1) using the Taylor formula
    
    Keyword arguments:
    x   -- decomposition point
    eps -- error rate
    """

    exact_answer = math.log(x + 1)
    apprx_answer = 0

    n = 1
    while (abs(apprx_answer - exact_answer) >= eps and n < 500):
        apprx_answer += (-1)**(n-1) * (x**n / n)
        n += 1

    return (x, n, apprx_answer, exact_answer, eps)


def get_task3_text_solution(solutions: list):
    """ Return the solution of the first task in the next format:
    +-----------+---------+---------+--------------+---------+
    |     x     |    n    |   F(x)  |  Math(F(x))  |   eps   |
    +-----------+---------+---------+--------------+---------+

    Keyword arguments:
    solution -- the tuple of (x, n, approximation_value, exact_answer, epsilon)
    """

    answer = "+-----------+---------+-------------+--------------+-----------+\n" \
             "|     x     |    n    |     F(x)    |  Math(F(x))  |    eps    |\n" \
             "+-----------+---------+-------------+--------------+-----------+\n"

    for solution in solutions:
        answer += ("|%11f|%9d|%13f|%14f|%11f|\n" \
                   "+-----------+---------+-------------+--------------+-----------+\n" %
                   (solution[0], solution[1], solution[2], solution[3], solution[4]))
    return answer


class MathSequence:
    """ The class of math sequence with the next possibilities to calculate:
        1. The value of MS in certain point
        2. An average value
        3. The median
        4. The mode
        5. The variance
        6. The standard deviation
    """

    def __init__(self, sequence, scope_range: tuple, init_n: int):
        """ The constructor of the class.
            Parameters:
            sequence - the function object that give value in every point (signature: func(x, n))
            scope_range - the scope of function definition
            init_n -  the initial n for the sequence
        """
        self.__sequence = sequence
        self.__scope_range = scope_range
        self.__init_n  = init_n

    @property
    def sequence(self):
        return self.__sequence

    @property
    def scope_range(self):
        return self.__scope_range

    @property
    def init_n(self):
        return self.__init_n

    
    def __check_invariant(self, x: float, n: int):
        """ Check the invariant of the class: x must be in __scoped_range and n must be larger __init_n.
            Can raise exceptions.
        """
        if ((self.__scope_range[0] < x < self.__scope_range[1]) is False):
            raise ValueError(f"x not in scope_range={self.__scope_range}")
        elif (n < self.__init_n):
            raise ValueError(f"n must be larger than init_n={self.__init_n}")

    
    def __get_delpoyed_sequence(self, x: float, n: int) -> list:
        """ Return deployed sequence.
        """
        value_sequence = []
        for i in range(self.__init_n, n+1):
            value_sequence.append(self.__sequence(x, i))

        return value_sequence
        
    def calculate_value(self, x: float, n: int) -> float:
        """ Calculate the function value in point with n members and return it.
        """
        self.__check_invariant(x, n)

        result = 0
        for i in range(self.__init_n, n+1):
            result += self.__sequence(x, i)

        return result

        
    def calculate_average_value(self, x:float, n: int) -> float:
        """ Calculate an average value of sequence and return it.
        """
        self.__check_invariant(x, n)
        value_sequence = self.__get_delpoyed_sequence(x, n)
        return statistics.fmean(value_sequence)

    
    def calculate_median(self, x: float, n: int) -> float:
        """ Calculate the median of the sequence and return it.
        """
        self.__check_invariant(x, n)
        value_sequence = self.__get_delpoyed_sequence(x, n)
        statistics.median(value_sequence)

    
    def calculate_mode(self, x: float, n: int) -> float:
        """ Calculate the mode of the sequence and return it.
        """
        self.__check_invariant(x, n)
        value_sequence = self.__get_delpoyed_sequence(x, n)
        return statistics.mode(value_sequence)


    def calculate_variant(self, x: float, n: int) -> float:
        """ Calculate the variant of the sequence and return it.
        """
        self.__check_invariant(x, n)
        value_sequence = self.__get_delpoyed_sequence(x, n)
        return statistics.mode(value_sequence)


    def calculate_standard_deviation(self, x: float, n: int) -> float:
        """ Caclulate the standard deviation of the sequence and return it.
        """
        self.__check_invariant(x, n)
        value_sequence = self.__get_delpoyed_sequence(x, n)
        return statistics.stdev(value_sequence)