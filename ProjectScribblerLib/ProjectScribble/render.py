"""
Useful functions to preview what paths will look like
"""

from PIL import Image, ImageDraw

def prototype(coord_paths, penup=True, machine_limits=True): 
    im = Image.new(mode="RGBA", size=(950,650))
    d = ImageDraw.Draw(im)

    wire_length = 800

    #offset = (290,150)
    #scale = 0.68
    last_point = None
    for tpath in coord_paths:
        if len(tpath)>0:
            if last_point:
                #point = ((tpath[0][0]+offset[0])*scale, (tpath[0][1]+ offset[1])*scale)
                point = tpath[0]
                if penup:
                    d.line((last_point,point), fill=(0,255,0))
            #last_point = ((tpath[0][0]+offset[0])*scale, (tpath[0][1]+ offset[1])*scale)
            last_point = tpath[0]
            for point in tpath[1:]:
                #point = ((point[0]+offset[0])*scale, (point[1]+ offset[1])*scale)
                d.line((last_point,point), fill=(255,255,255))
                last_point = point
    
    if machine_limits:
        d.ellipse(((-wire_length,-wire_length),(wire_length,wire_length)), fill=None, outline=(0,0,255,255))
        d.ellipse(((950-wire_length,-wire_length),(950+wire_length,wire_length)), fill=None, outline=(0,0,255,255))
        d.line((0,100,950,100), fill=(0,0,255,255))
    return im


def proto_before_after(paths_a, paths_b, pen_up=True, machine_limits=True):
    im_one = prototype(paths_a, pen_up, machine_limits).resize((950//2, 650//2))

    im_two = prototype(paths_b, pen_up, machine_limits).resize((950//2, 650//2))


    im = Image.new(mode="RGBA", size=(950, 650//2))


    im.paste(im_one, (0,0))
    print(im.mode)
    im.paste(im_two, (950//2, 0))

    return im