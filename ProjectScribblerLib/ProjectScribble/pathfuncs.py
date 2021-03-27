"""
Functions that can manipulate paths. Some are lossless, some are intentionally 
lossy (e.g. path simplification).
"""

import json
from .analysis import distance, dimensions

def scale(coord_paths, scale_factor):
    """
    Take an array of paths, and scale them all away from (0,0) cartesian using a
    scalar factor, return the resultinv paths.
    """
    new_paths = []
    for path in coord_paths:
        new_path = []
        for point in path:
            new_path.append( (point[0]*scale_factor, point[1]*scale_factor))
        new_paths.append(new_path)
        
    return new_paths


def shift(coord_paths, shift_vector):
    """
    Take an array of paths and shift them by the coordinate. 
    """
    new_paths = []
    for path in coord_paths:
        new_path = []
        for point in path:
            new_path.append( (point[0] + shift_vector[0], point[1]+ shift_vector[1]))
        new_paths.append(new_path)
        
    return new_paths


def normalise(coord_paths):
    """
    Take an array of coord, remove any empty paths, and make sure that all the coords
    are tuples not arrays (Which can happen after json.load())
    """
    new_paths = []
    for path in coord_paths:
        if len(path) > 0:
            new_path = []
            for point in path:
                # convert to tuple
                new_path.append((point[0], point[1]))
            new_paths.append(new_path)
            
    return new_paths
    

def load_paths(filename):
    """
    Load and normalise paths
    """
    with open(filename, "r") as fp:
        paths = json.load(fp)
        paths = normalise(paths)

    return paths


def save_paths(filename, paths):
    """
    Save paths to a file in json format
    """
    with open(filename, "w") as fp:
        json.dump(paths, fp)


def optimise_order(paths):
    """
    Optimise the order of multiple paths to minimise the pen-down time
    """

    new_paths = []
    
    path = paths.pop()
    new_paths.append(path)
    
    while len(paths) > 0:
        shortest = None
        shortest_val = float('inf')
        
        #orig_side = None # at the moment always the 'far'
        bottom_side = None
        
        for p in paths:
            #print(new_paths)
            #print(p)
            ndist = distance(new_paths[-1][-1], p[0])
            if ndist < shortest_val:
                shortest = p
                shortest_val = ndist
                bottom_side ='Near'
    
            fdist = distance(new_paths[-1][-1], p[-1])
            if fdist < shortest_val:
                shortest = p
                shortest_val = fdist
                bottom_side='Far'
                
        # path finder, reverser. 
        #print(shortest)
        paths.remove(shortest)
        if bottom_side == 'Far':
            shortest.reverse()
        #print(shortest)
        new_paths.append(shortest)
        
    return new_paths


def center_and_fit(paths, center_x=950//2, center_y=300, target_width=550, target_height=450):
    """ 
    Center and fit into the target box.
    """

    # get original size & positon:
    orig_dimensions = dimensions(paths)

    # Shift back to 0,0 for scaling
    new_paths = shift(paths, (-orig_dimensions[0], -orig_dimensions[1]))

    # Pick a scale
    current_width = orig_dimensions[2] - orig_dimensions[0]
    current_height = orig_dimensions[3] - orig_dimensions[1]

    #print(current_height)

    target_ratio = target_width/target_height
    current_ratio = current_width/current_height

    #print(target_ratio, current_ratio)

    if current_ratio > target_ratio:
        # this means the width is bigger in ratio then the target, i.e scale width
        ratio = target_width / current_width

    else:
        # this means its taller then the target i.e. scale height
        ratio = target_height / current_height

    #print(ratio)
    # Scale
    new_paths_scaled = scale(new_paths, ratio)

    # Shift to center

    # left and top be 0 becuase we shifted it to 0 back up a few steps
    _, _, width, height = dimensions(new_paths_scaled)
    
    left_shift = center_x - width//2
    down_shift = center_y - height//2

    #print("w, l_shift %s %s" % (width, left_shift) )
    new_paths_shifted = shift(new_paths_scaled, (left_shift, down_shift))

    # Return
    return new_paths_shifted


