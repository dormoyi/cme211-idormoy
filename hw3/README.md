## Provide a description of your code design to someone who has never read this assignment handout. 
The purpose of this code is to compute the stagnation point and lift coefficient of a wing for several
input coefficients. The wing is described by several points (x,y), so I created a class Point to 
represent the points and perform some basic operations (distance for example). 

The main purpose of the airfoil class is to contain the wing's information, it is to say its chord length,
its lift coefficient etc. This class needs methods to read the data files (load_data),
process the data to get the cl and stagnation point values (data_computation), and to
represent the computed data in a convenient way for the user (repr).


## Be sure to explain how the design illustrates key OOP concepts such as abstraction, decomposition, and encapsulation.
abstraction: the airfoil attributes represent key data to the airfoil: points, leading edge... The point class contains
two familiar attributes (x and y) and some intuitive functions (distance)

decomposition: the decomposition is esentially made in three parts: reading the data, processing it, and representing it

encapsulation: the details our data structure aren't shown to the user. The data representation choice made with lists, dicionnaries and points is hidden

## Also describe what error checking and exception generation you incorporated into your class implementation.
I checked for several error types:
- the directory is not valid
- xy.dat file is missing in the directory
- no alpha/pressure coefficient files in the directory 
- the format of the file is wrong (the line cannot be splitted and converted into a float)
