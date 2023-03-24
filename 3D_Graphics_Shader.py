"""
    Majd Hamdan
    3D_Graphics_Shader.py
    NOV 24/2022
"""


import math
import copy
import time
import pygame




###############################################################
#---------------------Driver Code-----------------------------#
###############################################################


# Global variables
screen_height = 600;
screen_width = 800;
pi = 3.14159;
max_z = 1000;
min_z = 0.1;
theta_view = 90;
file_name = "cube.txt";
# assign in main
max_coord = 0;
projection = 0;

def main():

    # read input file
    num_vertices, num_faces, vectors, triangles, mc  = read_text_input(file_name)
    # uncomment this line to run it with cube.txt
    # num_vertices, num_faces, vectors, triangles, mc  = read_text_input("cube.txt")

    global max_coord
    max_coord = mc
    global projection
    projection = Projection(max_z, min_z, theta_view, screen_height, screen_width)

    # Initialize Pygame
    pygame.init()

    # Create surface
    surface = pygame.display.set_mode((screen_width, screen_height))

    # fill surface with white
    surface.fill((255,255,255))

    # initial drawing of all triangles
    DrawTriangles(surface, triangles, 0, 0)

    sustain_display = True;
    rotate = False;
    xr_angle = 0; # initial rotation in rad
    yr_angle = 0; # initial rotation in rad

    while sustain_display:
        # Iterating over all the events received from
        # pygame.event.get()
        for event in pygame.event.get():

            # quit on escape
            if event.type == pygame.QUIT:
                sustain_display = False;

            # allow rotation when user clicks
            elif event.type == pygame.MOUSEBUTTONDOWN:
                rotate = True;
            # allow rotation when user release
            elif event.type == pygame.MOUSEBUTTONUP:
                rotate = False;
                position = event.pos

            elif event.type == pygame.MOUSEMOTION and rotate:
                # find the amount of movement in x and y since the previous call
                x_movement, y_movement = event.rel;

                # Every 1 position unit = 2*pi/(x or y screen_dimension) angle
                xr_angle += 2*(y_movement/screen_width)*pi;
                yr_angle += 2*(x_movement/screen_height)*pi;

                DrawTriangles(surface, triangles, xr_angle, yr_angle)

    pygame.display.quit()
    pygame.quit()


###############################################################
#-------------------------Classes-----------------------------#
###############################################################

class Vector:
    # x, y, and z are float values
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z
        self.v = [x, y, z];

    def DotProduct(v1, v2):
        return v1.x*v2.x + v1.y*v2.y + v1.z*v2.z;

    def Normalize(v):
        magnitude = math.sqrt(v.x**2 + v.y**2 + v.z**2);
        return Vector(v.x/magnitude, v.y/magnitude, v.z/magnitude)

    def CrossProduct(v1, v2):
        v = Vector();
        v.x = v1.y * v2.z - v1.z * v2.y;
        v.y = v1.z * v2.x - v1.x * v2.z;
        v.z = v1.x * v2.y - v1.y * v2.x;
        return v;

    def __str__(self):
        return f"({self.x}, {self.y}, {self.z})"

class Triangle:
    # v1, v2 and v3 are vectors
    def __init__(self, v1 = Vector(), v2 = Vector(), v3 = Vector()):
        self.t = [v1, v2, v3];
        self.color = 0; # color of painting
        self.order = 0; # order of painting

    # find the normal to a triangle by finding the cross product
    # of two lines making up the triangle
    def FindNormal(triangle):
        l1 = Vector();
        l2 = Vector();
        l1.x = triangle.t[1].x - triangle.t[0].x;
        l1.y = triangle.t[1].y - triangle.t[0].y;
        l1.z = triangle.t[1].z - triangle.t[0].z;

        l2.x = triangle.t[2].x - triangle.t[0].x;
        l2.y = triangle.t[2].y - triangle.t[0].y;
        l2.z = triangle.t[2].z - triangle.t[0].z;

        return Vector.CrossProduct(l1, l2);


    def __str__(self):
        return f"[({self.t[0]}), ({self.t[1]}), ({self.t[2]})]"

class Projection:
    def __init__(self, max_z, min_z, theta_view, screen_height, screen_width):
        self.max_z = max_z;
        self.min_z = min_z;
        self.theta_view = theta_view;
        self.screen_height = screen_height;
        self.screen_width = screen_width;
        self.a = screen_height/screen_width; #aspect ratio
        self.x_y_scale = 1/math.tan(theta_view*(3.14159/180)/2)
        self.pm = [[self.a*self.x_y_scale, 0, 0, 0],
                   [0, self.x_y_scale, 0, 0],
                   [0, 0, max_z/(max_z - min_z), 1],
                   [0, 0, (-max_z*min_z)/(max_z - min_z), 0]
                    ]; # pm = projection matrix
        self.vcamera = Vector(); # we take the viewer stationtioned at (0,0,0)


    # Vector multiplication with a transition matrix
    # iv = input vector
    def MatrixMultiplication(self, iv, tm):
        x = iv.x*tm[0][0] + iv.y*tm[1][0] + iv.z*tm[2][0] + tm[3][0];
        y = iv.x*tm[0][1] + iv.y*tm[1][1] + iv.z*tm[2][1] + tm[3][1];
        z = iv.x*tm[0][2] + iv.y*tm[1][2] + iv.z*tm[2][2] + tm[3][2];
        z_0 = iv.x*tm[0][3] + iv.y*tm[1][3] + iv.z*tm[2][3] + tm[3][3];
        if z_0 != 0:
            x = x/z_0;
            y = y/z_0;
            z = z/z_0;
        return Vector(x, y, z)


    # Project a 3D triangle into the 2D plane
    def ProjectTriangle(self, triangle):

        # first translate the z of each vector into the page with a magnituede of 3
        # to create an offset of 3 units into the page
        translated_triangle = copy.deepcopy(triangle)
        translated_triangle.t[0].z = triangle.t[0].z + 3;
        translated_triangle.t[1].z = triangle.t[1].z + 3;
        translated_triangle.t[2].z = triangle.t[2].z + 3;

        # find the normal of the triangle
        normal = Triangle.FindNormal(translated_triangle);

        # normalize the normal
        normal = Vector.Normalize(normal);

        # arrange triangle by clockwise order
        # This code assumes all triangles vertices must be sorted clockwise such that
        # the normal of the triangle is always pointing away from the z axis. This piece
        # of code re-arrange the triangle vertices clockwise in case they are not.
        theta = math.degrees(math.acos(normal.z/1))
        if theta < 90:
            return self.ProjectTriangle( Triangle(triangle.t[2], triangle.t[1], triangle.t[0]))




        # Take the dot product between the line from the viewer to the normal
        # and the normal
        l_vn = Vector(translated_triangle.t[0].x - self.vcamera.x, translated_triangle.t[0].y - self.vcamera.y, translated_triangle.t[0].z - self.vcamera.z )
        dot_product = Vector.DotProduct(normal, l_vn)

        # Projection to 2D and light
        # We take the simplifying assumption that we only see the triangles
        # with normal dot product < 0 (ie. the normal is negative (pointing
        # towards the viewer) and |dot_product| > 0)
        projected_triangle = Triangle();
        if dot_product < 0:

            # Light: we assume light is coming from the direction of the viewer in
            # a single direction (the light source is large compared to the display)
            light_normal = Vector(0, 0, -1); # -1 here instead of 1 to gurentee positive dot product
                                             # when the triange's normal is towards the viewer.


            # normalize the normal
            light_normal = Vector.Normalize(light_normal)

            # Take the dot product between the light normal and the triangle normal
            dot_product = Vector.DotProduct(normal, light_normal);

            # find the color from dot product
            projected_triangle.color = self.ConvertToColor(dot_product);

            # Find order of triangle
            projected_triangle.order = (translated_triangle.t[0].z+translated_triangle.t[1].z+translated_triangle.t[2].z)/3;

            # project to 2D
            i = 0;
            for v in translated_triangle.t:
                projected_triangle.t[i] = self.MatrixMultiplication(v, self.pm);
                i = i+1;

        return projected_triangle

    # Rotate a triangle around the x axis with an angle theta
    def XRotation(self, triangle, rotation_theta):
        xrm = [[1, 0, 0, 0 ],
               [0, math.cos(rotation_theta), math.sin(rotation_theta), 0],
               [0, -math.sin(rotation_theta), math.cos(rotation_theta), 0],
               [0, 0, 0, 1]
               ]; # x rotation matrix

        rotated_triangle = Triangle();

        i = 0;
        for v in triangle.t:
            rotated_triangle.t[i] = self.MatrixMultiplication(v, xrm);
            i += 1;

        return rotated_triangle

    # Rotate a triangle around the y axis with an angle theta
    def YRotation(self, triangle, rotation_theta):
        yrm = [[math.cos(rotation_theta), 0, math.sin(rotation_theta), 0 ],
               [0, 1, 0, 0],
               [-math.sin(rotation_theta), 0, math.cos(rotation_theta), 0],
               [0, 0, 0, 1]
               ]; # y rotation matrix

        rotated_triangle = Triangle();

        i = 0;
        for v in triangle.t:
            rotated_triangle.t[i] = self.MatrixMultiplication(v, yrm);
            i += 1;

        return rotated_triangle

    # Convert a value between 0 and 1 to a value between #00005F and #0000FF
        # There are 160 values beween #00005F and #0000FF. For
        # simplification, we will only use 100 of them by only
        # taking t sig fig of dot_product
    def ConvertToColor(self, dot_product):
        # this line is not necessirly as dot_product is expcted to be larger than 0.
        # Usefull for handling errors
        if dot_product < 0:
            color = (0,0,0)
            return color
        color = hex(int(round(dot_product, 2)*100*1.6) + 95) # 5F = 95
        color = color.split('x');
        color = color[1];
        color = "#0000"+color;
        return color




    # Print projection matrix for when printing a projection object
    def __str__(self):
        return f"[{self.pm}]"



###############################################################
#---------------------Helper Function-------------------------#
###############################################################




# draw one triangle on pygame surface.
# triangle must be a projected triangle using Projection.ProjectTriangle
def DrawTriangle(surface, triangle):

    # scale such that max_coord be 1/4 of screen size
    x_scale = 0.8/max_coord*screen_width;
    y_scale = 0.8/max_coord*screen_height;

    for i in range(3):
        triangle.t[i].x = triangle.t[i].x*x_scale + screen_width/2;
        triangle.t[i].y = triangle.t[i].y*y_scale + screen_height/2;

    # draw triangle
    color = 0;
    if triangle.color != 0:
        color = pygame.color.Color(triangle.color)

    pygame.draw.polygon(surface, color, [[triangle.t[0].x, triangle.t[0].y],
                                         [triangle.t[1].x, triangle.t[1].y],
                                         [triangle.t[2].x, triangle.t[2].y]], 0)

    # Useful for debugging.
#     pygame.draw.polygon(surface, (0,0,0), [[triangle.t[0].x, triangle.t[0].y],
#                                            [triangle.t[1].x, triangle.t[1].y],
#                                            [triangle.t[2].x, triangle.t[2].y]], 5)

    # draw vertices
    pygame.draw.circle(surface, (0, 0, 200), (triangle.t[0].x, triangle.t[0].y), 7, 0)
    pygame.draw.circle(surface, (0, 0, 200), (triangle.t[1].x, triangle.t[1].y), 7, 0)
    pygame.draw.circle(surface, (0, 0, 200), (triangle.t[2].x, triangle.t[2].y), 7, 0)



# draw a list of Triangle object on pygame surface after performing
# x and y rotations then projecting to 2D
def DrawTriangles(surface, triangles, xrot_angle, yrot_angle):

    # reset surface
    surface.fill((255,255,255))

    sorted_triangles = [Triangle()]*len(triangles);
    i = 0;
    # apply rotation then projection
    for t in triangles:
        rotated_triangleX = projection.XRotation(t, xrot_angle);
        rotated_triangleXY = projection.YRotation(rotated_triangleX , yrot_angle);
        p = projection.ProjectTriangle(rotated_triangleXY);
        sorted_triangles[i] = p;
        i += 1;

    # order the triangles by furthest from viewer in descending order
    # paint far triangles first
    sorted_triangles.sort(key = lambda x:x.order, reverse=True)
    for t in sorted_triangles:
        if t.order != 0:
            DrawTriangle(surface, t)

    pygame.display.update()


# return num of vertices, num of triangles, a list of all
# vectors as Vector objects, list of all triangles as Triangle objects
# and max coordinate
def read_text_input(file_name):

    f = open(file_name);
    max_coord = 0;

    # first line num_vertices, num_faces
    line = f.readline();

    # remove new line charecters and split the string
    line = line.strip();
    line = line.split(',');

    num_vertices = int(line[0]);
    num_faces = int(line[1]);

    # the num_verices lines indicating the vertices coordinates
    vectors = [Vector()]*num_vertices;
    for i in range(num_vertices):
        line = f.readline();
        line = line.strip();
        line = line.split(',');
        for i in range(1, 4):
            if float(line[i]) > max_coord:
                max_coord = float(line[i])
        vectors[int(line[0])-1] = Vector(float(line[1]), float(line[2]), float(line[3]));

    # the num_faces lines defining the three vertices composing a triangular face
    triangles = [Triangle()]*num_faces;
    for i in range(num_faces):
        line = f.readline();
        line = line.strip();
        line = line.split(',');

        triangles[i] = Triangle(vectors[int(line[0])-1], vectors[int(line[1])-1], vectors[int(line[2])-1]);

    f.close();

    return num_vertices, num_faces, vectors, triangles, max_coord






###############################################################
#---------------------Driver Code-----------------------------#
###############################################################

if __name__=="__main__":
    main()
