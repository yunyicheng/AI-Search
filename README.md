# AI-Sokoban-Solver
This is a course project from CSC384: Intro to AI at University of Toronto. In this project, I implemented an AI Sokoban solver which utilizes search strategies such as heurustic search, weighted A*, greedy best-first search.
## Introduction
The goal of this assignment will be to implement a working solver for the puzzle game Sokoban. Sokoban is a puzzle game in which a warehouse robot must push boxes into storage spaces. The rules hold that only one box can be moved at a time, that boxes can only be pushed by robots and not pulled, and that neither robots nor boxes can pass through obstacles (walls or other boxes). In addition, robots cannot push more than one box, i.e., if there are two boxes in a row, they cannot push them. The game is over when all the boxes are in their storage spots.

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

My goal is to implement an anytime algorithm for this problem, meaning that your algorithm should generate better solutions (i.e., shorter plans) the more computation time it is given.
## Tasks
### Iterative Greedy Best-First Search
Greedy best-first search expands nodes with lowest h(node) first. The solution found by this algorithm may not be optimal. Iterative greedy-best first search (which is called iterative gbfs in the code) continues searching after a solution is found in order to improve solution quality. Since we have found a path to the goal after the first iteration, we can introduce a cost bound for pruning: if node has g(node) greater than the best path the goal found so far, we can prune it. The algorithm returns either when we have expanded all non-pruned nodes, in which case the best solution found by the algorithm is the optimal solution, or when it runs out of time. We prune based on the g-value of the node only because greedy best-first search is not necessarily run with an admissible heuristic.

Record the time when iterative gb fs is called with os.times()[0]. Each time you call search, you should update the time bound with the remaining allowed time. The automarking script will confirm that your algorithm obeys the specified time bound.
### Weighted A*
Instead of A*’s regular node-valuation formula f(node) = g(node)+h(node), Weighted A* introduces a weighted formula:

f(node) = g(node)+w∗h(node)

where g(node) is the cost of the path to node, h(node) the estimated cost of getting from node to the goal, and w ≥ 1 is a bias towards states that are closer to the goal. Theoretically, the smaller w is, the better the first solution found will be (i.e., the closer to the optimal solution it will be ... why??). However, different values of w will require different computation times.

Start by implementing Weighted A* in the function weighted astar(initial state,heur fn,weight,timebound) using the f-value function above. This will require you to instantiate a custom SearchEngine and an f-value of your own design. When you are passing in fval function to init search for this problem, you will need to have specified the weight for fval function. You can do this by wrapping the fval function(sN,weight) you have written in an anonymous function, i.e., wrapped fval function = (lambda sN: fval function(sN, weight)) Explore the performance of your weighted A* implementation on the test problems that have been provided using the Manhattan distance heuristic and the following weights: 10, 5, 2, 1. Which weights yield the fastest time to a solution? Which yields the least cost solution?

### Iterative Weighted A*
You have hopefully discovered that, even when using an admissible heuristic, the length of Weighted A* solutions may not be optimal when w is anything larger than 1. We can therefore keep searching after we have found a solution in order to try and find a better one. More specifically, we can continue to use Weighted A* with smaller and smaller weights, as time allows, in an effort to improve on our solution with our remaining time. This is the idea behind Iterative Weighted A*. Iterative Weighted A* continues to search for solutions until either there are no nodes left to expand (and our best solution is the optimal one) or it runs out of time. It will do this by running Weighted A* again and again, with increasingly small weights.

Since Iterative Weighted A* will have found a path to the goal after its first search iteration, we can use this solution to guide our search in subsequent iterations. More specifically, we can introduce a cost bound that will help prune nodes in future iterations: if any node we generate has a g(node)+h(node) value greater than the cost of the best path to the goal found so far, we can prune it. Implement an iterative version of weighted A* search using the following function stub:

iterative astar(initial state,heur fn,weight,timebound). This should be an iterative search that makes use of your weighted A*. When a solution is found, remember it and, if time allows, iterate upon it. Change your weight at each iteration and enforce a cost boundary so that you will move toward more optimal solutions at each iteration.
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
