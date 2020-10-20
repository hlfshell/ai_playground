from grid import Grid, open_grid
from bfs_robot import BFS_Robot
from dfs_robot import DFS_Robot

g = Grid(5, 5)
g.set_robot(3, 3)
g.set_goal(0,0)
g.mark_obstacles([ [1,1], [1,2], [1,3], [2,1], [3,1], [1,4] ])
g.print()

g.write_grid("test.grid")

print()

g2 = open_grid("test.grid")
g2.print()

bfs = BFS_Robot(g)
path = None
x = 0
while path == None:
    print(f"Step {x}")
    bfs.grid.save_im(f"out/bfs_{x}.jpg")
    x +=1
    path = bfs.step()

print("Path found", path)

bfs.grid.save_im(f"out/bfs_{x}.jpg")

dfs = DFS_Robot(g2)
path = None
x = 0
while path == None:
    print(f"Step {x}")
    dfs.grid.save_im(f"out/dfs_{x}.jpg")
    x +=1
    path = dfs.step()

print("Path found", path)

dfs.grid.save_im(f"out/dfs_{x}.jpg")