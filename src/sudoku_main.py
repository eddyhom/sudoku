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

class SudokuBoard:
    x_coord = 0
    y_coord = 0
    exit_game = False
    highlight_flag = False
    defaultgrid =[
        [0, 0, 1, 0, 0, 0, 0, 0, 9],
        [0, 0, 0, 0, 0, 1, 5, 0, 2],
        [0, 7, 6, 5, 0, 0, 0, 8, 0],
        [0, 0, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 4, 0, 0, 0],
        [0, 4, 0, 0, 0, 0, 3, 9, 1],
        [0, 8, 2, 0, 0, 7, 0, 0, 0],
        [0, 9, 7, 0, 3, 0, 0, 0, 6],
        [4, 0, 0, 8, 9, 0, 0, 0, 0],
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
        solve_game()


def solve_game():
    '''Solve game if user pressed RETURN key'''


def valid_value(grid, x_pos, y_pos, value):
    '''Check if its possible to put value in given place'''
    for i in range(0, 9):
        if grid[x_pos][i] == value:
            return False
        if grid[i][y_pos] == value:
            return False
    x0 = (x_pos//3)*3
    y0 = (y_pos//3)*3
    for i in range(0, 3):
        for j in range (0, 3):
            if grid[x0+i][y0+j] == value:
                return False
    return True


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

    for row in range (9):
        for col in range (9):
            if defaultgrid[row][col] != 0:
                pygame.draw.rect(Window, pygame.Color("yellow"), (row * diff + BOARD_OFFSET, col * diff + BOARD_OFFSET, diff + 1, diff + 1))
                draw_number(defaultgrid[row][col], row, col)
            elif updatedgrid[row][col] != 0:
                draw_number(updatedgrid[row][col], row, col)


def draw_number(value, x_coord, y_coord):
    '''Given a value and coordinates, draw value in those coordinates'''
    num_offset = 15
    number_to_draw = font.render(str(value), 1, pygame.Color("black"))
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

    while not sudoku_board.exit_game:
        Window.fill(pygame.Color("white"))

        handle_events(sudoku_board)
        draw_background(sudoku_board)
        draw_lines()
        highlight_box(sudoku_board)


        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    run_game()
