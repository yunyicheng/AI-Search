# AI-Sokoban-Solver
This is a course project from CSC384: Intro to AI at University of Toronto. In this project, I implemented an AI Sokoban solver which utilizes search strategies such as heurustic search, weighted A*, greedy best-first search. More details are available in project handout.

## Mark Breakdown for Assignment 1
Overall: 80.0/100
### Test Case: [function=test_fval_function]	[5.0/5]
### Test Case: [function=test_heuristic]	[17/25]
- Best First Search, with manhattan distance, solved 18/40 problems.
- Best First Search, with an alternate heuristic, solved 32/40 problems.
- Best First Search, with the student heuristic, solved 27/40 problems.
- The student outperformed the 'better' benchmark 18 times.
- Score for alternate heuristic portion: 17/25.
### Test Case: [function=test_iterative_gbfs]	[17/25]
- WARNING: Anytime solutions were outperformed by best first search.
- Anytime gbfs, with the student heuristic, solved 27/40 problems.
- Anytime gbfs, with manhattan distance, solved 18/40 problems.
- Anytime gbfs, with an alternate heuristic, solved 32/40 problems.
- The student outperformed the 'better' benchmark 23 times.
- Score for anytime_gbfs tests: 17/25.
### Test Case: [function=test_iterative_weighted_astar]	[21/25]
- Iterative Weighted astar, with the student heuristic, solved 26/40 problems.
- Iterative Weighted astar, with an alternate heuristic, solved 23/40 problems.
- The student outperformed the 'better' benchmark 21 times.
- Margin over benchmark: 3 problems.
- Iterative Weighted astar, with manhattan distance, solved 19/40.
- Score for this portion of the assignment: 21/25.
### Test Case: [function=test_manhattan]	[10/10]

### Test Case: [function=test_weighted_astar]	[10/10]
- Weighted a-star expanded more nodes as weights decreased 5 of 5 times
Of the 20 runs over 5 problems, 3 solutions were found with weighted a star in the time allotted.
- Score is 10 of 10.
