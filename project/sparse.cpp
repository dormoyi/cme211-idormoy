# include <iostream>
# include <vector>

# include "COO2CSR.hpp"
# include "sparse.hpp"

void SparseMatrix::AddEntry(int i, int j, double val){
    this->i_idx.push_back(i);
    this->j_idx.push_back(j);
    this->a.push_back(val);
}

void SparseMatrix::ConvertToCSR() {
    COO2CSR(this->a, this->i_idx, this->j_idx);
}

std::vector<int> SparseMatrix::get_i() {return this->i_idx;}
std::vector<int> SparseMatrix::get_j() {return this->j_idx;}
std::vector<double> SparseMatrix::get_a() {return this->a;}