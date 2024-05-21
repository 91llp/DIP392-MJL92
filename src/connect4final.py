import tkinter as tk
from tkinter import colorchooser, messagebox
import numpy as np
import pygame
import sys
import math

class ConnectFourSetup:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four Setup")

        self.player_names = ['Player 1', 'Player 2']
        self.colors = [(255, 0, 0), (255, 255, 0)]  # Default colors (red, yellow)
        self.columns = 7
        self.rows = 6

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.master, text="Player 1 Name:").grid(row=0, column=0)
        self.p1_name = tk.Entry(self.master)
        self.p1_name.grid(row=0, column=1)
        self.p1_name.insert(0, 'Player 1')

        tk.Label(self.master, text="Player 2 Name:").grid(row=1, column=0)
        self.p2_name = tk.Entry(self.master)
        self.p2_name.grid(row=1, column=1)
        self.p2_name.insert(0, 'Player 2')

        tk.Button(self.master, text="Select Player 1 Color", command=lambda: self.choose_color(0)).grid(row=0, column=2)
        tk.Button(self.master, text="Select Player 2 Color", command=lambda: self.choose_color(1)).grid(row=1, column=2)

        tk.Label(self.master, text="Number of Columns:").grid(row=2, column=0)
        self.column_entry = tk.Entry(self.master)
        self.column_entry.grid(row=2, column=1)
        self.column_entry.insert(0, '7')

        tk.Button(self.master, text="Start Game", command=self.start_game).grid(row=3, column=1)

    def choose_color(self, player):
        color, _ = colorchooser.askcolor()
        if color:
            self.colors[player] = tuple(int(c) for c in color)

    def start_game(self):
        try:
            columns = int(self.column_entry.get())
            if columns < 4:
                raise ValueError("Columns must be at least 4.")
            self.columns = columns
            self.player_names = [self.p1_name.get(), self.p2_name.get()]
            self.master.quit()
            self.master.destroy()
            ConnectFourGame(self.rows, self.columns, self.player_names, self.colors)
        except ValueError as e:
            messagebox.showerror("Error", str(e))

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
        self.myfont = pygame.font.SysFont("monospace", 75)

        self.draw_board()
        self.mainloop()

    def draw_board(self):
        self.screen.fill((0, 0, 0))
        for c in range(self.columns):
            for r in range(self.rows):
                pygame.draw.rect(self.screen, (0, 0, 255), (c * self.SQUARESIZE, (r + 1) * self.SQUARESIZE, self.SQUARESIZE, self.SQUARESIZE))
                pygame.draw.circle(self.screen, (0, 0, 0), (int(c * self.SQUARESIZE + self.SQUARESIZE / 2), int((r + 1) * self.SQUARESIZE + self.SQUARESIZE / 2)), self.SQUARESIZE // 2 - 5)

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
        message_font = pygame.font.SysFont("monospace", 50)
        message_text = message_font.render("Play again? Click to continue.", True, (255, 255, 255))
        self.screen.blit(message_text, (50, self.height // 2))
        pygame.display.update()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    # Reset the game
                    self.board = self.create_board()
                    self.game_over = False
                    self.turn = 0
                    self.draw_board()
                    waiting_for_input = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()

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
        font = pygame.font.SysFont("monospace", 75)
        label = font.render(message, 1, (255, 255, 255))
        self.screen.blit(label, (40, 10))
        pygame.display.update()
        pygame.time.wait(2000)

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFourSetup(root)
    root.mainloop()
