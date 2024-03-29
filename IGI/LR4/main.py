import utility
import task1
import task2
import task3

# ДОБАВЬ СПИСКИ НЕУСПЕВАЮЩИХ И ОТЛИЧНИКОВ И ПРОЦЕНТ КАКОЙ-ТО ТАМ
task_solver = { 1: task1.solve_task1,
                2: task2.solve_task2,
                3: task3.solve_task3 }

utility.print_welcome_msg()

while (True):
    task_number = utility.get_task_number()
    if (task_number == 0):
        utility.print_quit_msg()
        break

    task_solver[task_number]()
    print(utility.DELIMETER)

