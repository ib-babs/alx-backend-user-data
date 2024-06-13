#!/usr/bin/python3
'''Rotate a 2 Dimensional Matrix'''


def rotate_2d_matrix(matrix: list):
    '''Function to rotate a 2D matrix in\
        90 degrees clockwise.'''
    rotated_matrix = [[0 for _ in range(len(matrix[0]))]
                      for _ in range(len(matrix))]

    # Changin the 0 values in rotated_matrix to\
    # corresponding calculated index
    for i in range(len(matrix)):
        row = matrix[i]
        ci = len(row)
        j = 0
        while j < len(row):
            ci -= 1
            rotated_matrix[i][j] = matrix[ci][i]
            j += 1

    # Populating the original matrix to 2D rotated matrix
    for i in range(len(matrix)):
        row = matrix[i]
        j = 0
        while j < len(row):
            matrix[i][j] = rotated_matrix[i][j]
            j += 1
