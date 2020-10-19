from grid import Grid

class BFS_Robot():

    def __init__(self, grid):
        self.grid : Grid
        self.grid = grid

        # Add in the "current" and "past" children colors
        self.grid.add_color('V', 'grey')   # Visited
        self.grid.add_color('C', 'blue')   # Considering
        self.grid.add_color('P', 'purple') # Path 

        self.current_position = self.grid.robot
        self.goal = self.grid.goal

        # Set the root node as the first enqueued node
        self.fifo = []
        self.fifo.append(self.current_position)

        self.parents = {}
        
    def step(self):
        # If the queue is empty, there is no path :-(
        if len(self.fifo) == 0:
            raise Exception("No path to the goal exists")

        # Get the current to-consider position from the fifo queue
        current = self.fifo.pop(0)
        current_value = self.grid.get_value(current[0], current[1])

        # Is this the goal? If so, generate the path!
        if current_value == 'G':
            path = [current]
            while True:
                # If the cell is not the goal or robot, paint the path
                if current_value != 'G' and current_value != 'R':
                    self.grid.set_value(current[0], current[1], 'P')

                # Set the "current" to the parent cell
                current = self.parents[current]
                current_value = self.grid.get_value(current[0], current[1])
                path.append(current)

                # If we've reached the robot, escpae!
                if current_value == 'R':
                    return path


        # Mark that node as currently visited
        if current_value != 'R':
            self.grid.set_value(current[0], current[1], 'V')

        # Get each neighbor and queue them. Mark them as potential.
        # Ignore obstacles and pre-visited (C or V) places to
        # prevent backtracking
        # For each of these nodes, mark the current node
        # as the parent.
        neighbors = self.grid.get_neighbors(current[0], current[1])
        for neighbor in neighbors:
            value = self.grid.get_value(neighbor[0], neighbor[1])
            if value in ['X', 'C', 'V', 'R']:
                continue

            if value != 'G':
                self.grid.set_value(neighbor[0], neighbor[1], 'C')
            if neighbor not in self.parents:
                self.parents[neighbor] = current
            self.fifo.append(neighbor)

        # At this point we return nothing, as we have no path built
        return