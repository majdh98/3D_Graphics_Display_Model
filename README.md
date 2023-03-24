# 3D Graphics Display Model


The repository contains two 3D graphics display programs that display 3D object from a comma-separated text file specified by the user:
- 3D_Graphiscs_Wireframe.py
- 3D_Graphics_Shader.py

Both programs will display a 3D object defined by vertices and edges of the faces of the object. Vertices are represented using blue circles and the edges using blue lines. Edges are defined as lines between the vertices. 

In 3D_Graphiscs_Wireframe.py, faces are transparent to get a wireframe of the 3D object. While in 3D_Graphics_Colored_faces.py, visible faces are colored by a shade of blue. 

cube.text is an example of an input file. The format of the comma-separated file is as follows:
1- The first line contains two integers, first is the number of vertices of the 3D object, and the second is the number of faces of the 3D object.
2- Vertices section: starting from the second line, each line will define one vertex of the 3D object. Each line contains an integer representing the vertex id, and 3 real numbers representing (x,y,z) coordinates of the vertex. Number of lines in this section is equal to the first integer in line 1. 
3- Faces section: After the vertices section, each line defines the faces of the 3D object. Each line contains three integers each representing an id of a vertex. Each line defines a triangle that is a face of the object. 




To run the programs, please specify the name of the input file (if it is in the same path as the code) in line 27 under the” file name” variable. Please specify the path to the input file and the name of the file otherwise.  

To run the program, you need the math, pygame, time, and copy libraries installed. If the libraries are installed, you may run the programs from any IDE or execute it from the command line. 

To run the program from the command line, please navigate to the folder where the programs are saved then type:
python .\3D_Graphiscs_Wireframe.py in the command line. 


As a default, the input file is specified as  ”cube.txt” and is expected to be in the same folder as the programs.

When running the code a 800x600px display will appear containing the shape specified by the input file. You may change the dimension of the display in line 21 and 22 in the code. 

When the mouse is clicked, the shape will rotate around the x-axis for vertical movement of the mouse and around the y-axis for horizontal movement of the mouse. When the mouse is released, the shape will stop rotating. 

You can exit the program by clicking on the red x button on the top right of the display. 

A description of the mathematical model is provided in Hamdan_3D_graphics_display_model.pdf. 

There are 3 classes in the code:
- A vector class to represent the x,y, and z coordinates of a vector with methods to perform dot product, cross product and normalization:
- A Triangle class to represent a triangle as a clockwise list of its vertices with a method to find the normal of the triangle. 
- A Projection class that define the perspective projection matrix and projection constant in additions to methods to perform vector and matrix multiplication and rotation around the x and y axis. 



The classes are slightly different between 3D_Graphiscs_Wireframe.py and 3D_Graphics_Shader.py where we defined additional class variables in 3D_Graphics_Shader.py 
to facilitate shading. 

You can run 3D_Graphics_Shader.py without having the triangles shaded by commenting line 325 and uncommenting line 330. This is useful to see which triangles are visible and which are not.

