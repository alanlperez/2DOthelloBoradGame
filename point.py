##########################
# Build and Check Points #
##########################


import math



class Point:
    def __init__(self, frac: (float, float)):
        '''
        Initializes a Point object, given a tuple containing fractional
        x and y coordinates.
        '''
        frac_x, frac_y = frac
        self.frac_x = frac_x
        self.frac_y = frac_y


    def frac(self) -> (float, float):
        '''
        Returns an (x, y) tuple that contains fractional coordinates
        for this Point object.
        '''
        return (self.frac_x, self.frac_y)


    def pixel(self, total_size: (int, int)) -> (int, int):
        '''
        Returns an (x, y) tuple that contains pixel coordinates for
        this Point object.  The total_size parameter specifies the
        total size, in pixels, of the area in which the point needs
        to be specified -- this is used to make the appropriate
        conversion, since the pixel position of a fractional point
        changes as the size changes.
        '''
        size_x, size_y = total_size
        return (int(self.frac_x * size_x), int(self.frac_y * size_y))


    def frac_distance_from(self, p: 'Point') -> float:
        '''
        Given another Point object, returns the distance, in
        terms of fractional coordinates, between this Point and the
        other Point.
        '''

        return math.sqrt(
            (self.frac_x - p.frac_x) * (self.frac_x - p.frac_x)
            + (self.frac_y - p.frac_y) * (self.frac_y - p.frac_y))




# These two functions are used to create Points that are either
# being created from fractional or absolute coordinates.  Given these
# two functions, we'll never create Point objects by calling the
# Point constructor; instead, we'll just call the appropriate
# of these two functions, depending on whether we have fractional or
# absolute coordinates already.

def from_frac(frac: (float, float)) -> Point:
    '''Builds a Point given fractional x and y coordinates.'''
    return Point(frac)



def from_pixel(pixel: (int, int), total_size: (int, int)) -> Point:
    '''
    Builds a Point given pixel x and y coordinates, along with
    the width and height of the area (necessary for conversion
    to fractional).
    '''
    pixel_x, pixel_y = pixel
    size_x, size_y = total_size
    return Point((pixel_x / size_x, pixel_y / size_y))
