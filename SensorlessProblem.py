#Author: Elias Rosenberg
#Date: October 2, 2021
#Purpose: MazeWorld object to solve the localization problem of a blind robot. Also holds the different get_successors function
#and goal function.

from Maze import Maze
from time import sleep
from astar_search import astar_search
from MazeworldProblem import MazeworldProblem

class SensorlessProblem:

    def __init__(self, maze):
        self.start_state = None
        self.maze = maze
        self.possible_actions = [(-1,0), (1,0), (0, 1), (0,-1)]  # move left, right, up, down, wait isn't needed since there's one robot
        self.map_state = [] #the current state that the robot is in
        self.temp_goal_state = []


        whole_map = []
        for x in range(maze.width):
            for y in range(maze.height):
                if maze.is_floor(x, y):
                    state = x ,y
                    whole_map.append(state)


        self.map_state = whole_map
        self.start_state = self.map_state #state that holds all possible locations for the robot

    def __str__(self):
        string =  "Blind robot problem: "
        return string


        # given a sequence of states (including robot turn), modify the maze and print it out.
        #  (Be careful, this does modify the maze!)

    def animate_path(self, path):
        # reset the robot locations in the maze
        #need to alter this to print out the path without the start location
        self.maze.robotloc = tuple(self.start_state)

        for state in path:
            self.maze.robotloc = []
            for coord in state:
                x = coord[0]
                y = coord[1]
                if len(coord) == 2:
                    self.maze.robotloc.append(x)
                    self.maze.robotloc.append(y)
            self.maze.robotloc = tuple(self.maze.robotloc)
            sleep(1)
            print(str(self.maze))

    def goal(self, state):
        if len(state) == 1:
            return True
        else:
            return False

    def get_successors(self, state):
        successors = set([]) #list of all possible successors
        for action in self.possible_actions:
            next_state = set([])
            for coord in state:
                dx, dy = action
                newX = coord[0] + dx
                newY = coord[1] + dy
                possibleMove = (newX, newY)
                if self.maze.is_floor(newX, newY):
                    next_state.add(possibleMove)
                else:
                    next_state.add(coord)
            successors.add(tuple(next_state))
        return tuple(successors)

    def sensorless_heuristic(self, state): #heuristic for this problem is just the smallest set of states.
        heuristic = len(state) -1
        return heuristic








## THIS IS WHERE IS RUN TEST CODE. NOT IN sensorless_test.py

if __name__ == "__main__":
    test_maze1 = Maze("sensorless_maze1")
    test_problem1 = SensorlessProblem(test_maze1)
    result = astar_search(test_problem1, test_problem1.sensorless_heuristic)
    print(result)
    test_problem1.animate_path(result.path)

    test_maze2 = Maze("sensorless_maze2")
    test_problem2 = SensorlessProblem(test_maze2)
    result = astar_search(test_problem2, test_problem2.sensorless_heuristic)
    print(result)
    test_problem2.animate_path(result.path)
