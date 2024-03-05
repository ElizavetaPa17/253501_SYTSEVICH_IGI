import datetime

AUTHOR_LAST_NAME  = "Sytsevich"
AUTHOR_FIRST_NAME = "Elizaveta"
AUTHOR_PATRONYMIC = "Romanovna"

LABORATORY_NUMBER = 3
LABORATORY_NAME   = "Standard data types, collections, functions, modules"
PROGRAM_VERSION   = "1.0.0"

DEVELOPMENT_DATE  = datetime.date(2024, 3, 4)

DELIMETER = '='*80 + '\n'

task_information = {1 : "Decompose ln(x+1) function using Taylor approximation"
                        "(|x| < 1).\n",
                    2 : "Determine how many numbers in the list are greater than 23.",
                    3 : "Determine if the entered string is a hexadecimal number.",
                    4 : "Determine the count of the words which starts with the upper character.",
                    5 : "Determine the count of the negative odd numbers and the sum of all the numbers."}


def print_welcome_msg():
    """ Print general information about the author.

    The information includes:
    - the laboratory number and name
    - the author last name, first name and patronymic
    - the day of the implementation
    """

    print(DELIMETER +
          f'This program includes the implementation of the {LABORATORY_NUMBER}-th laboratory with the name\n',
          f'"{LABORATORY_NAME}".\n'
          f'The version of the progam is {PROGRAM_VERSION}. Development data is {DEVELOPMENT_DATE}.\n'
          f'The author of the program is {AUTHOR_LAST_NAME} {AUTHOR_FIRST_NAME} {AUTHOR_PATRONYMIC}.\n' + 
          DELIMETER)


def get_task_number() -> int:
    """ Invite the user to choose task number and return it.

    The function return when the user print valid task number (1-5).
    """

    task_number = 0
    while True:
        try:
            task_number = int(input("Choose the task number (1-5) or (0 to quit): "))
            if ( 0 <= task_number <= 5):
                break
            else:
                raise ValidError
        except:
            print("Please, enter only integer number from 1 to 5.")

    print(DELIMETER)
    return task_number


def print_task_info(task_number: int):
    """ Print information about the task with task_number.
    """

    print(task_information[task_number])


def get_numbers_until(end: int) -> list:
    """ Get input data for the 2-nd task. Return list of the numbers until getting end.
    """

    numbers = []
    number = 0
    while True:
        while True:
            try:
                number = int(input(f"Enter the number ({end} to quit): "))
                break
            except:
                print("Please, enter only integer numbers.")

        if (number == end):
            break
        else:
            numbers.append(number)

    return numbers


def print_quit_msg():
    """ Print message when the user is quit.
    """

    print("Thanks for your attention. Good bye!")