import truss
import sys

if __name__ == '__main__':
    if len(sys.argv) !=3 and len(sys.argv) !=4:
        print("Usage:")
        print(" $ python3 main.py [joints file] [beams file] [optional plot output file]")
        sys.exit(0)

    joints_file, beans_file = sys.argv[1], sys.argv[2]

    if len(sys.argv)==4:
        output_file = sys.argv[3]
        structure = truss.Truss(joints_file, beans_file, output_file) 
    else:
        structure = truss.Truss(joints_file, beans_file) 

    structure.PlotGeometry()
    print(structure)
    

