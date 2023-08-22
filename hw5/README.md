## Brief statement of the problem.
A robot wants to escape a maze. It enters by the first row, and has to exit by the last row. To find its path, it follows the wall on its right, until it reaches the end of the maze.  

## Description of your C++ code.
We use a 2D static array to store the maze. This static array is of size superior to the biggest array we will have to handle in this problem.
Obstacles are represented by 1 in this array. Free path is represented by 0.

Here are the steps of the algorithm:
- Verify that appropriate static array storage is available for storing the maze. 
- Find the maze entrance at the opening in the first row.
- Use the right hand wall following algorithm to move through the maze without going through any
walls, storing each position in the solution file. To perform the right hand wall following algorithm, we do the following: 
track the robot's direction in the maze and choose the robot's next step in function of its current position and the obstacles surrounding it.
- Exit on the last row and store this as your last position in the solution file.

## Brief summary of your code verification with ’checksoln.py‘.
performs checks on the solution file to see if it's valid
- the maze was properly entered on the first row
- reach the exit of the maze on the last row
- move one position at a time
- don't go through a wall
- stay within the bounds of the maze
- move at each step

exits if the solution is not valid 

The maze is stored in a numpy array. 1 in the array means that there is an obtacle.
