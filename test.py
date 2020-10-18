from grid import Grid
from bfs_robot import BFS_Robot

g = Grid(5, 5)
g.set_robot(3, 3)
g.set_goal(0,0)
g.mark_obstacles([ [1,1], [1,2], [1,3], [2,1], [3,1] ])
g.print()

bfs = BFS_Robot(g)
path = None
x = 0
while path == None:
    print(f"Step {x}")
    bfs.grid.save_im(f"out/{x}.jpg")
    x +=1
    path = bfs.step()

print("Path found", path)

bfs.grid.save_im(f"out/{x}.jpg")