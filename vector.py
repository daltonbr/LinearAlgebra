#from functools import reduce
from math import acos, pi, sqrt
from decimal import Decimal, getcontext

# The number of significant digits (precision)
getcontext().prec = 7

class Vector(object):
    """This is an implementation of a Vector from a standpoint of Linear Algebra \n"""

    # Constants for messages
    CANNOT_NORMALIZE_ZERO_VECTOR_MSG = 'Cannot normalize the zero vector'
    NO_UNIQUE_PARALLEL_COMPONENT_MSG = 'No unique parallel component'
    NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG = 'No unique orthogonal component'
    ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG = 'Only defined in two or three dimensions'

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

    def plus(self, v):
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
        coordinates_squared = [x**Decimal(2) for x in self.coordinates]
        return sum(coordinates_squared)

    def magnitude(self):
        """Returns the length of this vector. """
        return self.square_magnitude().sqrt()

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
        coordinates_multiplied = [x*y for x, y in zip(self.coordinates, v.coordinates)]
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

    def component_orthogonal_to(self, basis):
        """Return an orthogonal vector projection"""
        try:
            projection = self.component_parallel_to(basis)
            return self.minus(projection)

        except Exception as e:
            if str(e) == self.NO_UNIQUE_PARALLEL_COMPONENT_MSG:
                raise Exception(self.NO_UNIQUE_ORTHOGONAL_COMPONENT_MSG)
            else:
                raise e


    def component_parallel_to(self, basis):
        """Return an parallel vector projection"""
        try:
            u = basis.normalized()
            weight = self.dot(u)
            return u.times_scalar(weight)

        except Exception as e:
            if str(e) == self.CANNOT_NORMALIZE_ZERO_VECTOR_MSG:
                raise Exception(self.NO_UNIQUE_PARALLEL_COMPONENT_MSG)
            else:
                raise e

    def is_orthogonal_to(self, v, tolerance=1e-10):
        """Boolean check for orthogonality between two vectors (with a tolerance margin)"""
        return abs(self.dot(v)) < tolerance

    
    def is_parallel_to(self, v):
        """Boolean check for parallelity between two vectors"""
        return ( self.is_zero() or v.is_zero() or
                 self.angle_with(v) == 0 or self.angle_with(v) == pi )

    def is_zero(self, tolerance=1e-10):
        """Boolean check for zero (null) vector (with a tolerance)"""
        return self.magnitude() < tolerance

    def cross(self, v):
        """Return the cross product, between two 3 dimension vectors."""
        try:       
            x_1, y_1, z_1 = self.coordinates
            x_2, y_2, z_2 = v.coordinates
            return Vector( [  y_1*z_2 - y_2*z_1,
                            -(x_1*z_2 - x_2*z_1),
                              x_1*y_2 - x_2*y_1 ] )
            
        except ValueError as e:
            msg = str(e)
            if msg == 'need more than 2 values to unpack':
                self_embedded_in_R3 = Vector(self.coordinates + ('0',))
                v_embedded_in_R3 = Vector(self.coordinates + ('0',))
                return self_embedded_in_R3.cross(v_embedded_in_R3)
            elif (msg == 'too many values to unpack' or
                msg == 'need more than 1 value to unpack'):
                raise Exception(self.ONLY_DEFINED_IN_TWO_THREE_DIMS_MSG)
            else:
                raise e


    def parallelogram_area_with(self, v):
        """Return the parallelogram area between two vectors (only 2D and 3D vectors)"""
        # A Euclidean Geometric approach: base * height (our orthogonal projection)
        # return v.magnitude() * self.component_orthogonal_to(v).magnitude()
        cross_product = self.cross(v)
        return cross_product.magnitude()


    def triangle_area(self, v):
        """Return the triangle area between two vectors (only 2D and 3D vectors)"""
        return self.parallelogram_area_with(v) / Decimal(2.0)
