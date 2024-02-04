import numpy as np
from grid import Grid

def Main():
    grid = Grid(8 , 8, 0.0, (0, 2), (7, 7))
    grid.display()  # Display the grid
    grid.grassfire()
    # grid.trace_path()
    grid.display_distance()  # Display the distance grid
    
    grid.display()  # Display the grid with the path
    



if __name__ == "__main__":
    Main()