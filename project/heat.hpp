#ifndef HEAT_HPP
#define HEAT_HPP

#include <string>
#include <vector>

#include "sparse.hpp"

class HeatEquation2D
{                                                                  /// change to private again later (A, b, x, nrows, ncols, ninc)
    
  private:
    SparseMatrix A;
    std::vector<double> b, x;
    unsigned int nrows, ncols; // number of rows and cols in the grid 
    // representation (figure 2)
    unsigned int ninc; // number of unknowns (size of x)
    int niter; // number of iterations

  public:
    /* Method to setup Ax=b system */
    int Setup(std::string inputfile);

    /* Method to solve system using CGsolver */
    // soln_prefix = prefix name to put in the solution file
    // returns 0 if the run was successful
    int Solve(std::string soln_prefix);

};

#endif /* HEAT_HPP */
