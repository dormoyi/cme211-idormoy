## Brief statement of the problem.
Implement an image class that can read and write JPEG files, and has
methods to compute the sharpness of the image and smooth (blur) the image using 
a box blur kernel of a specified size. The sharpness and blurring steps are 
performed thanks to a convolution function.

## Description of your C++ code.
Here are the steps of the algorithm:
- Loading the original image and outputting the sharpness
- For kernel sizes of 3, 7, . . . , 23, 27
- Reload the original image 
- Blur the image
- Compute and output the sharpness of the resulting image
- Save the output image

## Structure of the functions/class
We use an image class to represent the image on which we are performing 
computations with an array. Here is how the Image class is implemented \
Attributes:
- std::string file_input
- std::string file_output \
Functions:
- Image(std::string file) - constructor of the class
- void Save(std::string file) - method to save the output image
- void Boxblur(int kernel_size) - method to blur the image - calls the 
convolution function
- unsigned int Sharpness(boost::multi_array<unsigned char,2>& input) - method
to compute the sharpness of an image - calls the convolution function

## The convolution function
This is the main function, necessary for the implementation of the boxblur 
and sharpness functions. The idea is to apply a kernel filter on the image.
Before applying this filter, it is necessary to perform padding of the input
image to be able to perform the kernel computation on the edges. 
