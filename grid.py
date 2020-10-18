from PIL import Image, ImageDraw

class Grid():

    def __init__(self, rows, cols, robot=[0, 0], goal=None, cell_size=25):

        self.robot = robot
        if goal is not None:
            self.goal = goal
        else:
            self.goal = [rows - 1, cols - 1]

        self.cell_size = cell_size

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
                print(self.values[r][c], end='')
                if c < len(self.values[r]) - 1:
                    print(', ', end='')
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

    def get_color(self, row, col):
        value = self.values[row][col]

        if value == "O":
            return 'white'
        elif value == 'R':
            return 'red'
        elif value == 'G':
            return 'green'
        elif value == 'X':
            return 'black'

        return 'pink'

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

g = Grid(5, 5)
g.set_robot(3, 3)
g.set_goal(0,0)
g.mark_obstacles([ [1,1], [1,2], [1,3], [2,1], [3,1] ])
g.print()

im = g.draw()
im.show()