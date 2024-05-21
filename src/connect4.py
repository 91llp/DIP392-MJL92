import numpy as np
import pygame
import sys
import math

# Colors
BLUE = (0, 0, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
DARK_BLUE = (0, 0, 139)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)

# Game dimensions
ROW_COUNT = 6
COLUMN_COUNT = 7
SQUARESIZE = 100
RADIUS = int(SQUARESIZE / 2 - 5)

# Screen dimensions
width = COLUMN_COUNT * SQUARESIZE
height = (ROW_COUNT + 2) * SQUARESIZE
size = (width, height)

# Button dimensions
BUTTON_WIDTH = 150
BUTTON_HEIGHT = 50

def create_board():
    board = np.zeros((ROW_COUNT, COLUMN_COUNT))
    return board

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[ROW_COUNT - 1][col] == 0

def get_next_open_row(board, col):
    for r in range(ROW_COUNT):
        if board[r][col] == 0:
            return r

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Check horizontal locations for win
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT):
            if board[r][c] == piece and board[r][c + 1] == piece and board[r][c + 2] == piece and board[r][c + 3] == piece:
                return True

    # Check vertical locations for win
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c] == piece and board[r + 2][c] == piece and board[r + 3][c] == piece:
                return True

    # Check positively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(ROW_COUNT - 3):
            if board[r][c] == piece and board[r + 1][c + 1] == piece and board[r + 2][c + 2] == piece and board[r + 3][c + 3] == piece:
                return True

    # Check negatively sloped diagonals
    for c in range(COLUMN_COUNT - 3):
        for r in range(3, ROW_COUNT):
            if board[r][c] == piece and board[r - 1][c + 1] == piece and board[r - 2][c + 2] == piece and board[r - 3][c + 3] == piece:
                return True

def is_draw(board):
    return not np.any(board == 0)

def draw_board(board):
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            color = LIGHT_BLUE if (r + c) % 2 == 0 else DARK_BLUE
            pygame.draw.rect(screen, color, (c * SQUARESIZE, r * SQUARESIZE + SQUARESIZE, SQUARESIZE, SQUARESIZE))
            pygame.draw.circle(screen, BLACK, (int(c * SQUARESIZE + SQUARESIZE / 2), int(r * SQUARESIZE + SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    
    for c in range(COLUMN_COUNT):
        for r in range(ROW_COUNT):
            if board[r][c] == 1:
                pygame.draw.circle(screen, RED, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, YELLOW, (int(c * SQUARESIZE + SQUARESIZE / 2), height - int(r * SQUARESIZE + SQUARESIZE / 2)), RADIUS)
    pygame.display.update()

def draw_buttons():
    new_game_rect = pygame.draw.rect(screen, WHITE, (width // 2 - 1.5 * BUTTON_WIDTH, height - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT))
    restart_rect = pygame.draw.rect(screen, WHITE, (width // 2 - 0.5 * BUTTON_WIDTH, height - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT))
    exit_rect = pygame.draw.rect(screen, WHITE, (width // 2 + 0.5 * BUTTON_WIDTH, height - BUTTON_HEIGHT - 20, BUTTON_WIDTH, BUTTON_HEIGHT))
    
    screen.blit(font.render('New Game', True, BLACK), (width // 2 - 1.5 * BUTTON_WIDTH + 10, height - BUTTON_HEIGHT - 10))
    screen.blit(font.render('Restart', True, BLACK), (width // 2 - 0.5 * BUTTON_WIDTH + 10, height - BUTTON_HEIGHT - 10))
    screen.blit(font.render('Exit', True, BLACK), (width // 2 + 0.5 * BUTTON_WIDTH + 10, height - BUTTON_HEIGHT - 10))
    
    return new_game_rect, restart_rect, exit_rect

def new_game():
    global board, game_over
    board = create_board()
    game_over = False
    draw_board(board)
    draw_buttons()

def restart():
    global board
    board = create_board()
    draw_board(board)
    draw_buttons()

def exit_game():
    pygame.quit()
    sys.exit()

pygame.init()

screen = pygame.display.set_mode(size)
font = pygame.font.SysFont("monospace", 35)

board = create_board()
game_over = False

draw_board(board)
new_game_rect, restart_rect, exit_rect = draw_buttons()

myfont = pygame.font.SysFont("monospace", 75)

turn = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            posx = event.pos[0]
            posy = event.pos[1]

            if new_game_rect.collidepoint(posx, posy):
                new_game()

            if restart_rect.collidepoint(posx, posy):
                restart()

            if exit_rect.collidepoint(posx, posy):
                exit_game()

            if not game_over:
                col = int(math.floor(posx / SQUARESIZE))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    drop_piece(board, row, col, turn + 1)

                    if winning_move(board, turn + 1):
                        label = myfont.render(f"Player {turn + 1} wins!!", 1, RED if turn == 0 else YELLOW)
                        screen.blit(label, (40, 10))
                        game_over = True

                    if is_draw(board):
                        label = myfont.render("Draw!!", 1, BLACK)
                        screen.blit(label, (40, 10))
                        game_over = True

                    turn += 1
                    turn = turn % 2

                    draw_board(board)
                    new_game_rect, restart_rect, exit_rect = draw_buttons()

    pygame.display.update()
