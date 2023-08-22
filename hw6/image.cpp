# include <boost/multi_array.hpp>
# include <iostream>
# include <string>

#include "image.hpp"
#include "hw6.hpp"


boost::multi_array<unsigned char, 2> arr;
// constructor of the class Image
Image::Image(std::string file) {
this-> file_input = file;
ReadGrayscaleJPEG(file, this->image);
}

// save method to save the method as a jpg image
void Image::Save(std::string file) {
    // use original filename if string is empty
    if (file.length()==0){
        file = this->file_input;
    }
    WriteGrayscaleJPEG(file, this->image);
}

// boxblur method
void Image::Boxblur(int kernel_size){
    int i_input = (int)this->image.shape()[0];
    int j_input = (int)this->image.shape()[1];
    boost::multi_array<float, 2> kernel(boost::extents[kernel_size][kernel_size]);
    boost::multi_array<unsigned char, 2> output(boost::extents[i_input][j_input]);
    
    // creating the array
    for (int i=0;i<kernel_size;i++) {
      for (int j=0;j<kernel_size;j++) {
        kernel[i][j] = 1.f/(float)(kernel_size*kernel_size);
     }
    }
    // calling the convolution function
    Convolution(this->image, output,kernel);
    this->image = output;
}

// sharpness method
unsigned int Image::Sharpness(boost::multi_array<unsigned char,2>& input){
    // creating the kernel array
    boost::multi_array<float, 2> kernel(boost::extents[3][3]);
    kernel[0][0]=0;
    kernel[1][0]=1;
    kernel[2][0]=0;
    kernel[0][1]=1;
    kernel[1][1]=-4;
    kernel[2][1]=1;
    kernel[0][2]=0;
    kernel[1][2]=1;
    kernel[2][2]=0;

    int i = (int)input.shape()[0];
    int j = (int)input.shape()[1];
    boost::multi_array<unsigned char, 2> output(boost::extents[i][j]);

    // calling the convolution function
    Convolution(input, output,kernel);

    // compute max output sharpness
    unsigned int max = *std::max_element(output.origin(), output.origin() + \
    output.num_elements());
    return max;
}

// convolution method
void Convolution(boost::multi_array<unsigned char,2>& input,
boost::multi_array<unsigned char,2>& output,
boost::multi_array<float,2>& kernel) {
    // Test for odd size, square kernels of at least size 3
    if (kernel.shape()[0] != kernel.shape()[1] || kernel.shape()[0]<3 || 
    kernel.shape()[0] % 2 == 0){
        throw std::runtime_error("misspecified kernel");
    }

    // create a bigger array with necessary padding
    int ni = (int)input.shape()[0];
    int nj = (int)input.shape()[1];
    int ik_mid = (int)(kernel.shape()[0] / 2);
    int new_ni = 2*ik_mid + ni;
    int new_nj = 2*ik_mid + nj;
    boost::multi_array<double, 2> padded(boost::extents[new_ni][new_nj]);

    for (int i=0; i<new_ni; i++){
        for (int j=0; j<new_nj;j++){
            // top left corner
            if (i<ik_mid && j<ik_mid){
                padded[i][j]=input[0][0];} 
            // bottom left corner
            else if (i>=ni+ik_mid && j<ik_mid){
                 padded[i][j]=input[ni-1][0];}
            // top right corner
            else if (i<ik_mid && j>=nj+ik_mid){
                 padded[i][j]=input[0][nj-1];}
            // bottom right corner
            else if (i>=ni+ik_mid && j>=nj+ik_mid){
                 padded[i][j]=input[ni-1][nj-1];}
            // left edge
            else if (j<ik_mid){
                padded[i][j]=input[i-ik_mid][0];}
            // upper edge
            else if (i<ik_mid){
                padded[i][j]=input[0][j-ik_mid];} 
            // right edge
            else if (j>=nj+ik_mid){
                padded[i][j]=input[i-ik_mid][nj-1];}
            // bottom edge
            else if (i>=ni+ik_mid){
                padded[i][j]=input[ni-1][j-ik_mid];}
            // non-padded parts
            else {
                padded[i][j]=input[i-ik_mid][j-ik_mid];}
        }
    }

    // perform the convolution
    double new_pixel;    
    for (int i = 0; i < ni; i++) {
        for (int j = 0; j < nj; j++) {
            new_pixel = 0;
            for (int ik = 0; ik < (int)kernel.shape()[0]; ik++)
                for (int jk= 0; jk < (int)kernel.shape()[1]; jk++)
                    new_pixel += kernel[ik][jk]*padded[i+ik][j+jk];

            // handling overflow/underflow
            if (new_pixel < 0)
                output[i][j] = (unsigned char) 0;
            else if (new_pixel > 255)
                output[i][j] = (unsigned char) 255;
            else{
                output[i][j] = (unsigned char) new_pixel;
            }
        }
    }
}