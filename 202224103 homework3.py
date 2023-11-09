import math
import random
import matplotlib.pyplot as plt

###############################################################
# Function Definitions
###############################################################


# Compute distance between two points
def distance(pt1, pt2):
    return math.sqrt((pt1[0] - pt2[0]) ** 2 + (pt1[1] - pt2[1]) ** 2)


# Rotate a point by theta radians
def rotation(theta, pt):
    """
    theta: angle in radians
    pt: point to be rotated
    """
    len_x = pt[0] * math.cos(theta) - pt[1] * math.sin(theta)
    len_y = pt[0] * math.sin(theta) + pt[1] * math.cos(theta)
    len = (len_x, len_y)
    return len
    


# Find the left-bottom most and right-top most points
def find_end_pts(ch_list):
    """
    ch_list: list of points in all pollygons
    """
    
    left_most = ch_list[0]
    right_most = ch_list[0]
    
    for i in range(len(ch_list)):
        if left_most[0] > ch_list[i][0]: # and left_most[1] > ch_list[i][1]:
            left_most = ch_list[i]
        elif left_most[0] == ch_list[i][0] and left_most[1] > ch_list[i][1]:
            left_most = ch_list[i]
        if right_most[0] < ch_list[i][0]: # and right_most[1] < ch_list[i][1]:
            right_most = ch_list[i]
        elif right_most[0] == ch_list[i][0] and right_most[1] > ch_list[i][1]:
            right_most = ch_list[i]

    return left_most, right_most



# Gets the slope of a line given two points
def get_slope(pt1, pt2, move_right, ext_pt):
    """
    pt1: first point
    pt2: second point
    move_right: boolean value to indicate whether the convex hull is moving right or left
    ext_pt: the point that is not on the convex hull
    """
    
    if move_right:
        if pt1 == ext_pt:
            return math.inf
        else:
            if pt2[0] > pt1[0]:
                return (pt2[1]-pt1[1])/(pt2[0]-pt1[0])
            else:
                return math.inf
    else:
        if pt1 == ext_pt:
            return math.inf
        else:
            if pt2[0] < pt1[0]:
                return (pt2[1]-pt1[1])/(pt2[0]-pt1[0])
            else:
                return math.inf

    


# Compute the convex hull of a list of points    
def compute_convex_hull(ch_list):
    cvx_hull = []

    left_most, right_most = find_end_pts(ch_list)
    
    cvx_hull.append(left_most)
    move_right = True

    cur_pt = cvx_hull[0]
    ch_list.sort(key=lambda x: get_slope(cur_pt, x, move_right, right_most))

    while len(cvx_hull) == 1 or (len(cvx_hull) != 1 and left_most != cvx_hull[-1]):
        # Just for your step-by-step debugging - If you need it, just uncomment it
        # print(f"\tMove Right: {move_right} Current Point: {cur_pt}, Convex Hull: {cvx_hull} Sorted List: {ch_list}")
        # print(cur_pt, ch_list[0])
        # input()

        cvx_hull.append(ch_list[0])

        cur_pt = cvx_hull[-1]
        if cur_pt == right_most:
            move_right = False

        if move_right:
            ch_list.sort(key=lambda x: get_slope(cur_pt, x, move_right, right_most))
        else:
            ch_list.sort(key=lambda x: get_slope(cur_pt, x, move_right, left_most))

    return cvx_hull, left_most, right_most

# Print and draw the polygons and convex hull
def print_and_draw(polygons, cvx_hull, left_most, right_most):
    plt.grid(True)
 
    for i, poly in enumerate(polygons):
        print(i, poly.name, poly.pt_list)
        print(f"\tPerimeter: {poly.get_perimeter()}") 
        print(f"\tArea: {poly.get_area()}")

        plt.plot([item[0] for item in poly.cy_list], [item[1] for item in poly.cy_list], 'k--')

    plt.plot([item[0] for item in cvx_hull], [item[1] for item in cvx_hull], 'r-')
    plt.plot(left_most[0], left_most[1], 'ro')
    plt.plot(right_most[0], right_most[1], 'bo')
    

    plt.axis('equal')
    plt.show()


###############################################################
# Class Definitions
###############################################################

# Parent Class
class Shape:
    def __init__(self, name):
        self.name = name

# Child Class - Triangle
class Triangle(Shape):
    NUM_OF_EDGES = 3

    def __init__(self, pt_list, name):
        """
        pt_list: list of points of the triangle
        cy_list: list of points of the triangle with the first point appended to the end
        length_list: list of lengths of the triangle
        """
        super().__init__(name)
        self.pt_list = pt_list
	    # Your codes must be below
        self.pt_list = pt_list
        self.cy_list = self.pt_list + [self.pt_list[0]] 
        self.length_list = []
        

    def get_perimeter(self):
        """
        Use distance() function to fill out the length_list if needed, 
	    and then to calculate perimeter of a triangle
        """
        for i in range(len(self.pt_list)):
            self.length_list.append(distance(self.cy_list[i], self.cy_list[i+1]))
        return sum(self.length_list)

        

    def get_area(self):
        """
        Use distance() function to fill out the length_list if needed, 
	    and then apply the Heron's Formula: s = (a + b + c)/2, A = sqrt(s(s-a)(s-b)(s-c))
        """
        s = sum(self.length_list)/2 
        return s
        
        
  

# Child Class - Rectangle
class Rectangle(Shape):
    NUM_OF_EDGES = 4

    def __init__(self, pt_list, name):
        """
        pt_list: list of points of the rectangle
        cy_list: list of points of the rectangle with the first point appended to the end
        length_list: list of lengths of the rectangle
        """        
        super().__init__(name)
        self.pt_list = pt_list
	    # Your codes must be below
        self.pt_list = pt_list
        self.cy_list = self.pt_list + [self.pt_list[0]] 
        self.length_list = []

    def get_perimeter(self):
        """
        Use distance() function to fill out the length_list if needed, 
	    and then calculate perimeter of a rectangle
        """
        for i in range(len(self.pt_list)):
            self.length_list.append(distance(self.cy_list[i], self.cy_list[i+1]))
        return sum(self.length_list)

    def get_area(self):
        """
        Use distance() function to fill out the length_list if needed, 
	    and then apply the formula: A = w * h
        """
        A = self.length_list[0] * self.length_list[1]
        return A


###############################################################
# Main Function
###############################################################

def main():
    polygons = []
    for i in range(10):
        # Triangle Generation
        if random.randint(0, 1) == 0:
            pt_list = [(random.randint(-10, 10), random.randint(-10, 10)), (random.randint(-10, 10), random.randint(-10, 10))]
            
            # The third point should not be on the same line as the first two points
            pt = (random.randint(-10, 10), random.randint(-10, 10))            
            while math.atan2(pt_list[0][1]-pt[1], pt_list[0][0]-pt[0]) == math.atan2(pt_list[1][1]-pt[1], pt_list[1][0]-pt[0]):
                pt = (random.randint(-10, 10), random.randint(-10, 10))

            pt_list.append(pt)

            polygons.append(Triangle(pt_list, name="Triangle"))
        # Rectangle Generation
        else:
            width = random.randint(1, 8)
            height = random.randint(1, 8)
            center = (random.randint(-10, 10), random.randint(-10, 10))
            pt_list = [(center[0] - width/2, center[1] - height/2), (center[0] + width/2, center[1] - height/2), (center[0] + width/2, center[1] + height/2), (center[0] - width/2, center[1] + height/2)]

            # Rotate the rectangle by theta radians
            theta = random.random() * math.pi
            for i in range(len(pt_list)):
                pt_list[i] = rotation(theta, pt_list[i])

            polygons.append(Rectangle(pt_list, name="Rectangle"))
            

    # Get all the points from all the polygons
    ch_list = []
    for i in range(len(polygons)):
        for j in range(len(polygons[i].pt_list)):
           ch_list.append(polygons[i].pt_list[j])
    
    

    # Compute the convex hull
    cvx_hull, left_most, right_most = compute_convex_hull(ch_list)


    # Print and draw the polygons and convex hull
    plt.figure()
    print_and_draw(polygons, cvx_hull, left_most, right_most)

if __name__ == "__main__":
    main()    


    