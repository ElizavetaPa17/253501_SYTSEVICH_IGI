import utility

def solve_task5():
    """ Solve the 5-th task of the laboratory work.
    """

    numbers = utility.get_numbers_until(0)

    negative_odd_count = get_negative_odd_count(numbers)
    number_sum = get_number_sum(numbers)

    print_task5_solution(negative_odd_count, number_sum)


def get_negative_odd_count(numbers: list) -> int:
    """ Return the count of negative odd numbers in the list.
    """

    count  = 0
    for number in numbers:
        if number % 2 and number < 0:
            count += 1

    return count


def get_number_sum(numbers: list) -> int:
    """ Return the sum of the numbers in the list
    """

    sum = 0
    for number in numbers:
        sum += number

    return sum


def print_task5_solution(negative_odd_count: int, number_sum: int):
    print(f"The count of the negative odd numbers is: {negative_odd_count}\n"
          f"The sum of the numbers: {number_sum}")