from grid import Grid

class DFS_Robot():

    def __init__(self, grid : Grid):
        self.grid : Grid = grid

        # Add in the "current" and "past" children colors
        self.grid.add_color('V', 'grey')   # Visited
        self.grid.add_color('C', 'blue')   # Considering
        self.grid.add_color('P', 'purple') # Path 

        self.current_position = self.grid.robot
        self.goal = self.grid.goal

        # Set the root node as the first enqueued node
        self.lifo = []
        self.lifo.append(self.current_position)

        self.parents = {}

    def step(self):
        # if the queue is empty, there is no path
        if len(self.lifo) == 0:
            raise Exception("No path to the goal exists")

        # Get the current position to consider moving forward
        current = self.lifo.pop()
        current_value = self.grid.get_value(current[0], current[1])

        # If this is the goal, generate your path:
        if current_value == 'G':
            path = [current]
            while True:
                # If the cell is not the goal or the robot, paint hte path
                if current_value != 'G' and current_value != 'R':
                    self.grid.set_value(current[0], current[1], 'P')
                
                # Set the 'current' to the parent cell
                current = self.parents[current]
                current_value = self.grid.get_value(current[0], current[1])
                path.append(current)

                # If we've reached the robot, escape!
                if current_value == 'R':
                    return path

        # Mark the current node as currently being visited
        if current_value != 'R':
            self.grid.set_value(current[0], current[1], 'V')

        # Get each neighbor and queue them into our LIFO.
        # This way we'll continually queue up children into
        # the LIFO queue and pull depth-wise first.
        neighbors = self.grid.get_neighbors(current[0], current[1])
        for neighbor in neighbors:
            value = self.grid.get_value(neighbor[0], neighbor[1])
            if value in ['X', 'C', 'V', 'R']:
                continue

            if value != 'G':
                self.grid.set_value(neighbor[0], neighbor[1], 'C')
            if neighbor not in self.parents:
                self.parents[neighbor] = current
            self.lifo.append(neighbor)

        return