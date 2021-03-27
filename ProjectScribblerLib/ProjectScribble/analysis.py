"""
Functions used for analysis of the paths etc.
"""

import math

from rich.console import Console
from rich.table import Table

def distance(pointa, pointb):
    """
    Calculate the distance between two points on a flat plane 
    """
    return math.sqrt((pointa[0]-pointb[0]) ** 2 + (pointa[1]-pointb[1])**2)


def calc_total_move(paths):
    """
    Calculate and return the total pen down and pen up distance for an array of
    paths. Used for pre-post calculations.
    """
    total_draw = 0
    total_move = 0
    
    last_point = None
    for path in paths:
        if len(path) > 0:
            if last_point:
                total_move += distance(last_point, path[1])
                last_point = path[1]
            else:
                last_point = path[1]
            
            for point in path[1:]:
                #print(last_point)
                total_draw += distance(last_point, point)
                last_point = point
    
    return (total_draw, total_move)


def compare(set_one, set_two):
    """
    Useful (but prints) function to compare paths
    """
    
    set_one_stats = calc_total_move(set_one)
    set_two_stats = calc_total_move(set_two)

    area_a = multipath_area(set_one)
    area_b = multipath_area(set_two)

    draw_delta = set_one_stats[0] - set_two_stats[0]
    move_delta = set_one_stats[1] - set_two_stats[1]


    table = Table(title="Set Comparison")

    table.add_column("Metric", justify="right", style="cyan", no_wrap=True)
    table.add_column("Set A", justify="right")
    table.add_column("Set B", justify="right")
    table.add_column("Delta", justify="right")
    table.add_column("% Change", justify="right")

    table.add_row("Pen Down", "%.f" %set_one_stats[0], "%.f" % set_two_stats[0], "%.f" %draw_delta, "%.1f" %(100* draw_delta/(set_one_stats[0]+1)) )
    table.add_row("Pen Up", "%.f" % set_one_stats[1], "%.f" %set_two_stats[1], "%.f" %move_delta, "%.1f" %(100*  move_delta/(1+set_one_stats[1])) )

    table.add_row("Total", "%.f" % (set_one_stats[0] + set_one_stats[1]), "%.f" %(set_two_stats[0]+set_two_stats[1]),"%.f" %( move_delta+draw_delta), "%.1f" %(100*  (move_delta+draw_delta)/(1+set_one_stats[1]+set_one_stats[0])) )
    table.add_row("(in)Efficiency", "%.1f" % (100*set_one_stats[1] / (set_one_stats[0] + set_one_stats[1])), "%.1f" % (100*set_two_stats[1] / (set_two_stats[0] + set_two_stats[1])), "", "")
    
    table.add_row("Area(*)", "%.1f" % area_a, "%.1f" % area_b, "%.1f" %(area_a-area_b) , "%.1f" %(100*(area_a-area_b)/area_a))

    console = Console()
    console.print(table)


# Taken from https://stackoverflow.com/questions/24467972/calculate-area-of-polygon-given-x-y-coordinates
def shoelace_area(points):
    """
    Calculate the area of a *simple* polygon
    """
    n = len(points) # of corners
    area = 0.0
    for i in range(n):
        j = (i + 1) % n
        area += points[i][0] * points[j][1]
        area -= points[j][0] * points[i][1]
    area = abs(area) / 2.0
    return area


def multipath_area(paths):
    area = 0.0
    for path in paths:
        area += shoelace_area(path)
    return area


def dimensions(paths):
    """
    Calculate the dimensions of a set of paths (i.e. minumum box)
    Returns (left, top, right, bottom) as a box.
    """

    min_x = float('inf')
    min_y = float('inf')
    max_x = float('-inf')
    max_y = float('-inf')

    for path in paths:
        for point in path:
            #print("point: %s" % point)
            x = point[0]
            y = point[1]

            min_x = min(x, min_x)
            min_y = min(y, min_y)
            max_x = max(x, max_x)
            max_y = max(y, max_y)

    #print("Dimens: (%s %s) (%s %s)" % (min_x, min_y, max_x, max_y))

    return (min_x, min_y, max_x, max_y)