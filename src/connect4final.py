import numpy as np
import pygame
import sys
import math

class ConnectFourGame:
    def __init__(self, rows, columns, player_names, colors):
        pygame.init()
        self.rows = rows
        self.columns = columns
        self.player_names = player_names
        self.colors = colors
        self.board = np.zeros((rows, columns))
        self.game_over = False
        self.turn = 0

        self.SQUARESIZE = 100
        self.width = columns * self.SQUARESIZE
        self.height = rows * self.SQUARESIZE  # Adjust height to remove black area
        self.size = (self.width, self.height)
        self.screen = pygame.display.set_mode(self.size)
        self.myfont = pygame.font.SysFont("comicsansms", 75)  # Using a more casual font

        pygame.display.set_caption('Connect Four')
        self.draw_board()
        self.mainloop()

    def draw_board(self):
        self.screen.fill((0, 0, 0))  # Clear the screen each time to draw anew
        for c in range(self.columns):
            for r in range(self.rows):
                pygame.draw.rect(self.screen, (30, 144, 255), (c * self.SQUARESIZE, r * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))  # Adjusted
                pygame.draw.circle(self.screen, (255, 255, 255), (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(r * self.SQUARESIZE + self.SQUARESIZE / 2)), self.SQUARESIZE // 2 - 5)  # Adjusted

        for c in range(self.columns):
            for r in range(self.rows):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.colors[0], (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(self.height - (r * self.SQUARESIZE + self.SQUARESIZE / 2))), self.SQUARESIZE // 2 - 5)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.colors[1], (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(self.height - (r * self.SQUARESIZE + self.SQUARESIZE / 2))), self.SQUARESIZE // 2 - 5)
        pygame.display.update()

    def mainloop(self):
        while True:
            if self.game_over:
                self.prompt_restart()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if not self.game_over:
                        x_pos = event.pos[0]
                        col = int(math.floor(x_pos / self.SQUARESIZE))

                        if self.is_valid_location(col):
                            row = self.get_next_open_row(col)
                            self.drop_piece(row, col, self.turn + 1)
                            self.draw_board()

                            if self.check_win(self.turn + 1):
                                self.game_over = True
                                self.display_message(f"{self.player_names[self.turn]} wins!")

                            self.turn += 1
                            self.turn = self.turn % 2

                            if all(self.board[-1] != 0):  # Check for a draw
                                self.game_over = True
                                self.display_message("Draw!")

    def prompt_restart(self):
        self.game_over = True  # Ensure no further moves can be made
        result = messagebox.askyesno("Game Over", "Would you like to play again?")
        if result:
            self.restart_game()
        else:
            pygame.quit()
            sys.exit()

    def restart_game(self):
        self.board = np.zeros((self.rows, self.columns))
        self.game_over = False
        self.turn = 0
        self.draw_board()

    def is_valid_location(self, col):
        return self.board[self.rows-1][col] == 0

    def get_next_open_row(self, col):
        for r in range(self.rows):
            if self.board[r][col] == 0:
                return r
        return None

    def drop_piece(self, row, col, piece):
        self.board[row][col] = piece

    def check_win(self, piece):
        # Horizontal, vertical, and diagonal checks
        for c in range(self.columns-3):
            for r in range(self.rows):
                if self.board[r][c] == piece and self.board[r][c+1] == piece and self.board[r][c+2] == piece and self.board[r][c+3] == piece:
                    return True
        for c in range(self.columns):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c] == piece and self.board[r+2][c] == piece and self.board[r+3][c] == piece:
                    return True
        for c in range(self.columns-3):
            for r in range(3, self.rows):
                if self.board[r][c] == piece and self.board[r-1][c+1] == piece and self.board[r-2][c+2] == piece and self.board[r-3][c+3] == piece:
                    return True
        for c in range(self.columns-3):
            for r in range(self.rows-3):
                if self.board[r][c] == piece and self.board[r+1][c+1] == piece and self.board[r+2][c+2] == piece and self.board[r+3][c+3] == piece:
                    return True
        return False

    def display_message(self, message):
        self.screen.fill((0, 0, 0))
        font = pygame.font.SysFont("comicsansms", 75)
        label = font.render(message, 1, (255, 255, 255))
        self.screen.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(2000)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFourSetup(root)
    root.mainloop()
