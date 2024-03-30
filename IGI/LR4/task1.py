import pickle
import utility
import csv

def solve_task1():
    """ Solve the first task of the 4-th laboratory work.
    """

    school_class = ""
    while (True):
        try:
            filename = input("Enter the file that contains serialized data: ")
            if (filename.endswith(".csv")):
                school_class = get_data_from_csv_file(filename)
            else:
                school_class = get_data_from_file(filename)
            break
        except OSError as ex:
            print("File error: ", ex)

    print(utility.DELIMETER)

    while(True):
        print("What do you want to do with student collection? (0 to quit)\n"
              "1. Print to console\n"
              "2. Find student by name\n"
              "3. Print sorted students by mark\n"
              "4. Update student mark by student name\n"
              "5. Serialize school to the file\n" + 
              utility.DELIMETER)
        user_choice = utility.get_integer()
        if (user_choice == 0):
            break
        elif (user_choice == 1):
            print_students_to_console(school_class)
        elif (user_choice == 2):
            find_student_by_name(school_class)
        elif (user_choice == 3):
            print_sorted_students_by_mark(school_class)
        elif (user_choice == 4):
            update_student_by_name(school_class)
        elif (user_choice == 5):
            serialize_school(school_class)
        else:
            print("Incorrect value. Try again.")

        print(utility.DELIMETER)


def get_data_from_file(filename : str):
    """ Get values from file using module pickle.
    """

    file = open(filename, "rb")
    school_class = pickle.load(file)
    file.close()

    return school_class


def get_data_from_csv_file(filename: str):
    """ Get values from csv-file using
    """

    rows = []
    with open(filename, "r", encoding="utf-8", newline="") as file:
        reader = csv.reader(file)
        rows = list(reader)

    students = []
    school_class = SchoolClass("Undefined")
    try:
        school_class = SchoolClass(rows[0])
        for row in rows[2:]:
            student = Student(row[0], (float)(row[1]))
            students.append(student)
        
        school_class.students = students
    except Exception as ex:
        print("Error while reading csv-file: ", ex)
    
    return school_class


def print_students_to_console(school_class):
    """ Print student collection from SchoolClass to the console.
    """
    print("%-20s %3s" % ("Student_name", "average_mark"))
    for student in school_class.students:
        print("%-20s %3f" % (student.name, student.average_mark))


def find_student_by_name(school_class):
    """ Find student from SchoolClass and print it to the console
    """
    student_name = input("Enter student name: ")
    try:
        student = school_class.get_student(student_name)
        print("%-20s %3s" % ("Student_name", "average_mark"))
        print("%-20s %3f" % (student.name, student.average_mark))
    except:
        print("The student is not in this class")


def print_sorted_students_by_mark(school_class):
    """ Print sorted student collection to the console.
    """
    sorted_students = school_class.get_sorted_students_by_mark()

    print("Good students:")
    print("%-20s %3s" % ("Student_name", "average_mark"))
    i = 0
    while i < len(sorted_students):
        if sorted_students[i].average_mark < 7:
            break
        print("%-20s %3f" % (sorted_students[i].name, sorted_students[i].average_mark))
        i += 1

    if (i != len(sorted_students)):
        print("Bad students:")
        print("%-20s %3s" % ("Student_name", "average_mark"))
        while i < len(sorted_students):
            print("%-20s %3f" % (sorted_students[i].name, sorted_students[i].average_mark))
            i += 1


def update_student_by_name(school_class):
    """ Update student by name in SchoolClass
    """
    student_name = input("Enter student name: ")
    try:
        student = school_class.get_student(student_name)
        mark = utility.get_float()

        student.average_mark = mark
        print("The student marks were updated")

    except ValueError as err:
        print(err)


def serialize_school(school_class):
    filename = input("Enter destination filename: ")
    file = ""
    
    try:
        if (filename.endswith(".csv")):
            file = open(filename, "w")

            writer = csv.writer(file, quoting=csv.QUOTE_ALL)
            writer.writerow(school_class.class_name)
            writer.writerow(["Student name", "average mark"])

            for student in school_class.students:
                writer.writerow([student.name, student.average_mark])
        else:
            file = open(filename, "wb")
            pickle.dump(school_class, file)
    except OSError as err:
        print("File error: ", err)
        return

    print(f"Successfull serialization to {filename}")
    file.close()


class SchoolClass:
    """ The class of school. Contains students objects.
    """

    def __init__(self, class_name : str):
        """ The constructor of the School class.
            Parameters:
            class_name - the name of the class (like "9A")
        """
        self.__class_name = class_name
        self.__students = []

    @property
    def class_name(self):
        return self.__class_name


    @property
    def students(self):
        return self.__students
    
    @students.setter
    def students(self, students: list):
        self.__students = students


    def add_student(self, student):
        """ Add student to the student lists. 
            If the student is already in the list it will raise an exception.
        """
        for stud in self.__students:
            if student.name == stud.name:
                raise ValueError("The student is already in the list")
        
        self.__students.append(student)

    
    def get_student(self, student_name: str):
        """ Get the student by his name.
            If the student is not in the list it will be raise an exception.
        """
        for stud in self.__students:
            if stud.name == student_name:
                return stud

        raise ValueError("The student is not in the list")


    def get_sorted_students_by_mark(self):
        return sorted(self.__students, key=lambda student: student.average_mark, reverse=True)


class Student:
    """ The class of the student. 
    """

    def __init__(self, name : str, average_mark: float):
        """ The constructor of the student class.
            Parameters:
            name - the name of the student
        """
        self.__name = name
        self.__average_mark = average_mark

    @property
    def name(self) -> str:
        return self.__name

    @property
    def average_mark(self) -> float:
        return self.__average_mark

    @average_mark.setter
    def average_mark(self, value : float):
        if (0 <= value <= 10):
            self.__average_mark = value
        else:
            raise ValueError("Student average value cannot be negative")
