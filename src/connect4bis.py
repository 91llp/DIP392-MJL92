import tkinter as tk
import numpy as np

class Puissance4:
    def __init__(self, master):
        self.master = master
        self.master.title("Configuration de Puissance 4")

        # Initialiser les paramètres de jeu
        self.rows = 6
        self.columns = 7
        self.player1_name = "Joueur 1"
        self.player2_name = "Joueur 2"
        self.player1_color = "red"
        self.player2_color = "yellow"

        # Widgets pour la configuration
        tk.Label(self.master, text="Nombre de colonnes (4-10):").grid(row=0, column=0)
        self.columns_entry = tk.Entry(self.master)
        self.columns_entry.grid(row=0, column=1)

        tk.Label(self.master, text="Nom du joueur 1:").grid(row=1, column=0)
        self.player1_entry = tk.Entry(self.master)
        self.player1_entry.grid(row=1, column=1)

        tk.Label(self.master, text="Nom du joueur 2:").grid(row=2, column=0)
        self.player2_entry = tk.Entry(self.master)
        self.player2_entry.grid(row=2, column=1)

        tk.Button(self.master, text="Commencer le jeu", command=self.start_game).grid(row=3, columnspan=2)

    def start_game(self):
        # Récupérer les configurations
        self.columns = max(4, min(10, int(self.columns_entry.get())))
        self.player1_name = self.player1_entry.get()
        self.player2_name = self.player2_entry.get()

        # Créer et afficher la fenêtre de jeu
        game_window = tk.Toplevel(self.master)
        game_window.title("Puissance 4")
        self.game = GameBoard(game_window, self.rows, self.columns, self.player1_name, self.player2_name, self.player1_color, self.player2_color)

class GameBoard:
    def __init__(self, master, rows, columns, player1_name, player2_name, player1_color, player2_color):
        self.master = master
        self.rows = rows
        self.columns = columns
        self.player1_name = player1_name
        self.player2_name = player2_name
        self.player1_color = player1_color
        self.player2_color = player2_color
        self.turn = 1

        # Initialiser la grille de jeu
        self.grid = np.zeros((self.rows, self.columns), dtype=int)

        # Boutons pour chaque colonne
        self.buttons = [tk.Button(self.master, text=f"Colonne {i+1}", command=lambda c=i: self.play(c)) for i in range(self.columns)]
        for i, button in enumerate(self.buttons):
            button.grid(row=0, column=i)

        # Affichage de la grille du jeu
        self.labels = [[tk.Label(self.master, text=' ', width=12, height=2, relief="ridge", bg='light grey') for _ in range(self.columns)] for _ in range(self.rows)]
        for r in range(self.rows):
            for c in range(self.columns):
                self.labels[r][c].grid(row=r+1, column=c)

    def play(self, column):
        # Ajouter le jeton dans la grille
        for row in range(self.rows-1, -1, -1):
            if self.grid[row][column] == 0:
                self.grid[row][column] = self.turn
                color = self.player1_color if self.turn == 1 else self.player2_color
                self.labels[row][column].config(bg=color, text=' ')
                self.turn = 3 - self.turn
                break

def main():
    root = tk.Tk()
    app = Puissance4(root)
    root.mainloop()

if __name__ == "__main__":
    main()
