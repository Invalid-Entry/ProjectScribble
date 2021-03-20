"""
Functions that can manipulate paths. Some are lossless, some are intentionally lossy.
"""

import json

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