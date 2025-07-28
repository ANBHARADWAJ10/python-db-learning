# # lambda arguments: expression
# # map expression, iterable
# # zip iterable, iterable
# # enumerate iterable -- prints index, data in the list
# # filter - expression, iterable
# # reduce - expression, iterable -- from functools import reduce
#
# add10 = lambda x: x + 10
# print(add10(5))
#
# def add(x):
#     return x + 10
#
# mul = lambda x, y: x * y
# print(mul(5, 4))
#
#

# points2d = [(1, 2), (15, 1), (5, -1), (10, 4)]
# points_sorted = sorted(points2d, key=lambda order:order[1]) # sorts by second value
# print(points2d)
# print(points_sorted)

diameters = [10, 12, 16, 20, 25]
# Compute circle area by list comprehension
areas = [3.14 * (d/2)**2 for d in diameters]

# Print (diameter, area) pairs
for d, a in zip(diameters, areas):
    print(d, a)

# zip prints two list side by side
# enumerate - prints index and the data side by side
# map - iterate and expression gets combined

for i in enumerate(diameters):
    print(i)

comp = [x*2 for x in [1,2,3,4,5]]
print(comp)
comp02 = [x*2 if x<3 else x*1 for x in [1,2,3,4,5]]
print(comp02)

# map transforms the elements
# filter - filters the existing elements

a = [1,2,3,4,5]

fil = filter(lambda x: x % 2 == 0, a)
print(list(fil))

from functools import reduce

product = reduce(lambda x, y: x * y, a)
print(product)


