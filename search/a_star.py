from searcher import Searcher
from grid import Grid
from math import sqrt

class OrderedQueue():

    def __init__(self):
        self._values = []

    def __len__(self):
        return len(self._values)

    def append(self, item, value):
        try:
            self._values.remove((item, value))
        except:
            pass
        self._values.append((item, value))
        self._values.sort(key=lambda x: x[1], reverse=False)

    def pop(self):
        if len(self._values) == 0:
            return None
        value = self._values.pop(0)
        return value[0], value[1]

class AStar(Searcher):

    def __init__(self, grid : Grid):
        super().__init__(grid)

        self.queue = OrderedQueue()

        self.parents = {}
        
        self.queue.append(self.current_position, 0)

    # cost takes the base_cost (squares traveled) and then adds in
    # the estimated distance to the goal from the position
    def cost(self, location, base_cost):
        g_x, g_y = self.grid.goal
        x, y = location
        h_n = sqrt((g_x - x)**2 + (g_y - y)**2)
        return h_n

    def step(self):
        # If the queue is empty, there is no path
        if len(self.queue) == 0:
            raise Exception("Not path to the goal")

        current, cost = self.queue.pop()
        current_value = self.grid.get_value(current[0], current[1])

        # If we reached the goal, we're done. Build the path
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

        # current_cost is current_value with R being 0
        if current_value is 'R':
            current_cost = 0
        else:
            current_cost = current_value

        # Get each neighbor to this node and check their cost.
        # If they have a lower cost already associated we ignore the
        # neighbor. If the cost assigned is higher, we queue
        # the child and set the new parent to the current
        neighbors = self.grid.get_neighbors(current[0], current[1])
        for neighbor in neighbors:
            value = self.grid.get_value(neighbor[0], neighbor[1])
            if value in ['X', 'C', 'V', 'R']:
                continue

            # Since the goal is our target, if a neighbor is goal
            # we are just going to set that as the guaranteed next to
            # be processed and return here - we're almost done
            if value is 'G':
                self.queue.append(neighbor, -1)
                self.parents[neighbor] = current
                return

            # The cost to move to the next square is our
            # current_cost + 1. If the current_cost +1 is
            # equal to or more than the value already there
            if value is not 'O' and value < current_cost + 1:
                continue

            # estimated_cost is calculated by the cost function
            self.queue.append(neighbor, self.cost(neighbor, current_cost+1))
            self.grid.set_value(neighbor[0], neighbor[1], current_cost+1)
            self.parents[neighbor] = current

        # We've added whatever children we could with updated
        # costs - return for now
        return