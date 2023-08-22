#ifndef SPARSE_HPP
#define SPARSE_HPP

#include <vector>

class SparseMatrix
{
  private:
    std::vector<int> i_idx; // line indexes
    std::vector<int> j_idx; // cols indexes
    std::vector<double> a; // values in the matrix
    int ncols;
    int nrows;


  public:
    /* Method to modify sparse matrix dimensions */
    
    //void Resize(int nrows, int ncols);

    /* Method to add entry to matrix in COO format */
    void AddEntry(int i, int j, double val);

    /* Method to convert COO matrix to CSR format using provided function */
    void ConvertToCSR();

    /* Method to perform sparse matrix vector multiplication using CSR formatted matrix */
    
    //std::vector<double> MulVec(std::vector<double> &vec);

    // methods to retrive the private arguments 
    std::vector<int> get_i();
    std::vector<int> get_j();
    std::vector<double> get_a();
    
};

#endif /* SPARSE_HPP */