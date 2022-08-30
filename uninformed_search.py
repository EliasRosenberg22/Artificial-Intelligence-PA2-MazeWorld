#Author: Elias Rosenberg
#Date: September 23, 2021
#Purpose: Implement BFS, DFS, and IDS to find solutions to the chicken-fox problem. Finds a path through nodes where each node is an orientation
#of the number of chickens, foxes, and the bot on the left side of the river.

from collections import deque
from SearchSolution import SearchSolution

class SearchNode:
    def __init__(self, state, parent=None):
        # you write this part
        self.state = state
        self.parent = parent



#helper function to do backchaing once goal node is found
 #this is the problem when running multiple tests. Path is appended everytime to final solution. Can't figure out how else to store this AND recurse

def backchaining(node, search_problem, path):
    if node.state != search_problem.start_state:
        path.append(node.state)
        backchaining(node.parent, search_problem, path) #recursively call again to bubble up the tree following parent pointers

def bfs_search(search_problem):
    sol = SearchSolution(search_problem, "BFS") #successful solution object for bfs
    visitedSet = set([]) #set of nodes that have been visited, and don't need to be added to the fringe
    frontier = deque([]) #frontier(fringe) = new queue
    start = SearchNode(search_problem.start_state, None) #pack start state into a node
    frontier.append(start) #add node to frontier

    while frontier: #while frontier not empty
       currNode = frontier.popleft() #get curr node from frontier
       currState = currNode.state #get state from node
       visitedSet.add(currState) #add node to set of unique visited states

       if currState == search_problem.goal_state: #if the current state is the goal state
           path = sol.path
           backchaining(currNode, search_problem, path) #run the backchaining helper function
           path.append(search_problem.start_state)
           sol.path = path #setting up the search solution object
           sol.nodes_visited = len(visitedSet)
           return sol

       else: #if we are not at the goal state
        for child in search_problem.get_successors(currState): #for every child in the list of sucessors
            newNode = SearchNode(child, currNode) #pack that state into a node with a backpointer to current node
            if newNode.state not in visitedSet: #add the node to the frontier if it hasn't been visited already
                frontier.append(newNode)

    sol.nodes_visited = len(visitedSet)
    return sol


def pathchecking(node, state, search_problem):
    while node.parent: #while the node has a parent
        if node.parent.state == state: #if the state of the parent is the same as the current state, we're in a loop
            return False
        node = node.parent #bubble back up to see if there are other loops
    return True

def dfs_search(search_problem, depth_limit = 100, node=None, solution=None):
    frontier = []
    if node == None:
        node = SearchNode(search_problem.start_state)
        solution = SearchSolution(search_problem, "DFS")
    frontier.append(node)
    solution.nodes_visited += 1 #adding start node to the count of visited nodes

    while frontier:
        currNode = frontier.pop()
        currState = currNode.state

        if currState == search_problem.goal_state:  # if the start node is already the goal state
            path = solution.path
            backchaining(currNode, search_problem, path)  # run the backchaining helper function
            path.append(search_problem.start_state)
            solution.path = path  # setting up the search solution object
            return solution
        else:

         for child in search_problem.get_successors(currState):
            if pathchecking(currNode, child, search_problem):
                newNode = SearchNode(child, currNode)
                solution.nodes_visited += 1
                recurse = dfs_search(search_problem, depth_limit= depth_limit-1, node = newNode, solution = solution)
                if len(recurse.path) > 0: #when the path lenght != 0, you know a solution was found and kept in the path
                    return recurse
    return solution


def ids_search(search_problem, depth_limit = 100):
    solution = SearchSolution(search_problem, "IDS")
    node = SearchNode(search_problem.start_state)

    for i in range(0, depth_limit): #for every tree depth before the solution is found
        if dfs_search(search_problem, depth_limit = i, node = node, solution = solution): #if there is a solution
            return solution
        else:
            i += 1 #if no solution found at this depth, increase the depth

