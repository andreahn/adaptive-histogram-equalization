# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
#
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"

    "visited is a set to keep track of visited nodes in order to avoid"
    "searching the same node multiple times"
    visited = set()

    "In DFS a stack will be used to search each node by depth first"
    stack = util.Stack()

    "The stack has elements with state and actions to reach state"
    stack.push((problem.getStartState(), []))

    while not stack.isEmpty():
        state, actions = stack.pop()

        if not state in visited:
            visited.add(state)
            if problem.isGoalState(state): return actions

            for succ, action, cost in problem.getSuccessors(state):
                if succ not in visited:
                    stack.push((succ, actions + [action]))


    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"


    "Code is almost the same as DFS, but in order to search level by level,"
    "a FIFO data structure (queue) is used in stead of stack(LIFO)."
    visited = set()
    queue = util.Queue()
    queue.push ((problem.getStartState(), []))

    while not queue.isEmpty():
        state, actions = queue.pop()

        if not state in visited:
            visited.add(state)
            if problem.isGoalState(state): return actions

            for succ, action, cost in problem.getSuccessors(state):
                if succ not in visited:
                    queue.push((succ, actions + [action]))

    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"

    "Again, the code of the function is very similar to DFS and BFS, but"
    "a priority queue is used so that the next node searched is the node"
    "with the lowest cost."
    visited = set()
    pqueue = util.PriorityQueue()
    "Each element in the priority queue also includes cost (initialized to 0 here)"
    pqueue.push ((problem.getStartState(), []), 0)

    while not pqueue.isEmpty():
        state, actions = pqueue.pop()

        if not state in visited:
            visited.add(state)
            if problem.isGoalState(state): return actions

            for succ, action, cost in problem.getSuccessors(state):
                if succ not in visited:
                    pqueue.push((succ, actions + [action]), cost + problem.getCostOfActions(actions))

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"

    "Code will be almost the same as uniformCostSearch"
    visited = set()
    pqueue = util.PriorityQueue()
    pqueue.push((problem.getStartState(), []), 0)

    while not pqueue.isEmpty():
        state, actions = pqueue.pop()

        if not state in visited:
            visited.add(state)
            if problem.isGoalState(state): return actions

            for succ, action, cost in problem.getSuccessors(state):
                if succ not in visited:
                    "The value from the heuristic function is also added to the cost in order"
                    "to have A*  search and not uniform cost search"
                    pqueue.push((succ, actions + [action]), cost + problem.getCostOfActions(actions) + heuristic(succ, problem))

    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
