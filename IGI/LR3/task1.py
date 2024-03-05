import math

def solve_task1():
    """ Solve the 1-st task of the laboratory work.
    """

    task1_data = get_task1_input()
    solution = decompose_log(task1_data[0], task1_data[1])
    print_task1_solution(solution)


def decompose_log(x: float, eps: float = 1e-3) -> tuple:
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


def get_task1_input() -> tuple:
    """ Get input data for the 1-st task. Return the tuple { x, epsilon }.
    """
    
    x = 0
    epsilon = 0
    while True:
        try:
            x = float(input("Enter x (|x|<1): "))
            if (-1 < math.fabs(x) < 1):
                break
            else:
                raise ValidError
        except:
            print("Please, enter float number (|x|<1)")
    
    while True:
        try:
            epsilon = float(input("Enter epsilon: "))
            break
        except:
            print("Please, enter float number.")

    return (x, epsilon)


def print_task1_solution(solution: tuple):
    """ Print the solution of the first task in the next format:
    +-----------+---------+---------+--------------+---------+
    |     x     |    n    |   F(x)  |  Math(F(x))  |   eps   |
    +-----------+---------+---------+--------------+---------+
    """

    print("+-----------+---------+-------------+--------------+-----------+\n"
          "|     x     |    n    |     F(x)    |  Math(F(x))  |    eps    |\n"
          "+-----------+---------+-------------+--------------+-----------+\n"
          "|%11f|%9d|%13f|%14f|%11f|\n"
          "+-----------+---------+-------------+--------------+-----------+\n" %
          (solution[0], solution[1], solution[2], solution[3], solution[4]))