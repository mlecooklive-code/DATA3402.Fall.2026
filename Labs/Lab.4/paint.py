class Canvas:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        # Empty canvas is a matrix with element being the "space" character
        self.data = [[' '] * width for i in range(height)]

    def set_pixel(self, row, col, char='*'):
        self.data[row][col] = char

    def get_pixel(self, row, col):
        return self.data[row][col]
    
    def clear_canvas(self):
        self.data = [[' '] * self.width for i in range(self.height)]
    
    def v_line(self, x, y, h, **kargs):
        for i in range(x,x+h):
            self.set_pixel(i,y, **kargs)

    def h_line(self, x, y, w, **kargs):
        for i in range(y,y+w):
            self.set_pixel(x,i, **kargs)
            
    def line(self, x1, y1, x2, y2, **kargs):
        slope = (x2-x1) / (y2-y1)
        for y in range(y1,y2):
            x= x1 + int(slope * (y-y1))
            self.set_pixel(x,y, **kargs)
            
    def display(self):
        print("\n".join(["".join(row) for row in self.data]))



# Base class Shape
class Shape:
    def __init__(self, coordinates, name=""):
        self.__coordinates = coordinates
        self.name = name

    def compute_area(self):
        raise NotImplementedError

    def compute_perimeter(self):
        raise NotImplementedError

    def get_coordinates(self):
        return self.__coordinates

    def get_perimeter_points(self):
        return NotImplementedError

    def is_inside(self, point):
        return NotImplementedError

    def is_overlapping(self, test_shape):
        test_points = test_shape.get_perimeter_points()
        for i in range(len(test_points)):
            if self.is_inside(test_points[i]):
                return True
        return False

    def paint(self, canvas): pass


# rectangle subclass
class rectangle(Shape):
    def __init__(self, length, width, coordinates):
        Shape.__init__(self, coordinates)
        self.__length = length
        self.__width = width

    def compute_area(self):
        area = self.__length*self.__width
        return area

    def compute_perimeter(self):
        perimeter = 2*(self.__length+self.__width)
        return perimeter

    def get_length(self):
        return self.__length

    def get_width(self):
        return self.__width

    def get_perimeter_points(self):
        coordinates = self.get_coordinates()
        length = self.get_length()
        width = self.get_width()
        point1 = coordinates
        point2 = (coordinates[0]+width, coordinates[1])
        point3 = (coordinates[0]+width, coordinates[1]+length)
        point4 = (coordinates[0], coordinates[1]+length)

        corners = [point1, point2, point3, point4]
        return corners

    def is_inside(self, test_point):
        point1, point2, point3, point4 = self.get_perimeter_points()
        # point0 = starting point, point2 = furthest point from start
        if (point1[0] < test_point[0] < point3[0]) and (point1[1] < test_point[1] < point3[1]):
            return True
        else:
            return False

    def paint(self, canvas):
        coordinates = self.get_coordinates()
        length = self.get_length()
        width = self.get_width()

        canvas.h_line(coordinates[1], coordinates[0], width + 1)
        canvas.h_line(coordinates[1] + length, coordinates[0], width + 1)

        canvas.v_line(coordinates[1], coordinates[0], length + 1)
        canvas.v_line(coordinates[1], coordinates[0] + width, length + 1)

    def __repr__(self):
        return "rectangle(" + repr(self.get_length()) + "," + \
           repr(self.get_width()) + "," + \
           repr(self.get_coordinates()) + ")"

# circle subclass
class circle(Shape):
    def __init__(self, radius, coordinates):
        Shape.__init__(self, coordinates)
        self.__radius = radius

    def compute_area(self):
        pi = 3.14
        area = pi*(self.__radius**2)
        return area

    def compute_perimeter(self):
        pi = 3.14
        perimeter = 2*pi*self.__radius
        return perimeter

    def get_radius(self):
        return self.__radius

    def get_perimeter_points(self):
        import math
        coordinates = self.get_coordinates()
        x = coordinates[0]
        y = coordinates[1]
        r = self.get_radius()
        points = []
        for i in range(16):
            angle = (2*math.pi*i)/16
            x_points = x + r*math.cos(angle)
            y_points = y + r*math.sin(angle)
            points.append((x_points, y_points))
        return points

    def is_inside(self, test_point):
        import math
        center = self.get_coordinates()
        radius = self.get_radius()
        d = math.sqrt((center[0]-test_point[0])**2+(center[1]-test_point[1])**2)
        if d < radius:
            return True
        else:
            return False

    def paint(self, canvas):
        points = self.get_perimeter_points()

        for point in points:
            x = int(round(point[0]))
            y = int(round(point[1]))
            canvas.set_pixel(y, x)

    def __repr__(self):
        return "circle(" + repr(self.get_radius()) + "," + \
           repr(self.get_coordinates()) + ")"


# triangle subclass
class triangle(Shape):
    def __init__(self, side1, side2, side3, coordinates):
        Shape.__init__(self, coordinates)
        self.__side1 = side1
        self.__side2 = side2
        self.__side3 = side3

    def compute_perimeter(self):
        perimeter = self.__side1+self.__side2+self.__side3
        return perimeter

    def compute_area(self):
        import math
        perimeter = self.compute_perimeter()
        s = perimeter/2
        a = self.__side1
        b = self.__side2
        c = self.__side3
        area = math.sqrt(s*(s-a)*(s-b)*(s-c))
        return area

    def get_side_lengths(self):
        return self.__side1, self.__side2, self.__side3

    def get_perimeter_points(self):
        import math
        point1 = self.get_coordinates() # starting coordinate
        a, b, c = self.get_side_lengths()
        point2 = (point1[0]+a, point1[1]) # second coordinate extends 'a' in the x direction to form base
        angle = math.acos((a**2+b**2-c**2)/(2*a*b))
        point3 = (point1[0]+(b*math.cos(angle)), point1[1]+(b*math.sin(angle)))
        return point1, point2, point3

    def is_inside(self, test_point):
        import math
        point_a, point_b, point_c = self.get_perimeter_points()
        area_whole = self.compute_area()

        def area(x1, y1, x2, y2, x3, y3):
            return abs((x1 * (y2 - y3) + x2 * (y3 - y1) + x3 * (y1 - y2)) / 2.0)
        # Calculate area of triangle PBC
        A1 = area(test_point[0], test_point[1], point_b[0], point_b[1], point_c[0], point_c[1])

        # Calculate area of triangle PAC
        A2 = area(point_a[0], point_a[1], test_point[0], test_point[1], point_c[0], point_c[1])

        # Calculate area of triangle PAB
        A3 = area(point_a[0], point_a[1], point_b[0], point_b[1], test_point[0], test_point[1])

        # Check if sum of A1, A2 and A3
        # is same as A
        if math.isclose((A1+A2+A3), area_whole):
            return True
        else:
            return False

    def paint(self, canvas):
        point1, point2, point3 = self.get_perimeter_points()

        canvas.h_line(
            int(point1[1]),
            int(point1[0]),
            int(point2[0] - point1[0]) + 1)

        canvas.line(
            int(point2[1]), int(point2[0]),
            int(point3[1]), int(point3[0]))

        canvas.line(
            int(point3[1]), int(point3[0]),
            int(point1[1]), int(point1[0]))

    def __repr__(self):
        side1, side2, side3 = self.get_side_lengths()

        return "triangle(" + repr(side1) + "," + \
           repr(side2) + "," + \
           repr(side3) + "," + \
           repr(self.get_coordinates()) + ")"

class CompoundShape(Shape):
    def __init__(self, shapes, coordinates=(0, 0)):
        Shape.__init__(self, coordinates)
        self.shapes = shapes

    def paint(self, canvas):
        for shape in self.shapes:
            shape.paint(canvas)


class RasterDrawing:
    def __init__(self):
        self.shapes = dict()
        self.shape_names = list()

    def add_shape(self, shape):
        if shape.name == "":
            shape.name = self.assign_name()

        self.shapes[shape.name] = shape
        self.shape_names.append(shape.name)

    def update(self, canvas):
        canvas.clear_canvas()
        self.paint(canvas)

    def paint(self, canvas):
        for shape_name in self.shape_names:
            self.shapes[shape_name].paint(canvas)

    def assign_name(self):
        name_base = "shape"
        name = name_base + "_0"

        i = 1
        while name in self.shapes:
            name = name_base + "_" + str(i)
            i += 1

        return name
    
    def save(self, filename):
        f = open(filename, "w")

        for shape_name in self.shape_names:
            f.write(repr(self.shapes[shape_name]) + "\n")

        f.close()

def drawing_loader(filename):
    drawing = RasterDrawing()

    f = open(filename, "r")

    for line in f:
        shape = eval(line.strip())
        drawing.add_shape(shape)

    f.close()

    return drawing
