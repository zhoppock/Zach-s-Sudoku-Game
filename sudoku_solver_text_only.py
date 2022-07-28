from sudoku_solver_code import solve_sudoku, print_sudoku_board  # the functions that were made for both the text solver and GUI programs
from dokusan import generators # will be used to generate random boards of solvable sudoku puzzles
import numpy as np # helps put the generated sudoku values into a usable array form

sudoku_board_1 = [
    [0, 0, 0, 2, 6, 0, 7, 0, 1],
    [6, 8, 0, 0, 7, 0, 0, 9, 0],
    [1, 9, 0, 0, 0, 4, 5, 0, 0],
    [8, 2, 0, 1, 0, 0, 0, 4, 0],
    [0, 0, 4, 6, 0, 2, 9, 0, 0],
    [0, 5, 0, 0, 0, 3, 0, 2, 8],
    [0, 0, 9, 3, 0, 0, 0, 7, 4],
    [0, 4, 0, 0, 5, 0, 0, 3, 6],
    [7, 0, 3, 0, 1, 8, 0, 0, 0]
] # easy sudoku puzzle

sudoku_board_2 = [
    [7, 0, 2, 0, 0, 5, 0, 8, 0],
    [0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 8, 0, 6, 0, 0],
    [0, 4, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 9],
    [5, 0, 8, 0, 0, 2, 0, 6, 0],
    [0, 1, 0, 0, 0, 0, 0, 7, 0],
    [4, 0, 7, 2, 0, 0, 3, 0, 0],
    [0, 6, 0, 0, 0, 4, 0, 0, 0]
] # very difficult sudoku puzzle

sudoku_array = np.array(list(str(generators.random_sudoku(avg_rank = 50)))) # generates a random solvable sudoku board, difficulty can be set with the 'avg_rank' variable
sudoku_array_int = sudoku_array.astype(np.int) # converts the array above from string to integer
sudoku_board_3 = sudoku_array_int.reshape(9, 9) # organizes the values in the array to make a 2D array that can be converted into a game board

print("Starting Board #1:")
print_sudoku_board(sudoku_board_1)
solve_sudoku(sudoku_board_1)
print("\n\nSolved Board #1:")
print_sudoku_board(sudoku_board_1)

print("\n========================")
print("\nStarting Board #2:")
print_sudoku_board(sudoku_board_2)
solve_sudoku(sudoku_board_2)
print("\n\nSolved Board #2:")
print_sudoku_board(sudoku_board_2)

print("\n========================")
print("\nStarting Board #3:")
print_sudoku_board(sudoku_board_3)
solve_sudoku(sudoku_board_3)
print("\n\nSolved Board #3:")
print_sudoku_board(sudoku_board_3)