import numpy as np
import matplotlib.pyplot as plt
import random

class SudokuUI:
    def __init__(self):
        self.grid = np.zeros((9, 9), dtype=int)
        self.fig, self.ax = plt.subplots()
        self.ax.set_aspect('equal')
        self.selected_cell = None

        self.draw_sudoku_grid()
        self.update_display()
        
        self.fig.canvas.mpl_connect('button_press_event', self.on_click)
        self.fig.canvas.mpl_connect('key_press_event', self.on_key_press)

    def draw_sudoku_grid(self):
        for i in range(10):
            linewidth = 2 if i % 3 == 0 else 1
            self.ax.axhline(i, lw=linewidth, color='k')
            self.ax.axvline(i, lw=linewidth, color='k')
        self.ax.set_xlim(0, 9)
        self.ax.set_ylim(0, 9)
        self.ax.axis('off')

    def update_display(self):
        self.ax.clear()
        self.draw_sudoku_grid()
        for i in range(9):
            for j in range(9):
                if self.grid[i, j] != 0:
                    self.ax.text(j + 0.5, 8.5 - i, str(self.grid[i, j]), ha='center', va='center', fontsize=20)
        plt.draw()


    def on_click(self, event):
        if event.inaxes == self.ax:
            x, y = int(event.xdata), int(9 - event.ydata)
            self.selected_cell = (y, x)
            

    def on_key_press(self, event):
        if self.selected_cell:
            y, x = self.selected_cell
            if event.key.isdigit() and 1 <= int(event.key) <= 9:
                self.grid[y, x] = int(event.key)
                self.update_display()
            elif event.key == '0' or event.key == 'backspace':
                self.grid[y, x] = 0
                self.update_display()
            print(f"Grid updated:\n{self.grid}")
    def get_grid(self):
        return self.grid

    def show(self):
        plt.show()



def is_valid(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num or grid[x][col] == num:
            return False
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if grid[i + start_row][j + start_col] == num:
                return False
    return True

def solve_sudoku(grid):
    for row in range(9):
        for col in range(9):
            if grid[row][col] == 0:
                for num in range(1, 10):
                    if is_valid(grid, row, col, num):
                        grid[row][col] = num
                        if solve_sudoku(grid):
                            return True
                        grid[row][col] = 0
                return False
    return True

def display_sudoku(grid):
    ax = draw_sudoku_grid()
    for i in range(9):
        for j in range(9):
            if grid[i][j] != 0:
                ax.text(j + 0.5, 8.5 - i, str(grid[i][j]), ha='center', va='center', fontsize=20)
    plt.show()

def draw_sudoku_grid():
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    for i in range(10):
        if i % 3 == 0:
            linewidth = 2
        else:
            linewidth = 1
        ax.axhline(i, lw=linewidth, color='k')
        ax.axvline(i, lw=linewidth, color='k')
    ax.set_xlim(0, 9)
    ax.set_ylim(0, 9)
    ax.axis('off')
    return ax

def draw_solved_sudoku(grid):
    ax = draw_sudoku_grid()
    for i in range(9):
        for j in range(9):
            if grid[i, j] != 0:
                ax.text(j + 0.5, 8.5 - i, str(grid[i, j]), ha='center', va='center', fontsize=20)
    plt.show()

def generate_complete_sudoku():
    grid = np.zeros((9, 9), dtype=int)
    def fill_grid(grid):
        num_list = list(range(1, 10))
        for i in range(9):
            for j in range(9):
                if grid[i][j] == 0:
                    random.shuffle(num_list)
                    for num in num_list:
                        if is_valid(grid, i, j, num):
                            grid[i][j] = num
                            if not any(0 in row for row in grid) or fill_grid(grid):
                                return True
                            grid[i][j] = 0
                    return False
        return True
    fill_grid(grid)
    return grid

# Function to remove numbers from the Sudoku grid to create a puzzle
def remove_numbers(grid, num_holes):
    holes = 0
    while holes < num_holes:
        row, col = random.randint(0, 8), random.randint(0, 8)
        if grid[row][col] != 0:
            backup = grid[row][col]
            grid[row][col] = 0
            grid_copy = grid.copy()
            if solve_sudoku(grid_copy):
                holes += 1
            else:
                grid[row][col] = backup
    return grid

# Generate and display a Sudoku puzzle
def generate_sudoku_puzzle(num_holes=40):
    complete_grid = generate_complete_sudoku()
    puzzle_grid = remove_numbers(complete_grid, num_holes)
    display_sudoku(puzzle_grid)

#----------------------------------------------------------------------------
import tkinter as tk


def button_a_clicked():
    sudoku_ui = SudokuUI()
    sudoku_ui.show()
    grid = sudoku_ui.get_grid()  # Call get_grid using the instance sudoku_ui
    solve_sudoku(grid)
    draw_solved_sudoku(grid)



def button_b_clicked():
    generate_sudoku_puzzle()

# Create the main window
root = tk.Tk()
root.title("SUDOKU")

# Create buttons
button_a = tk.Button(root, text="sudoku çözdür", command=button_a_clicked)
button_b = tk.Button(root, text="sudoku oluştur", command=button_b_clicked)

# Place buttons in the window
button_a.pack()
button_b.pack()

# Start the main loop
root.mainloop()
