import numpy as np
import matplotlib.pyplot as plt
from collections import deque

class Grid:
    START = 1
    GOAL = 2
    OBSTACLE = -1
    FREE = 0
    PATH = 3

    COLOR_START = np.array([0, 0.75, 0])
    COLOR_DEST = np.array([0.75, 0, 0])
    COLOR_UNVIS = np.array([1, 1, 1])
    COLOR_VIS = np.array([0, 0.5, 1])
    COLOR_OBST = np.array([0, 0, 0])
    COLOR_PATH = np.array([1, 1, 0])

    def __init__(self, rows = 8, cols = 8, obstacles = 0.15, start = (0,0), goal = (7,7)):
        if rows < 8 or cols < 8:
            print("The grid is too small")
            return

        if start[0] > 0:
            print("The start node should be at the top")
            return
        
        if goal[0] <= rows // 2 or goal[1] <= int(cols * 2/3):
            print("The goal node should be at the bottom half of the grid and to the right side of the grid")
            return
        
        self.rows = rows
        self.cols = cols
        self.obstacles = obstacles  # Percentage of obstacles
        self.grid = np.zeros((rows, cols))  # Create a 2D array of zeros
        
        # Set the start and goal
        self.start = start
        self.goal = goal
        self.grid[start] = self.START
        self.grid[goal] = self.GOAL

        # Add obstacles   
        self.add_obstacles()

        # init distance grid
        self.distance = np.full((rows, cols), np.inf)
        self.distance[start] = 0

    def add_obstacles(self):
        obs_cells = int(self.rows * self.cols * self.obstacles)
        available_positions = [(r, c) for r in range(self.rows) for c in range(self.cols) if (r, c) not in [self.start, self.goal]]
        selected_obstacles = np.random.choice(range(len(available_positions)), size=obs_cells, replace=False)
        
        for index in selected_obstacles:
            position = available_positions[index]
            self.grid[position] = self.OBSTACLE

    def display(self):
        color_map = np.zeros((self.rows, self.cols, 3))
        for r in range(self.rows):
            for c in range(self.cols):
                if self.grid[r, c] == self.START:
                    color_map[r, c] = self.COLOR_START
                elif self.grid[r, c] == self.GOAL:
                    color_map[r, c] = self.COLOR_DEST
                elif self.grid[r, c] == self.OBSTACLE:
                    color_map[r, c] = self.COLOR_OBST
                elif self.grid[r, c] == self.FREE:
                    color_map[r, c] = self.COLOR_UNVIS
                elif self.grid[r, c] == self.PATH:
                    color_map[r, c] = self.COLOR_PATH
                # Add more conditions here if necessary

        plt.imshow(color_map, interpolation='nearest')
        plt.show()

    def display_distance(self):
        for row in self.distance:
            print(row)


    def apply_grassfire(self):
        queue = deque([self.start])

        while queue:
            current = queue.popleft()
            current_distance = self.distance[current]

            for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:  # Right, Down, Left, Up
                neighbor = (current[0] + direction[0], current[1] + direction[1])

                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
                    if self.grid[neighbor] != self.OBSTACLE and self.distance[neighbor] == np.inf:
                        self.distance[neighbor] = current_distance + 1
                        queue.append(neighbor)

    def display_path(self, path):
        for cell in path:
            print(cell)

    def trace_path(self):
        if self.distance[self.goal] == np.inf:  # If the goal is unreachable
            print("Path not found.")
            return

        current = self.goal
        path = [current]

        while current != self.start:
            self.grid[current] = self.PATH if current != self.goal else self.GOAL
            current_distance = self.distance[current]
            for direction in [(0, -1), (1, 0), (0, 1), (-1, 0)]:  # Up, Right, Down, Left
                neighbor = (current[0] + direction[0], current[1] + direction[1])
                if 0 <= neighbor[0] < self.rows and 0 <= neighbor[1] < self.cols:
                    if self.distance[neighbor] < current_distance:
                        current = neighbor
                        path.append(current)
                        break

        self.display_path(path[::-1])

    def grassfire(self):
        self.apply_grassfire()
        self.trace_path()
