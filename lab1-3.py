import matplotlib.pyplot as plt
import numpy as np

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Punkt({self.x}, {self.y})"

    def translate(self, dx, dy):
        return Point(self.x + dx, self.y + dy)


class Line:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        self.A = p2.y - p1.y
        self.B = p1.x - p2.x
        self.C = self.A * p1.x + self.B * p1.y

    def equation(self):
        return self.A, self.B, self.C

    def contains_point(self, p):
        return self.A * p.x + self.B * p.y == self.C

    def point_on_segment(self, p):
        if self.contains_point(p):
            return min(self.p1.x, self.p2.x) <= p.x <= max(self.p1.x, self.p2.x) and min(self.p1.y, self.p2.y) <= p.y <= max(self.p1.y, self.p2.y)
        return False

    def point_position(self, p):
        val = self.A * p.x + self.B * p.y - self.C
        if val > 0:
            return "lewo"
        elif val < 0:
            return "prawo"
        else:
            return "na linii"

    def translate(self, dx, dy):
        new_p1 = self.p1.translate(dx, dy)
        new_p2 = self.p2.translate(dx, dy)
        return Line(new_p1, new_p2)

    def reflect_point(self, p):
        d = self.A * 2 + self.B * 2
        x = p.x - 2 * self.A * (self.A * p.x + self.B * p.y - self.C) / d
        y = p.y - 2 * self.B * (self.A * p.x + self.B * p.y - self.C) / d
        return Point(x, y)


def line_length(p1, p2):
    return ((p1.x-p2.x)**2 + (p1.y -p2.y)**2)**0.5


class Triangle:
    def __init__(self, line1, line2, line3):
        self.line1 = line1
        self.line2 = line2
        self.line3 = line3

    def visualize(self):
        plt.figure()
        lines = [self.line1, self.line2, self.line3]
        for line in lines:
            x_values = [line.p1.x, line.p2.x]
            y_values = [line.p1.y, line.p2.y]
            equation = f"{line.A}x + {line.B}y + {line.C} = 0"
            plt.plot(x_values, y_values, '-m', label=equation)
        plt.xlabel('Oś X')
        plt.ylabel('Oś Y')
        plt.axis('equal')
        plt.legend(loc='best')
        plt.show()

    def area(self):
        a = line_length(self.line1.p1, self.line1.p2)
        b = line_length(self.line2.p1, self.line2.p2)
        c = line_length(self.line3.p1, self.line3.p2)
        p = (a + b + c) / 2
        print(p)
        S = (p * (p - a) * (p - b) * (p - c)) ** 0.5
        return S

    def contains_point_normal(self, point):

        triangle_area = self.area()
        area_PAB = abs(0.5 * (point.x * (self.line1.p1.y - self.line2.p1.y) +
                              self.line1.p1.x * (self.line2.p1.y - point.y) +
                              self.line2.p1.x * (point.y - self.line1.p1.y)))

        area_PBC = abs(0.5 * (point.x * (self.line2.p1.y - self.line3.p1.y) +
                              self.line2.p1.x * (self.line3.p1.y - point.y) +
                              self.line3.p1.x * (point.y - self.line2.p1.y)))

        area_PAC = abs(0.5 * (point.x * (self.line1.p1.y - self.line3.p1.y) +
                              self.line1.p1.x * (self.line3.p1.y - point.y) +
                              self.line3.p1.x * (point.y - self.line1.p1.y)))

        return triangle_area == area_PAB + area_PBC + area_PAC

    def contains_point_edges(self, point):#znak iloczynu wektorowego  trzech punktow
        #dla kazdego wierzchołka obliczamy iloczyn wektorowy z punktem testowym i dwoma wirz i sprawdzamy
        #czy znaki sa takie same jesli tak to punkt w srodku
        def sign(p1, p2, p3):
            return (p1.x - p3.x) * (p2.y - p3.y) - (p2.x - p3.x) * (p1.y - p3.y)
#okreslenie znakow iloczynow
        b1 = sign(point, self.line1.p1, self.line2.p1) < 0
        b2 = sign(point, self.line2.p1, self.line3.p1) < 0
        b3 = sign(point, self.line3.p1, self.line1.p1) < 0

        return (b1 == b2) and (b2 == b3)

def area_between_lines(line1, line2):
    if line1.A == line2.A and line1.B == line2.B and line1.C == line2.C:
        return 0.0

    if intersection_lines(line1, line2) == None:
        if intersection_lines(Line(line1.p1, line2.p2), Line(line1.p2, line2.p1)) == None:
            t1 = Triangle(line1, Line(line1.p2, line2.p1), Line(line1.p1, line2.p1))
            t2 = Triangle(line2, Line(line1.p1, line2.p1), Line(line1.p1, line2.p2))

            return t1.area() + t2.area()
        else:
            t1 = Triangle(line1, Line(line1.p2, line2.p2), Line(line1.p1, line2.p2))
            t2 = Triangle(line2, Line(line1.p1, line2.p2), Line(line1.p1, line2.p1))
            return t1.area() + t2.area()
    else:
        t1 = Triangle(line1, Line(line1.p1, line2.p1), Line(line2.p1, line1.p2))
        t2 = Triangle(line1, Line(line1.p2, line2.p2), Line(line2.p2, line1.p1))
        return t1.area() + t2.area()

class Polygon:
    def __init__(self, *vertices):
        self.vertices = vertices

    def visualize(self):
        plt.figure()
        for i in range(len(self.vertices)):
            x_values = [self.vertices[i].x, self.vertices[(i + 1) % len(self.vertices)].x]
            y_values = [self.vertices[i].y, self.vertices[(i + 1) % len(self.vertices)].y]
            plt.plot(x_values, y_values, '-r', label='Wielokąt')

        plt.xlabel('Oś X')
        plt.ylabel('Oś Y')
        plt.axis('equal')
        plt.legend()
        plt.show()

    def contains_point(self, point):

        intersections = 0 #do liczby przecuiec
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            # Sprawdzenie, czy współrzędna y punktu leży w zakresie współrzędnych y krawędzi
            if (point.y > min(p1.y, p2.y)) and (point.y <= max(p1.y, p2.y)):
                # Sprawdzenie, czy współrzędna x punktu jest na lewo od maksymalnej współrzędnej x krawędzi

                if point.x <= max(p1.x, p2.x):
                    # Sprawdzenie, czy krawędź nie jest pozioma
                    if p1.y != p2.y:
                        x_intersect = (point.y - p1.y) * (p2.x - p1.x) / (p2.y - p1.y) + p1.x
                        # Inkrementacja licznika przecięć, jeśli punkt jest na lewo od punktu przecięcia

                        if (p1.x == p2.x) or (point.x <= x_intersect):
                            intersections += 1
 # Jeśli liczba przecięć jest nieparzysta, punkt znajduje się wewnątrz wielokąta; w przeciwnym razie jest na zewnątrz

        return intersections % 2 != 0


# Funkcja do obliczania punktu przecięcia dwóch prostych na podstawie współczynników równania w postaci ogólnej
def intersection_general(A1, B1, C1, A2, B2, C2):
    determinant = A1 * B2 - A2 * B1

    if determinant == 0:
        return None
    else:
        x = (C1 * B2 - C2 * B1) / determinant
        y = (A1 * C2 - A2 * C1) / determinant
        return Point(x, y)


# Funkcja do obliczania punktu przecięcia dwóch prostych na podstawie dwóch linii o znanym początku i końcu
def intersection_lines(line1, line2):
    A1, B1, C1 = line1.equation()
    A2, B2, C2 = line2.equation()

    return intersection_general(A1, B1, C1, A2, B2, C2)


# Funkcja do obliczania odległości między punktem a linią
def distance_point_to_line(point, line):
    x0, y0 = point.x, point.y
    A, B, C = line.equation()
    distance = abs(A * x0 + B * y0 + C) / (A ** 2 + B ** 2) ** 0.5
    return distance


# Przykładowe punkty i linie
p1 = Point(0, 0)
p2 = Point(4, 4)
line = Line(p1, p2)
p3 = Point(2, 2)
p4 = Point(1, 2)

# Inicjalizacja równań prostych definiujących trójkąt
line1 = Line(p1, p2)
line2 = Line(p1, p4)
line3 = Line(p2, p4)

# Tworzenie trójkąta na podstawie równań prostych
triangle = Triangle(line1, line2, line3)

# Wizualizacja trójkąta
#triangle.visualize()
print("Area of a the tringle: ", triangle.area())


# Inicjalizacja wierzchołków definiujących wielokąt
polygon_vertices = [Point(1, 1), Point(3, 1), Point(2, 4), Point(1, 3)]
polygon = Polygon(*polygon_vertices)


polygon.visualize()

# Testowanie metody sprawdzającej czy punkt należy do trójkąta
print("Czy punkt (2, 2) należy do trójkąta:", triangle.contains_point_normal(Point(2, 2)))
print("Czy punkt (2, 2) należy do trójkąta:", triangle.contains_point_edges(Point(2, 2)))

# Testowanie metody sprawdzającej czy punkt należy do wielokąta
print("Czy punkt (2, 2) należy do wielokąta:", polygon.contains_point(Point(2, 2)))


# Inicjalizacja dwóch linii
line1 = Line(Point(1, 1), Point(4, 1))
line2 = Line(Point(2, 3), Point(5, 3))

# Obliczenie pola między liniami

print("Pole między liniami:", area_between_lines(line1, line2))
polygon_vertices2 = [Point(1, 1), Point(4, 1), Point(5, 3), Point(2, 3)]
polygon2 = Polygon(*polygon_vertices2)
#polygon2.visualize()