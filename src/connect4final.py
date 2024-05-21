import numpy as np
import pygame
import sys
import math

def create_board(rows, columns):
    return np.zeros((rows, columns))

def drop_piece(board, row, col, piece):
    board[row][col] = piece

def is_valid_location(board, col):
    return board[-1][col] == 0

def get_next_open_row(board, col):
    for r in range(board.shape[0]):
        if board[r][col] == 0:
            return r
    return None

def print_board(board):
    print(np.flip(board, 0))

def winning_move(board, piece):
    # Horizontal, vertical, and diagonal checks
    rows, cols = board.shape
    for c in range(cols - 3):
        for r in range(rows):
            if board[r][c:c+4].all() == piece:
                return True
    for c in range(cols):
        for r in range(rows - 3):
            if board[r:r+4, c].all() == piece:
                return True
    for c in range(cols - 3):
        for r in range(rows - 3):
            if board[r:r+4, c:c+4].diagonal().all() == piece:
                return True
    for c in range(cols - 3):
        for r in range(3, rows):
            if np.fliplr(board[r-3:r+1, c:c+4]).diagonal().all() == piece:
                return True
    return False

def draw_board(board, colors, screen, squaresize, radius):
    for c in range(board.shape[1]):
        for r in range(board.shape[0]):
            pygame.draw.rect(screen, (0, 0, 0), (c * squaresize, r * squaresize + squaresize, squaresize, squaresize))
            pygame.draw.circle(screen, (173, 216, 230), (int(c * squaresize + squaresize / 2), int(r * squaresize + squaresize + squaresize / 2)), radius)
            if board[r][c] == 1:
                pygame.draw.circle(screen, colors[0], (int(c * squaresize + squaresize / 2), int(squaresize * (board.shape[0] + 1) - r * squaresize - squaresize / 2)), radius)
            elif board[r][c] == 2:
                pygame.draw.circle(screen, colors[1], (int(c * squaresize + squaresize / 2), int(squaresize * (board.shape[0] + 1) - r * squaresize - squaresize / 2)), radius)
    pygame.display.update()

def initialize_game():
    pygame.init()
    player1_name = input("Enter the name for Player 1: ")
    player2_name = input("Enter the name for Player 2: ")
    colors = []
    colors.append(tuple(int(x) for x in input(f"Enter RGB for {player1_name} (e.g. 255 0 0): ").split()))
    colors.append(tuple(int(x) for x in input(f"Enter RGB for {player2_name} (e.g. 0 0 255): ").split()))
    columns = int(input("Enter the number of columns (7 is standard): "))
    rows = 6  # standard row count

    board = create_board(rows, columns)
    game_over = False
    turn = 0

    squaresize = 100
    width = columns * squaresize
    height = (rows + 1) * squaresize
    size = (width, height)
    radius = int(squaresize / 2 - 5)

    screen = pygame.display.set_mode(size)
    myfont = pygame.font.SysFont("monospace", 75)

    return board, game_over, turn, colors, screen, squaresize, radius, myfont, player1_name, player2_name

def main():
    board, game_over, turn, colors, screen, squaresize, radius, myfont, player1_name, player2_name = initialize_game()
    draw_board(board, colors, screen, squaresize, radius)

    while not game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                posx = event.pos[0]
                col = int(math.floor(posx / squaresize))

                if is_valid_location(board, col):
                    row = get_next_open_row(board, col)
                    if row is not None:
                        drop_piece(board, row, col, turn + 1)
                        if winning_move(board, turn + 1):
                            label = myfont.render(f"{player1_name if turn == 0 else player2_name} wins!", 1, colors[turn])
                            screen.blit(label, (40, 10))
                            game_over = True

                        draw_board(board, colors, screen, squaresize, radius)

                        turn += 1
                        turn = turn % 2

                        if not np.any(board == 0):
                            label = myfont.render("Draw!", 1, (255, 255, 255))
                            screen.blit(label, (40, 10))
                            game_over = True

if __name__ == "__main__":
    main()
