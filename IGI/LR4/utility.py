import datetime
import time
import zipfile

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


def read_from_file(filename) -> str:
    """ Read all content from the file and return it as a string
        Parameters:
        filename - name of the source file
    """

    file_content = ""

    try:
        with open(filename, "r") as file:
            file_content = file.read()
    except OSError as err:
        print("File error: ", err)
        raise

    return file_content


def write_to_file(filename, text):
    """ Write text to file.
    """

    try:
        with open(filename, "w") as file:
            file.write(text)
    except OSError as err:
        print("File error: ", err)
        raise


def make_verbose_arhieve(arhievename, file_name):
    """ Create arhieve of "filename" file and print information about it to console.
    """
    with zipfile.ZipFile(arhievename, "w", compression=zipfile.ZIP_STORED) as zip_file:
        zip_file.write(file_name)
        zip_info = zip_file.infolist()[0]

        print(f"Information about {arhievename}:\n" \
              f"File origin name: {zip_info.filename}\n" \
              f"Touch date: {zip_info.date_time}\n" \
              f"Compress type: {zip_info.compress_type}\n" \
              f"Size after compress: {zip_info.compress_size}\n" \
              f"Size before compress: {zip_info.file_size}\n")