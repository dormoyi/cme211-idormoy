# include <fstream>
# include <iostream>
# include <string>

int read_file (std::string input_file, int maze[202][202], \
int n, int dimensions[2]) {
    /* Reads the maze file, input:
    - input file <string>
    - maze static array <int[202][202]>
    - n <int> dimensions of the static array
    - dimensions <int[2]> static array containing the dimensions of the
    actual maze for rows (dimensions[0]) and columns (dimensions[1])
     */

    std::ifstream f(input_file);

    if (f.is_open()) {
        // reach each value of the input file
        int nif, njf; 
        f >> nif >> njf;
        dimensions[0] = nif;
        dimensions[1] = njf;
        if (nif > n or njf > n) {
            std::cout << "Not enough storage available" << std::endl;
        return 0; 
        }

        // complete the array, 1 in the array means there is an obtacle
        int x,y;
        while (f >> x >> y) {
            maze[x][y] = 1;
            }
        }
    f.close();
    return 1;
 }


void find_path(std::string solution_file, int maze[202][202], \
int dimensions[2]) {
    /*Finds a path through the maze, writes it in the output file, input:
    - solution file <string>
    - maze static array <int[202][202]>
    - dimensions <int[2]> static array containing the dimensions of the
    actual maze for rows (dimensions[0]) and columns (dimensions[1])
     */

    std::ofstream f;
    f.open(solution_file);
    int row = 0;
    int col = 0;

    //  Find the maze entrance at the opening in the first row 
    for (int j = 0; j < dimensions[1]; j++) {
        if (maze[0][j] ==0){
            col = j;
            break;
        }
    }

    // store this as first position in the solution file
    if (f.is_open()) {
        f << "0 " << col << std::endl;
    }

    //  right hand wall following algorithm
    enum direction
    {
        left,
        right,
        up,
        down
    };

    // the robot starts looking down
    direction d = down;


    while (row < dimensions[0] - 1){
        // find the next step in function of the direction of the robot in 
        // the maze
        switch (d)
        {
        case left:
        if (maze[row-1][col] == 0){
            row--;
            d = up;
        } else if (maze[row][col-1] == 0) {
            col--;
            d = left;
        } else if (maze[row+1][col] == 0) {
            row++;
            d = down;
        } else {
            col++;
            d = right;
        } 
        f << row << " " << col << std::endl;
        break;


        case right:
        if (maze[row+1][col] == 0){
            row++;
            d = down;
        } else if (maze[row][col+1] == 0) {
            col++;
            d = right;
        } else if (maze[row-1][col] == 0) {
            row--;
            d = up;
        } else {
            col--;
            d = left;
        } 
        f << row << " " << col << std::endl;
        break;


        case up:
        if (maze[row][col+1] == 0){
            col++;
            d = right;
        } else if (maze[row-1][col] == 0) {
            row--;
            d = up;
        } else if (maze[row][col-1] == 0) {
            col--;
            d = left;
        } else {
            row++;
            d = down;
        } 
        f << row << " " << col << std::endl;
        break;

        case down:
        if (maze[row][col-1] == 0){
            col--;
            d = left;
        } else if (maze[row+1][col] == 0) {
            row++;
            d = down;
        } else if (maze[row][col+1] == 0) {
            col++;
            d = right;
        } else {
            row--;
            d = up;
        } 
        f << row << " " << col << std::endl;
        break;
        }
    }
        
    // dot not forget to close the file
    if (f.is_open()) {
        f.close();
    }

}

int main (int argc , char * argv []) {

    const int n = 202;
    int maze[n][n] =  { 0 }; 
    int dimensions[2] =  { 0 }; 

    if (argc < 3) {
        std :: cout << " Usage : " << std :: endl ;
        std :: cout << " " << argv [0] << " <maze file> <solution file> " \
        << std :: endl ;
    return 0;
    }

    std::string maze_file = argv [1];
    std::string solution_file = argv [2];

    read_file(maze_file, maze, n, dimensions);

    find_path(solution_file, maze, dimensions);



return 0; 

}