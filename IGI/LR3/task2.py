import math
import utility

def solve_task2():
    """ Solve the 1-st task of the laboratory work.
    """

    numbers = []
    user_choice = utility.get_user_sequence_choice()
    if (user_choice == "E"):
        numbers = utility.get_numbers_until(15)
    elif (user_choice == "R"):
        numbers = utility.get_random_sequence_interactive()
    else:
        for number in utility.get_degree_sequence_until():
            numbers.append(number)
    
    count = get_certain_numbers_count(numbers)
    print_task2_solution = lambda count: print(f"There are {count} numbers in the list "
                                               "that are greater than 23.\n")
    print_task2_solution(count)


def get_certain_numbers_count(numbers: list) -> int:
    """ Calculate the count of numbers which are greater than 23. Return this count.

    Keyword arguments:
    numbers -- the numeric list
    """

    count = 0
    for number in numbers:
        if (number > 23):
            count += 1

    return count