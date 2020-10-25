from PIL import Image, ImageDraw

class Connect4Board():

    def __init__(self, rows, cols, cell_size = 25):
        self.rows = rows
        self.cols = cols

        self.values = [None] * self.rows
        for r in range(0, self.rows):
            self.values[r] = [None] * self.cols
            for c in range(0, self.cols):
                self.values[r][c] = 'O'

        self.color_legend = {
            '1': 'red',
            '2': 'blue',
            'O': 'white'
        }
        self.images = []
        self.cell_size = cell_size

    def print(self):
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                print(self.values[r][c], end=' ')
            print()

    def move(self, player : str, location : int):
        if location not in self.possible_moves():
            raise Exception("Illegal move - column is filled")
        for r in range(self.rows - 1, -1, -1):
            if self.values[r][location] == 'O':
                self.values[r][location] = player
                return
        # I don't think it's possible to reach this,
        # but just in case...
        raise Exception("Illegal move - column is filled")

    # possible_moves returns all columns that are not completely full
    def possible_moves(self):
        legal_moves = []
        for c in range(0, self.cols):
            if self.values[0][c] == 'O':
                legal_moves.append(c)

        return legal_moves

    def winner(self):
        # No moves, no winner?
        if len(self.possible_moves()) == 0:
            return 'Draw'

        # Horizontal Case
        # needs at least 4 cols to do
        if self.cols >= 4:
            for r in range(0, self.rows):
                stack = []
                for value in self.values[r]:
                    if value == 'O':
                        stack = []
                    elif len(stack) == 0 or stack[0] != value:
                        stack = [value]
                    elif stack[0] == value:
                        stack.append(value)
                    if len(stack) >= 4:
                        return value
        
        # Vertical Case
        # needs at least 4 tall in rows to do
        if self.rows >= 4:
            for c in range(0, self.cols):
                for r in range(0, self.rows):
                    value = self.values[r][c]
                    if value == 'O':
                        stack = []
                    elif len(stack) == 0 or stack[0] != value:
                        stack = [value]
                    elif stack[0] == value:
                        stack.append(value)
                    if len(stack) >= 4:
                        return value

        # if the map is not tall and wide enough, we just skip diagonal checking
        if self.rows < 4 or self.cols < 4:
            return None

        # Diagonal - checking from top left to bottom right
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                value = self.values[r][c]
                stack = []
                if value != 'O':
                    stack.append(value)
                for change in range(1, max(self.rows, self.cols)):
                    if r + change >= self.rows or c + change >= self.cols:
                        break
                    value = self.values[r+change][c+change]
                    if value == 'O':
                        stack = []
                    elif len(stack) == 0 or stack[0] != value:
                        stack = [value]
                    elif stack[0] == value:
                        stack.append(value)
                    if len(stack) >= 4:
                        return value
        # Diagonal - checking from top right to bottom left
        for r in range(0, self.rows):
            for c in range(0, self.cols):
                value = self.values[r][c]
                stack = []
                if value != 'O':
                    stack.append(value)
                for change in range(1, max(self.rows, self.cols)):
                    if r + change >= self.rows or c - change < 0:
                        break
                    value = self.values[r+change][c-change]
                    if value == 'O':
                        stack = []
                    elif len(stack) == 0 or stack[0] != value:
                        stack = [value]
                    elif stack[0] == value:
                        stack.append(value)
                    if len(stack) >= 4:
                        return value
            
        return None

    def draw(self):
        width = self.rows * self.cell_size
        height = self.cols * self.cell_size

        im = Image.new(mode="RGB", size=(width, height))
        draw = ImageDraw.Draw(im)

        for r in range(0, self.rows):
            for c in range(0, self.cols):
                upper_left = (c * self.cell_size, r * self.cell_size)
                bottom_right = (upper_left[0] + self.cell_size, upper_left[1] + self.cell_size)
                print(r, c, upper_left, bottom_right)
                draw.rectangle([upper_left, bottom_right], fill = self.color_legend[self.values[r][c]])

        return im

    def store_im(self):
        self.images.append(self.draw())

    def write_gif(self, path : str, duration : int = 100, loop : int = 0, end_frame_count = 5):
        frames = self.frames[1:]
        if path_frame_count > 1:
            for i in range(1, end_frame_count):
                frames.append(frames[-1])
        self.images[0].save(path, save_all=True, append_images=frames, duration=duration, loop=loop)