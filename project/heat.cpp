#include <fstream>
# include <iostream>  
#include <iomanip> 
# include <math.h>    
# include <string>
# include <vector>

#include "CGSolver.hpp"
#include "heat.hpp"
#include "sparse.hpp"

int HeatEquation2D::Solve(std::string soln_prefix){
    double tol = 0.00001;
    // vector with the solutions found during the process
    std::vector<std::vector<double>> sols;

    // start with vector of zeros
    for (unsigned int n=0; n<this->ninc;n++)
      this->x.push_back(0);

    // convert the matrix and get the solution (project part 1)
    A.ConvertToCSR();
    std::vector<int> i_idx = A.get_i();
    std::vector<int> j_idx = A.get_j();
    std::vector<double> a = A.get_a();
    sols = CGSolver(a,i_idx,j_idx,this->b,this->x,tol);

    // output the solutions found every 10 iterations
    // (1 st iteration and then for every multiple of 10)  
    // add last iteration too 
    std::ofstream f_out; 
    std::string file_output;
    int num;
    for (unsigned int n=0; n<sols.size();n++)  {
      num = n*10;
      file_output = soln_prefix + std::to_string(num) + ".txt";

      f_out.open(file_output);
      for (unsigned int i=0;i<sols[n].size();i++){
        f_out<<std::setprecision(4)<<std::scientific<< sols[n][i] << std::endl;}
      f_out.close();
    }
    return 0;
}

int HeatEquation2D::Setup(std::string inputfile){
    // read the input file
    std::ifstream f;
    float len, wid, step, Tc, Th;
    f.open(inputfile);
    if (f.is_open()) {
        f >>len>> wid >>step;
        f >> Tc>> Th;
    }
    f.close();

    // initialize class attributes
    this->nrows = (unsigned int)(wid/step -2); // we remove 
    // unknows in the number of rows as we have up and down boundary conditions
    this->ncols = (unsigned int)(len/step);
    this->ninc = this->nrows * this->ncols;

    // number of lines in A matrix: nb of eq = nb of points
    // number of columns in A matrix: nb of inc = nb of points too
    // each line of A corresponds to an equation over a point
    // we solve -Ax = -b
    // the x vector is ordered in the following way: u11, u21, u31 etc
    int eq_num=0;
    for (unsigned int col=0;col<ncols;col++) {
     for (unsigned int row=0;row<nrows;row++) {
       //in the center of the rectangle (no boundaries)
       if (col>0 && col < ncols-1 && row>0 && row<nrows-1) {
         this->b.push_back(0);
         this->A.AddEntry(eq_num, row+(col-1)*nrows,-1/(step*step));
          this->A.AddEntry(eq_num, row+col*nrows+1,-1/(step*step));
         this->A.AddEntry(eq_num, row+col*nrows,4*1/(step*step));
         this->A.AddEntry(eq_num, row+col*nrows-1,-1/(step*step));
          this->A.AddEntry(eq_num, row+(col+1)*nrows,-1/(step*step));
         }

       // up boundary condition (hot)
       else if (col < ncols-1 && row==0 && col>0) {
           this->b.push_back(1/(step*step)*Th); 
           this->A.AddEntry(eq_num,(col+1)*nrows,-1/(step*step));
           this->A.AddEntry(eq_num,col*nrows+1,-1/(step*step));
          this->A.AddEntry(eq_num,(col-1)*nrows,-1/(step*step));
           this->A.AddEntry(eq_num,col*nrows,4*1/(step*step));
           }

        // down boundary condition (cold)
        else if (col>0 && col < ncols-1 && row == nrows-1) {
            this->b.push_back(1/(step*step)*-Tc*(exp(-10*(step*(float)col-len/2)\
            *(step*(float)col-len/2))-2)); 
           this->A.AddEntry(eq_num,row+(col-1)*nrows,-1/(step*step));
          this->A.AddEntry(eq_num,row+(col+1)*nrows,-1/(step*step));
           this->A.AddEntry(eq_num,row+col*nrows-1,-1/(step*step));
           this->A.AddEntry(eq_num,row+col*nrows,4*1/(step*step));
       }

      //left boundary (periodic)
       else if (col==0 && row>0 && row<nrows-1) {
           this->b.push_back(0);
           this->A.AddEntry(eq_num, row-1,-1/(step*step));
          this->A.AddEntry(eq_num, nrows+row,-1/(step*step));
          this->A.AddEntry(eq_num,row+1,-1/(step*step));
           this->A.AddEntry(eq_num, row,4*1/(step*step));
           this->A.AddEntry(eq_num,row+(ncols-1)*nrows,-1/(step*step));
           }
         
        // right boundary (periodic)
        else if (col == ncols-1 && row>0 && row<nrows-1) {
           this->b.push_back(0);
           this->A.AddEntry(eq_num,row+col*nrows-1,-1/(step*step));
           this->A.AddEntry(eq_num,row+col*nrows,4*1/(step*step));
           this->A.AddEntry(eq_num,row+(col-1)*nrows,-1/(step*step));
          this->A.AddEntry(eq_num,row+col*nrows+1,-1/(step*step));
           this->A.AddEntry(eq_num,row,-1/(step*step));
            }
       
       //special corner cases
       // up left corner (hot and periodic)
       else if (col == 0 && row==0) {
         this->b.push_back(1/(step*step)*Th);
         this->A.AddEntry(eq_num,(ncols-1)*nrows,-1/(step*step));
         this->A.AddEntry(eq_num,1,-1/(step*step));
         this->A.AddEntry(eq_num,nrows,-1/(step*step));
         this->A.AddEntry(eq_num,0,4*1/(step*step));
          }
         
      // up right corner (hot and periodic)
       else if (col==ncols-1 && row==0) {
         this->b.push_back(1/(step*step)*Th); 
         this->A.AddEntry(eq_num,(col-1)*nrows,-1/(step*step));
         this->A.AddEntry(eq_num,0,-1/(step*step));
         this->A.AddEntry(eq_num,col*nrows+1,-1/(step*step));
         this->A.AddEntry(eq_num,col*nrows,4*1/(step*step));
         }

      // down left corner (cold and periodic)         
       else if (col == 0 && row==nrows-1) {
         this->b.push_back(1/(step*step)*-Tc*(exp(-10*(step*(float)col-len/2)\
            *(step*(float)col-len/2))-2)); 
         this->A.AddEntry(eq_num,row+(ncols-1)*nrows,-1/(step*step));
        this->A.AddEntry(eq_num,row+nrows,-1/(step*step));
         this->A.AddEntry(eq_num,row-1,-1/(step*step));
         this->A.AddEntry(eq_num,row,4*1/(step*step));
         }
         
        // down right corner (cold and periodic)
       else if (col==ncols-1 && row==nrows-1) {
         this->b.push_back(1/(step*step)*-Tc*(exp(-10*(step*(float)col-len/2)\
            *(step*(float)col-len/2))-2)); 
        this->A.AddEntry(eq_num,col*nrows+row-1,-1/(step*step));
         this->A.AddEntry(eq_num,(col-1)*nrows+row,-1/(step*step));
         this->A.AddEntry(eq_num,row,-1/(step*step));
         this->A.AddEntry(eq_num,col*nrows+row,4*1/(step*step));
         }
       eq_num++;
     }
  }
  return 0;
}

