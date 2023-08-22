# Part 1 writeup


### 1. What were your considerations when creating this test data?
I created a test data similar to the type of input that we would like to pass to the data (described in the next question). I made this case pretty simple to be able to verify the output easily. I also created an other test which made it more complicated to verify the solution, but included some special cases: include the null case in the scalar product, different number of raters for movies (to test different thesholds), put a movie only rated by one user...


### 2. Were there certain characteristics of the real data and file format that you made sure to capture in your test data?
I made sure to choose random numbers for the movies and users IDs. The grades were also pretty varied. I also made sure that I didn't replicate replicate some lines (a user cannot grade a movie two times!). 

### 3. Did you create a reference solution for your test data? If so, how?
I did not computed a reference solution, although it would have been possible. I instead tryed to create an example with movies that seemed similar and check that the correlation values vary accordingly to that. As an example, 34 and 473 are positively correlated in my example. On the contrary, 6 and 34 are negatively correlated.

# Part 2 writeup

### 1. Include a command line log of using your program to compute similarities on the ml-100k/u.data data file. Also include the first 10 lines of the output similarity file.

python3 similarity.py ml-100k/u.data similarities.txt  
Input MovieLens file:  ml-100k/u.data  
Output file for similarity data:  similarities.txt  
Minimum number of common users:  5  
Read  100000  lines with total of  1682  movies and  943  users  
Computed similarities in  70.70288133621216  seconds  


### 2. Briefly explain in no more than one paragraph the decomposition of your program in terms of functions.

**create_dict(data_file):** function used to create the data structure (dictionary of dictionaries) used to solve the problem   
**scalar_product(r1, r2, movie1, movie2, common_keys):** computes the scalar product between two "lists" (here those are dicionnaries)   
**similarity(dict, movie1, movie2, user_thresh):** returns the similarity of two movies   
**most_similar_movie(dict, user_thresh):** finds the most similar movie for each movie   
**write_file(values, output_file):** writes the results in the output file   
