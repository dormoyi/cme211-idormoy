from readline import insert_text
import sys
import random

def generate_base_sequence(file, ref_length):
    """
    generates a string genome sequence of ref_length length
    including A, C, G, T letters
    output: the generated string
    """
    letters = ["A", "C", "G", "T"]
    genome = ""
    # the +ref_length%4 in next calculus is to integrate the case when ref_length is not divisible by 4
    # for a 14 string length, we put AGA | TGU | ATC | TT | ATC
    # to integrate those two letters that are missing
    first_75_percent = (ref_length//4)*3 +ref_length%4
    for _ in range(first_75_percent):
        letter_category = random.randint(0,3)
        genome+= letters[letter_category]
    last_25_percent = ref_length//4
    for i in range(last_25_percent):
        genome+=genome[(ref_length//4)*2+i]
    assert len(genome) == ref_length
    file.write(genome)
    return(genome)

def once_read(f1, ref_length, genome, read_len):
    """
    returns a str read of read_len length
    copied from the first 50% part of the genome
    """
    which_read = random.randint(0, ref_length//4*2)
    read = ""
    for i in range(read_len):
        read += genome[which_read + i]
    f1.write(read+ "\n")
    #f2.write(read+ " "+ str(which_read)+ "\n")

def twice_read(f1, ref_length, genome, read_len):
    """
    returns a str read of read_len length
    copied from the last 25% part of the genome
    """
    last_25_percent = (ref_length//4)*3 +ref_length%4
    which_read = random.randint(last_25_percent, ref_length-read_len)
    read = ""
    for i in range(read_len):
        read += genome[which_read + i]
    which_read2 = which_read - ref_length//4 - ref_length%4
    assert genome[which_read]==genome[which_read2]
    f1.write(read+ "\n")
    #f2.write(read+ " "+str(which_read2)+ " "+str(which_read)+"\n")

def generate_read(read_len):
    """
    returns a str read of length read_len
    """
    letters = ["A", "C", "G", "T"]
    read = ""
    for _ in range(read_len):
        letter_category = random.randint(0,3)
        read+= letters[letter_category]
    return(read)

def none_read(f1, read_len, genome):
    """
    returns a str read which does not appear in the genome
    """
    in_genome=1
    while in_genome!=-1:
        read = generate_read(read_len)
        in_genome = genome.find(read)
    f1.write(read+ "\n")
    #f2.write(read+ " -1\n")

if __name__ == '__main__':
    if len(sys.argv) !=6:
        print("Usage:")
        print(" $ python3 generatedata.py <ref_length> <nreads> <read_len> <ref_file> <reads_file>")
        sys.exit(0)
    # assign arguments
    ref_length, nreads, read_len, ref_file, reads_file = int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), sys.argv[4], sys.argv[5]

    f0 = open(ref_file, 'w')
    genome = generate_base_sequence(f0, ref_length)
    f0.close()

    once_rate, twice_rate, none_rate = 0.75, 0.10, 0.15
    once_count, twice_count, none_count = 0, 0, 0

    f1 = open(reads_file, 'w')
    for i in range(nreads):
        align_category = random.random()
        # determine how many times the read will appear

        if align_category < once_rate:
            # the string should appear once
            once_read(f1, ref_length, genome, read_len)
            once_count+=1

        elif (1 - align_category)  < none_rate:
            # the string should not appear
            none_read(f1, read_len, genome)
            none_count+=1

        else:
            # the string should appear twice
            twice_read(f1, ref_length, genome, read_len)
            twice_count+=1
    f1.close()



    print("reference length: ", ref_length)
    print("number reads: ", nreads)
    print("read length: ", read_len)
    print("aligns 0: ", none_count/nreads)
    print("aligns 1: ", once_count/nreads)
    print("aligns 2: ", twice_count/nreads)