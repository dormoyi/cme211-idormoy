import math
import sys
import time

def create_dict(data_file):
    """
    creates a data structure dict[movie][user] = rating
    returns dict, movies_nb, lines_nb, users_nb
    """
    f1 = open(data_file, 'r')
    ratings = f1.readlines()
    f1.close()
    lines_nb = len(ratings)
    dic = {}
    users = set()

    for rating in ratings:
        user, movie, grade, _ = rating.split()
        users.add(user)
        if not movie in dic:
            dic[str(movie)] = {str(user): int(grade)}
        else:
            dic[str(movie)][str(user)]= int(grade)
    
    movies_nb = len(dic.keys())
    users_nb = len(users)
    return(dic, movies_nb, lines_nb, users_nb)

def scalar_product(r1, r2, movie1, movie2, common_keys):
    """
    input: r1 (average of the grades given to movie1), r2 (average of the grades
     given to movie2),
    movie1 (dict[movie1]), movie2 (dict[movie2])
    common_keys list of the common keys in the two dictionaries
    """
    product = 0
    for key in common_keys:
        product+=(movie1[key]-r1)*(movie2[key]-r2)
    return(product)


def similarity(dict, movie1, movie2, user_thresh):
    """
    returns the pearson similarity between 2 movies
    returns 0 if one of the movies has a 0 norm
    returns None if the number of common movies is below the threshold
    output format: score, number of raters
    """
    dictm1_set = set(dict[movie1].keys())
    dictm2_set = set(dict[movie2].keys())
    common_keys = dictm1_set.intersection(dictm2_set)
    if len(common_keys)<user_thresh:
        return None, None
    r1= sum(dict[movie1].values()) / float(len(dict[movie1]))
    r2= sum(dict[movie2].values()) / float(len(dict[movie2]))
    norm1=scalar_product(r1, r1, dict[movie1], dict[movie1], common_keys)
    norm2=scalar_product(r2, r2, dict[movie2], dict[movie2], common_keys)
    if norm1==0 or norm2==0:
        return 0, len(common_keys)
    return scalar_product(r1, r2, dict[movie1], dict[movie2], common_keys)/ \
        math.sqrt(norm1*norm2), len(common_keys)


def most_similar_movie(dict, user_thresh):
    """
    finds the most similar movie for each movie and writes the 
    results in the output_file 
    """
    values = []
    ordered_movies = [int(i) for i in dict.keys()]
    ordered_movies.sort()
    for movie1 in ordered_movies:
        movie1 = str(movie1)
        max_movie=None
        max_score=-2
        max_raters=0
        for movie2 in dict.keys():
            if movie1!=movie2:
                score, raters_nb = similarity(dict, movie1, movie2, user_thresh)
                if score!=None and score>max_score:
                    max_score=score
                    max_movie=movie2
                    max_raters=raters_nb
        values.append((movie1, max_movie, str(max_score), str(max_raters)))
    return(values)

def write_file(values, output_file):
    f = open(output_file, 'w')
    for val in values:
        if val[1]==None:
            f.write(str(val[0])+"\n")
        else:
            f.write(str(val[0])+" ("+val[1]+","+val[2]+","+val[3]+")\n")
    f.close()

if __name__ == '__main__':
    if len(sys.argv)!=3 and len(sys.argv)!=4:
        print("Usage:")
        print(" $ python3 similarity.py <data_file> <output_file>\
             [user_thresh (default = 5)]")
        sys.exit(0)
    # assign arguments
    data_file, output_file = sys.argv[1], sys.argv[2]
    if len(sys.argv)==4:
        user_thresh = int(sys.argv[3])
    else:
        user_thresh = 5

    start= time.time()

    dict, movies_nb, lines_nb, users_nb = create_dict(data_file)  

    values = most_similar_movie(dict, user_thresh)

    write_file(values, output_file)

    exec_time = time.time() - start
 
    print("Input MovieLens file: ", data_file)
    print("Output file for similarity data: ", output_file)
    print("Minimum number of common users: ", user_thresh)
    print("Read ", lines_nb, " lines with total of ",\
         movies_nb, " movies and ", users_nb, " users")
    print("Computed similarities in ", exec_time, " seconds")