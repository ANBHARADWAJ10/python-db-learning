# collections, Counter, Ordereddict(not used), namedtuple, defaultdict, deque

from collections import Counter

# a = 'aaabbcccc'
#
# count = Counter(a)
# print(count)
#
# s = ''
# for key,value in count.items():
#     s += key + str(value)
#
# print(s)

from collections import defaultdict

# a = defaultdict(str)
# a['a'] = 'apple'
# a['b'] = 'ball'
# a['c'] = 'cat'
# print(a)

from collections import namedtuple


# point = namedtuple('point', ('x', 'y'))
# pt = point(10, 20)
# pt2 = point(30, 40)
# result = (pt.x + pt2.y, pt2.x + pt.y)
# print(result)

from collections import deque

d = deque()
d.append(1)
d.appendleft(1)
d.appendleft(2)
d.appendleft(3)
d.append(4)
print(d)

for i in d:
    print(i)

print(sorted(d))

set01 = set(d)
print(set01)
