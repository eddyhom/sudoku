import pygame

ARROW_PRESSED = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
NUM_PRESSED = [pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9]
map_key_to_number = {pygame.K_1 : 1, pygame.K_2 : 2, pygame.K_3 : 3, pygame.K_4 : 4, pygame.K_5 : 5, pygame.K_6 : 6, pygame.K_7 : 7, pygame.K_8 : 8, pygame.K_9 : 9}

WINDOW_SIZE = 600
SUDOKU_SIZE = 500
NUMBER_FONT_SIZE = 40
diff = SUDOKU_SIZE / 9
THICK_LINE = 6

pygame.font.init()
Window = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
pygame.display.set_caption("SUDOKU GAME")
font = pygame.font.SysFont("comicsans", NUMBER_FONT_SIZE)

class SudokuBoard:
    x_coord = 0
    y_coord = 0
    defaultgrid =[
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
        [7, 8, 0, 4, 0, 0, 0, 2, 0],
        [0, 0, 2, 6, 0, 1, 0, 7, 8],
        [6, 1, 0, 0, 7, 5, 0, 0, 9],
        [0, 0, 7, 5, 4, 0, 0, 6, 1],
        [0, 0, 1, 7, 5, 0, 9, 3, 0],
        [0, 7, 0, 3, 0, 0, 0, 1, 0],
        [0, 4, 0, 2, 0, 6, 0, 0, 7],
        [0, 2, 0, 0, 0, 7, 4, 0, 0],
    ]


    def coord(self, pos):
        '''Set x and y coordinates'''
        self.x_coord = pos[0]//diff
        self.y_coord = pos[1]//diff


def valid_value(m, k, l, value):
    for it in range(9):
        if m[k][it]== value:
            return False
        if m[it][l]== value:
            return False
    it = k//3
    jt = l//3
    for k in range(it * 3, it * 3 + 3):
        for l in range (jt * 3, jt * 3 + 3):
            if m[k][l]== value:
                return False
    return True


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


def handle_number_pressed(number_pressed):
    '''Map the pressed key to an integer value'''
    return map_key_to_number[number_pressed]


def draw_lines():
    '''Draw Horizontal and vertical lines in sudoku, with different thickness'''
    for lines in range(10):
        line_thickness = get_line_thickness(lines)
        line_coord = lines * diff
        pygame.draw.line(Window, pygame.Color("black"), (0 + 5, line_coord + 5), (SUDOKU_SIZE + 5, line_coord + 5), line_thickness)  # Draw horizontal lines
        pygame.draw.line(Window, pygame.Color("black"), (line_coord + 5, 0 + 5), (line_coord + 5, SUDOKU_SIZE + 5), line_thickness) # Draw vertical lines

def get_line_thickness(line):
    '''Return line thickness, every third line should be thicker to separate boxes'''
    line_thickness = 1
    if line % 3 == 0 :
        line_thickness = THICK_LINE

    return line_thickness


def draw_bg(defaultgrid):
    for i in range (9):
        for j in range (9):
            if defaultgrid[i][j] != 0:
                pygame.draw.rect(Window, pygame.Color("yellow"), (i * diff, j * diff, diff + 1, diff + 1))
                number_to_draw = font.render(str(defaultgrid[i][j]), 1, pygame.Color("black"))
                Window.blit(number_to_draw, (i * diff + 15, j * diff))


def draw_number(value, sudoku_board):
    number_to_draw = font.render(str(value), 1, pygame.Color("black"))
    Window.blit(number_to_draw, (sudoku_board.x_coord * diff + 15 + 20, sudoku_board.y_coord * diff + 15))


def highlight_box(xy_coord):
    x_coord = xy_coord[0]
    y_coord = xy_coord[1]
    line_thickness = THICK_LINE

    for k in range(2):
        pygame.draw.line(Window, pygame.Color("blue"), (x_coord * diff - 3, (y_coord + k)*diff), (x_coord * diff + diff + 3, (y_coord + k)*diff), line_thickness) # Horizontal lines
        pygame.draw.line(Window, pygame.Color("blue"), ((x_coord + k) * diff, y_coord * diff), ((x_coord + k) * diff, y_coord * diff + diff), line_thickness)     # Vertical lines


def initializeWindow():
    sudoku_board = SudokuBoard()
    exit_game = False
    highlight_flag = False
    num_pressed = 0


    while not exit_game:
        Window.fill(pygame.Color("white"))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True
            
            elif event.type == pygame.MOUSEBUTTONDOWN:
                handle_mouse_event(sudoku_board)
                highlight_flag = True

            elif event.type == pygame.KEYDOWN:
                if event.key in ARROW_PRESSED:
                    handle_arrow_pressed(event.key, sudoku_board)
                    highlight_flag = True
                elif event.key in NUM_PRESSED:
                    num_pressed = handle_number_pressed(event.key)

        if num_pressed != 0:
            draw_number(num_pressed, sudoku_board)
            sudoku_board.defaultgrid[int(sudoku_board.x_coord)][int(sudoku_board.y_coord)] = num_pressed  # TODO: Only do this if num_pressed is allowed
            num_pressed = 0

        draw_bg(sudoku_board.defaultgrid)
        draw_lines()

        if highlight_flag:
            highlight_box([sudoku_board.x_coord, sudoku_board.y_coord])

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    initializeWindow()