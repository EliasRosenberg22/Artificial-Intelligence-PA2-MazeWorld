
#Elias Rosenberg
#CS76
#Professor Quattrini Li
#21F
#October 2nd, 2021

# PA2: Mazeworld

# Introduction: 
In this assignment, we were tasked with implementing a version of the A* search algorithm that calulates the best proceeding node traveled to with a heursitic. The heurstic used was the manhattan distance between a maze coordinate and the goal state, calculated by taking the absolute value of the distance between those two spots in the maze. The algortihm is built to handle multiple robots seeking multiple goal states. We were also tasked with writing a second, shorter algorithm that could localize a robot withtout telling it its start state, and that could not sense its surroundings. 

# Discussion: 
Similarly to the first lab, following the pseudocode for the A* implementation was very useful. Also, starting with a UCS (uniform cost search) implementation using a Nulll heurstic was important for testing that the algorithm could return a path before the heuristic was implemented. A* works similarly to UCS, propogating to children at every new depth, and popping the first child in a list of successors to the pqueue if it hasn't been visited yet. The difference comes in with the heuristic, which favors nodes in the priority queue with a lower value, which means that they are closer to the goal state. If a path with a node that has already been visited is now calculated to have a lower heursitc, we keep a dictionary of Node keys mapped to their heuristic values to see if it is lower. If it is, we put in the lower value heuristic with the same Node key to show that we found a cheaper path using the same node. Once the goal solution is found, we use the same backchaining method to go from parent to parent to return a successful path. 

The main design decision I had to decide first, and fiddle with throughout the whole process, was how to represent the states. I settled on a list of tuples, with each tuple holding an x and y value for the coordinates of a robot. This was fine at first, until I inevitably got errors saying that this state is iteratable in some contexts and not iteratable in others. It was a nightmare to go through the code painstakingly switching back and forth between a list of values and a tuple of the same list! I visualized my state as a list, so I was stubborn and stuck with that format. Other important design decisions affected how A* was generalized between MazeWoldProblem, and SensorlessProblem. 

Each problem class required its own 'has_goal', 'get_successor', and heuristic functions to be generalizable within A*. For MazeWorldProblem, the goal state was a parameter of all the x, y values of where we wanted the robot to end up. If the current state == the goal state of the search_problem, then we have found a solution! For Sensorless problem, there was technically no goal state. We didn't care about where the robot ended up, just where its start state was. The state for this problem was all the possible locations where the robot could be, each one removed when going through a list of all possible actions. When the length of the set of possible states reached 1, we knew where the robot had localized to. So that 'has_goal' method just checked if the lenght of the set was equal to 1. The 'get_successor' method for MazeWorldProblem looped through a list of possible actions for any given state and then checked if they were legal using a helper function. If they were, they were added to a successor list and sent off to A* to loop through child nodes. The SensorlessProblem method was more clever, checking which coordinates were still a floor tile in the maze based on the possible movements of the robot. If you could move to a floor tile with that action, that coordinate was added to a list of next states. If it wasn't, the coordinate was added back to the list of coordinates to check in the future; maybe that coordinate could be accessed with a different combination of actions, so it should be visited again. The heuristic for MazeWorldProblem was the Manhattan Distance described in the intro, and the one for SensorProblem favored next states that were smaller than the current state, because we watned a state length == 1. 

This lab was much harder than the first, because instead of worrying about the movements of one thing, you had to worry about the movements of multiple robots. It took me a long time to figure out the proper structure of returning a state holding all the movements of each robot while also looping through the robots one at a time. To do this, I had an integer called 'currRobot' that incremented everytime I wanted to find the children of the next robot. With this integer, I could index into the current state and alter the coordinates of the right one.

# Evaluation:
As far as I can tell everything runs fine. All the given examples and the test mazes I created for both MazeWorldProblem and SensorlessProblem return reasonable paths and visit around the right number of nodes. Again, I have nothing to compare to with these answers, so they seem reasonable without a 'correct' set of stats to look at. If I wasn't so stubborn, the uniformity of how I store/alter the state throughout A* could have been better. I was so set on keeping the state as a list, when I should have just caved and made it a tuple from the start. It still works though. I can tell that my heuristics are accurate because the order in which nodes were popped from the priority cue in the UCS implementation with a Null heuristic was different than the order with the Manhattan Heurstic. In 'maz1.maz' my robot would often get stuck in the bottom right-hand corner instead of reaching the goal state at the top because that corner node was added to the pqueue first. With the Manhattan heuristic, this was no longer a problem, as the goal state had a lower heuristic than the bottom corner of the maze. 
# Discussion Questions:


1. I represnted the state of the system as a list of tuples. In this context, there were k tuples within the list, each holding a set of coordinates for the location of that robot. So, if there is one robot, we have a list with one tuple containing an x and a y. If there are three robots, there would be three tuples in a list, each with two coordinate values. To determine of a possible state is legal you need to see if the coordinate is a floor tile. This was given to us with the is_floor() helper function that sees if the coordinate is within the boundaries of the maze, and if it is a wall. You also need to keep test if the floor tile is occupied by another robot before it can be called a legal child state. 

2. If k represnts the number of robots, and n is the number of tiles, the upper bound of states would be nk. If there is only one robot, for example, and there are 20 possible tiles it could be on, there would be twenty states. If there are three robots, and 50 tiles, then there are 150 combinations of states to pick from. 

3. If n is much larger than k and w is also not too large then the chance of a collision is small because there are so many legal tiles to go to. This could be shown by abs[nk-kw], where we calculate the number of states if each robot hit a wall. 


4. No I don't. Ten robots is a lot of robots running around. The chances that just two of them would run into eachother to yield a premature path seems high. If they all share the same explored_nodes set, then the chances of finding an uninterrupted/unexplored path are even lower. There is also the chance that any one of them would hit a wall is also something to be worried about. This algorithm would also take much longer than A*, as there is no heuristic pulling the robots towards the goal. In a 100x100 space it would take a long time for BFS to explore every single node.  

5. A heuristic is monotonic when it is less than the actual cost of the path to the goal, and when it is less than the paths of adjacent nodes to the goal plus their heursitic. ℎ(𝑥)<=𝑑(𝑥,𝑦)+ℎ(𝑦). The Euclidean distance between a robot's coordinate and the goal coordinate is gaurunteed to be an optimistic, monotonic heuristic. It will always underestimate the distance to the goal because it doesn't take into account all the tiles needed to be crossed because a robot can't travel diagonally. It will also be smaller than the distances of adjacent nodes + their heuristics if the robot is traveling towards the goal state, which it should be. 


6. The 8-puzzle in the book is a special case of this problem because robots(in this case numbered tiles 1-8) need to retread spots they've already been on to get to the goal state. If you look at it from the perspective of the blank spot moving, the maze of tiles rebuilds itself around the blank spot every turn. You can think of the 8-puzzle as a maze being rebuilt around a robot, where each maze tile must end up in the proper place. Euclidean distance would be a bad heuristic for this puzzle, because it doesn't take into account where each puzzle tile should be. The Manhattan heuristic would be better for this puzzle, because the value of the heuristic takes into accound the distances of where all the tiles are from where they should be in the goal state. 

7. The only disjoint sets I can think of for this problem are the goal state and the start state. Those are the only two sets that are 'disjoint' and have completely different elements. To prove this, you can run the 8-puzzle through A* to find the solution. If the solution is correct, it should be a set with tiles in positions different to the start state (as long as there are tiles that aren't in the correct orientation to begin with). The way I represent a state would have to be completely different. You could represent the state as a dictionary of tile numbers mapped to coorinate values within the 3x3 space. Each new state just holds different coords for the tile key. 


ASCII output for maze_1.maz

##.#
#...
#A#B

##.#
#A..
#.#B

##.#
#A.B
#.#.

Extra test maps
- I used https://www.dcode.fr/maze-generator as a way to randomly generate a couple of the maps I used. The maps it generates are larger than what you enter into the website's dimensional paramters, but the robots still find a path. The first map is a the websites version of a '40x40' map with one robot. The second is a 50x50 with two robots. The third was manually made, but is good for testing four or five robots. The fourth isn't meant to be solved, so it should return 'no path found.'The fifth tests the hallway problem described in the lab instructions, where multiple robots need to wait for eachother to move down a narrow path. 

Description of sensorless_search plan:
The plan for my sensorless search doesn't run one action at a time like a string of direction (North, North, South, West, East...) but checks all the actions that are legal at a state, and adds the ones that aren't legal back into the list of legal floor tiles to be checked. This way, you can check off multiple possible locations at a time from the set of all legal tiles instead of one at a time. 

1. Final Discussion Question(s):
    The heuristic used for A* search was the Manhattan distance, which is just the distance between the goal state and the current state. This is optimistic, as it doesn't accound for walls or any weird paths the robot must take becuase of obstacles, so it the heuristic is lower than the actual path cost. You could also use Euclidean distance between the two states, but it would be dominated by the Manhattan distance which yields higher values. We never touched on why larger heuristics are actually better, just that they 'dominate.'Maybe because there is more room for different values. 
2. This second section is labeled as "Hint" but it looks like another question, so I'll answer it. All the successor function in A* does is take all the values in a state of each robots coordinates, and add values to them to represent possible new coordinates for any robot in the state. If the new coordinate is legal (is a floor and doesn't currenlty have a robot on it), then it is added to the list of next states for that robot. 


