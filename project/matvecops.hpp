#ifndef MATVECOPS_HPP
#define MATVECOPS_HPP

# include <vector>

// l2 norm
double L2norm( std::vector<double> &vec);

// dot product
double dot(std::vector<double> &vec1, std::vector<double> &vec2);

// matrix - vector product
std::vector<double> mat_vec_prod(std::vector<double> &val,
             std::vector<int>    &row_ptr,
             std::vector<int>    &col_idx,
             std::vector<double> &x);

// sum of 2 vectors
std::vector<double> vec_sum(std::vector<double> &vec1, std::vector<double> &vec2);

// substraction of 2 vectors
std::vector<double> vec_sub(std::vector<double> &vec1, std::vector<double> &vec2);

// scalar multiplication
std::vector<double> scal_mult(std::vector<double> &v, double alpha);

#endif /* MATVECOPS_HPP */
