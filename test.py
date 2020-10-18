from grid import Grid

g = Grid(5, 5)
g.set_robot(3, 3)
g.set_goal(0,0)
g.mark_obstacles([ [1,1], [1,2], [1,3], [2,1], [3,1] ])
g.print()

im = g.draw()
im.show()