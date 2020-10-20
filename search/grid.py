from PIL import Image, ImageDraw
import csv

class Grid():

    def __init__(self, rows, cols, robot=[0, 0], goal=None, cell_size=25, map_legend=None):
        if rows is None:
            rows = 5
        if cols is None:
            cols = 5

        self.robot = robot
        if goal is not None:
            self.goal = goal
        else:
            self.goal = [rows - 1, cols - 1]

        self.cell_size = cell_size

        self.map_legend = map_legend
        if map_legend is None:
            self.map_legend = {
                'R': 'red',     # Robot
                'G': 'green',   # Goal
                'O' : 'white',  # Open
                'X': 'black'    # Obstacle
            }

        self.rows = rows
        self.cols = cols
        self.values = [None] * self.rows
        for r in range(0, self.rows):
            self.values[r] = [None] * self.cols
            for c in range(0, self.cols):
                self.values[r][c] = "O"

        self.set_robot(robot[0], robot[1])
        self.set_goal(self.goal[0], self.goal[1])

    def print(self):
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                print(self.values[r][c], end=' ')
            print()

    def set_robot(self, row, col):
        self.values[self.robot[0]][self.robot[1]] = 'O'
        self.robot = [row, col]
        self.values[row][col] = 'R'

    def mark_obstacle(self, row, col):
        self.values[row][col] = "X"

    def mark_obstacles(self, obstacles):
        for obstacle in obstacles:
            self.mark_obstacle(obstacle[0], obstacle[1])

    def set_goal(self, rows, cols):
        self.values[self.goal[0]][self.goal[1]] = 'O'
        self.goals = [rows, cols]
        self.values[rows][cols] = 'G'

    def get_value(self, row, col):
        return self.values[row][col]

    def set_value(self, row, col, value):
        self.values[row][col] = value

    def get_neighbors(self, row, col):
        neighbors = []
        #rm, cm (row move, column move) - if you can, make the change in that direction
        for rm in [-1, 1]:
            rc = row + rm # row current
            if rc < 0 or rc >= self.rows:
                continue

            child_value = self.values[rc][col]
            if child_value == 'X':
                continue
                
            neighbors.append((rc, col))

        for cm in [-1, 1]:
            cc = col + cm # column current
            if cc < 0 or cc >= self.cols:
                continue

            child_value = self.values[row][cc]
            if child_value == 'X':
                continue
                
            neighbors.append((row, cc))
                
        return neighbors

    def add_color(self, value : str, color : str):
        self.map_legend[value] = color

    def get_color(self, row, col):
        value = self.values[row][col]
        return self.map_legend[value]

    def draw(self):
        width = self.rows * self.cell_size
        height = self.cols * self.cell_size
        
        im = Image.new(mode="RGB", size=(width, height))
        draw = ImageDraw.Draw(im)

        for r in range(0, self.rows):
            for c in range(0, self.cols):
                upper_left = (r * self.cell_size, c * self.cell_size)
                bottom_right = (upper_left[0] + self.cell_size, upper_left[1] + self.cell_size)
                draw.rectangle([upper_left, bottom_right], fill = self.get_color(r, c))

        return im

    def save_im(self, path : str):
        im = self.draw()
        im.save(path)

    def write_grid(self, path : str, delimiter : str = ' '):
        with open(path, 'w', newline='') as gridfile:
            gridwriter = csv.writer(gridfile, delimiter=delimiter, quoting=csv.QUOTE_NONE)
            for row in self.values:
                gridwriter.writerow(row)

class GridGIFMaker():

    def __init__(self, grid : Grid):
        self.grid : Grid = grid
        self.frames = []
        self.add_frame()

    def add_frame(self):
        self.frames.append(self.grid.draw())

    def write_gif(self, path : str, duration : int = 500, loop : int = 1):
        self.frames[0].save(path, save_all=True, append_images=self.frames[1:], duration=duration, loop=loop)

def open_grid(path: str, delimiter : str = ' '):
    with open(path, newline='') as gridfile:
        gridreader = csv.reader(gridfile, delimiter=delimiter, quoting=csv.QUOTE_NONE)
        read = []
        goal = (0, 0)
        robot = (0, 0)
        for r_index, row in enumerate(gridreader):
            for c_index, cell in enumerate(row):
                if cell == 'R':
                    robot = (r_index, c_index)
                elif cell == 'G':
                    goal = (r_index, c_index)
            read.append(row)


        grid = Grid(len(read), len(read[0]))
        grid.values = read
        grid.robot = robot
        grid.goal = goal

        return grid