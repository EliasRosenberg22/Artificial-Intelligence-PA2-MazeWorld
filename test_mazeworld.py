#Author: Elias Rosenberg
#Date: October 2, 2021
#Purpose: Test the A* function using MazeWorldProblem states and a Manhattan distance as the heuristic. Prints out
#the animated paths.



from MazeworldProblem import MazeworldProblem
from Maze import Maze
from astar_search import astar_search
from uninformed_search import bfs_search

# null heuristic, useful for testing astar search without heuristic (uniform cost search).
def null_heuristic(state):
    return 0


test_maze = Maze("maze1.maz")
test_mp1 = MazeworldProblem(test_maze, (1, 1, 3, 1))
print(test_maze)
result = astar_search(test_mp1, test_mp1.manhattan_heuristic)
print(result)
test_mp1.animate_path(result.path)

# Your additional tests here:

test_maze1 = Maze("manhattan_maze1") #randomly generated 40x40
test_mp1 = MazeworldProblem(test_maze1, (0, 80))
print(test_maze1)
result = astar_search(test_mp1, test_mp1.manhattan_heuristic)
print(result)
test_mp1.animate_path(result.path)

test_maze2 = Maze("manhattan_maze2") #randomly generated 50x50. takes about a minute to load a solution
test_mp2 = MazeworldProblem(test_maze2, (0, 40, 1, 40))
print(test_maze2)
result = astar_search(test_mp2, test_mp2.manhattan_heuristic)
print(result)
test_mp2.animate_path(result.path)

#test_maze3 = Maze("manhattan_maze3") #manually generated, includes 4 robots
#test_mp3 = MazeworldProblem(test_maze3, (120, 1))
#print(test_maze3)
#result = astar_search(test_mp3, test_mp3.manhattan_heuristic)
#print(result)
#test_mp3.animate_path(result.path)

#test_maze4 = Maze("manhattan_maze4") #manually generated, no solution possible
#test_mp4 = MazeworldProblem(test_maze4, (1, 1, 3, 1))
#print(test_maze4)
#result = astar_search(test_mp4, test_mp4.manhattan_heuristic)
#print(result)
#test_mp4.animate_path(result.path)

#test_maze5 = Maze("manhattan_maze5") #manually generated. 'hallway problem' tight squeeze for multiple robots
#test_mp5 = MazeworldProblem(test_maze5, (0, 39))
#print(test_maze5)
#result = astar_search(test_mp5, test_mp5.manhattan_heuristic)
#print(result)
#test_mp5.animate_path(result.path)
