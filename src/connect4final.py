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
        self.height = (rows + 1) * self.SQUARESIZE
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
                pygame.draw.rect(self.screen, (30, 144, 255), (c * self.SQUARESIZE, (r + 1) * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, (255, 255, 255), (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int((r + 1) * self.SQUARESIZE + self.SQUARESIZE / 2)), self.SQUARESIZE // 2 - 5)

        for c in range(self.columns):
            for r in range(self.rows):
                if self.board[r][c] == 1:
                    pygame.draw.circle(self.screen, self.colors[0], (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(self.height - (r * self.SQUARESIZE + self.SQUARESIZE / 2))), self.SQUARESIZE // 2 - 5)
                elif self.board[r][c] == 2:
                    pygame.draw.circle(self.screen, self.colors[1], (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int(self.height - (r * self.SQUARESIZE + self.SQUARESIZE / 2))), self.SQUARESIZE // 2 - 5)
        pygame.display.update()

    # Remaining methods for handling game logic...

# Rest of the ConnectFourGame class code remains same
