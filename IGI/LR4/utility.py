import datetime
import time

AUTHOR_LAST_NAME  = "Sytsevich"
AUTHOR_FIRST_NAME = "Elizaveta"
AUTHOR_PATRONYMIC = "Romanovna"

LABORATORY_NUMBER = 4
LABORATORY_NAME   = "Working with files, classes, serializers, regular expressions, and standard libraries"
PROGRAM_VERSION   = "1.0.0"

DEVELOPMENT_DATE  = datetime.date(2024, 3, 25)

DELIMETER = '='*80 + '\n'


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


def print_quit_msg():
    """ Print message when the user is quit.
    """

    print("Thanks for your attention. Good bye!")


def get_integer() -> int:
    """ Get integer number
    """

    number = 0
    while True:
        try:
            number = int(input(f"Enter the number: "))
            break
        except:
            print("Please, enter only integer numbers.")

    return number


def get_float() -> float:
    """ Get float and return it
    """
    
    number = 0
    while True:
        try:
            number = float(input("Enter float number: "))
            break
        except:
            print("Please, enter float number.")

    return number