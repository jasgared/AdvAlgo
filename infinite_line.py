from graphics import *
from scipy.spatial import ConvexHull


minX = 0.0
minY = 0.0
maxX = 1000.0
maxY = 500.0
intersection_list = []
line_list = []
input_key = "a"
# border points for line segment extension

def min_line_X(m,c):
    # substitute y = minY to get min X
    if m == 0:
        return None
    else:
        x1 = (minY - c) / m
        # print("x:",x1)
        if (minX < x1 < maxX):
            return [x1, minY]
        else:
            return None

def max_line_X(m,c):
    # substitute y = maxY to get max X
    if m == 0:
        return None
    else:
        x2 = (maxY - c) / m
        # print("x:", x2)
        if (minX < x2 < maxX):
            return [x2, maxY]
        else:
            return None
def min_line_Y(m,c):
    # substitute x = minX to get min Y
    y1 = m * minX + c
    # print("y:", y1)
    if (minY < y1 < maxY):
        return [minX, y1]
    else:
        return None

def max_line_Y(m,c):
    # substitute x = maxX to get max Y
    y2 = m * maxX + c
    # print("y:", y2)
    if (minY < y2 < maxY):
        return [maxX, y2]
    else:
        return None

def border_line_points(m,c):
    border_points = []
    if(min_line_X(m,c)):
        # print("Y = 0")
        border_points.append(min_line_X(m,c))
        # print("---------")

    if(max_line_X(m,c)):
        # print("Y = 500")
        border_points.append(max_line_X(m,c))
        # print("---------")

    if(min_line_Y(m,c)):
        # print("X = 0")
        border_points.append(min_line_Y(m,c))
        # print("---------")

    if(max_line_Y(m,c)):
        # print("X = 1000")
        border_points.append(max_line_Y(m,c))
        # print("---------")

    print(border_points)
    return border_points

def draw_me_line(win):

    # handle exceptions??
    # three lines through same point?
    # vertical line
    # clicking same point
    p1 = win.getMouse()
    # check if p1 is in intersection list
    point1 = [round(p1.getX(), 0), round(p1.getY(), 0)]
    while (point1 in intersection_list):
        # if point clicked is an intersecting point
        # it takes the input again, until correct is given
        print("point in intersection list")
        p1 = win.getMouse()
        point1 = [round(p1.getX(), 0), round(p1.getY(), 0)]
    p1 = Point(point1[0], point1[1])
    p1.draw(win)
    p2 = win.getMouse()
    if((maxX-50)<=p2.getX()<maxX)and(minY<=p2.getY()<(minY+50)):
        p1.undraw()
        return 0
    else:
        # check if p1 is in intersection list
        point2 = [round(p2.getX(), 0), round(p2.getY(), 0)]

        while (point2 in intersection_list) or (point2[0] == point1[0]):
            # if point clicked is an intersecting point
            # takes the input again, until correct is given
            #                      , if p1 and p2 are same
            #                      , if vertical line
            print("p2 in intersection list or same as first point")
            p2 = win.getMouse()
            point2 = [round(p2.getX(), 0), round(p2.getY(), 0)]
        p2 = Point(point2[0], point2[1])
        p2.draw(win)
        print("points: ", point1, point2)
        l = MyLine([], [], {})
        # slope
        slope_m = (point2[1] - point1[1]) / (point2[0] - point1[0])
        l.dual.append(slope_m)
        # constant c in line equation(y intercept)
        const_c = point1[1] - (l.dual[0]) * point1[0]
        l.dual.append(const_c)
        print("dual: ", l.dual)
        border_point_set = border_line_points(l.dual[0], l.dual[1])
        border1 = Point(border_point_set[0][0], border_point_set[0][1])
        border2 = Point(border_point_set[1][0], border_point_set[1][1])
        l.line_points = [border1, border2]
        print("line_points in class: ", l.line_points)
        # line = Line(p1, p2)
        # line.draw(win)
        return l


class MyLine:

    def __init__(self, dual, line_points, intersecting_lines):
        self.dual = dual
        self.line_points = line_points
        self.intersecting_lines = intersecting_lines

    def check_point(self, point):
        # failing few cases
        equation = point.getY() - ( self.dual[0] * point.getX() + self.dual[1])
        # print(equation)
        if(round(equation, 0) == 0):
            # print("line passes through point")
            return True
        else:
            # print("line doesnt pass through point")
            return False

    def get_y_bound(self):
        y = maxY
        if(self.dual[0] != 0):
            x = ( y - self.dual[1]) / self.dual[0]
        return Point(x,y)
    def get_x_bound(self):
        if(self.dual[0] > 0):
            x = minX
            y = ( self.dual[0] * x) + self.dual[1]
        elif(self.dual[0] < 0):
            x = maxX
            y = (self.dual[0] * x) + self.dual[1]
        return Point(x,y)
    def intersection_points_other_lines(self):
        for l in line_list:
            if(self.dual[0] == l.dual[0]):
                # no intersection point
                pass
            else:
                x_coord = (l.dual[1] - self.dual[1]) / (self.dual[0] - l.dual[0])
                y_coord = (self.dual[0] * x_coord) + self.dual[1]
                point_of_intersection = Point(x_coord, y_coord)
                # chance that the point repeats in the list
                intersection_list.append(point_of_intersection)
                # line object is the index
                self.intersecting_lines[l] = point_of_intersection
                l.intersecting_lines[self] = point_of_intersection

final_list = []

def traverse(t_list, l_line):
    print("l_line: ", l_line)
    dup_list = list(t_list)
    dup_list.remove(l_line)
    if(len(dup_list) == 0):
        return l_line
    else:
        curr_line = line_list[l_line]
        # req_y has the info of next line and the vertex to be considered
        req_y = []
        req_y.append(dup_list[0])
        req_y.append(curr_line.intersecting_lines[line_list[dup_list[0]]].getY())
        req_y.append(curr_line.intersecting_lines[line_list[dup_list[0]]].getX())
        for next_line in  dup_list:
            if(curr_line.dual[0] == 0) and (curr_line.intersecting_lines[line_list[next_line]].getX() < req_y[2]):
                req_y[0] = next_line
                req_y[1] = curr_line.intersecting_lines[line_list[next_line]].getY()
                req_y[2] = curr_line.intersecting_lines[line_list[next_line]].getX()

            elif(curr_line.dual[0] != 0) and (curr_line.intersecting_lines[line_list[next_line]].getX() < req_y[2]):
                req_y[0] = next_line
                req_y[1] = curr_line.intersecting_lines[line_list[next_line]].getY()
                req_y[2] = curr_line.intersecting_lines[line_list[next_line]].getX()
            else:
                print("other")
        req_point = Point(req_y[2], req_y[1])
        final_list.append(req_point)
        r_line = traverse(dup_list, req_y[0])
        print("cl_line: ", l_line)
        return r_line


def check_if_all_parallel():
    top_line = 0
    max_intercept = line_list[0].dual[1]
    flag = 0
    for c_line in line_list:
        if(c_line.dual[0] == 0):
            if(max_intercept < c_line.dual[1]):
                top_line = line_list.index(c_line)
            flag = 0
        else:
            flag = 1
            break
    return flag,top_line

def draw_lower_hull_lines(win,lower_hull):
    for i in lower_hull:
        print("drawing red lines")
        line_draw = Line(line_list[i].line_points[0], line_list[i].line_points[1])
        line_draw.setOutline('Red')
        line_draw.draw(win)


def main():
    lower_hull = []
    complete_hull = []
    win = GraphWin("Draw lines", maxX, maxY)
    win.setCoords(0, 0, maxX, maxY)
    red_region = Polygon(Point(maxX, minY), Point(maxX, minY+50), Point(maxX-50, minY+50), Point(maxX-50, minY))
    red_region.setOutline('red')
    red_region.draw(win)
    input_key = "z"
    while(True):
        print(win.checkKey())
        # if(input_key == "z"):
        #     print("entered break: ", input_key)
        #     break
        # else:
        print("normal: ", win.checkKey())
        l = draw_me_line(win)
        if l == 0:
            break
        else:
            for p in intersection_list:
                print("checking intersection list")
                print("_____________________________________________________________________________________")
                while (l.check_point(p)):
                    print("concurrent")
                    l = draw_me_line(win)
            # intersection points with other lines
            l.intersection_points_other_lines()
            # append line
            line_list.append(l)
            # draw line
            line_extend = Line(l.line_points[0], l.line_points[1])
            line_extend.draw(win)
            print("Checking if line added to input list and points added to intersection_list")
            print("lines: ", line_list)
            print(line_list[0].dual)
            print("Intersecting points: ", intersection_list)
            # input_key = win.checkKey()


    if (input_key == "z"):
        if (len(line_list) == 0):
            print("No lines in the list")
        elif (len(line_list) == 1):
            print("one line")
            if (line_list[0].dual[0] == 0):
                final_list.append(Point(minX, line_list[0].dual[1]))
                final_list.append(Point(minX, maxY))
                final_list.append(Point(maxX, maxY))
                final_list.append(Point(maxX, line_list[0].dual[1]))

            elif (line_list[0].dual[0] > 0):
                final_list.append(line_list[0].get_y_bound())
                final_list.append(line_list[0].get_x_bound())
                final_list.append(Point(0, maxY))

            else:
                final_list.append(line_list[0].get_y_bound())
                final_list.append(line_list[0].get_x_bound())
                final_list.append(Point(maxX, maxY))

            visible = Polygon(final_list)
            visible.setFill('gray')
            visible.draw(win)


        elif (len(line_list) == 2):
            print("two lines")
            check = check_if_all_parallel()
            if (check[0] == 0):
                final_list.append(Point(minX, line_list[check[1]].dual[1]))
                final_list.append(Point(minX, maxY))
                final_list.append(Point(maxX, maxY))
                final_list.append(Point(maxX, line_list[check[1]].dual[1]))
                visible = Polygon(final_list)
                visible.setFill('gray')
                visible.draw(win)
            elif (line_list[0].dual[0] != 0) and (line_list[1].dual[0] != 0):
                final_list.append(line_list[0].intersecting_lines[line_list[1]])
                final_list.append(line_list[0].get_y_bound())
                final_list.append(line_list[1].get_y_bound())
                visible = Polygon(final_list)
                visible.setFill('gray')
                visible.draw(win)

            else:
                print("other cases")
                if (line_list[0].dual[0] == 0):
                    if (line_list[1].dual[0] > 0):
                        final_list.append(Point(minX, line_list[0].dual[1]))
                    # (line_list[1].dual[0] < 0)
                    else:
                        final_list.append(Point(maxX, line_list[0].dual[1]))
                    final_list.append(line_list[0].intersecting_lines[line_list[1]])
                    final_list.append(line_list[1].get_y_bound())
                elif (line_list[1].dual[0] == 0):
                    if (line_list[0].dual[0] > 0):
                        final_list.append(Point(minX, line_list[1].dual[1]))
                    # (line_list[0].dual[0] < 0)
                    else:
                        final_list.append(Point(maxX, line_list[1].dual[1]))
                    final_list.append(line_list[0].intersecting_lines[line_list[1]])
                    final_list.append(line_list[0].get_y_bound())
                line1 = Line(final_list[0], final_list[1])
                line2 = Line(final_list[1], final_list[2])
                line1.setOutline("Blue")
                line2.setOutline("Blue")
                line1.draw(win)
                line2.draw(win)

        else:
            check = check_if_all_parallel()
            if (check[0] == 0):
                final_list.append(Point(minX, line_list[check[1]].dual[1]))
                final_list.append(Point(minX, maxY))
                final_list.append(Point(maxX, maxY))
                final_list.append(Point(maxX, line_list[check[1]].dual[1]))
                visible = Polygon(final_list)
                visible.setFill('gray')
                visible.draw(win)

            else:
                print("entered convex hull part")
                temp_list = []
                for l in line_list:
                    temp_list.append(l.dual)
                hull = ConvexHull(temp_list)
                print("hull vertices: ", hull.vertices)

                # find lower convex_hull
                minX_slope = line_list[hull.vertices[0]].dual[0]
                maxX_slope = line_list[hull.vertices[0]].dual[0]
                minX_const = line_list[hull.vertices[0]].dual[1]
                maxX_const = line_list[hull.vertices[0]].dual[1]

                # to get the y coordinate of left most and right most hull points
                for index in hull.vertices:

                    if (line_list[index].dual[0] < minX_slope):
                        minX_slope = line_list[index].dual[0]
                        minX_const = line_list[index].dual[1]
                    if (line_list[index].dual[0] > maxX_slope):
                        maxX_slope = line_list[index].dual[0]
                        maxX_const = line_list[index].dual[1]
                        # print("computed the lmy and rmy")

                # print("lmy:", minX_const)
                # print("rmy", maxX_const)
                cut_slope = (maxX_const - minX_const) / (maxX_slope - minX_slope)
                cut_const = minX_const - (cut_slope * minX_slope)
                lower_vertex_list = []
                for index in hull.vertices:
                    cut_eq = line_list[index].dual[1] - (cut_slope * line_list[index].dual[0] + cut_const)
                    # print("checking for lower vertices")
                    if (round(cut_eq, 10) >= 0):
                        # print("found a lower vertex")
                        lower_vertex_list.append(index)
                # print("lower hull: ", lower_vertex_list)
                # complete_hull = hull.vertices
                lower_hull = lower_vertex_list
                print("Lower_hull: ", lower_hull)
                if (len(lower_hull) == 2):
                    print("two lines on top")
                    if (line_list[lower_hull[0]].dual[0] != 0) and (line_list[lower_hull[1]].dual[0] != 0):
                        final_list.append(line_list[lower_hull[0]].intersecting_lines[line_list[lower_hull[1]]])
                        final_list.append(line_list[lower_hull[0]].get_y_bound())
                        final_list.append(line_list[lower_hull[1]].get_y_bound())
                        visible = Polygon(final_list)
                        visible.setFill('gray')
                        visible.draw(win)

                    print("other cases")
                    if (line_list[lower_hull[0]].dual[0] == 0):
                        if (line_list[lower_hull[1]].dual[0] > 0):
                            final_list.append(Point(minX, line_list[lower_hull[0]].dual[1]))
                        # (line_list[1].dual[0] < 0)
                        else:
                            final_list.append(Point(maxX, line_list[lower_hull[0]].dual[1]))
                        final_list.append(line_list[lower_hull[0]].intersecting_lines[line_list[lower_hull[1]]])
                        final_list.append(line_list[lower_hull[1]].get_y_bound())
                    elif (line_list[lower_hull[1]].dual[0] == 0):
                        if (line_list[lower_hull[0]].dual[0] > 0):
                            final_list.append(Point(minX, line_list[lower_hull[1]].dual[1]))
                        # (line_list[0].dual[0] < 0)
                        else:
                            final_list.append(Point(maxX, line_list[lower_hull[1]].dual[1]))
                        final_list.append(line_list[lower_hull[0]].intersecting_lines[line_list[lower_hull[1]]])
                        final_list.append(line_list[lower_hull[0]].get_y_bound())
                    draw_lower_hull_lines(win, lower_hull)
                    line1 = Line(final_list[0], final_list[1])
                    line2 = Line(final_list[1], final_list[2])
                    line1.setOutline("Blue")
                    line2.setOutline("Blue")
                    line1.draw(win)
                    line2.draw(win)



                else:

                    # get the points
                    # coloring the region
                    # aPolygon = Polygon()
                    # left_most_line = polygon_vertices(lower_hull)

                    #  get the leftmost line
                    left_most_x = []
                    left_most_x.append(lower_hull[0])
                    the_point = [line_list[0].intersecting_lines[line_list[1]].getX(),
                                 line_list[0].intersecting_lines[line_list[1]].getY()]
                    # print(the_point)
                    left_most_x.append(the_point)
                    left_most_x.append(line_list[0].dual[0])
                    # print("k2")
                    for i in lower_hull:
                        loop_list = list(lower_hull)
                        current_line = line_list[i]
                        loop_list.remove(i)
                        for j in loop_list:
                            # print("the req: ", current_line.intersecting_lines[line_list[j]].getX())
                            if (current_line.intersecting_lines[line_list[j]].getX() < left_most_x[1][0]):
                                left_most_x[1][0] = current_line.intersecting_lines[line_list[j]].getX()
                                left_most_x[1][1] = current_line.intersecting_lines[line_list[j]].getY()
                                left_most_x[0] = i
                                left_most_x[2] = current_line.dual[0]
                            if (current_line.intersecting_lines[line_list[j]].getX() == left_most_x[1][0]) and (
                                        left_most_x[2] > current_line.dual[0]):
                                left_most_x[0] = i
                                left_most_x[2] = current_line.dual[0]
                        print(left_most_x)
                        #  left_most_x has the left most line in the visible area

                    if (line_list[left_most_x[0]].dual[0] == 0):
                        final_list.append(Point(0, maxY))
                        final_list.append(Point(0, line_list[left_most_x[0]].dual[1]))
                    else:
                        bound_point1 = line_list[left_most_x[0]].get_y_bound()
                        final_list.append(bound_point1)
                    traverse_list = list(lower_hull)
                    right_line = traverse(traverse_list, left_most_x[0])
                    # print("r_line: ", right_line)
                    if (line_list[right_line].dual[0] == 0):
                        final_list.append(Point(maxX, line_list[right_line].dual[1]))
                        final_list.append(Point(maxX, maxY))
                    else:
                        bound_point2 = line_list[right_line].get_y_bound()
                        final_list.append(bound_point2)

                    print(final_list)

                    visible = Polygon(final_list)
                    visible.setFill('gray')
                    visible.draw(win)

                    draw_lower_hull_lines(win,lower_hull)

                    print("drawing blue lines")
                    left_line_draw = Line(line_list[left_most_x[0]].line_points[0],
                                          line_list[left_most_x[0]].line_points[1])
                    left_line_draw.setOutline('Blue')
                    left_line_draw.draw(win)

                    print("drawing blue lines")
                    left_line_draw = Line(line_list[right_line].line_points[0], line_list[right_line].line_points[1])
                    left_line_draw.setOutline('Blue')
                    left_line_draw.draw(win)

    win.getMouse()
    win.close()

main()


