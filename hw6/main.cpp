# include <boost/multi_array.hpp>
# include <iostream>
# include <string>
# include <vector>

# include "image.hpp"
# include "hw6.hpp"

int main () {

    // Loading the original image and outputting the sharpness
    std::string file = "stanford.jpg";
    Image img(file);
    unsigned int a = img.Sharpness(img.image);
    std::cout << "Original image: " << a << " "; 
    
    std::vector<Image> images;
    std::string filename;
    int i=0;

    for (int k=3; k<28; k=k+4){
        // Reload the original image 
        images.push_back(img);
        // Blur the image
        images[i].Boxblur(k);

        // Compute and output the sharpness of the resulting image
        a = images[i].Sharpness(images[i].image);
        std::cout << "Boxblur(" << k << "): " << a << " ";

        // Save the output image
        filename = "BoxBlur";
        if (k<10){
            filename+= "0";}
        filename+=std::to_string(k) + ".jpg";
        images[i].Save(filename);
        i++;
    }

    std::cout << std::endl;

return 0; 

}