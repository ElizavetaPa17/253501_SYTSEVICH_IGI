import math

def solve_task2():
    """ Solve the 1-st task of the laboratory work.
    """
    numbers = get_task2_input()
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


def get_task2_input() -> list:
    """ Get input data for the 2-nd task. Return list of the numbers until getting '15'.
    """

    numbers = []
    number = 0
    while True:
        while True:
            try:
                number = int(input("Enter the number (15 to quit): "))
                break
            except:
                print("Please, enter only integer numbers.")

        if (number == 15):
            break
        else:
            numbers.append(number)

    return numbers