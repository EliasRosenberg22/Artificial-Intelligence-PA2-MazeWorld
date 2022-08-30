#Author: Elias Rosenberg
#Date: October 2, 2021
#Purpose: Mazeworld object to build and manipulate robot states. Also holds the start and goal states for a search_problem


from Maze import Maze
from time import sleep

class MazeworldProblem:

    ## you write the constructor, and whatever methods your astar function needs

    def __init__(self, maze, goal_locations):
        self.maze = maze
        self.goal_locations = goal_locations
        self.possible_actions = [(-1,0), (1,0), (0, 1), (0,-1)]      # move left, right, up, down, or wait
        self.map_state = [] #the current state that the robot is in
        self.currRobot = 0 #a count
        self.number_of_robots = len(maze.robotloc)//2 #number of robots in the system
        self.start_state = self.map_state
        self.goal_state = goal_locations
        self.temp_goal_state = [] #proper formatting of the necessary goal state for this setup

        for i in range(0, len(self.maze.robotloc)-1, 2): #putting the robot locations into the proper format
            tup = (self.maze.robotloc[i], self.maze.robotloc[i+1])
            self.map_state.append(tup)
        self.map_state = tuple(self.map_state)


        for i in range(0, len(self.goal_state)-1, 2): #putting the goal values given into the proper format
            tupl = (self.goal_state[i], self.goal_state[i+1])
            self.temp_goal_state.append(tupl)
        self.temp_goal_state = tuple(self.temp_goal_state)


    def __str__(self):
        string =  "Mazeworld problem: "
        return string


    def animate_path(self, path):
        # reset the robot locations in the maze
        self.maze.robotloc = tuple(self.start_state[1:])
        for state in path:
            list = []
            for coords in state:
                x ,y = coords
                list.append(x)
                list.append(y)
            self.maze.robotloc = tuple(list)
            sleep(1)
            print(str(self.maze))

    def get_successors(self, state):
        successors = set([])
        x, y = state[self.currRobot]

        for action in self.possible_actions: #for the values in possible actions (up, down, left, right, wait)
            dx, dy = action
            newX = x + dx
            newY = y + dy
            possibleMove = (newX, newY) #create a new value
            if self.legal_actions(state, possibleMove):
                pseudoState = list(state)#copy of map_state
                pseudoState[self.currRobot] = possibleMove
                successors.add(tuple(pseudoState)) #add the new state to the list of sucessors


        #print("sucessors_list:" + str(successors))
        self.currRobot = (self.currRobot + 1) % self.number_of_robots #go to the next robot in the state and get its sucessors
        #print("currRobot" + str(self.currRobot))
        return successors


    def legal_actions(self, map_state, tuple):
        if self.maze.is_floor(tuple[0], tuple[1]):
            for i in range(len(map_state)):
                if map_state[i] == tuple and i != self.currRobot:
                    return False
            return True
        return False


    def has_robot_state(self, map_state, node): #tests if a robot is occupying the given tile
        for s in map_state: #length of items in the state list:
            if s == node:
                return True
        return False

    def manhattan_heuristic(self, state):
        p1 = state[self.currRobot]
        p2 = self.temp_goal_state[self.currRobot]
        return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

    def goal(self,node):
        if node == self.temp_goal_state:
            return True


def wait(self, node): #helper function to tell a robo to wait if it can't move. Equivalent to the move (0, 0)
    self.map_state = list(self.map_state)
    self.map_state[self.currRobot] = self.map_state[self.currRobot]  # don't change the coordinate of the robot --> equivalent to (0, 0)
    self.map_state = tuple(self.map_state)


## A bit of test code. You might want to add to it to verify that things
#  work as expected.

if __name__ == "__main__":
    test_maze3 = Maze("maze1.maz")
    test_mp = MazeworldProblem(test_maze3, (1, 4, 1, 3, 1, 2))
    #print(test_maze3)
    #print(test_maze3.robotloc)
    #print(test_mp.map_state)
    #print(test_mp.get_successors((0, 1)))
    #print(test_mp.get_successors(test_mp.map_state))
    #print(test_mp.get_successors(test_mp.map_state))

