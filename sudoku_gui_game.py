import pygame # the library that allows us to put our sudoku game in GIU form
from sudoku_solver_code import solve_sudoku, prove_valid, find_empty_space # the functions that were made for both the text solver and GUI programs
import time # needed to run the timer in our game
from dokusan import generators # will be used to generate random boards of solvable sudoku puzzles
import numpy as np # helps put the generated sudoku values into a usable array form
pygame.font.init() # needed to give us a library of fonts to use

class sudoku_grid(): # holds the squares of the game in a row and column structure
    sudoku_array = np.array(list(str(generators.random_sudoku(avg_rank = 50)))) # generates a random solvable sudoku board, difficulty can be set with the 'avg_rank' variable
    sudoku_array_int = sudoku_array.astype(np.int) # converts the array above from string to integer
    sudoku_board = sudoku_array_int.reshape(9, 9) # organizes the values in the array to make a 2D array that can be converted into a game board

    def __init__(self, rows, columns, width, height, window): # set the values needed to run the game window
        self.rows = rows
        self.columns = columns
        self.squares = [[square(self.sudoku_board[horiz][vert], horiz, vert, width, height) for vert in range(columns)] for horiz in range(rows)] # calls the Square class to make each of the 9 squares for the board
        self.width = width
        self.height = height
        self.solver_base = None
        self.chosen = None
        self.window = window
    
    def update_solver(self): # updates the window actively to send to the solver function to see if it can be solved
        self.solver_base = [[self.squares[horiz][vert].number for vert in range(self.columns)] for horiz in range(self.rows)]
    
    def place_number(self, number): # this determines if a space on a square is valid to enter a number or not.  It will place if valid
        row, column = self.chosen
        if self.squares[row][column].number == 0: # placing a number only works if the selected space is empty, AKA is set to 0
            self.squares[row][column].set_num(number)
            self.update_solver()
            if prove_valid(self.solver_base, number, (row, column)) and solve_sudoku(self.solver_base):
                return True # the placed number gets to stay on the selected space and is permament on the board
            else:
                self.squares[row][column].set_num(0)
                self.squares[row][column].temporary(0)
                self.update_solver()
                return False # the selected space gets set back to 0 and can have another attempt at placing a number

    def place_possibility(self, number): # place a temporary number on a space that could possibly be the correct number
        row, column = self.chosen
        self.squares[row][column].temporary(number)

    def display_board(self): # creates the visually interactive game window
        # Grid lines will be drawn by the program
        space_between = self.width / 9
        for horiz in range(self.rows + 1):
            if horiz % 3 == 0 and horiz != 0:
                line_thickness = 4
            else:
                line_thickness = 1
            pygame.draw.line(self.window, (0, 0, 0), (0, horiz * space_between), (self.width, horiz * space_between), line_thickness)
            pygame.draw.line(self.window, (0, 0, 0), (horiz * space_between, 0), (horiz * space_between, self.height), line_thickness)
        # Squares will be drawn by the program
        for horiz in range(self.rows):
            for vert in range(self.columns):
                self.squares[horiz][vert].display_square(self.window)
    
    def space_select(self, row, column): # let the player select a space on the board
        # first, reset all other space from being selected
        for horiz in range(self.rows):
            for vert in range (self.columns):
                self.squares[horiz][vert].chosen = False
        self.squares[row][column].chosen = True
        self.chosen = (row, column)

    def space_clear(self): # clear a space of a temporary number placed in it
        row, column = self.chosen
        if self.squares[row][column].number == 0:
            self.squares[row][column].temporary(0)

    def user_click(self, position): # takes the input of the user clicking somewhere on the board
        """
        Parameter(s): position
        Returns: row and column coordinates
        """
        if position[0] < self.width and position[1] < self.height:
            space_between = self.width / 9
            x_coord = position[0] // space_between
            y_coord = position[1] // space_between
            return (int(y_coord), int(x_coord))
        else:
            return None

    def complete_or_not(self): # tests each space on the board to see if the board is completely filled or not
        for horiz in range(self.rows):
            for vert in range(self.columns):
                if self.squares[horiz][vert].number == 0:
                    return False
        return True
    
    def solve_sudoku_gui(self): # runs a backtracking recursion process to solve the sudoku board when called
        self.update_solver()
        search = find_empty_space(self.solver_base)
        if not search:
            return True
        else:
            row, column = search
        for index in range(1, 10):
            if prove_valid(self.solver_base, index, (row, column)):
                self.solver_base[row][column] = index
                self.squares[row][column].set_num(index)
                self.squares[row][column].solver_change(self.window, True)
                self.update_solver()
                pygame.display.update()
                pygame.time.delay(100)
                if self.solve_sudoku_gui(): # if a space is filled, the program will run again in the next empty space it finds
                    return True # function ends once the whole board is solved
                self.solver_base[row][column] = 0 # if a value could not be found, the previous space is reset to 0 and starts over
                self.squares[row][column].set_num(0)
                self.update_solver()
                self.squares[row][column].solver_change(self.window, False)
                pygame.display.update()
                pygame.time.delay(100)
        return False # goes to the previous call of this function if a valid value could not be found
        
class square(): # holds the spaces of each square in a row and column structure
    rows = 9
    columns = 9

    def __init__(self, number, row, column, width, height): # set the values needed to populate each square on the board
        self.number = number
        self.temp_num = 0
        self.row = row
        self.column = column
        self.width = width
        self.height = height
        self.chosen = False
    
    def display_square(self, window): # creates each visually interactive square on the game board
        font_type = pygame.font.SysFont("calibri", 40)
        space_between = self.width / 9
        x_val = self.column * space_between
        y_val = self.row * space_between
        if self.temp_num != 0 and self.number == 0: # sets the font and color of the temporary number text
            temp_text = font_type.render(str(self.temp_num), 1, (136, 166, 106))
            window.blit(temp_text, (x_val + 5, y_val + 5))
        elif not(self.number == 0): # sets the font and color of the main number text
            main_text = font_type.render(str(self.number), 1, (33, 22, 36))
            window.blit(main_text, (x_val + (space_between / 2 - main_text.get_width() / 2), y_val + (space_between / 2 - main_text.get_height() / 2)))
        if self.chosen:
            pygame.draw.rect(window, (204, 0, 255), (x_val, y_val, space_between, space_between), 3)

    def solver_change(self, window, valid = True): # the program will go through each empty space and display a colored box depending on what process it is in
        font_type = pygame.font.SysFont("calibri", 40)
        space_between = self.width / 9
        x_val = self.column * space_between
        y_val = self.row * space_between
        pygame.draw.rect(window, (240, 252, 227), (x_val, y_val, space_between, space_between), 0)
        solve_text = font_type.render(str(self.number), 1, (33, 22, 36))
        window.blit(solve_text, (x_val + (space_between / 2 - solve_text.get_width() / 2), y_val + (space_between / 2 - solve_text.get_height() / 2)))
        if valid: # displays an aqua green box on spaces that have been validated and solved
            pygame.draw.rect(window, (77, 255, 181), (x_val, y_val, space_between, space_between), 3)
        else: # displays an magenta box on spaces that turn out to not yield a valid answer yet
            pygame.draw.rect(window, (255, 54, 141), (x_val, y_val, space_between, space_between), 3)

    def set_num(self, value): # sets a permament number for a space
        self.number = value

    def temporary(self, value): # sets a temporary number for a space
        self.temp_num = value

def window_refresh(window, sudoku_board, time, invalid_entries, invalid_entries_counter): # constantly refreshes the game window on account of the timer or user moves
    window.fill((240, 252, 227))
    # set the timer in the bottom right of the window that runs while the user is playing
    font_type = pygame.font.SysFont("calibri", 30)
    time_text = font_type.render("Time: " + clock_format(time), 1, (33, 22, 36))
    window.blit(time_text, (540 - 180, 560))
    # set an X to appear in the bottom left of the window every time you enter in a bad number in a space
    invalid_text = font_type.render("X " * invalid_entries, 1, (173, 17, 17))
    window.blit(invalid_text, (55, 560))
    # display a counter for every 10 invalid entries you get
    counter_text = font_type.render(str(invalid_entries_counter) + ": ", 1, (173, 17, 17))
    window.blit(counter_text, (15, 560))
    # display the game board and its grid
    sudoku_board.display_board()

def clock_format(seconds): # a timer will run at the beginning of each game
    second = seconds % 60
    minute = seconds // 60
    hour = minute // 60
    timer = str(hour) + ":" + str(minute) + ":" + str(second)
    return timer

def main(): # the main function that runs everything above together
    window = pygame.display.set_mode((540, 600))
    pygame.display.set_caption("Zach's Sudoku Game")
    sudoku_board = sudoku_grid(9, 9, 540, 540, window)
    key = None # this will be used to recognize user inputs from the keyboard
    run = True # keeps the game going until it ends
    start = time.time()
    invalid_entries = 0
    invalid_entries_counter = 0
    while run:
        play_time = round(time.time() - start)
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # detects if the game window is closed
                run = False
            if event.type == pygame.KEYDOWN: # detects if certain keys on the keyboard has been pressed
                """
                I wanted to try and use dictionary values for my keyboard inputs but if you hit something other than the keys listed below it crashes the game
                options = {pygame.K_1 : 1, pygame.K_2 : 2, pygame.K_3 : 3, pygame.K_4 : 4, pygame.K_5 : 5, pygame.K_6 : 6, pygame.K_7 : 7, pygame.K_8 : 8, pygame.K_9 : 9, pygame.K_DELETE : 'delete', pygame.K_BACKSPACE: 'delete', pygame.K_RETURN : 'return'}
                key = options[event.key] # there are 12 different keyboard inputs that will work in this game: 1 through 9 keys, the DELETE key, the BACKSPACE key and the ENTER/RETURN key
                if key == 'delete':
                    sudoku_board.space_clear()
                    key = None
                if key == 'return':
                    horiz, vert = sudoku_board.chosen
                    if sudoku_board.squares[horiz][vert].temp_num != 0:
                        if sudoku_board.place_number(sudoku_board.squares[horiz][vert].temp_num):
                            print("Correct!") # the selected space with ther user's inputted number worked
                        else:
                            print("Incorrect...") # the selected space with ther user's inputted number was an invalid entry
                            invalid_entries += 1
                            if invalid_entries == 10:
                                invalid_entries = 0
                                invalid_entries_counter += 1
                    key = None
                    if sudoku_board.complete_or_not():
                        print("Game Over.")
                        run = False
                """
                # there are 12 different keyboard inputs that will work in this game: 1 through 9 keys, the DELETE key, the BACKSPACE key and the ENTER/RETURN key
                if event.key == pygame.K_1:
                    key = 1
                if event.key == pygame.K_2:
                    key = 2
                if event.key == pygame.K_3:
                    key = 3
                if event.key == pygame.K_4:
                    key = 4
                if event.key == pygame.K_5:
                    key = 5
                if event.key == pygame.K_6:
                    key = 6
                if event.key == pygame.K_7:
                    key = 7
                if event.key == pygame.K_8:
                    key = 8
                if event.key == pygame.K_9:
                    key = 9
                if event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    sudoku_board.space_clear()
                    key = None
                if event.key == pygame.K_RETURN:
                    horiz, vert = sudoku_board.chosen
                    if sudoku_board.squares[horiz][vert].temp_num != 0:
                        if sudoku_board.place_number(sudoku_board.squares[horiz][vert].temp_num):
                            print("Correct!") # the selected space with ther user's inputted number worked
                        else:
                            print("Incorrect...") # the selected space with ther user's inputted number was an invalid entry
                            invalid_entries += 1
                            if invalid_entries == 10:
                                invalid_entries = 0
                                invalid_entries_counter += 1
                    key = None
                    if sudoku_board.complete_or_not(): # will initiate when the user presses enter after the board has been completed
                        pygame.draw.rect(window, (0, 0, 0), (540 / 2 - 124, 600 / 2 - 100, 250, 45)) # creates a black rectangle behind the Game Over text to be seen by the user
                        font_type = pygame.font.SysFont("calibri", 50)
                        end_text = font_type.render("GAME OVER", 1, (165, 80, 199))
                        window.blit(end_text, (540 / 2 - 124, 600 / 2 - 100)) # when the game ends, it will display Game Over
                        pygame.display.update()
                        print("Game Over.")
                        pygame.time.delay(5000) # gives the program about 5 seconds to let the Game Over text be seen before closing the window
                        run = False # ends the loop and lets the program close
                if event.key == pygame.K_SPACE:
                    sudoku_board.solve_sudoku_gui()

            if event.type == pygame.MOUSEBUTTONDOWN:
                position = pygame.mouse.get_pos()
                clicked_space = sudoku_board.user_click(position)
                if clicked_space:
                    sudoku_board.space_select(clicked_space[0], clicked_space[1])
                    key = None
        if sudoku_board.chosen and key != None:
            sudoku_board.place_possibility(key)
        window_refresh(window, sudoku_board, play_time, invalid_entries, invalid_entries_counter)
        pygame.display.update()
    if run == False:
        print("Thank you for playing.")

main()
pygame.quit() # pygame ends when the game ends or the window is closed