import task1
import task2
import utility

task_solver = { 1: task1.solve_task1,
                2: task2.solve_task2 }

utility.print_welcome_msg()
task_number = utility.get_task_number()
utility.print_task_info(task_number)

task_solver[task_number]()