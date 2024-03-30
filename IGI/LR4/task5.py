import numpy as np
import utility
import time

def solve_task5():
    """ Solve the fifth task of the 4-th laboratory work.
    """

    matrix = get_random_matrix()
    print("Initial matrix is:\n", matrix)
    matrix = sort_matrix_by_last_column(matrix)
    print("Sorted matrix by last column is:\n", matrix)

    start_time = time.time()
    answer = matrix.mean()
    end_time = time.time() - start_time
    print("The average value of the matrix is (build-in): %.2f, time: %.3fms" % (answer, end_time * 10**6))

    start_time = time.time()
    answer = get_average_matrix_value(matrix)
    end_time = time.time() - start_time
    print("The average value of the matrix is (user): %.2f, time: %.3fms" % (answer, end_time * 10**6))
    

def get_random_matrix():
    """ Generate random matrix with certains rows and columns and return it.
        (using console input to get rows and columns)
    """

    rows = 0
    cols = 0
    while True:
        print("Enter matrix rows count:")
        rows = utility.get_integer()
        if (rows <= 0):
            print("Matrix rows must be positive!")
        else:
            break

    while True:
        print("Enter matrix columns count:")
        cols = utility.get_integer()
        if (cols <= 0):
            print("Matrix columns must be positive!")
        else:
            break


    matrix = np.random.random((rows, cols)) * 100
    return matrix


def sort_matrix_by_last_column(matrix):
    """ Sort matrix by last column and return it.
    """

    # get the the last column
    c = -matrix[:,-1]
    # get the indexes of reversed sorting sequence
    i = np.argsort(c)
    print(i)
    # sort matrix according to the indexes
    matrix = matrix[:,i]

    return matrix


def get_average_matrix_value(matrix) -> int:
    """ Return the average value of the matrix.
    """
    elem_count = matrix.shape[0] * matrix.shape[1]
    if (elem_count == 0):
        raise ValueError("matrix mustn't be empty")

    whole_value = 0
    for i in range(matrix.shape[0]):
        for j in range(matrix.shape[1]):
            whole_value += matrix[i,j]

    return whole_value / elem_count