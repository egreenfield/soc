
import math


BLUE_HEAD = -100
BLUE_BUTT = 100
ORANGE_HEAD = -200
ORANGE_BUTT = 200
PINK_HEAD = -300
PINK_BUTT = 300

reverse = {
    BLUE_HEAD: "B-head",
    BLUE_BUTT: "B-butt",
    ORANGE_BUTT: "O-butt",
    ORANGE_HEAD: "O-head",
    PINK_BUTT: "P-butt",
    PINK_HEAD: "P-head"
}

BOTTOM = 0
LEFT = 1
RIGHT = 2
'''
each triangle is a series of three numbers.
the first number is the value on the bottom edge.
the second number is the value on the left edge.
the third number is the value on the right edge.
'''

triangles = [
    [PINK_BUTT,ORANGE_HEAD,PINK_HEAD],
    [ORANGE_HEAD,BLUE_HEAD,ORANGE_BUTT],
    [PINK_HEAD,ORANGE_BUTT,BLUE_BUTT],
    [ORANGE_BUTT,BLUE_HEAD,PINK_BUTT],
    [BLUE_HEAD,PINK_BUTT,PINK_BUTT],
    [BLUE_BUTT,BLUE_HEAD,PINK_BUTT],
    [ORANGE_HEAD,BLUE_BUTT,PINK_BUTT],
    [PINK_HEAD,PINK_BUTT,ORANGE_BUTT],
    [BLUE_HEAD,BLUE_HEAD,PINK_BUTT]
]

#
#
#      ^
#     ^v^
#    ^v^v^
#   ^v^v^v^
#  ^v^v^v^v^

def prettify(tri):
    return list(map(lambda x:reverse[x],tri))



