import pygame
import copy

ARROW_PRESSED = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
NUM_PRESSED = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
map_key_to_number = {pygame.K_1 : 1, pygame.K_2 : 2, pygame.K_3 : 3, pygame.K_4 : 4, pygame.K_5 : 5, pygame.K_6 : 6, pygame.K_7 : 7, pygame.K_8 : 8, pygame.K_9 : 9}

WINDOW_WIDTH = 700
WINDOW_HEIGHT = 510
SUDOKU_SIZE = 500
NUMBER_FONT_SIZE = 40
diff = SUDOKU_SIZE / 9
THICK_LINE = 3
BOARD_OFFSET = 3

# Initialize pygame
pygame.font.init()
Window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("SUDOKU GAME")
font = pygame.font.SysFont("comicsans", NUMBER_FONT_SIZE)

class Button():
    def __init__(self, x, y, button_text):
        self.width = 170
        self.height = 50
        self.x_pos = x
        self.y_pos = y
        self.text = button_text
        self.button = pygame.Rect(x, y, self.width, self.height)
        self.button_clicked = False
        self.last_state = False # TODO: Use this to check for only one click

    def draw(self):
        # Get Mouse Position
        pos = pygame.mouse.get_pos()
        if self.button.collidepoint(pos):
            pygame.draw.rect(Window, pygame.Color("yellow"), self.button, 0)
            pygame.draw.rect(Window, pygame.Color("black"), self.button, 4)
            draw_text = font.render(str(self.text), 1, pygame.Color("red"))

            if pygame.mouse.get_pressed()[0] == 1 and self.button_clicked == False: # 0th index is left click.
                self.button_clicked = True
        else:
            pygame.draw.rect(Window, pygame.Color("black"), self.button, 4)
            draw_text = font.render(str(self.text), 1, pygame.Color("black"))

        if pygame.mouse.get_pressed()[0] == 0: # 0th index is left click.
            self.button_clicked = False

        Window.blit(draw_text, (self.x_pos + self.width // 5, self.y_pos - 5))




class SudokuBoard:
    x_coord = 0
    y_coord = 0
    exit_game = False
    highlight_flag = False
    defaultgrid =[
        [0, 0, 0, 0, 0, 6, 0, 0, 0],
        [0, 0, 5, 0, 9, 0, 0, 0, 8],
        [0, 6, 0, 5, 0, 2, 7, 0, 4],
        [0, 0, 8, 0, 0, 0, 0, 0, 9],
        [3, 4, 0, 0, 8, 0, 0, 0, 7],
        [6, 5, 0, 0, 0, 0, 0, 1, 2],
        [0, 1, 2, 9, 0, 0, 3, 0, 0],
        [5, 8, 0, 4, 0, 0, 9, 7, 0],
        [9, 0, 0, 0, 0, 0, 0, 8, 6],
    ]
    updatedgrid = copy.deepcopy(defaultgrid)


    def coord(self, pos):
        '''Set x and y coordinates'''
        max_pos = 9
        x_pos = int(pos[0]//diff)
        y_pos = int(pos[1]//diff)

        if x_pos >= max_pos or y_pos >= max_pos:
            return

        self.highlight_flag = True
        self.x_coord = x_pos
        self.y_coord = y_pos


def handle_events(sudoku_board):
    '''Given a mouse/keyboard event handle it here'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sudoku_board.exit_game = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            handle_mouse_event(sudoku_board)
        elif event.type == pygame.KEYDOWN:
            if event.key in ARROW_PRESSED:
                handle_arrow_pressed(event.key, sudoku_board)
                sudoku_board.highlight_flag = True
            elif event.key in NUM_PRESSED:
                handle_number_pressed(event.key, sudoku_board)
            else:
                handle_other_keys(event.key, sudoku_board)


def handle_mouse_event(sudoku_board):
    '''Given a mouse click, the coordinates are obtained and saved'''
    mouse_pos = pygame.mouse.get_pos()
    sudoku_board.coord(mouse_pos)


def handle_arrow_pressed(arrow_pressed, sudoku_board):
    '''Given an arrow pressed, update coordinates'''
    if arrow_pressed == pygame.K_LEFT:
        sudoku_board.x_coord -= 1
    if arrow_pressed == pygame.K_RIGHT:
        sudoku_board.x_coord += 1
    if arrow_pressed == pygame.K_UP:
        sudoku_board.y_coord -= 1
    if arrow_pressed == pygame.K_DOWN:
        sudoku_board.y_coord += 1


def handle_number_pressed(number_pressed, sudoku_board):
    '''Map the pressed key to an integer value'''
    num_pressed = map_key_to_number[number_pressed]

    if sudoku_board.defaultgrid[sudoku_board.x_coord][sudoku_board.y_coord] == 0:
        sudoku_board.updatedgrid[sudoku_board.x_coord][sudoku_board.y_coord] = num_pressed


def handle_other_keys(key_pressed, sudoku_board):
    '''Handle other keys'''
    if key_pressed == pygame.K_DELETE:
        if sudoku_board.defaultgrid[sudoku_board.x_coord][sudoku_board.y_coord] == 0:
            sudoku_board.updatedgrid[sudoku_board.x_coord][sudoku_board.y_coord] = 0
    elif key_pressed == pygame.K_RETURN:
        solve_game(sudoku_board, 0, 0)


def solve_game(sudoku_board, i, j):
    grid = sudoku_board.updatedgrid
    while grid[i][j] != 0:
        if i<8:
            i+= 1
        elif i == 8 and j<8:
            i = 0
            j+= 1
        elif i == 8 and j == 8:
            return True
    
    pygame.event.pump()

    for it in range(1, 10):
        if valid_value(grid, i, j, it) == True:
            grid[i][j]= it

            Window.fill(pygame.Color("white"))
            draw_background(sudoku_board)
            draw_lines()
            pygame.display.update()
            pygame.time.delay(5)

            if solve_game(sudoku_board, i, j)== 1:
                return True
            else:
                grid[i][j]= 0
            
    return False


def reset_game(sudoku_board):
    '''Reset board to original numbers'''
    sudoku_board.updatedgrid = copy.deepcopy(sudoku_board.defaultgrid)


def create_board(sudoku_board):
    '''Let user create a board'''
    sudoku_board.defaultgrid = [[0 for _ in sublist] for sublist in sudoku_board.defaultgrid]
    sudoku_board.updatedgrid = copy.deepcopy(sudoku_board.defaultgrid)



def valid_value(grid, x_pos, y_pos, value):
    '''Check if value is valid for given place'''
    if is_duplicate_in_column(grid, x_pos, y_pos, value):
        return False
    if is_duplicate_in_row(grid, x_pos, y_pos, value):
        return False
    if is_dublicate_in_box(grid, x_pos, y_pos, value):
        return False
    
    return True

def is_duplicate_in_column(grid, x_pos, y_pos, value):
    '''Check for duplicate number in same column'''
    for i in range(0, 9):
        if i == y_pos:
            continue
        if grid[x_pos][i] == value:
            return True
    return False

def is_duplicate_in_row(grid, x_pos, y_pos, value):
    '''Check for duplicate number in same column'''
    for i in range(0, 9):
        if i == x_pos:
            continue
        if grid[i][y_pos] == value:
            return True
    return False
    
        
def is_dublicate_in_box(grid, x_pos, y_pos, value):
    '''Check for dublicate numbers in same box'''
    x_box = (x_pos//3)*3
    y_box = (y_pos//3)*3
    for i in range(0, 3):
        for j in range (0, 3):
            if x_box+i == x_pos and y_box+j == y_pos:
                continue
            if grid[x_box+i][y_box+j] == value:
                return True
    return False
    

def draw_lines():
    '''Draw Horizontal and vertical lines in sudoku, with different thickness'''
    for lines in range(10):
        line_thickness = get_line_thickness(lines)
        line_coord = lines * diff
        pygame.draw.line(Window, pygame.Color("black"), (0 + BOARD_OFFSET, line_coord + BOARD_OFFSET), (SUDOKU_SIZE + BOARD_OFFSET, line_coord + BOARD_OFFSET), line_thickness) # Draw horizontal lines
        pygame.draw.line(Window, pygame.Color("black"), (line_coord + BOARD_OFFSET, 0 + BOARD_OFFSET), (line_coord + BOARD_OFFSET, SUDOKU_SIZE + BOARD_OFFSET), line_thickness) # Draw vertical lines


def get_line_thickness(line):
    '''Return line thickness, every third line should be thicker to separate boxes'''
    line_thickness = 1
    if line % 3 == 0 :
        line_thickness = THICK_LINE

    return line_thickness


def draw_background(sudoku_board):
    '''Draw background and numbers'''
    defaultgrid = sudoku_board.defaultgrid
    updatedgrid = sudoku_board.updatedgrid

    for col in range (9):
        for row in range (9):
            if defaultgrid[col][row] != 0:
                # Draw yellow background to original numbers
                pygame.draw.rect(Window, pygame.Color("yellow"), (col * diff + BOARD_OFFSET, row * diff + BOARD_OFFSET, diff + 1, diff + 1))
                
            if updatedgrid[col][row] != 0:
                # Draw all numbers
                is_value_valid = valid_value(updatedgrid, col, row, updatedgrid[col][row])
                draw_number(updatedgrid[col][row], col, row, is_value_valid)


def draw_number(value, x_coord, y_coord, valid_num):
    '''Given a value and coordinates, draw value in those coordinates'''
    num_offset = 15
    num_color = pygame.Color("black")
    if not valid_num:
        num_color = pygame.Color("red")

    number_to_draw = font.render(str(value), 1, num_color)
    Window.blit(number_to_draw, (x_coord * diff + num_offset + BOARD_OFFSET, y_coord * diff + BOARD_OFFSET))


def highlight_box(sudoku_board):
    '''Highlight box we are currently on by drawing a square of different color'''
    if not sudoku_board.highlight_flag:
        return

    line_width = 3
    x_hori = sudoku_board.x_coord * diff + BOARD_OFFSET
    y_vert = sudoku_board.y_coord * diff + BOARD_OFFSET
    pygame.draw.rect(Window, pygame.Color("red"), (x_hori, y_vert, diff + 1, diff + 1), line_width)


def run_game():
    sudoku_board = SudokuBoard()
    start_button = Button(520, 25, "Solve")
    reset_button = Button(520, 90, "Reset")
    create_button = Button(520, 155, "Create")


    while not sudoku_board.exit_game:
        Window.fill(pygame.Color("white"))
        start_button.draw()
        reset_button.draw()
        create_button.draw()

        # TODO: Fix these, they are being called to many times.
        if start_button.button_clicked:
            solve_game(sudoku_board, 0, 0)
        if reset_button.button_clicked:
            reset_game(sudoku_board)
        if create_button.button_clicked:
            create_board(sudoku_board)

        handle_events(sudoku_board)
        draw_background(sudoku_board)
        draw_lines()
        highlight_box(sudoku_board)


        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    run_game()
