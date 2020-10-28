# AI Playground
Playground repos while playing with AI algorithms


## Search Algorithms

Search algorithms can be found in the `search` folder. Within, you'll find these files:

* `test.py` - will generate a random map and attempt to traverse it with each of the available algorithms. IF the map generated can't be solved, it'll error out.
- `searcher.py` - A generic `Searcher` class that sets up and manages basics a searcher would need. Expects children to implement a `step` function which expans the robot's consideration of a path by one "step" in its search algorithm.
- `grid.py` - a `Grid` class with internal functions that provide utility functions that include:
    - The ability to read and write grids to a text file with any CSV support (default is space delimited). This means a simple spreadsheet app can be used to easily generate maps.
    - The ability to draw the map out to an image
    - Controlled moving of a "robot" around the map, neighbor finding, obstacle awareness, goal awareness, etc.

    Within the `grid.py` file there is also a `GridGIFMaker` class which accepts a grid and can generate a gif of a given `Searcher` class. There is also a `grid_generator` that makes random `Grid` objects.
- `breadth_first_search.py` - implements a `BFS` breadth first search `Searcher`
- `depth_first_search.py` - implements a `DFS` depth first search `Searcher` 
- `a_star.py` - this implements an A* searcher that uses simple euclidean distance for its cost function.

### Search Examples

#### Breadth First Search
![Breadth First Search](search/example_gifs/bfs.gif)

#### Depth First Search
![Depth First Search](search/example_gifs/dfs.gif)

#### A* Search
![A* Search](search/example_gifs/astar.gif)

## Min Max

To experiment with the `min max` algorithm I coded up a **Connect 4** game. The files of note here are:

- `connect_four_board.py` - this is similar to `grid.py` before - it implements the connect four board of any given size, handles placing a piece (and having it "fall" to the correct place), has built in checks to determine a winner, and image drawing/gif writing capabilities.
- `play_connect_four.py` - is a file that will have an in-terminal game of connect four against a bot as specified in the code.
- `random_connect_four.py` - as a quick test and comparison bot, this bot literally just picks a random legal move each turn
- `min_max_connect_four.py` - implements a minmax bot that plays connect four. It has a specifiable depth (defaults to 4) for how many turns ahead it must view.
- `random_vs_minmax_connect_four.py` - pits the minmax bot against the random bot for 100 matches of Connect 4

### Example GIFs

#### Random (Red) vs Minmax (Blue) - 100 Games

*minmax bot won 99 of 100 games against the random bot*

![random bot vs minmax bot](search/example_gifs/random_vs_minmax.gif)
