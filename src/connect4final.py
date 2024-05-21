import tkinter as tk
from tkinter import colorchooser, messagebox, ttk  # Using ttk for improved widget styles

def start_game(rows, columns, player_names, colors):
    import threading
    game_thread = threading.Thread(target=lambda: ConnectFourGame(rows, columns, player_names, colors))
    game_thread.start()

class ConnectFourSetup:
    def __init__(self, master):
        self.master = master
        self.master.title("Connect Four Setup")
        style = ttk.Style(self.master)
        style.theme_use('clam')  # Using a theme for better appearance

        self.player_names = ['Player 1', 'Player 2']
        self.colors = [(255, 0, 0), (255, 255, 0)]  # Default colors (red, yellow)
        self.columns = 7
        self.rows = 6

        self.setup_ui()

    def setup_ui(self):
        ttk.Label(self.master, text="Player 1 Name:").grid(row=0, column=0, padx=10, pady=10)
        self.p1_name = ttk.Entry(self.master)
        self.p1_name.grid(row=0, column=1, pady=10)
        self.p1_name.insert(0, 'Player 1')

        ttk.Label(self.master, text="Player 2 Name:").grid(row=1, column=0, padx=10, pady=10)
        self.p2_name = ttk.Entry(self.master)
        self.p2_name.grid(row=1, column=1, pady=10)
        self.p2_name.insert(0, 'Player 2')

        ttk.Button(self.master, text="Select Player 1 Color", command=lambda: self.choose_color(0)).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(self.master, text="Select Player 2 Color", command=lambda: self.choose_color(1)).grid(row=1, column=2, padx=10, pady=10)

        ttk.Label(self.master, text="Number of Columns:").grid(row=2, column=0, padx=10, pady=10)
        self.column_entry = ttk.Entry(self.master)
        self.column_entry.grid(row=2, column=1, pady=10)
        self.column_entry.insert(0, '7')

        ttk.Button(self.master, text="Start Game", command=self.start_game).grid(row=3, column=1, pady=20)

    def choose_color(self, player):
        color, _ = colorchooser.askcolor()
        if color:
            self.colors[player] = tuple(int(c) for c in color)

    def start_game(self):
        try:
            columns = int(self.column_entry.get())
            if columns < 4:
                raise ValueError("Columns must be at least 4.")
            player_names = [self.p1_name.get(), self.p2_name.get()]
            start_game(self.rows, columns, player_names, self.colors)
            self.master.destroy()
        except ValueError as e:
            messagebox.showerror("Error", str(e))

if __name__ == "__main__":
    root = tk.Tk()
    app = ConnectFourSetup(root)
    root.mainloop()
