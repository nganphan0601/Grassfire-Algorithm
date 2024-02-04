from tkinter import ttk
import numpy as np
from grid import Grid
import tkinter as tk


def display_grid(grid, canvas):
    rows, cols = grid.grid.shape
    cell_width = canvas.winfo_width() / cols
    cell_height = canvas.winfo_height() / rows

    for i in range(rows):
        for j in range(cols):
            if grid.grid[i, j] == grid.START:
                color = "green"
            elif grid.grid[i, j] == grid.GOAL:
                color = "red"
            elif grid.grid[i, j] == grid.OBSTACLE:
                color = "black"
            elif grid.grid[i, j] == grid.PATH:
                color = "yellow"
            else:
                color = "white"
            canvas.create_rectangle(j * cell_width, i * cell_height, (j + 1) * cell_width, (i + 1) * cell_height, fill=color)

    canvas.update()

def validate_inputs(rows, cols, obstacle_density, start, goal):
    if rows < 8 or cols < 8:
        return False
    if obstacle_density < 0 or obstacle_density > 1:
        return False
    if start[0] < 0 or start[0] > rows // 2 or start[1] > cols:
        return False
    if goal[0] < 0 or goal[0] <= rows // 2 or goal[1] > cols or goal[1] <= int( cols * 2/3 ):
        return False
    return True

def start_algorithm(canvas, rows_num, cols_num, obstacle_density, start, goal):
    reset_grid(canvas)

    # collect inputs
    rows = int(rows_num.get())
    cols = int(cols_num.get())
    obstacle_density = float(obstacle_density.get())
    start = tuple(map(int, start.get().split(","))) 
    goal = tuple(map(int, goal.get().split(",")))

    # Validate inputs
    if not validate_inputs(rows, cols, obstacle_density, start, goal):
        print("Invalid inputs")
        return
    
    # Create a grid
    grid = Grid(rows, cols, obstacle_density, start, goal)

    grid.grassfire()
    
    display_grid(grid, canvas)

def reset_grid(canvas):
    canvas.delete("all")


def Main():
    # grid = Grid(8 , 8, 0.0, (0, 2), (7, 7))
    # grid.display()  # Display the grid
    # grid.grassfire()
    # # grid.trace_path()
    # grid.display_distance()  # Display the distance grid
    
    # grid.display()  # Display the grid with the path
    root = tk.Tk()
    root.configure(bg="black")
    root.geometry("1000x600")
    root.title("Grassfire Algorithm Visualization")

    label = tk.Label(root, text="Grassfire Algorithm Visualization", font=("Jokerman", 20), bg="black", fg="white")
    author = tk.Label(root, text="by Ngan Phan", font=("Comic Sans MS", 14), bg="black", fg="white")

    label.pack(padx=20, pady=10)
    author.pack(padx=20, pady=0)
    


    # Create a frame for the grid
    frame = tk.Frame(root)
    frame.configure(bg="black")
    frame.pack(fill="both", expand=True, padx=20, pady=20)

    # Create a frame for the inputs
    input_frame = tk.Frame(frame)
    input_frame.configure(bg="black")
    input_frame.grid(row=0, column=0, padx=40, pady=10, sticky="we")

    cols_num = tk.IntVar()
    rows_num = tk.IntVar()
    obstacle_density = tk.DoubleVar()
    start = tk.StringVar()
    goal = tk.StringVar()

    input_items = [
        ("Rows (8+)", rows_num),
        ("Columns (8+)", cols_num),
        ("Obstacle Density \n (10% - 20% recommended)", obstacle_density),
        ("Start (x,y)", start),
        ("Goal (x,y)", goal)
    ]

    # Create a canvas for the grid
    canvas = tk.Canvas(frame, borderwidth=0, background="white", width=400, height=400, highlightthickness=3, highlightbackground="#11FFEE")
    canvas.grid(row=0, column=1, sticky=(tk.W, tk.E, tk.N, tk.S))

    for i, (label, var) in enumerate(input_items):
        label = tk.Label(input_frame, text=label, font=("Helvetica", 14, "bold"), bg="black", fg="white")
        label.grid(row=i, column=0, padx=10, pady=10)
        entry = tk.Entry(input_frame, textvariable=var, font=("Segoe UI", 18), width=10, bg="black", fg="white", highlightthickness=2, highlightbackground="#11FFEE")
        entry.grid(row=i, column=1, padx=10, pady=10)

    start_button = tk.Button(input_frame, text="Start", padx=20, pady=10, font=("Arial", 14), bg="#11FFEE", fg="black", command= lambda: start_algorithm(canvas, rows_num, cols_num, obstacle_density, start, goal))
    start_button.grid(row=5, column=0, columnspan=2)


    root.mainloop()



if __name__ == "__main__":
    Main()