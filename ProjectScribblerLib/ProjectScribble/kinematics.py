import math

def translate_xy_to_ab(coord):
    x = coord[0]
    y = coord[1]
    a_len = math.sqrt(x**2 + y**2)
    b_len = math.sqrt((MAX_WIDTH-x)**2 + y**2)
    
    return [a_len, b_len]

def translate_ab_to_xy(lengths):
    a = lengths[0]
    b = lengths[1]
    
    # Cosine rule!
    #cos(left) =  (a**2 + MAX_WIDTH**2 - b**2) / (2 * a * MAX_WIDTH)
    
    try:
        left_angle = math.acos((a**2 + MAX_WIDTH**2 - b**2) / (2 * a * MAX_WIDTH))
    except Exception as e:
        # This specifically happens if the values just arn't a triangle!
        # i.e. consider maxwidth = 100, left length = 10, right = 10... one of
        # the wires must have broken!
        print("Not a triangle!")
        print((a**2 + MAX_WIDTH**2 - b**2) / (2 * a * MAX_WIDTH))
        raise e
        
    #print(left_angle) # in radians, remember.
    
    # sin(left) = opp / hyp
    # cos(right) = adj / hyp
    # hyp is 'a'
    # Lack of precision here - chop to mm. Rounding 'down'
    y = int(math.sin(left_angle) * a) 
    x = int(math.cos(left_angle) * a)
    
    return [x,y]