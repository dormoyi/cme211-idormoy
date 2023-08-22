# include <iostream>

# include "CGSolver.hpp"
# include "matvecops.hpp"

std::vector<std::vector<double>> CGSolver(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &b,
             std::vector<double> &x,
             double              tol){

    /* Function that implements the CG algorithm for a linear system
    *
    * Ax = b
    *
    * where A is in CSR format.  The starting guess for the solution
    * is provided in x, and the solver runs a maximum number of iterations
    * equal to the size of the linear system.  Function returns the
    * number of iterations to converge the solution to the specified
    * tolerance, or -1 if the solver did not converge.
    * 
    * 
    * MODIFICATION IN COMPARISON TO PART 1:
    * returns a vector of solution vectors
    */

    // initializations
    std::vector<double> u = x;
    std::vector<double> r;
    std::vector<double> rnew;
    std::vector<double> p;
    int niter;
    int nitermax = 100000; 
    double L2normr0;
    double L2normr;
    double alpha;
    double beta;
    std::vector<double> tmp1;
    std::vector<double> tmp2;
    std::vector<double> tmp3;
    std::vector<double> tmp4;
    std::vector<double> tmp5;

    std::vector<std::vector<double>> sols;
    
    // CG algorithm
    std::vector<double> tmp0 = mat_vec_prod(val, row_ptr,col_idx,u);
    r = vec_sub(b, tmp0);
    L2normr0 = L2norm(r);
    p = r;
    niter = 0;
    while (niter < nitermax){ 
        niter = niter + 1;
        
        tmp1 = mat_vec_prod(val, row_ptr,col_idx,p);
        alpha = dot(r,r) /dot(p, tmp1);

        tmp2 = scal_mult(p, alpha);
        u = vec_sum(u, tmp2);

        if (niter==1 ||  niter % 10 == 0) {
            sols.push_back(u); }

        tmp3 = mat_vec_prod(val, row_ptr,col_idx,p);
        tmp4 = scal_mult(tmp3, alpha);
        rnew = vec_sub(r, tmp4);

        L2normr = L2norm(rnew);
        if (L2normr/L2normr0 < tol){
            if (!(niter % 10 == 0))
                sols.push_back(u);
            x = u;
            std::cout << "SUCCESS: CG solver converged in " << niter << 
            " iterations" << std::endl;
            return sols;
        }
        beta = dot(rnew, rnew)/dot(r,r);
        r = rnew;
        tmp5 = scal_mult(p, beta);
        p = vec_sum(r, tmp5);
    }

    return sols;
}