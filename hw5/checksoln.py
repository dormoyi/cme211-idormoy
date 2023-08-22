import numpy as np
import sys

def create_maze(maze_file):
    """
    create a numpy array from the input maze file
    1 means there is a wall
    0 means the way is free
    output: numpy array 
    """
    f = open(maze_file, 'r')
    lines = f.readlines()
    f.close()

    nb_rows, nb_cols = lines[0].split()
    nb_rows, nb_cols = int(nb_rows), int(nb_cols)

    maze = np.zeros((nb_rows, nb_cols))
    
    for line in lines[1:]:
        row, col = line.split()
        row, col = int(row), int(col)
        maze[row][col] = 1

    return(maze)

def check_maze(maze, solution_file):
    """
    performs checks on the solution file to see if it's valid
    - the maze was properly entered on the first row
    - reach the exit of the maze on the last row
    - move one position at a time
    - don't go through a wall
    - stay within the bounds of the maze
    - move at each step
    exits if the solution is not valid 
    """
    f = open(solution_file, 'r')
    lines = f.readlines()
    f.close()

    # the maze was properly entered on the first row
    row1, col1 = lines[0].split()
    row1, col1 = int(row1), int(col1)
    if (row1 != 0) or (maze[row1][col1]==1) or (col1<0) or \
        (col1>maze.shape[1]-1):
        print("Invalid solution :(")
        sys.exit(0)

    # reach the exit of the maze on the last row
    rown, coln = lines[-1].split()
    rown, coln = int(rown), int(coln)
    if rown != maze.shape[0] -1:
        print("Invalid solution :(")
        sys.exit(0)

    p_row, p_col = row1, col1
    for line in lines[1:]:
        row, col = line.split()
        row, col = int(row), int(col)

        # move one position at a time
        if (p_row != row) and (p_col != col):
            print("Invalid solution :(")
            sys.exit(0)

        # don't go through a wall
        if maze[row1][col1]==1:
            print("Invalid solution :(")
            sys.exit(0)

        # stay within the bounds of the maze
        if (row<0) or (row>maze.shape[0]-1)or (col<0) or (col>maze.shape[1]-1):
            print("Invalid solution :(")
            sys.exit(0)

        # move at each step
        if (p_row == row) and (p_col == col):
            print("Invalid solution :(")
            sys.exit(0)

        p_row, p_col = row, col


if __name__ == '__main__':

    if len(sys.argv) !=3:
        print("Usage:")
        print(" $ python checksoln.py [maze file] [solution file]")
        sys.exit(0)

    maze_file, solution_file = sys.argv[1], sys.argv[2]

    maze = create_maze(maze_file)
    check_maze(maze, solution_file)

    print("Solution is valid!")