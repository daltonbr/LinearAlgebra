#from functools import reduce
from math import sqrt, acos, pi
from decimal import Decimal, getcontext

# The number of significant digits (precision)
getcontext().prec = 5

class Vector(object):

    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'

    def __init__(self, coordinates):
        try:
            if not coordinates:
                raise ValueError
            self.coordinates = tuple([Decimal(x) for x in coordinates])
            self.dimension = len(self.coordinates)

        except ValueError:
            raise ValueError('The coordinates must be nonempty')

        except TypeError:
            raise TypeError('The coordinates must be an iterable')

    def __str__(self):
        return 'Vector {}'.format(self.coordinates)

    def __eq__(self, v):
        return self.coordinates == v.coordinates

    def plus (self, v):
        """Returns the sum of these two vectors. """
        new_coordinates = [x+y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)

    def minus(self, v):     
        """Returns the subtraction of these two vectors. """
        new_coordinates = [x-y for x,y in zip(self.coordinates, v.coordinates)]
        return Vector(new_coordinates)
        
    def times_scalar(self, c):
        """Returns the the scalar product of this vector.\n
        Keyword arguments:\n
        c -- the scalar value
        """
        new_coordinates = [Decimal(c)*x for x in self.coordinates]
        return Vector(new_coordinates)

    def square_magnitude(self):
        """Returns the squared length of this vector"""       
        coordinates_squared = [x**2 for x in self.coordinates]
        return sum(coordinates_squared)     

    def magnitude(self):
        """Returns the length of this vector. """
        return sqrt(self.square_magnitude())

    def normalized(self):
        """Return Returns this vector with a magnitude of 1.
        Note that the current vector is unchanged and a new normalized vector is returned.
        """
        try:
            magnitude = self.magnitude()
            return self.times_scalar(Decimal('1.0')/Decimal(magnitude))
        except ZeroDivisionError:
            raise Exception(self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG)
        
    def dot(self, v):
        """Return the dot (aka inner) product between two vectors."""
        coordinates_multiplied = [x*y for x,y in zip(self.coordinates, v.coordinates)]
        return sum(coordinates_multiplied)

    def angle_with(self, v, in_degrees=False):
        """Return the angle between two vectors (in radians by default)."""
        try:
            u1 = self.normalized()
            u2 = v.normalized()
            angle_in_radians = acos(u1.dot(u2))

            if in_degrees:
                degrees_per_radian = 180. / pi
                return angle_in_radians * degrees_per_radian
            else:
                return angle_in_radians
        
        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception('Cannot compute an angle with the zero vector')
            else:
                raise e
