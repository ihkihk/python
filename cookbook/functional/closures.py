#!/usr/bin/python3

# Named enclosure
def f(x):
    def g(y):
        return x+y
    return g

# Closure of an anonymous function
def h(x):
    return lambda y: x+y

clos1 = f(1)
clos2 = f(2)
print("clos1(5) returned: {}".format(clos1(5)))
print("clos2(5) returned: {}".format(clos2(5)))

print(f(1)(5))
print(f(2)(5))

hclos1 = h(1)
hclos2 = h(2)

print(hclos1(5))
print(hclos2(5))


