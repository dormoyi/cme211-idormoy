#ifndef IMAGE_HPP
#define IMAGE_HPP

# include <string>

// convolution function
void Convolution(boost::multi_array<unsigned char,2>& input,
                 boost::multi_array<unsigned char,2>& output,
                 boost::multi_array<float,2>& kernel);

// image class
class Image {
private:
    std::string file_input;
    std::string file_output;
public:
    boost::multi_array<unsigned char, 2> image;
    Image(std::string file);
    void Save(std::string file);
    void Boxblur(int kernel_size);
    unsigned int Sharpness(boost::multi_array<unsigned char,2>& input);
};

# endif /* IMAGE_ HPP */