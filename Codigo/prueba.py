import numpy as np

reg = np.loadtxt("reg.text", dtype=int ,delimiter=" ")
print reg

a = np.array([1,2,3])
a[0] = 90
a = np.column_stack(a)
print a



save = np.savetxt("reg.text", a,  fmt="%i", delimiter=" ")
print save


reg = np.loadtxt("reg.text", dtype=int ,delimiter=" ")
print reg