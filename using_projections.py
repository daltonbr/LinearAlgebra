from vector import Vector


print("Component Parallel to")
v = Vector([3.039, 1.879])
w = Vector([0.825, 2.036])
print(v.component_parallel_to(w))

print("\nComponent Orthogonal to")
v = Vector([-9.88, -3.264, -8.159])
w = Vector([-2.155, -9.353, -9.473])
print(v.component_orthogonal_to(w))

v = Vector([3.009, -6.172, 3.692, -2.51])
w = Vector([6.404, -9.144, 2.759, 8.718])

vpar = v.component_parallel_to(w)
vort = v.component_orthogonal_to(w)

print("Parallel Component:", vpar)
print("Orthogonal Component", vort)
