#Author: Elias Rosenberg
#Date: October 2, 2021
#Purpose: Implementation of A* search algorithm. Takes a search problem that models the states of the robots being
#analyzed and a heuristic to alter which nodes are chosen first in the path. 

import itertools
from SearchSolution import SearchSolution
from heapq import heappush, heappop
from queue import *

class AstarNode:
    # each search node except the root has a parent node
    # and all search nodes wrap a state object

    def __init__(self, state, heuristic, parent=None, transition_cost=0):
        # you write this part
        self.state = state
        self.heuristic = heuristic
        self.parent = parent
        self.transition_cost = transition_cost

    def priority(self):
        # you write this part
        return self.heuristic + self.transition_cost #a node with a lower heuristic + transition cost has a higher priority in the pq

    # comparison operator,
    # needed for heappush and heappop to work with AstarNodes:
    def __lt__(self, other):
        return self.priority() < other.priority()



# take the current node, and follow its parents back
#  as far as possible. Grab the states from the nodes,
#  and reverse the resulting list of states.
def backchain(node):
    result = []
    current = node
    while current:
        result.append(current.state)
        current = current.parent

    result.reverse()
    return result


def astar_search(search_problem, heuristic_fn):
    start_node = AstarNode(search_problem.start_state, heuristic_fn(search_problem.start_state))
    pqueue = [] #frontier = new priority queue (ordered by path cost)
    heappush(pqueue, start_node) #add the start node to the priority que
    solution = SearchSolution(search_problem, "Astar with heuristic " + heuristic_fn.__name__)

    explored = set([])
    visited_cost = {} #need to do something with this :)
    visited_cost[tuple(start_node.state)] = start_node.priority()

    i = 0
    while pqueue: #while there are nodes in the priority queue
        currNode = heappop(pqueue)
        explored.add(tuple(currNode.state))
        #print("currNode.state: " + str(currNode.state))
        #print("temp_goal_state: " + str(temp_goal_state))
        solution.nodes_visited += 1
        if tuple(currNode.state) in explored and currNode.priority() > visited_cost[tuple(currNode.state)]:
            continue

        if search_problem.goal(currNode.state): #if the goal state is reached, backtrack and return the solution
            path = backchain(currNode)
            solution.cost = currNode.transition_cost
            solution.nodes_visited = len(explored)
            solution.path = path
            return solution
        else:
            children = search_problem.get_successors(currNode.state)
            if len(children) == 0: #if this robot has no children, move onto the next one.
                i += 1
                if i > search_problem.number_of_robots: #if i > than the number of robots, set i back to 0 and loop through robots again
                    break
                heappush(pqueue, currNode)
                continue
            else:
                i = 0
            for child in children: #adding child nodes to the priority.
                newNode = AstarNode(child, heuristic_fn(child), parent=currNode,transition_cost=currNode.transition_cost + 1)
                if tuple(child) not in explored:
                    explored.add(tuple(child))
                    visited_cost[tuple(newNode.state)] = newNode.priority()
                    heappush(pqueue, newNode)

                elif tuple(child) in visited_cost and newNode.priority() < visited_cost[tuple(child)]: #if the cost of a visited node is less than its previous value, change key's value in the dictionary to mark it as the better path.
                    explored.add(tuple(child))
                    visited_cost[tuple(newNode.state)] = newNode.priority()
                    heappush(pqueue, newNode)

    return solution