def solve_sudoku(board):
    search = find_empty_space(board)
    if not search:
        return True # this means the board has been solved and the sudoku game ends
    else:
        row, column = search
    for index in range(1, 10): # check if values 1 through 9 are valid solutions for each space on the board
        if prove_valid(board, index, (row, column)):
            board[row][column] = index # add the index value (1 - 9) to the empty space if valid for it
            if solve_sudoku(board): # using recursion to go to the next space until the board is eventually filled
                return True # this means the board has been solved and the sudoku game ends
            board[row][column] = 0 # if we have to backtrack, we go back to the previous space and reset it to 0 and try again
    return False # if an index value isn't value, it will go back to the previous iteration of the function


def prove_valid(board, num, position):
    # check if current row value is the same as a recently inserted number
    # and check if it's not the exact position that was recently inserted in
    for vert in range(len(board[0])):
        if board[position[0]][vert] == num and position[1] != vert:
            return False

    # check if current column value is the same as a recently inserted number
    # and check if it's not the exact position that was recently inserted in
    for horiz in range(len(board)):
        if board[horiz][position[1]] == num and position[0] != horiz:
            return False

    # each square on the board can be represented by range values: (0, 0), (0, 1), (0, 2), then (1, 0), (1, 1), (1, 2),
    # and lastly (2, 0), (2, 1), (2, 2).  The integer division below results in 0, 1, or 2
    square_x = position[1] // 3
    square_y = position[0] // 3

    # check if current square value is the same as a recently inserted number
    # and check if it's not the exact position that was recently inserted in
    for vert in range(square_y * 3, square_y * 3 + 3):
        for horiz in range(square_x * 3, square_x * 3 + 3):
            if board[vert][horiz] == num and (vert, horiz) != position:
                return False

    return True # if all the checks above prove the space is valid

def print_sudoku_board(board):
    for horiz in range(len(board)):
        if horiz % 3 == 0 and horiz != 0:
            print("- - - - - - - - - - - -") # prints after every 3 rows of values, except after the last 3 rows
        for vert in range(len(board[0])):
            if vert % 3 == 0 and vert != 0:
                print(" | ", end = "") # prints a wall after every 3 values in a row, except after the last 3 values in a row
            if vert == 8:
                print(board[horiz][vert]) # prints a value at the end of each row and then the program goes to the next row
            else:
                print(str(board[horiz][vert]) + " ", end = "") # prints a value one at a time in each row before the last value

def find_empty_space(board):
    for horiz in range(len(board)):
        for vert in range(len(board[0])):
            if board[horiz][vert] == 0:
                return (horiz, vert) # return the row and column of a found 0 value
    return None # returns nothing if a 0 could not be found on the board