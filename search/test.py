from grid import Grid, open_grid, GridGIFMaker, generate_grid
from breadth_first_search import BFS
from depth_first_search import DFS
from a_star import AStar

random_grid = generate_grid(25, 25)
random_grid.print()
bfs_g = random_grid

bfs_g.write_grid("test.grid")

dfs_g = open_grid("test.grid")
astar_g = open_grid("test.grid")

bfs = BFS(bfs_g)
giffer = GridGIFMaker(bfs_g)
path = None
x = 0
while path == None:
    print(f"Step {x}")
    giffer.add_frame()
    x +=1
    path = bfs.step()

print("Path found", path)
giffer.add_frame()
giffer.write_gif("out/bfs.gif", duration = 50, path_frame_count = 20)

dfs = DFS(dfs_g)
giffer = GridGIFMaker(dfs_g)
path = None
x = 0
while path == None:
    print(f"Step {x}")
    giffer.add_frame()
    x +=1
    path = dfs.step()

print("Path found", path)
giffer.add_frame()
giffer.write_gif("out/dfs.gif", duration = 50, path_frame_count = 20)

astar_g.show_values = True
astar = AStar(astar_g)
giffer = GridGIFMaker(astar_g)
path = None
x = 0
while path == None:
    print(f"Step {x}")
    giffer.add_frame()
    x +=1
    path = astar.step()

print("Path found", path)
giffer.add_frame()
giffer.write_gif("out/astar.gif", duration = 50, path_frame_count = 20)
