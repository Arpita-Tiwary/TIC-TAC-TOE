import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 600
LINE_WIDTH = 10
BOARD_ROWS, BOARD_COLS = 3, 3
SQUARE_SIZE = WIDTH // BOARD_COLS
CIRCLE_RADIUS = SQUARE_SIZE // 3
CIRCLE_WIDTH = 10
CROSS_WIDTH = 15
SPACE = 50
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LINE_COLOR = (23, 145, 135)
CIRCLE_COLOR = (239, 231, 200)
CROSS_COLOR = (66, 66, 66)

# Initialize screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Tic-Tac-Toe")
screen.fill(WHITE)

# Board
board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]

# Draw the grid lines
def draw_lines():
    pygame.draw.line(screen, LINE_COLOR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH)
    pygame.draw.line(screen, LINE_COLOR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH)

# Draw X and O
def draw_figures():
    for row in range(BOARD_ROWS):
        for col in range(BOARD_COLS):
            if board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2), CIRCLE_RADIUS, CIRCLE_WIDTH)
            elif board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), 
                                 (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH)

# Check winner
def check_winner(player):
    for row in range(BOARD_ROWS):
        if all(board[row][col] == player for col in range(BOARD_COLS)):
            draw_horizontal_winning_line(row, player)
            return True
    for col in range(BOARD_COLS):
        if all(board[row][col] == player for row in range(BOARD_ROWS)):
            draw_vertical_winning_line(col, player)
            return True
    if all(board[i][i] == player for i in range(BOARD_ROWS)):
        draw_diagonal_winning_line(player, True)
        return True
    if all(board[i][BOARD_ROWS - 1 - i] == player for i in range(BOARD_ROWS)):
        draw_diagonal_winning_line(player, False)
        return True
    return False

# Draw winning line
def draw_horizontal_winning_line(row, player):
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR, 
                     (0, row * SQUARE_SIZE + SQUARE_SIZE // 2), 
                     (WIDTH, row * SQUARE_SIZE + SQUARE_SIZE // 2), LINE_WIDTH)

def draw_vertical_winning_line(col, player):
    pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR, 
                     (col * SQUARE_SIZE + SQUARE_SIZE // 2, 0), 
                     (col * SQUARE_SIZE + SQUARE_SIZE // 2, HEIGHT), LINE_WIDTH)

def draw_diagonal_winning_line(player, main_diagonal):
    if main_diagonal:
        pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR, 
                         (0, 0), (WIDTH, HEIGHT), LINE_WIDTH)
    else:
        pygame.draw.line(screen, CIRCLE_COLOR if player == "O" else CROSS_COLOR, 
                         (0, HEIGHT), (WIDTH, 0), LINE_WIDTH)

# Check if board is full (draw)
def is_draw():
    return all(board[row][col] != " " for row in range(BOARD_ROWS) for col in range(BOARD_COLS))

# Reset game
def reset_game():
    global board, player
    screen.fill(WHITE)
    draw_lines()
    board = [[" " for _ in range(BOARD_COLS)] for _ in range(BOARD_ROWS)]
    player = "X"

# Game variables
player = "X"
game_over = False

# Draw initial board
draw_lines()

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
            x, y = event.pos
            row, col = y // SQUARE_SIZE, x // SQUARE_SIZE

            if board[row][col] == " ":
                board[row][col] = player
                draw_figures()

                if check_winner(player):
                    game_over = True
                elif is_draw():
                    game_over = True
                else:
                    player = "O" if player == "X" else "X"

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                reset_game()
                game_over = False

    pygame.display.update()
