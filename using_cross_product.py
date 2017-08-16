from vector import Vector


v = Vector([8.462, 7.893, -8.187])
w = Vector([6.984, -5.975, 4.778])
print("Cross Product", v.cross(w))

# 3D parallelogram area
v = Vector([-8.987, -9.838, 5.031])
w = Vector([-4.268, -1.861, -8.866])
print(v.parallelogram_area_with(w))

# 2D parallelogram area
v = Vector([2, 2])
w = Vector([0, 2])
print(v.parallelogram_area_with(w))

# 3D triangle area
v = Vector([1.5, 9.547, 3.691])
w = Vector([-6.007, 0.124, 5.772])
print(v.triangle_area(w))

