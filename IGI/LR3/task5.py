import utility

def solve_task5():
    """ Solve the 5-th task of the laboratory work.
    """

    numbers = []
    user_choice = utility.get_user_sequence_choice()
    if (user_choice == "E"):
        numbers = utility.get_numbers_until(0)
    elif (user_choice == "R"):
        numbers = utility.get_random_sequence_interactive()
    else:
        for number in utility.get_degree_sequence_until():
            numbers.append(number)

    negative_odd_count = get_negative_odd_count(numbers)
    number_sum = get_number_sum(numbers)

    print_task5_solution(negative_odd_count, number_sum)


def get_negative_odd_count(numbers: list) -> int:
    """ Return the count of negative odd numbers in the list.

    Keyword arguments:
    numbers -- the numeric list
    """

    count  = 0
    for number in numbers:
        if number % 2 and number < 0:
            count += 1

    return count


def get_number_sum(numbers: list) -> int:
    """ Return the sum of the numbers in the list

    Keyword arguments:

    numbers -- the numeric list
    """

    sum = 0
    for number in numbers:
        sum += number

    return sum


def print_task5_solution(negative_odd_count: int, number_sum: int):
    """ Print the solution of the 5-th laboratory task.

    Keyword arguments:
    negative_odd_count -- the count of negative odd numbers
    number_sum -- the sum of the list numbers
    """

    print(f"The count of the negative odd numbers is: {negative_odd_count}\n"
          f"The sum of the numbers: {number_sum}")