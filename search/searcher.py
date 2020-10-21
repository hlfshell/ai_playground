from grid import Grid

class Searcher():

    def __init__ (self, grid):
        self.grid : Grid = grid

        # Add in the "current" and "past" children colors
        self.grid.add_color('V', 'grey')   # Visited
        self.grid.add_color('C', 'blue')   # Considering
        self.grid.add_color('P', 'purple') # Path 

        self.current_position = self.grid.robot
        self.goal = self.grid.goal

    def step(self):
        raise Exception("Class does not implement a search algorithm")

    def search(self, gif_path : str = None):
        if gif_path is not None:
            giffer = GridGIFMaker(self.grid)
        
        path = None
        while path == None:
            if gif_path is not None:
                giffer.add_frame()
            path = self.step()

        if gif_path is not None:
            giffer.add_frame()
            giffer.write_gif(gif_path)

        return path