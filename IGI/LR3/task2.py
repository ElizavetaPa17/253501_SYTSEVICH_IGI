import math
import utility

def solve_task2():
    """ Solve the 1-st task of the laboratory work.
    """

    numbers = utility.get_numbers_until(15)
    count = get_certain_numbers_count(numbers)
    print_task2_solution = lambda count: print(f"There are {count} numbers in the list "
                                               "that are greater than 23.\n")
    print_task2_solution(count)


def get_certain_numbers_count(numbers: list) -> int:
    """ Calculate the count of numbers which are greater than 23. Return this count.
    """

    count = 0
    for number in numbers:
        if (number > 23):
            count += 1

    return count


