from PIL import Image, ImageDraw, ImageFont
import csv
from random import random, randint
import colorsys

class Grid():

    def __init__(self, rows, cols, robot=[0, 0], goal=None, cell_size=25, map_legend=None, show_values=False, value_range=None):
        if rows is None:
            rows = 5
        if cols is None:
            cols = 5

        if value_range is None:
            self.value_range = (0, rows * 3 if rows > cols else cols * 3)
        else:
            self.value_range = value_range

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

        self.show_values = show_values

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
        self.goal = [rows, cols]
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
        if isinstance(value, int):
            return self.value_to_color(value)
        else:
            return self.map_legend[value]

    # value_to_color maps the high/low to green (close) and red(far)
    # by utilizing HLS and then converts to RGB
    def value_to_color(self, value : int):
        # (x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min;
        mapped_value = (value - self.value_range[1]) * (120 - 0) / (self.value_range[0] - self.value_range[1]) + 0
        conversion = colorsys.hls_to_rgb(mapped_value / 360, 0.5, 1.0)
        return (int(conversion[0] * 255), int(conversion[1] * 255), int(conversion[2] * 255))


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
                if self.show_values:
                    value = self.get_value(r, c)
                    if value not in ['O', 'X', 'P']:
                        font = ImageFont.load_default()
                        x = int(upper_left[0] + (self.cell_size * .3))
                        y = int(bottom_right[1] - (self.cell_size * .66))
                        draw.text((x,y), str(value), font=font)

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

    def write_gif(self, path : str, duration : int = 100, loop : int = 0, path_frame_count = 5):
        frames = self.frames[1:]
        if path_frame_count > 1:
            for i in range(1, path_frame_count):
                frames.append(frames[-1])
        self.frames[0].save(path, save_all=True, append_images=frames, duration=duration, loop=loop)

def generate_grid(rows : int = 10, cols : int = 10, obstacle_chance : float = 0.3):
    grid = Grid(rows, cols)
    robot = (randint(0, rows - 1), randint(0, cols - 1))
    goal = robot
    while goal == robot:
        goal = (randint(0, rows - 1), randint(0, cols - 1))

    grid.set_robot(robot[0], robot[1])
    grid.set_goal(goal[0], goal[1])
    
    for r in range(0, rows):
        for c in range(0, cols):
            value = grid.get_value(r, c)
            if value != 'C' and value != 'R':
                # Check to see if we randomly generate an obstacle
                if random() <= obstacle_chance:
                    grid.set_value(r, c, 'X')

    return grid

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
