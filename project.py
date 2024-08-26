import tkinter as tk
import random

GRID_SIZE = 4
WIN_SCORE = 2048

class Game2048:
    def __init__(self, master):
        self.master = master
        self.master.title('2048 Game')
        self.game_grid = [[0] * GRID_SIZE for _ in range(GRID_SIZE)]
        self.create_gui()
        self.start_game()

    def create_gui(self):
        self.grid_frame = tk.Frame(self.master)
        self.grid_frame.grid()
        self.tiles = [[None] * GRID_SIZE for _ in range(GRID_SIZE)]
        
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                tile = tk.Label(self.grid_frame, text='', width=6, height=3, font=('Helvetica', 24), bg='lightgray')
                tile.grid(row=i, column=j, padx=5, pady=5)
                self.tiles[i][j] = tile

        self.master.bind("<Key>", self.key_handler)

    def start_game(self):
        self.add_new_tile()
        self.add_new_tile()
        self.update_gui()

    def add_new_tile(self):
        empty_cells = [(i, j) for i in range(GRID_SIZE) for j in range(GRID_SIZE) if self.game_grid[i][j] == 0]
        if empty_cells:
            i, j = random.choice(empty_cells)
            self.game_grid[i][j] = random.choice([2, 4])

    def update_gui(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                value = self.game_grid[i][j]
                tile = self.tiles[i][j]
                tile.config(text=str(value) if value != 0 else '', bg=self.get_tile_color(value))

    def get_tile_color(self, value):
        colors = {
            0: 'lightgray', 2: 'white', 4: 'lightyellow', 8: 'lightgoldenrod',
            16: 'orange', 32: 'orangered', 64: 'red', 128: 'lightgreen',
            256: 'green', 512: 'blue', 1024: 'purple', 2048: 'gold'
        }
        return colors.get(value, 'black')

    def key_handler(self, event):
        key = event.keysym
        if key in ('Up', 'Down', 'Left', 'Right'):
            self.move(key)

    def move(self, direction):
        moved = False
        if direction == 'Up':
            self.game_grid, moved = self.move_up_or_down(self.game_grid, reverse=False)
        elif direction == 'Down':
            self.game_grid, moved = self.move_up_or_down(self.game_grid, reverse=True)
        elif direction == 'Left':
            self.game_grid, moved = self.move_left_or_right(self.game_grid, reverse=False)
        elif direction == 'Right':
            self.game_grid, moved = self.move_left_or_right(self.game_grid, reverse=True)

        if moved:
            self.add_new_tile()
            self.update_gui()

            if self.check_win():
                self.show_win_message()
            elif self.check_game_over():
                self.show_game_over_message()

    def move_left_or_right(self, grid, reverse=False):
        moved = False
        new_grid = []
        for row in grid:
            if reverse:
                row = row[::-1]
            compressed_row, moved_row = self.compress(row)
            merged_row, merged_moved = self.merge_tiles(compressed_row)
            final_row, final_moved = self.compress(merged_row)
            if reverse:
                final_row = final_row[::-1]
            new_grid.append(final_row)
            if moved_row or merged_moved or final_moved:
                moved = True
        return new_grid, moved

    def move_up_or_down(self, grid, reverse=False):
        transposed_grid = self.transpose(grid)
        moved = False
        new_grid, moved = self.move_left_or_right(transposed_grid, reverse=reverse)
        return self.transpose(new_grid), moved

    def compress(self, row):
        new_row = [value for value in row if value != 0]
        new_row += [0] * (GRID_SIZE - len(new_row))
        return new_row, new_row != row

    def merge_tiles(self, row):
        moved = False
        for i in range(GRID_SIZE - 1):
            if row[i] == row[i + 1] and row[i] != 0:
                row[i] *= 2
                row[i + 1] = 0
                moved = True
        return row, moved

    def transpose(self, grid):
        return [[grid[j][i] for j in range(GRID_SIZE)] for i in range(GRID_SIZE)]

    def check_win(self):
        return any(WIN_SCORE in row for row in self.game_grid)

    def check_game_over(self):
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                if self.game_grid[i][j] == 0:
                    return False
                if j < GRID_SIZE - 1 and self.game_grid[i][j] == self.game_grid[i][j + 1]:
                    return False
                if i < GRID_SIZE - 1 and self.game_grid[i][j] == self.game_grid[i + 1][j]:
                    return False
        return True

    def show_win_message(self):
        tk.messagebox.showinfo('2048', 'Congratulations! You reached 2048!')

    def show_game_over_message(self):
        tk.messagebox.showinfo('2048', 'Game Over!')


if __name__ == '__main__':
    root = tk.Tk()
    game = Game2048(root)
    root.mainloop()
