#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
import math  # for infinity
import heapq
from typing import List, Any

from search import *  # for search engines
from sokoban import SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems

def sokoban_goal_state(state):
    """
    @return: Whether all boxes are stored.
    """
    for box in state.boxes:
        if box not in state.storage:
            return False
    return True


def heur_manhattan_distance(state):
    # IMPLEMENT
    """admissible sokoban puzzle heuristic: manhattan distance"""
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it
    # is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.
    total_m_dist = 0
    for box in state.boxes:
        if box not in state.storage:
            m_dist = math.inf
            for storage in state.storage:
                dist = (abs(box[0] - storage[0])) + (abs(box[1] - storage[1]))
                if dist <= m_dist:
                    m_dist = dist
            total_m_dist += m_dist
    return total_m_dist


# SOKOBAN HEURISTICS
def trivial_heuristic(state):
    """trivial admissible sokoban heuristic"""
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state 
    (# of moves required to get) to the goal.'''
    count = 0
    for box in state.boxes:
        if box not in state.storage:
            count += 1
    return count


def dead_corner(state, box):
    """Check for dead corners"""

    # 1. check for map corners
    (x, y) = box
    if (x == 0 or x == state.width - 1) and (y == 0 or y == state.height - 1):
        return True

    # 2. check for corners made up with obstacles and other boxes
    pos_u = (x, y + 1)
    pos_d = (x, y - 1)
    pos_l = (x - 1, y)
    pos_r = (x + 1, y)
    # curr_obstacles is state.obstacles and other boxes
    curr_obstacles = []
    for obs in state.obstacles:
        curr_obstacles.append(obs)
    for other_box in state.boxes:
        if other_box != box:
            curr_obstacles.append(box)
    # 2.1 box in leftmost or rightmost column locked by curr_obstacles
    if (x == 0 or x == state.width - 1) and ((pos_u in curr_obstacles) or (pos_d in curr_obstacles)):
        return True
    # 2.2 box in uppermost or bottommost row locked by curr_obstacles
    if (y == 0 or y == state.height - 1) and ((pos_l in curr_obstacles) or (pos_r in curr_obstacles)):
        return True
    return False


def dead_boundary(state, box):
    """Check for dead boundaries"""
    (x, y) = box
    available_storage = possible_storage(state, box)
    storage_x, storage_y = [], []
    for storage in available_storage:
        storage_x.append(storage[0])
        storage_y.append(storage[1])
    # 1. box is in the leftmost/rightmost column and no storage along that column
    if (x == 0 or x == state.width - 1) and x not in storage_x:
        return True
    # 2. box is in the uppermost/bottommost row and no storage along that row
    elif (y == 0 or y == state.height - 1) and y not in storage_y:
        return True
    else:
        return False


def possible_storage(state, box):
    """Find available storage for the box"""
    if box in state.storage:
        return [box]
    potential = []
    for storage in state.storage:
        potential.append(storage)
    for b in state.boxes:
        if b != box and b in state.storage:
            potential.remove(b)
    return potential


def unsolved_boxes(state):
    """Find boxes that are not stored yet"""
    unsolved = []
    for box in state.boxes:
        if box not in state.storage:
            unsolved.append(box)
    return unsolved


def detect_dead_state(state):
    """detect whether the state is a dead state: it can never be solved once entered this state."""
    # 1. There exist at least one box against corner created by walls and obstacles or map corners.
    # 2. There are more than one boxes along wall or map boundaries where there are no storage spots.
    unsolved = unsolved_boxes(state)
    for box in unsolved:
        if dead_corner(state, box) or dead_boundary(state, box):
            return True
    return False


# def detect_obstacles(state, start, end):
#     """determine number of all the obstacles from start to end;
#     obstacles in the rectangular range bounded by start and end will be counted."""
#     count = 0
#     # define the rectangle surrounded by start and end
#     rec_up = max(start[1], end[1])
#     rec_down = min(start[1], end[1])
#     rec_left = min(start[0], end[0])
#     rec_right = max(start[0], end[0])
#     # current obstacles are state.obstacles and robots
#     for obs in state.obstacles:
#         (obs_x, obs_y) = obs
#         if (rec_left <= obs_x <= rec_right) and (rec_down <= obs_y <= rec_up):
#             count += 1
#     for bot in state.robots:
#         (bot_x, bot_y) = bot
#         if (rec_left <= bot_x <= rec_right) and (rec_down <= bot_y <= rec_up):
#             count += 1
#     return count


def heur_alternate(state):
    """a better heuristic"""
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    alt_heu = 0

    # 1. detect whether the state is already dead: it can never be solved once entered dead state
    if detect_dead_state(state):
        return math.inf

    # 2. evaluate unsolved boxes
    unsolved = unsolved_boxes(state)
    if len(unsolved) == 0:
        return 0
    for box in unsolved:
        bot_to_box = math.inf
        box_to_des = math.inf
        storage = possible_storage(state, box)
        # 2.1 approximation of distance from robot to box
        for bot in state.robots:
            m_dist = (abs(bot[0] - box[0]) + abs(bot[1] - box[1]))
            curr_heu = m_dist
            bot_to_box = min(curr_heu, bot_to_box)
        # 2.2 approximation of distance from box to storage
        for place in storage:
            m_dist = (abs(place[0] - box[0]) + abs(place[1] - box[1]))
            curr_heu = m_dist
            box_to_des = min(curr_heu, box_to_des)
        alt_heu += (bot_to_box + box_to_des)
    return alt_heu


def heur_zero(state):
    """Zero Heuristic can be used to make A* search perform uniform cost search"""
    return 0


def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    fval = sN.gval + weight * sN.hval
    return fval


# SEARCH ALGORITHMS
def weighted_astar(initial_state, heur_fn, weight, timebound):
    """Provides an implementation of weighted a-star, as described in the HW1 handout"""
    '''INPUT: a warehouse state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of weighted astar algorithm'''

    # initialize search engine
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    s_engine = SearchEngine(strategy='custom', cc_level='full')

    # set up a specific search
    s_engine.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

    # execute the search
    result = s_engine.search(timebound=timebound, costbound=None)
    return result


def iterative_astar(initial_state, heur_fn, weight=1, timebound=5):
    # IMPLEMENT
    """Provides an implementation of realtime a-star, as described in the HW1 handout"""
    '''INPUT: a warehouse state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of realtime astar algorithm'''

    # record the time when the function is called, and keep track of time limit
    start_time = os.times()[0]
    end_time = start_time + timebound
    iter_timebound = timebound

    # initialize search engine
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    s_engine = SearchEngine(strategy='custom', cc_level='full')

    # keep the best result obtained so far, initialize costbounds
    curr_best, curr_stats = False, None
    costbound = (math.inf, math.inf, math.inf)

    # set up a specific search and run for the first time
    s_engine.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

    # perform iterated search for improvement if time limit is not reached
    while start_time < end_time:
        result, stats = s_engine.search(timebound=iter_timebound-0.01, costbound=costbound)
        if not result:
            return curr_best, curr_stats
        # if finds better solution
        if result.gval <= costbound[2]:
            # update costbound for pruning
            costbound = (math.inf, math.inf, result.gval)
            # update best result so far
            curr_best, curr_stats = result, stats
        # decrease weight
        weight *= 0.75
        # update timebound
        curr_search_time = os.times()[0] - start_time
        start_time = os.times()[0]
        iter_timebound -= curr_search_time
    return curr_best, curr_stats


def iterative_gbfs(initial_state, heur_fn, timebound=5):  # only use h(n)
    # IMPLEMENT
    """Provides an implementation of anytime greedy best-first search, as described in the HW1 handout"""
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of weighted astar algorithm'''

    # record the time when the function is called, and keep track of time limit
    start_time = os.times()[0]
    end_time = start_time + timebound
    iter_timebound = timebound

    # initialize search engine
    s_engine = SearchEngine(strategy="best_first", cc_level='default')

    # keep the best result obtained so far, initialize costbounds
    curr_best, curr_stats = False, None
    costbound = (math.inf, math.inf, math.inf)

    # set up a specific search and run for the first time
    s_engine.init_search(initial_state, sokoban_goal_state, heur_fn)

    # perform iterated search for improvement if time limit is not reached
    while start_time < end_time:
        result, stats = s_engine.search(timebound=iter_timebound - 0.01, costbound=costbound)
        if not result:
            return curr_best, curr_stats
        # if finds better solution
        if result.gval <= costbound[0]:
            # update costbound for pruning
            costbound = (result.gval, math.inf, math.inf)
            # update best result so far
            curr_best, curr_stats = result, stats
        # update timebound
        curr_search_time = os.times()[0] - start_time
        start_time = os.times()[0]
        iter_timebound -= curr_search_time
    return curr_best, curr_stats



