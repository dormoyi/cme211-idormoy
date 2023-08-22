import sys
import time

def find_read(f2, genome, read, counter):
    """
    find reads in the genome
    updates the counters (read appears 1 time, 0 or 2)
    """
    in_genome = genome.find(read)
    # if the read doesn't appear
    if in_genome==-1:
        f2.write(read+ " -1\n")
        counter['none_count']+=1
        return
    in_genome2 = genome.find(read, in_genome+1, len(genome))
    # if the read appears once
    if in_genome2==-1:
        f2.write(read+ " "+ str(in_genome)+ "\n")
        counter['once_count']+=1
        return
    # the read appears twice
    f2.write(read+ " "+str(in_genome)+ " "+str(in_genome2)+"\n")
    counter['twice_count']+=1


if __name__ == '__main__':
    if len(sys.argv) !=4:
        print("Usage:")
        print(" $ python3 processdata.py <ref_file> <reads_file> <align_file>")
        sys.exit(0)
    # assign arguments
    ref_file, reads_file, align_file = sys.argv[1], sys.argv[2], sys.argv[3]
    counter = {'once_count':0, 'twice_count':0, 'none_count':0}

    # read the genome file
    f0 = open(ref_file, 'r')
    genome = f0.readlines()[0]
    f0.close()
    ref_length = len(genome)

    # get the reads
    f1 = open(reads_file, 'r')
    reads = f1.readlines()
    f1.close()

    # test every read
    begin = time.time()
    f2 = open(align_file, 'w')
    nreads=0
    for read in reads:
        nreads+=1
        find_read(f2, genome, read[:-1], counter)
    f2.close()

    # print output
    end = time.time() - begin
    print("reference length: ", ref_length)
    print("number reads: ", nreads)
    print("aligns 0: ", counter['none_count']/nreads)
    print("aligns 1: ", counter['once_count']/nreads)
    print("aligns 2: ", counter['twice_count']/nreads)
    print("elapsed time: ", end)
    