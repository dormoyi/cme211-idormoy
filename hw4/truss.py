
import math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.sparse.linalg
from scipy.sparse import csr_matrix
import warnings


class Truss():
    def __init__(self, joints_file, beams_file, output_file=None):
        """
        input: joints_file, beams_file -> names of the joints and beams files
        structure chosen: 2 dictionnaries
        joints_dict={'1': {'coords': (x1, x2), 'F': (Fx, Fy), \
            'R': 0, (support reaction?)\
             'beams': ['1', '2'] (list of beams connected to the joint)}
        beams_dict={'1' (beam number): ('1', '2' (joints number))}
        """
        self.joints_file = joints_file
        self.beams_file = beams_file
        self.output_file = output_file
        self.joints_dict, self.beams_dict, self.reac = self.load_files()

    def load_files(self):
        """
        loads the files joints.dat and beams.dat
        output: joints_dict and beams_dict described in __init__
        and reac = [0,0,1] means J1, J2 don't have reaction, J3 has a reaction
        """
        # reads the joints file
        f = open(self.joints_file, 'r')
        joints = f.readlines()[1:]
        f.close()
        joints_dict = {}
        reac = []
        for joint in joints:
            joint = joint.split( )
            joints_dict[joint[0]] = {}
            joints_dict[joint[0]]['coords']=(float(joint[1]),float(joint[2]))
            joints_dict[joint[0]]['F']=(float(joint[3]),float(joint[4]))
            joints_dict[joint[0]]['R']=int(joint[5])
            joints_dict[joint[0]]['beams']=[]
            reac.append(int(joint[5]))
        
        # read the beams file
        f = open(self.beams_file, 'r')
        beams = f.readlines()[1:]
        f.close()
        beams_dict={}
        for beam in beams:
            beam = beam.split()
            beams_dict[beam[0]] = (beam[1],beam[2])
            joints_dict[beam[1]]['beams'].append(beam[0])
            joints_dict[beam[2]]['beams'].append(beam[0])
        return joints_dict, beams_dict, reac

    def calc_coeff(self, pt1, pt2, case):
        """
        computes the coefficient in the matrix A of the linear system
        input: pt1 (str), pt2 (str), case ('x' or 'y')
            pt1 and pt2 are the numbers of the joints
            pt1 is the point of the joint which equation is being considered
            case 'x' if we compute the coefficient on x axis 
            equation, otherwise y
        output: coefficient of A (float)
        """
        J1x = self.joints_dict[pt1]['coords'][0]
        J2x = self.joints_dict[pt2]['coords'][0]
        J1y = self.joints_dict[pt1]['coords'][1]
        J2y = self.joints_dict[pt2]['coords'][1]

        delta_y = J1y - J2y
        delta_x = J1x - J2x

        norm = math.sqrt(delta_x**2 + delta_y**2)
        if case=='x':
            return(delta_x/norm)
        if case=='y':
            return(delta_y/norm)


    def create_system(self):
        """
        creates the A and b matrices to solve the Ax = b system
        A is a sparse matrix created with the data, rows and cols lists
        output: A and B matrices
        """
        eq_nb = len(self.joints_dict)*2
        inc_nb = len(self.beams_dict) + sum(self.reac)*2
        B = np.zeros((eq_nb, 1))

        # error handling
        if eq_nb!=inc_nb:
            error = 'Truss geometry not suitable for static equilbrium analysis'
            raise RuntimeError(error)

        data, rows, cols = [], [], []


        for ix in range(0, len(self.joints_dict)):
            # create equation on x
            B[2*ix][0] = -self.joints_dict[str(ix+1)]['F'][0]
            # add beams forces
            beams = self.joints_dict[str(ix+1)]['beams']
            for beam in beams:
                points = self.beams_dict[beam]
                pt1 = str(ix+1)
                if pt1==points[0]:
                    pt2 = points[1]
                else:
                    pt2=points[0]
                coeff = self.calc_coeff(pt1, pt2, 'x')

                if coeff!=0:
                    data.append(coeff)
                    rows.append(2*ix)
                    cols.append(int(beam)-1)
            # add reaction forces
            if self.joints_dict[str(ix+1)]['R']:
                col_rx = len(self.beams_dict)+sum(self.reac[:ix])*2

                if coeff!=0:
                    data.append(1)
                    rows.append(2*ix)
                    cols.append(col_rx)

            # create equation on y
            B[2*ix+1][0] = -self.joints_dict[str(ix+1)]['F'][1]
            # add beams forces
            beams = self.joints_dict[str(ix+1)]['beams']
            for beam in beams:
                points = self.beams_dict[beam]
                pt1 = str(ix+1)
                if pt1==points[0]:
                    pt2 = points[1]
                else:
                    pt2=points[0]
                coeff = self.calc_coeff(pt1, pt2, 'y')
                if coeff!=0:
                    data.append(coeff)
                    rows.append(2*ix+1)
                    cols.append(int(beam)-1)
            # add reaction forces
            if self.joints_dict[str(ix+1)]['R']:
                data.append(1)
                rows.append(2*ix+1)
                cols.append(col_rx+1)

        D = csr_matrix((data, (rows, cols)), shape=(eq_nb, inc_nb))
        return(D, B)



    def PlotGeometry(self):
        """
        show the geometry of the truss
        """
        max_x,min_x, max_y, min_y = -10E8,10E8,-10E8,10E8
        for beam in self.beams_dict.values():
            point1,point2 = beam[0], beam[1]
            x1,y1 = self.joints_dict[point1]['coords'][0], \
                self.joints_dict[point1]['coords'][1]
            x2,y2 = self.joints_dict[point2]['coords'][0], \
                self.joints_dict[point2]['coords'][1]
            plt.plot([x1,x2], [y1,y2], color='b')

            if x1>max_x:
                max_x=x1
            if x2>max_x:
                max_x=x2
            if x1<min_x:
                min_x=x1
            if x2<min_x:
                min_x=x2

            if y1>max_y:
                max_y=y1
            if y2>max_y:
                max_y=y2
            if y1<min_y:
                min_y=y1
            if y2<min_y:
                min_y=y2

        #ax.set(xlim=(xmin, xmax), ylim=(ymin, ymax))
        plt.xlim(min_x - 0.2, max_x + 0.2)
        plt.ylim(min_y - 0.2, max_y + 0.2)

        if self.output_file:
            plt.savefig(self.output_file)


    def solve_system(self, A, B):
        """
        solves the system Ax=B, returns x
        """
        warnings.filterwarnings('error')
        try:
            x = scipy.sparse.linalg.spsolve(A, B)
        except:
            error="Cannot solve the linear system, unstable truss?"
            raise RuntimeError(error)
            sys.exit(1)
        return x

    def __repr__(self):
        """
        solves the system and returns the result
        """
        A, B = self.create_system()
        x = self.solve_system(A, B)
        inc_nb = len(self.beams_dict)

        output=""
        output+=" Beam     Force\n"
        output+="-----------------\n"
        for i in range(inc_nb):
            token = " "
            if str(x[i])[0]=="-":
                token=""
            output+="  "+str(i+1) + "    " + token + "%0.3f\n"%x[i]
        return output