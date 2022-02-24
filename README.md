# AI-Sokoban-Solver
This is a course project from CSC384: Intro to AI at University of Toronto. In this project, I implemented an AI Sokoban solver which utilizes search strategies such as heurustic search, weighted A*, greedy best-first search.

## Introduction
The goal of this assignment will be to implement a working solver for the puzzle game Sokoban. Sokoban is a puzzle game in which a warehouse robot must push boxes into storage spaces. The rules hold that only one box can be moved at a time, that boxes can only be pushed by robots and not pulled, and that neither robots nor boxes can pass through obstacles (walls or other boxes). In addition, robots cannot push more than one box, i.e., if there are two boxes in a row, they cannot push them. The game is over when all the boxes are in their storage spots.

<img width="802" alt="Screen Shot 2022-02-23 at 11 08 17 PM" src="https://user-images.githubusercontent.com/55462866/155456351-a8bb32f3-4d8d-4391-b13c-a7fca7af889c.png">

In our version of Sokoban the rules are slightly more complicated, as there may be more than one warehouse robot available to push boxes. These robots cannot pass through one another nor can they move simultaneously, however.

Sokoban can be played online at https://www.sokobanonline.com/play. We recommend that you familiarize yourself with the rules and objective of the game before proceeding. It is worth noting that the version that is presented online is only an example. We will give a formal description of the puzzle in the next section.

## Description of Sokoban
Sokoban has the following formal description. Note that our version differs from the standard one. Read the description carefully.

- The puzzle is played on a board that is a grid board with N squares in the x-dimension and M squares in the y-dimension.
- Each state contains the x and y coordinates for each robot, the boxes, the storage spots, and the obstacles.
-  From each state, each robot can move North, South, East, or West. No two robots can move simultaneously, however. If a robot moves to the location of a box, the box will move one square in the same direction. Boxes and robots cannot pass through walls or obstacles, however. Robots cannot push more than one box at a time; if two boxes are in succession the robot will not be able to move them. Movements that cause a box to move more than one unit of the grid are also illegal. Whether or not a robot is pushing an object does not change the cost.
-  Each movement is of equal cost. Whether or not the robot is pushing an object does not change the cost.
- The goal is achieved when each box is located in a storage area on the grid.

Ideally, we will want our robots to organize everything before the supervisor arrives. This means that with each problem instance, you will be given a computation time constraint. You must attempt to provide some legal solution to the problem (i.e., a plan) within this constraint. Better plans will be plans that are shorter, i.e. that require fewer operators to complete.

## Files
### `search.py`
This files provides a generic search engine framework and code to perform several different search routines. A brief description of the functionality of search.py follows. The code itself is documented and worth reading.

An object of class `StateSpace` represents a node in the state space of a generic search problem. The base class defines a fixed interface that is used by the SearchEngine class to perform search in that state space.

For the Sokoban problem, we will define a concrete sub-class that inherits from `StateSpace`. This concrete sub-class will inherit some of the “utility” methods that are implemented in the base class.

Each `StateSpace` object s has the following key attributes:

– `s.gval`: the g value of that node, i.e., the total cost of getting to that state (from the initial state).

– `s.parent`: the parent StateSpace object of s, i.e., the StateSpace object that has s as a successor. This will be None if s is the initial state.

– `s.action`: a string that contains that name of the action that was applied to s.parent to generate s. Will be “START” if s is the initial state.

An object of class SearchEngine se runs the search procedure. A `SearchEngine` object is initialized with a search strategy (‘depth first’, ‘breadth first’, ‘best first’, ‘a star’, or ‘custom’) and a cycle checking level (‘none’, ‘path’, or ‘full’). 

Note that `SearchEngine` depends on two auxiliary classes:
– An object of class `sNode` sn which represents a node in the search space. Each object sn contains a `StateSpace` object and additional details: hval, i.e., the heuristic function value of that state and gval, i.e. the cost to arrive at that node from the initial state. An fval fn and weight are tied to search nodes during the execution of a search, where applicable.
– An object of class `Open` is used to represent the search frontier. The search frontier will be organized in the way that is appropriate for a given search strategy.

When a `SearchEngine`’s search strategy is set to ‘custom’, you will have to specify the way that f values of nodes are calculated; these values will structure the order of the nodes that are expanded during your search.

Once a `SearchEngine` object has been instantiated, you can set up a specific search with: `init_search(initial state,goal fn,heuristic fn, fval fn)` and execute that search with `search(timebound,costbound)`. The arguments are as follows:

– `initial_state` will be an object of type `StateSpace`; it is your start state.

– `goal_fn(s)` is a function which returns True if a given state s is a goal state and False otherwise.

– `heuristic_fn(s)` is a function that returns a heuristic value for state s. This function will only be used if your search engine has been instantiated to be a heuristic search (e.g., best first).

– `fval_fn(sNode,weight)` defines f values for states. This function will only be used by your search engine if it has been instantiated to execute a ‘custom’ search. Note that this function takes in an sNode and that an sNode contains not only a state but additional measures of the state (e.g., a gval). The function also takes in a float weight. It will use the variables that are provided to arrive at an f value calculation for the state contained in the sNode.

– `timebound` is a bound on the amount of time your code will execute the search. Once the run time exceeds the time bound, the search will stop; if no solution has been found, the search will return False.

– `costbound` is an optional parameter that is used to set boundaries on the cost of nodes that are explored. This costbound is defined as a list of three values. costbound[0] is used to prune states based on their g-values; any state with a g-value higher than costbound[0] will not be expanded. costbound[1] is used to prune states based on their h-values; any state with an hvalue higher than costbound[1] will not be expanded. Finally, costbound[2] is used to prune states based on their f-values; any state with an f-value higher than costbound[2] will not be expanded.

The output of the search function will include both a solution path as well as a SearchStats object (if a solution is found). A `SearchStats` object (`ss`) details some interesting statistics that are related to a given search. Its attributes are as follows:

- `ss.states_expanded`, which is a count of the number of states drawn from the Frontier during a search.

- `ss.states_generated`, which is a count of the number of states generated by the successor function during a search.

- `ss.states_pruned_cycles`, which is a count of the number of states pruned as a result of cycle checking.

- `ss.states_pruned_cost`, which is a count of the number of states pruned as a result of enforcing cost boundaries during a search.

### `sokoban.py`
The file sokoban.py contains:

An object of class `SokobanState,` which is a `StateSpace` with these additional key attributes:

– `s.width`: the width of the Sokoban board

– `s.height`: the height of the Sokoban board

– `s.robots`: positions for each robot that is on the board. Each robot position is a tuple (x,y), that denotes the robot’s x and y position.

– `s.boxes`: positions for each box as keys of a dictionary. Each position is an (x,y) tuple. The value of each key in the index for that box’s restrictions (see below).

– `s.storage`: positions for each storage bin that is on the board (also (x,y) tuples).

– `s.obstacles`: locations of all of the obstacles (i.e. walls) on the board. Obstacles, like robots and boxes, are also tuples of (x,y) coordinates.

SokobanState also contains the following key functions:

– `successors()`: This function generates a list of SokobanStates that are successors to a given SokobanState. Each state will be annotated by the action that was used to arrive at the SokobanState. These actions are (r,d) tuples wherein r denotes the index of the robot that moved d denotes the direction of movement of the robot.
– hashable state(): This is a function that calculates a unique index to represents a particular SokobanState. It is used to facilitate path and cycle checking.

– `print_state()`: This function prints a SokobanState to stdout.

Note that SokobanState depends on one auxiliary class:

– An object of class `Direction`, which is used to define the directions that the robot can move and the effect of this movement.

Also note that sokoban.py contains a set of 20 initial states for Sokoban problems, which are stored in the tuple PROBLEMS. You can use these states to test your implementations.

### `solution.py`
The file solution.py contains the key methods for implementation.

### `autograder.py`
The file autograder.py runs some tests on your code to give you an indication of how well your methods perform.


## Tasks
### Iterative Greedy Best-First Search
Greedy best-first search expands nodes with lowest h(node) first. The solution found by this algorithm may not be optimal. Iterative greedy-best first search (which is called iterative gbfs in the code) continues searching after a solution is found in order to improve solution quality. Since we have found a path to the goal after the first iteration, we can introduce a cost bound for pruning: if node has g(node) greater than the best path the goal found so far, we can prune it. The algorithm returns either when we have expanded all non-pruned nodes, in which case the best solution found by the algorithm is the optimal solution, or when it runs out of time. We prune based on the g-value of the node only because greedy best-first search is not necessarily run with an admissible heuristic.

Record the time when iterative gb fs is called with `os.times()[0]`. Each time you call search, you should update the time bound with the remaining allowed time. The automarking script will confirm that your algorithm obeys the specified time bound.

### Weighted A*
Instead of A*’s regular node-valuation formula f(node) = g(node)+h(node), Weighted A* introduces a weighted formula:

f(node) = g(node)+w∗h(node)

where g(node) is the cost of the path to node, h(node) the estimated cost of getting from node to the goal, and w ≥ 1 is a bias towards states that are closer to the goal. Theoretically, the smaller w is, the better the first solution found will be (i.e., the closer to the optimal solution it will be ... why??). However, different values of w will require different computation times.

Start by implementing Weighted A* in the function weighted astar(initial state,heur fn,weight,timebound) using the f-value function above. This will require you to instantiate a custom SearchEngine and an f-value of your own design. When you are passing in fval function to init search for this problem, you will need to have specified the weight for fval function. You can do this by wrapping the `fval_function(sN,weight)` you have written in an anonymous function, i.e., `wrapped_fval_function = (lambda sN: fval function(sN, weight))` Explore the performance of your weighted A* implementation on the test problems that have been provided using the Manhattan distance heuristic and the following weights: 10, 5, 2, 1. Which weights yield the fastest time to a solution? Which yields the least cost solution?

### Iterative Weighted A*
You have hopefully discovered that, even when using an admissible heuristic, the length of Weighted A* solutions may not be optimal when w is anything larger than 1. We can therefore keep searching after we have found a solution in order to try and find a better one. More specifically, we can continue to use Weighted A* with smaller and smaller weights, as time allows, in an effort to improve on our solution with our remaining time. This is the idea behind Iterative Weighted A*. Iterative Weighted A* continues to search for solutions until either there are no nodes left to expand (and our best solution is the optimal one) or it runs out of time. It will do this by running Weighted A* again and again, with increasingly small weights.

Since Iterative Weighted A* will have found a path to the goal after its first search iteration, we can use this solution to guide our search in subsequent iterations. More specifically, we can introduce a cost bound that will help prune nodes in future iterations: if any node we generate has a g(node)+h(node) value greater than the cost of the best path to the goal found so far, we can prune it. Implement an iterative version of weighted A* search using the following function stub: `iterative_astar(initial state,heur fn,weight,timebound)`. This should be an iterative search that makes use of your weighted A*. When a solution is found, remember it and, if time allows, iterate upon it. Change your weight at each iteration and enforce a cost boundary so that you will move toward more optimal solutions at each iteration.


## Mark Breakdown
Overall: 80.0/100
#### Test Case: [function=test_fval_function]	[5.0/5]
#### Test Case: [function=test_heuristic]	[17/25]
- Best First Search, with manhattan distance, solved 18/40 problems.
- Best First Search, with an alternate heuristic, solved 32/40 problems.
- Best First Search, with the student heuristic, solved 27/40 problems.
- The student outperformed the 'better' benchmark 18 times.
- Score for alternate heuristic portion: 17/25.
#### Test Case: [function=test_iterative_gbfs]	[17/25]
- WARNING: Anytime solutions were outperformed by best first search.
- Anytime gbfs, with the student heuristic, solved 27/40 problems.
- Anytime gbfs, with manhattan distance, solved 18/40 problems.
- Anytime gbfs, with an alternate heuristic, solved 32/40 problems.
- The student outperformed the 'better' benchmark 23 times.
- Score for anytime_gbfs tests: 17/25.
#### Test Case: [function=test_iterative_weighted_astar]	[21/25]
- Iterative Weighted astar, with the student heuristic, solved 26/40 problems.
- Iterative Weighted astar, with an alternate heuristic, solved 23/40 problems.
- The student outperformed the 'better' benchmark 21 times.
- Margin over benchmark: 3 problems.
- Iterative Weighted astar, with manhattan distance, solved 19/40.
- Score for this portion of the assignment: 21/25.
#### Test Case: [function=test_manhattan]	[10/10]
#### Test Case: [function=test_weighted_astar]	[10/10]
- Weighted a-star expanded more nodes as weights decreased 5 of 5 times
Of the 20 runs over 5 problems, 3 solutions were found with weighted a star in the time allotted.
- Score is 10 of 10.
