import glob
import math
import os

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def distance(self, point2):
        """
        returns the distance between two points
        """
        changex = self.x - point2.x
        changey = self.y - point2.y
        return math.sqrt(changex**2 + changey**2)

    def delta(self, point2):
        """
        returns delta_x = point2.x - point1.x
        and delta_y = point2.y - point1.y
        """
        delta_x = self.x - point2.x
        delta_y = self.y - point2.y
        return(-delta_x, -delta_y)

    def __repr__(self):
        """
        represents a point as (x,y), only useful for debugging
        """
        return("("+ str(self.x)+","+ str(self.y)+ ")")



class Airfoil:
    def __init__(self, inputdir):
        """
        initiate the class which has 7 attributes:
        - inputdir: the input directory with all the files used
        - Cps: a dicionnary containing a list of the pressure coefficients for
        each angle
        - points: a list containing the points describing the wings 
        (point objects)
        - leading_edge: a point object describing the leading edge
        - trailing_edge: a point object describing the trailing edge
        - chord: the chord length of the wing
        - data summary: a dicionnary containing a dicionnary containing 
        the stagnation point and the coefficient for each angle
        """
        self.inputdir = inputdir
        self.Cps, self.points, self.leading_edge, self.trailing_edge \
            = self.load_data()
        self.chord = \
            self.chord_length(self.leading_edge, self.trailing_edge)
        self.data_summary = self.data_computation()

    def get_file_name(self):
        """
        returns the file number of the naca case
        ex: 0012, 2412
        """
        i = self.inputdir.find("naca")
        return self.inputdir[i+4:i+8]

    def __repr__(self):
        """
        returns a string containing the desired output
        """
        string = "Test case: NACA "
        string+= self.get_file_name()+"\n\n"

        ordered_angles = [i for i in self.data_summary.keys()]
        ordered_angles.sort()
        string+=" alpha    cl          stagnation pt   \n"
        string+=" -----  ------  --------------------------\n"
        for angle in ordered_angles:
            if len(str(angle)) == 3:
                string += " " 
            string += " %0.2f " % angle
            if round(self.data_summary[angle]['cl'],4)==0:
                self.data_summary[angle]['cl']=0
            if self.data_summary[angle]['cl']>=0:
                string+=" "
            string += "%0.4f " % self.data_summary[angle]['cl']
            string +=" ("
            if self.data_summary[angle]['stagnation_point'][0]>=0:
                string+=" "
            string += "%0.4f, "%self.data_summary[angle]['stagnation_point'][0]
            if self.data_summary[angle]['stagnation_point'][1]>=0:
                string+=" "
            string += "%0.4f) "%self.data_summary[angle]['stagnation_point'][1]
            if self.data_summary[angle]['pressure_coefficient']>=0:
                string+=" "
            string += "%0.4f\n"%self.data_summary[angle]['pressure_coefficient']
        return(string[:-1])

    def load_data(self):
        """
        loads the files from the inputdir
        returns: 
            - points: a list of Point objects
            - angles: a dictionnary containing a list of Cps for each angle
                      angles[angle] = Cps_list
            - the leading edge and the trailing edge (point objects)
        """
        Cps = {}
        points = []

        # check if the directory is valid
        if not os.path.exists(self.inputdir):
            raise RuntimeError("the directory is not valid")

        # read the xy.dat file
        # we find the leading and trailing edges at the same time to avoid
        # a O(n) computation later
        try:
            f = open(self.inputdir + os.sep + "xy.dat",'r')
        except:
            raise RuntimeError("xy.dat cannot be found in the directory")
        lines = f.readlines()
        f.close()
        x_max = Point(-10E8, 0)
        x_min = Point(10E8, 0)
        for line in lines[1:]:
            try:
                tmp = line.split()
            except:
                raise RuntimeError("xy.dat format wrong")
            x = float(tmp[0])
            y = float(tmp[1])
            points.append(Point(x, y))

            if x<x_min.x:
                x_min = Point(x, y)
            if x>x_max.x:
                x_max = Point(x, y)

        # read the alpha files
        alpha_files = glob.glob("./"+self.inputdir+ "/alpha*.dat")
        for file in alpha_files:
            name = file.split(os.sep)[-1][5:-4]
            angle = float(name)

            f = open(file,'r')
            lines = f.readlines()
            f.close()

            coefficients = []
            for line in lines[1:]:
                try:
                    coefficients.append(float(line.split()[0]))
                except:
                    raise RuntimeError(str(file)+" format wrong")
            Cps[angle] = coefficients
        
        if len(alpha_files)==0:
            raise RuntimeError("no alphaXXXX.dat files in the directory")

        return Cps, points, x_min, x_max

    def chord_length(self, point1, point2):
        """
        computes the chord length
        """
        return point1.distance(point2)

    def data_computation(self):
        """
        returns data summary,
        a dicionnary containing a dicionnary containing 
        the stagnation point and the coefficient for each angle
        """
        data_summary = {}

        for angle in self.Cps.keys():
            angle_summary = {'cl':0, 'stagnation_point':(0,0),\
                 'pressure_coefficient': -10E8}
            cx, cy = 0, 0

            # we calculate the stagnation point and the lift coefficient at
            # the same time to avoid a O(n) computation
            for i in range(len(self.points)-1):
                delta_x, delta_y = self.points[i].delta(self.points[i+1])
                delta_cx = - self.Cps[angle][i] * delta_y / self.chord
                delta_cy = self.Cps[angle][i] * delta_x / self.chord
                cx += delta_cx
                cy += delta_cy

                if self.Cps[angle][i]>angle_summary['pressure_coefficient']:
                    angle_summary['pressure_coefficient'] = self.Cps[angle][i]
                    x = (self.points[i].x + self.points[i+1].x)/2
                    y = (self.points[i].y + self.points[i+1].y)/2
                    angle_summary['stagnation_point'] = (x,y)

            angle_rad = math.radians(angle)
            cl = cy * math.cos(angle_rad) - cx * math.sin(angle_rad)
            angle_summary['cl'] = cl
            data_summary[angle] = angle_summary
        return(data_summary)