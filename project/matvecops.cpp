
#include <cmath>
#include <iostream>
#include <vector>

# include "matvecops.hpp"

// l2 norm
double L2norm( std::vector<double> &vec){
    int n = (int)vec.size();
    double sum = 0;
    for(int i=0; i< n; i++){
        sum = sum + vec[i]*vec[i];
    }
    sum = sqrt(sum);
    return sum;
}

// dot product
double dot(std::vector<double> &vec1, std::vector<double> &vec2){
    int n = (int)vec1.size();
    double sum = 0;
    for(int i=0; i< n; i++){
        sum = sum + vec1[i]*vec2[i];
    }
    return sum;
}

// matrix - vector product
std::vector<double> mat_vec_prod(std::vector<double> &val,
                            std::vector<int> &row_ptr,
                            std::vector<int> &col_idx,
                            std::vector<double> &vec) {
  std::vector<double> v(vec.size());
  for(unsigned int n=0; n<vec.size();n++)
    v[n] = 0;
    
  for(unsigned int n=0; n<row_ptr.size()-1; n++)
    for(int k=row_ptr[n]; k<row_ptr[n+1]; k++)
      v[n] += val[k]*vec[col_idx[k]];
      
  return v;
}

// sum 
std::vector<double> vec_sum(std::vector<double> &vec1, std::vector<double> &vec2){
    int n = (int)vec1.size();
    std::vector<double> vec_res(n);

    for(int i=0; i< n; i++){
        vec_res[i] = vec1[i] + vec2[i];
    }
    return vec_res;
}

// substraction
std::vector<double> vec_sub(std::vector<double> &vec1, std::vector<double> &vec2){
    std::vector<double> vec_res(vec1.size());
    int n = (int)vec1.size();

    for(int i=0; i< n; i++){
        vec_res[i] = vec1[i] - vec2[i];
    }
    return vec_res;
}

// scalar multiplication
std::vector<double> scal_mult(std::vector<double> &v, double alpha){
    int n = (int)v.size();
    std::vector<double> vec_res(n, 0.0);

    for(int i=0; i< n; i++){
        vec_res[i] = v[i] * alpha;
    }
    return vec_res;
}