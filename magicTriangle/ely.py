
import math
import time

TOP_TO_BOTTOM = 0
RIGHT_TO_RIGHT = 1
LEFT_TO_LEFT = 2


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
# triangles = [
#     [BLUE_BUTT,BLUE_BUTT,PINK_HEAD],
#     [PINK_BUTT,ORANGE_HEAD,ORANGE_BUTT],
# ]

triangles = [
    [PINK_BUTT,ORANGE_HEAD,PINK_HEAD],
    [ORANGE_HEAD,BLUE_HEAD,ORANGE_BUTT],
    [PINK_HEAD,ORANGE_BUTT,BLUE_BUTT], #FLIPPED
    [ORANGE_BUTT,BLUE_HEAD,PINK_BUTT],
    [BLUE_HEAD,PINK_BUTT,PINK_BUTT],
    [BLUE_BUTT,BLUE_HEAD,PINK_BUTT], #FLIPPED
    [ORANGE_HEAD,BLUE_BUTT,PINK_BUTT],
    [PINK_HEAD,PINK_BUTT,ORANGE_BUTT], #FLIPPED
    [BLUE_HEAD,BLUE_HEAD,PINK_BUTT]
]

a = []
a.extend(triangles)
a.extend(triangles)
#a.extend(triangles)
#a.extend(triangles)
triangles = a
#
#
#      ^
#     ^v^
#    ^v^v^
#   ^v^v^v^
#  ^v^v^v^v^


def rotateTriangle(t,rotationCount):
    '''
        if count is zero, just return the triangle.
        if count is 1, take the last number, stick it on the front
        if count is 2, take the first number, stick it on the end.
    '''
    if rotationCount == 0:
        # we can just return t, but it looks like this:
        #return [t[BOTTOM],t[LEFT],t[RIGHT]]
        return t
    if (rotationCount == 1):
        return [t[RIGHT],t[BOTTOM],t[LEFT]]
    if (rotationCount == 2):
        return [t[LEFT],t[RIGHT],t[BOTTOM]]


def getTile(layout,row,col):
    rowStart = row*row
    return layout[rowStart + col]

def testTriangleAtPosition(candidate,layout,row,col,flipped):
    if col == 0:
        return True
    triangleBefore = getTile(layout,row,col-1)
    if (flipped):
        triangleAbove = getTile(layout,row-1,col-1)
        if candidate[BOTTOM] + triangleAbove[BOTTOM] != 0:
            return False
        if candidate[RIGHT] + triangleBefore[RIGHT] != 0:
            return False
    else:
        if candidate[LEFT] + triangleBefore[LEFT] != 0:
            return False

    return True




def lengthOfRow(row):
    return 2*row + 1

def placeTriangle(layout,row,col,flipped,freeTriangles):
    '''
        for each triangle available in the list...
            for each rotation of the triangle..
             place that triangle, with that rotation, in the target position.rotation
             if this is the last position:
                 check to see if the layout is valid,
            else
                try placing the remaining traingles in the next position.
    '''

    if(len(freeTriangles) == 0):
        return [layout],0

    result = []

    places = 0
    for triIndex,aTriangle in enumerate(freeTriangles):
        for i in range(3):
            places += 1
            candidate = rotateTriangle(aTriangle,i)
            if(testTriangleAtPosition(candidate,layout,row,col,flipped)):
                newLayout = list(layout)
                newLayout.append(candidate)
                newFreeTriangles = list(freeTriangles)
                newFreeTriangles.pop(triIndex)
                newCol = col+1
                if(newCol == lengthOfRow(row)):
                    newRow = row+1
                    newCol = 0
                    newFlipped = False
                else:
                    newRow = row
                    newFlipped = not flipped
                subResults,subPlaces = placeTriangle(newLayout,newRow,newCol, newFlipped, newFreeTriangles)
                places += subPlaces
                result.extend(subResults)
                # comment the next two lines out if you want to find all results
                if(len(subResults)):
                    return subResults,places
    return result,places

def prettify(tri):
    return list(map(lambda x:reverse[x],tri))
def dumpLayout(layout):
    for index,aTri in enumerate(layout):
        print(f'{index}:{prettify(aTri)}')

def runTest(triangles):
    flipped = False
    t = time.time()
    layout = []
    layouts,places = placeTriangle(layout=layout,row=0,col=0,freeTriangles=triangles,flipped=flipped)
    if(len(layouts) > 0):
        print(f'found {len(layouts)} valid layouts.')
        #print(f'First layout is...')
        #print(f'{dumpLayout(layouts[0])}')
        pass

    else:
        print("no valid layouts")
    d = time.time() - t
    print(f'{len(triangles)} tiles took {d} seconds and {places} placements')

for i in range(len(triangles)):
    runTest(triangles[:i])
